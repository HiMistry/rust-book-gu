// Rust Book → Gujarati Translation Pipeline
//
// Walks markdown events via pulldown-cmark, translates prose paragraphs
// via Ollama, rebuilds the markdown preserving all structure.

mod chunk;
mod config;
mod epub;
mod glossary;
mod progress;
mod translate;

use crate::config::Config;
use crate::glossary::Glossary;
use crate::progress::Progress;
use clap::Parser;
use pulldown_cmark::{Event, Parser as MdParser, Tag, TagEnd};
use std::io::Write;
use std::path::{Path, PathBuf};

#[derive(Parser, Debug)]
#[command(name = "translate", about = "Translate Rust Book from English to Gujarati")]
struct Cli {
    #[arg(long)]
    src: Option<String>,
    #[arg(long)]
    all: bool,
    #[arg(long, default_value = "../config.json")]
    config: String,
    #[arg(long)]
    model: Option<String>,
    #[arg(long)]
    resume: bool,
    #[arg(long)]
    build_epub: bool,
}

fn main() {
    let cli = Cli::parse();

    let config_path = Path::new(&cli.config);
    let mut config = Config::load(config_path);
    if let Some(model) = &cli.model {
        config.model = model.clone();
    }

    println!("=== Rust Book → Gujarati Translation Pipeline ===");
    println!("Config:     {}", config_path.display());
    println!("Source:     {}", config.src_dir_abs.display());
    println!("Output:     {}", config.out_dir_abs.display());
    println!("Model:      {}", config.model);

    let glossary_path = config_path.parent().unwrap_or(Path::new(".")).join("glossary.json");
    let glossary = Glossary::load(&glossary_path);
    println!("Glossary:   {} terms", glossary.terms.len());

    let progress_path = config_path.parent().unwrap_or(Path::new(".")).join("progress.json");
    let mut progress = if cli.resume {
        Progress::load(&progress_path)
    } else {
        Progress { completed: std::collections::HashSet::new() }
    };
    if cli.resume {
        println!("Resuming:   {} files done", progress.completed.len());
    }

    if cli.build_epub {
        println!("\n=== Building EPUB ===");
        match epub::build_epub(&config) {
            Ok(()) => println!("EPUB built successfully!"),
            Err(e) => eprintln!("EPUB build failed: {}", e),
        }
        return;
    }

    let src_dir = &config.src_dir_abs;
    let files: Vec<PathBuf> = if cli.all {
        find_md_files(src_dir)
    } else if let Some(pattern) = &cli.src {
        let full_pattern = if pattern.contains(std::path::MAIN_SEPARATOR_STR) {
            pattern.clone()
        } else {
            format!("{}/{}", src_dir.display(), pattern)
        };
        glob::glob(&full_pattern)
            .unwrap_or_else(|e| {
                eprintln!("Invalid glob '{}': {}", full_pattern, e);
                std::process::exit(1);
            })
            .filter_map(|entry| entry.ok())
            .collect()
    } else {
        eprintln!("Use --src <pattern> or --all");
        std::process::exit(1);
    };

    if files.is_empty() {
        eprintln!("No .md files found.");
        std::process::exit(1);
    }
    println!("\n{} file(s) to translate:", files.len());
    for f in &files {
        println!("  {}", f.display());
    }

    let client = reqwest::blocking::Client::builder()
        .timeout(std::time::Duration::from_secs(120))
        .build()
        .unwrap_or_else(|e| {
            eprintln!("FATAL: Cannot create HTTP client: {}", e);
            std::process::exit(1);
        });

    let mut total_groups = 0;
    let mut total_errors = 0;

    for file_path in &files {
        let relative_path = file_path
            .strip_prefix(src_dir)
            .unwrap_or(file_path)
            .to_string_lossy()
            .to_string();

        if cli.resume && progress.is_completed(&relative_path) {
            println!("  [SKIP] {}", relative_path);
            continue;
        }

        println!("\n--- {}", relative_path);

        let source_text = match std::fs::read_to_string(file_path) {
            Ok(t) => t,
            Err(e) => {
                eprintln!("  ERROR: Cannot read '{}': {}", file_path.display(), e);
                total_errors += 1;
                continue;
            }
        };

        // Translate the file by walking markdown events.
        let translated = process_markdown(&source_text, &config, &glossary, &client, &mut total_groups);

        let out_path = config.out_dir_abs.join(&relative_path);
        if let Some(p) = out_path.parent() {
            std::fs::create_dir_all(p).unwrap_or_else(|e| {
                eprintln!("  ERROR: Cannot create dir '{}': {}", p.display(), e);
            });
        }
        match std::fs::write(&out_path, &translated) {
            Ok(()) => {
                println!("  Saved: {}", out_path.display());
                progress.mark_completed(&relative_path, &progress_path);
            }
            Err(e) => {
                eprintln!("  ERROR: Cannot write '{}': {}", out_path.display(), e);
                total_errors += 1;
            }
        }
    }

    println!("\n=== Done ===");
    println!("Files:  {}", files.len());
    println!("Groups: {}", total_groups);
    if total_errors > 0 {
        println!("Errors: {}", total_errors);
    }
    println!("Tip: --build-epub to generate .epub");
}

