#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

EN_SRC="/tmp/book-src/src"
EN_EPUB_NAME="the-rust-programming-language-en.epub"
GU_OUT="$(cd ../gu_pipe/translations/gu && pwd)/book/epub"

[ -d "$EN_SRC" ] || { echo "missing English source at $EN_SRC"; exit 1; }

rm -rf src
cp -R "$EN_SRC" src

mdbook build .

EPUB_SRC="$(find book -maxdepth 2 -name '*.epub' | head -1)"
[ -n "$EPUB_SRC" ] || { echo "epub not produced"; exit 1; }

mkdir -p "$GU_OUT"
cp "$EPUB_SRC" "$GU_OUT/$EN_EPUB_NAME"

echo "English epub -> $GU_OUT/$EN_EPUB_NAME"
