# AGENTS.md

## Project overview
- **rust-book-gu**: Gujarati translation of *The Rust Programming Language* (the official Rust book), translated from the latest English source (rust-lang/book).
- Published to GitHub Pages at `https://himistry.github.io/rust-book-gu/`.
- Repo: `https://github.com/HiMistry/rust-book-gu` (branches: `main`, `gh-pages`).

## Directory layout
- `gu_pipe/translations/gu/` — the Gujarati book root.
  - `src/` — 112 Gujarati markdown chapters with `<Listing>` tags and `{{#rustdoc_include ../listings/...}}` / `{{#include ../listings/...}}` directives (728 directives total, all validated).
  - `listings/` — 1975 English listing files (8.6 MB). **MUST stay byte-identical to English originals** — code is never translated. Tracked in git.
  - `book.toml` — mdbook config: `[output.html]` (css/js, redirects), `[output.epub]`, and `[preprocessor.trpl-*]` entries that fail benignly (see below).
  - `book/` — mdbook build output. Gitignored, but HTML + epubs are force-added (`git add -f`) so they ship in the repo; this dir is copied verbatim to gh-pages on deploy.
  - `book/epub/` — epub output dir; contains the two published epubs.
- `english-epub/` — English epub build workspace (tracked): minimal epub-only `book.toml`, `build.sh`, and a `listings/` symlink → `../gu_pipe/translations/gu/listings`. Its `src/` and `book/` are gitignored (populated by build.sh from a local clone).
- `gu_pipe/translate/` — Rust translation tool (translates English → Gujarati via local Ollama, see `gu_pipe/config.json`).

## Build commands
- **GU book (HTML + epub)**: `mdbook build gu_pipe/translations/gu/`
  - Output HTML → `gu_pipe/translations/gu/book/`; epub → `gu_pipe/translations/gu/book/epub/<title>.epub` (title-based name).
  - **Epub must be renamed manually** after each build: `<title>.epub` → `the-rust-programming-language-gu.epub`.
- **English epub**: `./english-epub/build.sh` (requires the English source at `/tmp/book-src/src`; copies it into the gitignored `english-epub/src/`, builds, and copies the result to `gu_pipe/translations/gu/book/epub/the-rust-programming-language-en.epub`).
- Tools: `~/.cargo/bin/mdbook` (v0.5.4, modular) and `~/.cargo/bin/mdbook-epub` (v0.5.4 plugin).

## Key mdbook facts / gotchas
- **mdbook 0.5.4 has NO built-in epub backend** (removed in the modular 0.5.x line). Epubs require the `mdbook-epub` plugin, activated by an `[output.epub]` section in book.toml. Without it, no epub is produced.
- **Missing trpl preprocessors are benign**: book.toml declares `[preprocessor.trpl-listing]` / `[preprocessor.trpl-note]` with `command = "cargo run --manifest-path packages/mdbook-trpl/Cargo.toml ..."`, but `packages/` does not exist in this repo. mdbook logs `error: manifest path ... does not exist` and **skips them**; the build still succeeds. The core `links` preprocessor expands all `{{#include}}`/`{{#rustdoc_include}}` (anchors, `:N:M` line ranges, and `:all`) even inside `<Listing>` tags — so code renders correctly without the trpl preprocessor.
- **`../listings/` is resolved relative to each chapter's dir** (src_dir + chapter parent), so `listings/` must be a sibling of `src/`. The `mdbook build_dir_for` logic: with a single renderer the output goes directly to `book/`; with multiple renderers it goes to `book/<renderer-name>/` (this is why the GU build outputs epubs under `book/epub/` but the english-epub-only build outputs directly under `book/`).
- **Symlink gotcha**: do NOT make `src/` a symlink. `{{#include ../listings/...}}` is resolved lexically and the OS walks `..` from the symlink *target*, so a `src -> /tmp/book-src/src` link resolves `../listings` to `/tmp/book-src/listings` (which doesn't exist). Keep `src/` a real (gitignored) directory and only symlink `listings/`.
- Unclosed-HTML warnings (ch16-03, ch17-01, ch17-05) are pre-existing and harmless.
- `[[[build] extra-watch-dirs` and `[rust] edition = "2024"` are set in book.toml.

## Listings / English source
- English source is pinned at rust-lang/book commit **`917544888a55e4da7109bdba8c88c893c0da70f4`** = current `refs/heads/main` of rust-lang/book (verified up to date).
- GU include references match English source exactly (704 = 704; no EN-only, no GU-only).
- `:all` anchors use double `// ANCHOR: all` markers and do NOT require `ANCHOR_END` (mdbook's `take_rustdoc_include_anchored_lines` handles them).
- Local clones (ephemeral, in `/tmp`, cleared on reboot — re-fetch with `git clone https://github.com/rust-lang/book.git` and check out the pinned commit):
  - `/tmp/book-src` — English source (src/ only; no listings).
  - `/tmp/en-book` — sparse clone (listings/ only).

## gh-pages deployment workflow
1. `git worktree add /tmp/book-gh-pages gh-pages`
2. In the worktree: `git rm -rq --ignore-unmatch .`, then `rm -f .nojekyll`
3. `cp -R gu_pipe/translations/gu/book/. /tmp/book-gh-pages/` (mdbook's output includes `.nojekyll`, so it comes back)
4. `git add -A && git commit -m "Deploy: ..." && git push origin gh-pages`
5. Back in the main repo: `git worktree remove /tmp/book-gh-pages`

## GitHub Pages behavior
- Propagation takes ~1–2 minutes after push. Files can briefly return 404 (new) or 200 (old) during that window; verify against `raw.githubusercontent.com/HiMistry/rust-book-gu/gh-pages/<path>` to confirm the deploy landed, then re-test the site URL.
- epub files served correctly (correct content-length; no special config needed).

## URLs
- Site: `https://himistry.github.io/rust-book-gu/`
- README: `https://github.com/HiMistry/rust-book-gu/blob/main/README.md`
- GU epub: `https://himistry.github.io/rust-book-gu/epub/the-rust-programming-language-gu.epub`
- EN epub: `https://himistry.github.io/rust-book-gu/epub/the-rust-programming-language-en.epub`
- Epubs follow the `the-rust-programming-language-{gu,en}.epub` naming convention. Keep both names in sync in README, the epub folder, the repo, and gh-pages.

## gitignore notes
- `gu_pipe/translations/gu/book/` is gitignored but its HTML/epubs are force-added so they stay in the repo.
- `gu_pipe/translations/gu/listings/` was removed from `.gitignore` (source, tracked).
- `english-epub/{book,src}/` ignored; `english-epub/listings` is a tracked symlink (mode 120000).