// Each block is one translatable unit (paragraph, heading, or list item).
struct TextBlock {
    // The English text content (may span multiple lines in the original).
    text: String,
    // If true, this is a heading whose # prefix will be re-added.
    is_heading: bool,
    // 1-6 for heading level (only meaningful if is_heading).
    heading_level: u8,
    // MARKDOWN prefix to include when sending to the model (e.g. "## " for h2).
    // This helps the model understand it's a heading and translate accordingly.
    prefix: String,
}

// Process a markdown file: walk events, translate prose paragraphs,
// and return the full translated markdown.
fn process_markdown(
    md: &str,
    config: &Config,
    glossary: &Glossary,
    client: &reqwest::blocking::Client,
    total_groups: &mut usize,
) -> String {
    let parser = MdParser::new(md);

    // Output: the rebuilt markdown with translated text.
    let mut output = String::new();

    // State machine.
    enum State {
        Normal,      // Outside any special block
        CodeBlock,   // Inside ``` fences
        Heading(u8), // Inside heading with given level
        Html,        // Inside raw HTML block
    }
    let mut state = State::Normal;

    // Accumulator for text events in the current paragraph/heading/list item.
    let mut acc = String::new();

    // Buffer of completed blocks waiting to be translated.
    let mut block_buffer: Vec<TextBlock> = Vec::new();
    let mut buffer_words: usize = 0;

    // Helper: flush current accumulator as a block.
    let finish_block = |acc: &mut String, buffer: &mut Vec<TextBlock>, buffer_words: &mut usize, st: &State| {
        let text = acc.trim().to_string();
        if text.is_empty() {
            return;
        }
        let block = match st {
            State::Heading(lv) => TextBlock {
                prefix: "#".repeat(*lv as usize) + " ",
                text,
                is_heading: true,
                heading_level: *lv,
            },
            _ => TextBlock {
                prefix: String::new(),
                text,
                is_heading: false,
                heading_level: 0,
            },
        };
        *buffer_words += block.text.split_whitespace().count();
        buffer.push(block);
        acc.clear();
    };

    // Helper: translate all buffered blocks as one group, write to output.
    // If buffer is empty, does nothing.
    let mut flush_buffer = |buffer: &mut Vec<TextBlock>,
                            buffer_words: &mut usize,
                            output: &mut String,
                            total_groups: &mut usize,
                            config: &Config,
                            glossary: &Glossary,
                            client: &reqwest::blocking::Client| {
        if buffer.is_empty() {
            return;
        }
        *total_groups += 1;

        // Join all block texts for translation, including markdown prefixes.
        // E.g., "## Getting Started\nWelcome to the chapter..."
        let combined: Vec<String> = buffer.iter().map(|b| format!("{}{}", b.prefix, b.text)).collect();
        let combined_text = combined.join("\n");

        print!("  Group {} ({} paras, ~{} words)... ", *total_groups, buffer.len(), *buffer_words);
        std::io::stdout().flush().ok();

        let chunk = chunk::Chunk {
            text: combined_text.clone(),
            index: *total_groups,
        };
        let translated = translate::translate_chunk(&chunk, config, glossary, client)
            .unwrap_or_else(|e| {
                eprintln!("FAILED: {}", e);
                combined_text // fallback: use original
            });
        println!("OK ({} chars)", translated.len());

        // Each block was combined with "\n" separators for translation.
        // The model may have preserved those newlines or collapsed them.
        // We split the translated text back across blocks by finding newlines
        // in the translation. If there are no newlines, we use word-proportional split.
        let trans_lines: Vec<&str> = translated.split('\n').collect();

        if trans_lines.len() == buffer.len() {
            // Model preserved the line structure. Direct 1:1 mapping.
            for (idx, block) in buffer.iter().enumerate() {
                write_block(output, block, trans_lines[idx].trim());
            }
        } else {
            // Model collapsed lines. Use word-proportional split.
            let orig_word_counts: Vec<usize> = buffer.iter().map(|b| b.text.split_whitespace().count()).collect();
            let total_orig_words: usize = orig_word_counts.iter().sum();

            if total_orig_words == 0 {
                buffer.clear();
                *buffer_words = 0;
                return;
            }

            // Strip leading `#` markers so word counts reflect real text.
            let stripped = translated
                .lines()
                .map(|l| l.trim_start_matches(|c: char| c == '#' || c == ' '))
                .collect::<Vec<&str>>()
                .join(" ");
            let trans_words: Vec<&str> = stripped.split_whitespace().collect();
            let total_trans_words = trans_words.len();
            let mut word_offset: usize = 0;

            for (idx, block) in buffer.iter().enumerate() {
                let proportion = orig_word_counts[idx] as f64 / total_orig_words as f64;
                let word_count = ((total_trans_words as f64) * proportion).round() as usize;
                let word_count = word_count.max(1);
                let word_end = (word_offset + word_count).min(total_trans_words);

                let block_trans: String = trans_words[word_offset..word_end].join(" ");
                word_offset = word_end;

                write_block(output, block, &block_trans);
            }
        }

        buffer.clear();
        *buffer_words = 0;
    };

    // Walk events.
    for event in parser {
        match event {
            // -- Entering blocks --
            Event::Start(tag) => match tag {
                Tag::CodeBlock(_) => {
                    // Flush pending prose before code block.
                    finish_block(&mut acc, &mut block_buffer, &mut buffer_words, &state);
                    flush_buffer(&mut block_buffer, &mut buffer_words, &mut output, total_groups, config, glossary, client);
                    state = State::CodeBlock;
                }
                Tag::Heading { level, .. } => {
                    // Flush any pending prose BEFORE the heading.
                    finish_block(&mut acc, &mut block_buffer, &mut buffer_words, &state);
                    flush_buffer(&mut block_buffer, &mut buffer_words, &mut output, total_groups, config, glossary, client);
                    let lv = match level {
                        pulldown_cmark::HeadingLevel::H1 => 1,
                        pulldown_cmark::HeadingLevel::H2 => 2,
                        pulldown_cmark::HeadingLevel::H3 => 3,
                        pulldown_cmark::HeadingLevel::H4 => 4,
                        pulldown_cmark::HeadingLevel::H5 => 5,
                        pulldown_cmark::HeadingLevel::H6 => 6,
                    };
                    state = State::Heading(lv);
                }
                Tag::HtmlBlock => {
                    finish_block(&mut acc, &mut block_buffer, &mut buffer_words, &state);
                    flush_buffer(&mut block_buffer, &mut buffer_words, &mut output, total_groups, config, glossary, client);
                    state = State::Html;
                }
                Tag::Paragraph | Tag::Item => {
                    // Accumulate text within these.
                }
                _ => {}
            },

            // -- Leaving blocks --
            Event::End(tag) => match tag {
                TagEnd::CodeBlock => {
                    state = State::Normal;
                }
                TagEnd::Heading(_) => {
                    // Finish heading — add to buffer but DON'T flush yet.
                    // It will merge with the following paragraph (with a delimiter).
                    finish_block(&mut acc, &mut block_buffer, &mut buffer_words, &state);
                    state = State::Normal;
                }
                TagEnd::Paragraph | TagEnd::Item => {
                    finish_block(&mut acc, &mut block_buffer, &mut buffer_words, &state);
                    // If buffer is large enough, flush.
                    if buffer_words >= config.chunk_min_words {
                        flush_buffer(&mut block_buffer, &mut buffer_words, &mut output, total_groups, config, glossary, client);
                    }
                }
                TagEnd::HtmlBlock => {
                    state = State::Normal;
                }
                TagEnd::List(_) => {
                    // End of a list: flush any remaining list items.
                    finish_block(&mut acc, &mut block_buffer, &mut buffer_words, &state);
                    flush_buffer(&mut block_buffer, &mut buffer_words, &mut output, total_groups, config, glossary, client);
                }
                _ => {}
            },

            // -- Text content --
            Event::Text(text) => {
                match &state {
                    State::CodeBlock | State::Html => {
                        // Write verbatim.
                        output.push_str(&text);
                    }
                    _ => {
                        // Accumulate for translation.
                        if !acc.is_empty() {
                            acc.push(' ');
                        }
                        acc.push_str(&text);
                    }
                }
            }

            // -- Inline code --
            Event::Code(code) => {
                match &state {
                    State::CodeBlock | State::Html => {
                        output.push_str(&format!("`{}`", code));
                    }
                    _ => {
                        if !acc.is_empty() {
                            acc.push(' ');
                        }
                        acc.push_str(&format!("`{}`", code));
                    }
                }
            }

            // -- Raw HTML (inline) --
            Event::Html(html) => {
                output.push_str(&html);
            }

            // -- Line breaks --
            Event::SoftBreak | Event::HardBreak => {
                match &state {
                    State::CodeBlock | State::Html => {
                        output.push('\n');
                    }
                    _ => {
                        acc.push(' ');
                    }
                }
            }

            // -- Thematic break --
            Event::Rule => {
                finish_block(&mut acc, &mut block_buffer, &mut buffer_words, &state);
                flush_buffer(&mut block_buffer, &mut buffer_words, &mut output, total_groups, config, glossary, client);
                output.push_str("---\n\n");
            }

            // -- Other events (footnotes, task list markers) --
            _ => {}
        }
    }

    // Flush any remaining text.
    finish_block(&mut acc, &mut block_buffer, &mut buffer_words, &state);
    flush_buffer(&mut block_buffer, &mut buffer_words, &mut output, total_groups, config, glossary, client);

    output
}

