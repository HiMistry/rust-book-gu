use serde::{Deserialize, Serialize};
use std::collections::HashSet;
use std::path::Path;

// Progress tracks which files have been successfully translated.
// It is saved to progress.json after each file completes.
// This enables the pipeline to resume from where it left off if interrupted.
#[derive(Debug, Serialize, Deserialize)]
pub struct Progress {
    // Set of file paths (relative to src_dir) that have been translated.
    pub completed: HashSet<String>,
}

impl Progress {
    // Load progress from a JSON file.
    // If the file does not exist, returns an empty Progress (starting fresh).
    pub fn load(path: &Path) -> Self {
        match std::fs::read_to_string(path) {
            Ok(content) => {
                // Try to parse the JSON. If it fails, start fresh.
                serde_json::from_str(&content).unwrap_or_else(|err| {
                    eprintln!("WARNING: Corrupted progress file '{}': {}. Starting fresh.", path.display(), err);
                    Progress {
                        completed: HashSet::new(),
                    }
                })
            }
            Err(_) => {
                // File doesn't exist yet — first run.
                Progress {
                    completed: HashSet::new(),
                }
            }
        }
    }

    // Save progress to a JSON file.
    // Overwrites any existing file at the path.
    pub fn save(&self, path: &Path) {
        // Serialize to pretty-printed JSON for human readability.
        let json = serde_json::to_string_pretty(self).unwrap_or_else(|err| {
            eprintln!("WARNING: Cannot serialize progress: {}", err);
            return String::from("{}");
        });
        // Write to file. If the parent directory doesn't exist, create it.
        if let Some(parent) = path.parent() {
            std::fs::create_dir_all(parent).ok();
        }
        std::fs::write(path, &json).unwrap_or_else(|err| {
            eprintln!("WARNING: Cannot write progress file '{}': {}", path.display(), err);
        });
    }

    // Check if a file has already been translated.
    // file_path is a relative path like "ch01-00-getting-started.md".
    pub fn is_completed(&self, file_path: &str) -> bool {
        self.completed.contains(file_path)
    }

    // Mark a file as completed and save the progress to disk.
    pub fn mark_completed(&mut self, file_path: &str, path: &Path) {
        self.completed.insert(file_path.to_string());
        self.save(path);
    }
}
