use crate::chunk::Chunk;
use crate::config::Config;
use crate::glossary::Glossary;
use serde::Deserialize;
use std::time::Duration;

// The response from Ollama's /api/generate endpoint.
#[derive(Debug, Deserialize)]
struct OllamaResponse {
    // The generated text (translated Gujarati in our case).
    response: String,
    // True if generation completed (reached num_predict or stopped naturally).
    done: bool,
}

// Translate a single Chunk of English prose into Gujarati via Ollama.
// Returns the translated text as a String.
//
// Arguments:
//   chunk: The Chunk containing ~100 words of English prose plus its index.
//   config: Pipeline config (model name, Ollama URL, temperature, max_retries).
//   glossary: The Rust→Gujarati term mappings, injected into the prompt.
//   client: A shared reqwest blocking HTTP client (reused for all requests).
//
// How it works:
//   1. Build a prompt: system instructions + glossary terms + chunk text.
//   2. POST to Ollama's /api/generate endpoint as JSON.
//   3. Extract the generated text from the response.
//   4. If the request fails, retry up to config.max_retries times.
pub fn translate_chunk(
    chunk: &Chunk,
    config: &Config,
    glossary: &Glossary,
    client: &reqwest::blocking::Client,
) -> Result<String, String> {
    // Construct the full prompt that Ollama will process.
    // It has three parts:
    //   1. System prompt: overall instructions and rules for translation.
    //   2. Glossary terms: specific word mappings to ensure consistency.
    //   3. The chunk text: the actual prose to translate.
    let prompt = format!(
        "{}\n\nGlossary terms (use these translations for consistency):\n{}\n\nCHUNK TO TRANSLATE:\n{}",
        config.system_prompt.trim(),
        glossary.to_prompt_string(),
        chunk.text
    );

    // Prepare the JSON body for the POST request to Ollama.
    // temperature=0.0 ensures deterministic output (no creativity, same input = same output).
    // num_predict caps the maximum output tokens (500 should cover ~100 English words → Gujarati).
    let body = serde_json::json!({
        "model": config.model,
        "prompt": prompt,
        "stream": false,
        "options": {
            "temperature": config.temperature,
            "num_predict": 500
        }
    });

    let url = format!("{}/api/generate", config.ollama_url.trim_end_matches('/'));

    // Attempt the request up to max_retries times.
    let mut last_error: Option<String> = None;
    for attempt in 0..=config.max_retries {
        // If this is a retry (attempt > 0), wait before trying again.
        // Wait time: 2^attempt seconds (1s, 2s, 4s, ...) — exponential backoff.
        if attempt > 0 {
            let wait_secs = 2u64.pow(attempt);
            eprintln!(
                "  Retry {}/{} for chunk {} after {}s...",
                attempt, config.max_retries, chunk.index, wait_secs
            );
            std::thread::sleep(Duration::from_secs(wait_secs));
        }

        // Send the POST request to Ollama.
        match client.post(&url).json(&body).send() {
            Ok(response) => {
                // Check if the HTTP status code indicates success (200-299).
                if !response.status().is_success() {
                    let status = response.status();
                    last_error = Some(format!("HTTP {}", status));
                    eprintln!("  Ollama returned status {} on attempt {}", status, attempt + 1);
                    continue; // Try again.
                }

                // Parse the JSON response body into our OllamaResponse struct.
                match response.json::<OllamaResponse>() {
                    Ok(ollama_resp) => {
                        let translated = ollama_resp.response.trim().to_string();
                        // Verify the translation is non-empty.
                        if translated.is_empty() {
                            last_error = Some("Empty response from Ollama".to_string());
                            eprintln!("  Ollama returned empty text on attempt {}", attempt + 1);
                            continue;
                        }
                        // Success! Return the translated text.
                        return Ok(translated);
                    }
                    Err(err) => {
                        last_error = Some(format!("JSON parse error: {}", err));
                        eprintln!("  Failed to parse Ollama response on attempt {}: {}", attempt + 1, err);
                        continue;
                    }
                }
            }
            Err(err) => {
                last_error = Some(format!("HTTP error: {}", err));
                eprintln!("  HTTP request failed on attempt {}: {}", attempt + 1, err);
                continue;
            }
        }
    }

    // All retries exhausted. Return the last error message.
    Err(format!(
        "Failed to translate chunk {} after {} attempts. Last error: {}",
        chunk.index,
        config.max_retries + 1,
        last_error.unwrap_or_else(|| "Unknown error".to_string())
    ))
}
