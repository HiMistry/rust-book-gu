use std::collections::HashMap;

// Glossary holds a mapping from English Rust terms to their Gujarati translations.
// Loaded from glossary.json.
// Used to:
//   1. Inject the mappings into the Ollama prompt so the model uses consistent terms.
//   2. Post-verify the output contains the correct Gujarati terms.
#[derive(Debug)]
pub struct Glossary {
    // Key: English term (e.g. "ownership").
    // Value: Gujarati translation (e.g. "માલિકી").
    pub terms: HashMap<String, String>,
}

impl Glossary {
    // Load glossary from a JSON file at the given path.
    // The JSON should be a flat object: { "english_word": "gujarati_word", ... }
    pub fn load(path: &std::path::Path) -> Self {
        // Read the entire glossary file into a String.
        let content = std::fs::read_to_string(path).unwrap_or_else(|err| {
            eprintln!("WARNING: Cannot read glossary file '{}': {}", path.display(), err);
            // If no glossary file exists, use an empty map so the pipeline still works.
            String::from("{}")
        });
        // Parse JSON into HashMap<String, String>.
        let terms: HashMap<String, String> = serde_json::from_str(&content).unwrap_or_else(|err| {
            eprintln!("WARNING: Cannot parse glossary '{}': {}. Using empty glossary.", path.display(), err);
            HashMap::new()
        });
        Glossary { terms }
    }

    // Format the glossary as a prompt string for Ollama.
    // This produces text like: "ownership = માલિકી, borrowing = ઉધાર, ..."
    // The model sees these mappings so it uses consistent terminology.
    pub fn to_prompt_string(&self) -> String {
        // Collect all key=value pairs into a Vec, sort by key for consistent output.
        let mut pairs: Vec<(&String, &String)> = self.terms.iter().collect();
        pairs.sort_by(|a, b| a.0.cmp(b.0));
        // Format each pair as "english = ગુજરાતી" and join with ", ".
        pairs
            .iter()
            .map(|(en, gu)| format!("{} = {}", en, gu))
            .collect::<Vec<_>>()
            .join(", ")
    }

    // Check if the translated output contains all expected Gujarati terms.
    // Returns a list of English terms that are missing from the output.
    // This is a basic quality check to catch cases where the model ignored the glossary.
    pub fn verify(&self, translated_text: &str) -> Vec<String> {
        let mut missing = Vec::new();
        // Iterate over every term in the glossary.
        for (en_term, gu_term) in &self.terms {
            // If the Gujarati term is NOT found in the translated text, flag it.
            if !translated_text.contains(gu_term) {
                missing.push(en_term.clone());
            }
        }
        missing
    }
}
