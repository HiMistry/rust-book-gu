use crate::config::Config;
use std::process::Command;

// Build the translated book as an EPUB file.
//
// Steps:
//   1. Verify that mdbook is installed (needed to build the HTML from markdown).
//   2. Check if pandoc is installed (needed to convert HTML to EPUB).
//   3. Run `mdbook build` on the translated book directory.
//   4. Convert the built HTML to EPUB using pandoc.
//
// The output EPUB is written to book/translations/gu/build/epub/rust-book-gu.epub
pub fn build_epub(config: &Config) -> Result<(), String> {
    let book_dir = &config.book_dir_abs;
    let out_dir = &config.out_dir_abs;
    let translations_root = out_dir.parent().ok_or("out_dir has no parent")?;
    let translations_dir = translations_root.parent().ok_or("translations dir has no parent")?;

    // Step 1: Check if mdbook is installed.
    let mdbook_check = Command::new("which")
        .arg("mdbook")
        .output()
        .map_err(|e| format!("Cannot check for mdbook: {}", e))?;
    if !mdbook_check.status.success() {
        return Err("mdbook is not installed. Install it with: cargo install mdbook".to_string());
    }

    // Step 2: Check if pandoc is installed.
    let pandoc_check = Command::new("which")
        .arg("pandoc")
        .output()
        .map_err(|e| format!("Cannot check for pandoc: {}", e))?;
    if !pandoc_check.status.success() {
        return Err("pandoc is not installed. Install it with: brew install pandoc".to_string());
    }

    // Step 3: Create the translated book's book.toml if it doesn't exist.
    // We need a book.toml in the translation directory for mdbook to work.
    let translated_book_toml = translations_dir.join("book.toml");
    if !translated_book_toml.exists() {
        // Copy the original book.toml as a starting point.
        let original_book_toml = book_dir.join("book.toml");
        if original_book_toml.exists() {
            std::fs::copy(&original_book_toml, &translated_book_toml)
                .map_err(|e| format!("Cannot copy book.toml: {}", e))?;
        } else {
            // Create a minimal book.toml for the translation.
            let minimal_toml = r#"[book]
title = "The Rust Programming Language (Gujarati)"
authors = ["Steve Klabnik", "Carol Nichols", "Chris Krycho"]

[output.html]
"#;
            std::fs::write(&translated_book_toml, minimal_toml)
                .map_err(|e| format!("Cannot write book.toml: {}", e))?;
        }
    }

    // Step 4: Run mdbook build in the translations directory.
    println!("  Building translated book with mdbook...");
    let mdbook_output = Command::new("mdbook")
        .args(["build"])
        .current_dir(translations_dir)
        .output()
        .map_err(|e| format!("Failed to run mdbook: {}", e))?;
    if !mdbook_output.status.success() {
        let stderr = String::from_utf8_lossy(&mdbook_output.stderr);
        return Err(format!("mdbook build failed:\n{}", stderr));
    }
    println!("  mdbook build completed successfully.");

    // Step 5: Build the EPUB using pandoc.
    // Find the built HTML files (mdbook outputs to book/).
    let html_dir = translations_dir.join("book");
    if !html_dir.exists() {
        return Err(format!(
            "mdbook output directory '{}' not found. mdbook may have failed silently.",
            html_dir.display()
        ));
    }

    // Create EPUB output directory.
    let epub_dir = translations_dir.join("build").join("epub");
    std::fs::create_dir_all(&epub_dir)
        .map_err(|e| format!("Cannot create epub directory: {}", e))?;

    // The main HTML file for the book is index.html in the output directory.
    let index_html = html_dir.join("index.html");
    if !index_html.exists() {
        return Err(format!(
            "index.html not found at '{}'. Cannot build EPUB.",
            index_html.display()
        ));
    }

    let epub_path = epub_dir.join("rust-book-gu.epub");
    println!("  Converting to EPUB with pandoc...");
    let pandoc_output = Command::new("pandoc")
        .args([
            index_html.to_str().unwrap(),
            "-o",
            epub_path.to_str().unwrap(),
            "--metadata",
            "title=The Rust Programming Language (Gujarati)",
            "--metadata",
            "author=Steve Klabnik, Carol Nichols, Chris Krycho",
            "--metadata",
            "language=gu",
            "-t",
            "epub3",
        ])
        .output()
        .map_err(|e| format!("Failed to run pandoc: {}", e))?;
    if !pandoc_output.status.success() {
        let stderr = String::from_utf8_lossy(&pandoc_output.stderr);
        return Err(format!("pandoc conversion failed:\n{}", stderr));
    }

    println!(
        "  EPUB created successfully at: {}",
        epub_path.display()
    );
    Ok(())
}
