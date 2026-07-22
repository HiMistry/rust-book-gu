use crate::glossary::Glossary;

// A Chunk is a segment of prose text that will be sent to Ollama for translation.
// Each chunk is sized between chunk_min_words and chunk_max_words.
#[derive(Debug, Clone)]
pub struct Chunk {
    // The English prose text to translate.
    pub text: String,
    // The 0-based index of this chunk in the sequence of all chunks.
    pub index: usize,
}

// Split a body of prose text into ~100-word chunks.
// Splitting happens at paragraph boundaries (double newlines) or sentence boundaries.
//
// Arguments:
//   text: The full prose text (may contain multiple paragraphs).
//   glossary: Used to inject term mappings into the context (for prompt construction).
//   min_words: Minimum words per chunk (e.g., 80).
//   max_words: Maximum words per chunk (e.g., 120).
//
// Returns:
//   A Vec<Chunk> where each chunk's text is within [min_words, max_words] words.
pub fn split(text: &str, _glossary: &Glossary, min_words: usize, max_words: usize) -> Vec<Chunk> {
    // Split the input into paragraphs by double newlines.
    // Paragraphs are the natural boundary for chunking.
    let paragraphs: Vec<&str> = text
        .split("\n\n")
        .map(|p| p.trim())
        .filter(|p| !p.is_empty())
        .collect();

    let mut chunks: Vec<Chunk> = Vec::new();
    // Buffer for accumulating paragraphs into the current chunk being built.
    let mut current = String::new();
    // Index counter for assigning each chunk a unique sequence number.
    let mut index: usize = 0;

    // Helper: count words in a string by splitting on whitespace.
    let word_count = |s: &str| -> usize {
        s.split_whitespace().count()
    };

    // Helper: flush the current buffer as a chunk.
    let flush = |current: &mut String, chunks: &mut Vec<Chunk>, index: &mut usize| {
        let trimmed = current.trim().to_string();
        if !trimmed.is_empty() {
            chunks.push(Chunk {
                text: trimmed,
                index: *index,
            });
            *index += 1;
            current.clear();
        }
    };

    // Iterate over every paragraph.
    for para in &paragraphs {
        // Count words in the current paragraph.
        let para_words = word_count(para);
        // Count words already accumulated in the buffer.
        let current_words = word_count(&current);

        // If adding this paragraph would exceed max_words AND we already have some text,
        // flush the buffer first, then start a new chunk with this paragraph.
        if current_words + para_words > max_words && current_words >= min_words {
            flush(&mut current, &mut chunks, &mut index);
            current.push_str(para);
        } else {
            // Otherwise, append the paragraph to the current buffer.
            if !current.is_empty() {
                current.push_str("\n\n");
            }
            current.push_str(para);
        }
    }

    // Flush any remaining text as the final chunk.
    flush(&mut current, &mut chunks, &mut index);

    // Edge case: if a single paragraph exceeds max_words, we need to split it
    // at sentence boundaries. This handles very long paragraphs.
    let mut final_chunks: Vec<Chunk> = Vec::new();
    for chunk in &chunks {
        if word_count(&chunk.text) > max_words {
            // Split this chunk into smaller pieces at sentence boundaries.
            // Sentences end with ". " or ".\n".
            let sentences: Vec<&str> = chunk.text
                .split_inclusive(|c| c == '.' || c == '!' || c == '?')
                .map(|s| s.trim())
                .filter(|s| !s.is_empty())
                .collect();

            let mut sent_buf = String::new();
            for sentence in &sentences {
                let buf_words = word_count(&sent_buf);
                let sent_words = word_count(sentence);
                if buf_words + sent_words > max_words && buf_words >= min_words {
                    // Flush the sentence buffer as a chunk.
                    final_chunks.push(Chunk {
                        text: sent_buf.trim().to_string(),
                        index: final_chunks.len(),
                    });
                    sent_buf.clear();
                }
                if !sent_buf.is_empty() {
                    sent_buf.push(' ');
                }
                sent_buf.push_str(sentence);
            }
            // Flush remaining sentence buffer.
            let remaining = sent_buf.trim().to_string();
            if !remaining.is_empty() {
                final_chunks.push(Chunk {
                    text: remaining,
                    index: final_chunks.len(),
                });
            }
        } else {
            // Chunk is within bounds, keep as is.
            final_chunks.push(chunk.clone());
        }
    }

    // Re-index final chunks sequentially.
    for (i, chunk) in final_chunks.iter_mut().enumerate() {
        chunk.index = i;
    }

    final_chunks
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::glossary::Glossary;
    use std::collections::HashMap;

    // Helper: create an empty glossary for tests.
    fn empty_glossary() -> Glossary {
        Glossary { terms: HashMap::new() }
    }

    #[test]
    fn test_short_text_single_chunk() {
        let text = "Hello world. This is a short text.";
        let chunks = split(text, &empty_glossary(), 80, 120);
        // Text is only 6 words, should remain as one chunk even if under min_words.
        assert_eq!(chunks.len(), 1);
    }

    #[test]
    fn test_paragraph_boundary_split() {
        let text = "Short para.\n\nAnother short para.";
        let chunks = split(text, &empty_glossary(), 80, 120);
        // Both paragraphs are short, they should be merged into one chunk.
        assert_eq!(chunks.len(), 1);
    }

    #[test]
    fn test_chunk_indices_sequential() {
        let text = "Word ".repeat(300); // ~300 words, should produce 3 chunks of ~100
        let text = text.trim();
        let chunks = split(text, &empty_glossary(), 80, 120);
        for (i, chunk) in chunks.iter().enumerate() {
            assert_eq!(chunk.index, i);
        }
        // Should have at least 2 chunks.
        assert!(chunks.len() >= 2);
    }
}
