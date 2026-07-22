use serde::Deserialize;
use std::path::{Path, PathBuf};

// Config holds all settings for the translation pipeline.
// It is loaded from config.json at startup.
#[derive(Debug, Deserialize)]
pub struct Config {
    // URL of the Ollama server (e.g. "http://localhost:11434")
    pub ollama_url: String,
    // Ollama model name to use (e.g. "gemma3:12b")
    pub model: String,
    // Directory containing the English .md source files (relative to config file)
    pub src_dir: String,
    // Directory where translated .md files will be written (relative to config file)
    pub out_dir: String,
    // Directory containing book.toml, SUMMARY.md, etc. (relative to config file)
    pub book_dir: String,
    // Model temperature: 0.0 = deterministic, no creativity
    pub temperature: f64,
    // Maximum number of times to retry a failed translation request
    pub max_retries: u32,
    // Minimum words per chunk sent to the model
    pub chunk_min_words: usize,
    // Maximum words per chunk sent to the model
    pub chunk_max_words: usize,
    // System prompt sent to Ollama before each chunk of text
    pub system_prompt: String,

    // ---- Resolved absolute paths (computed at load time) ----
    #[serde(skip)]
    pub src_dir_abs: PathBuf,
    #[serde(skip)]
    pub out_dir_abs: PathBuf,
    #[serde(skip)]
    pub book_dir_abs: PathBuf,
}

impl Config {
    // Load config from a JSON file at the given path.
    // Reads the file, parses JSON into Config, resolves relative paths.
    // If the file cannot be read or parsed, prints an error and exits.
    pub fn load(path: &Path) -> Self {
        // Read the entire config file into a String.
        let content = std::fs::read_to_string(path).unwrap_or_else(|err| {
            eprintln!("FATAL: Cannot read config file '{}': {}", path.display(), err);
            std::process::exit(1);
        });
        // Parse the JSON string into our Config struct (auto-deserialized by serde).
        let mut config: Config = serde_json::from_str(&content).unwrap_or_else(|err| {
            eprintln!("FATAL: Cannot parse config file '{}': {}", path.display(), err);
            std::process::exit(1);
        });

        // Resolve relative paths: they are relative to the config file's directory.
        // If the config file is at ~/rustlings/gu_pipe/config.json, then
        // src_dir = "../book/src" resolves to ~/rustlings/book/src.
        let config_dir = path.parent().unwrap_or(Path::new("."));
        config.src_dir_abs = Self::resolve(&config.src_dir, config_dir);
        config.out_dir_abs = Self::resolve(&config.out_dir, config_dir);
        config.book_dir_abs = Self::resolve(&config.book_dir, config_dir);

        config
    }

    // Resolve a path string relative to a base directory.
    // If the path is already absolute, use it as-is.
    // If relative, join it with the base directory.
    fn resolve(path_str: &str, base: &Path) -> PathBuf {
        let p = Path::new(path_str);
        if p.is_absolute() {
            p.to_path_buf()
        } else {
            base.join(p)
        }
    }
}