// Helper: write a translated block to the output, handling headings vs prose.
fn write_block(output: &mut String, block: &TextBlock, text: &str) {
    let trimmed = text.trim();
    let cleaned = trimmed.trim_start_matches(|c: char| c == '#' || c == ' ');
    if block.is_heading {
        let prefix = "#".repeat(block.heading_level as usize);
        let content = if cleaned.is_empty() { "" } else { cleaned.trim() };
        output.push_str(&format!("{} {}\n\n", prefix, content));
    } else {
        if cleaned.is_empty() {
            return;
        }
        output.push_str(cleaned.trim());
        output.push_str("\n\n");
    }
}

// Find the byte offset of a character index in a UTF-8 string.
fn char_boundary(s: &str, char_idx: usize) -> usize {
    if char_idx == 0 {
        return 0;
    }
    let mut count = 0;
    for (byte_idx, _) in s.char_indices() {
        if count >= char_idx {
            return byte_idx;
        }
        count += 1;
    }
    s.len()
}

fn find_md_files(dir: &Path) -> Vec<PathBuf> {
    let mut files = Vec::new();
    if dir.is_dir() {
        if let Ok(entries) = std::fs::read_dir(dir) {
            for entry in entries.flatten() {
                let path = entry.path();
                if path.is_dir() {
                    files.extend(find_md_files(&path));
                } else if path.extension().map_or(false, |ext| ext == "md") {
                    files.push(path);
                }
            }
        }
    }
    files.sort();
    files
}
