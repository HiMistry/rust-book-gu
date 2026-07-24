#!/usr/bin/env python3
"""Strip <Listing> tags from Gujarati translation files, preserving captions.

<Listing number="1-1" file-name="main.rs" caption="A program..."> 
  ```rust
  ...
  ```
</Listing>

Becomes:

**Listing 1-1: A program...**

```rust
...
```
"""

import os
import re
import glob

GU_SRC = "/Users/himanshumistry/rustlings/gu_pipe/translations/gu/src"

listing_pattern = re.compile(r'<Listing\s+([^>]*)>')
closing_pattern = re.compile(r'</Listing>')

def parse_listing_attrs(attrs_str):
    num = ''
    caption = ''
    for m in re.finditer(r'(\w+(?:-\w+)*)\s*=\s*"([^"]*)"', attrs_str):
        key, val = m.group(1), m.group(2)
        if key == 'number':
            num = val
        elif key == 'caption':
            caption = val
    return num, caption

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    
    def replace_listing(m):
        attrs = m.group(1)
        num, caption = parse_listing_attrs(attrs)
        if num and caption:
            return f'**Listing {num}: {caption}**\n'
        return ''
    
    content = listing_pattern.sub(replace_listing, content)
    content = closing_pattern.sub('', content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    md_files = sorted(glob.glob(os.path.join(GU_SRC, '*.md')))
    changed = 0
    for md_path in md_files:
        fname = os.path.basename(md_path)
        if fix_file(md_path):
            print(f"FIXED {fname}")
            changed += 1
    print(f"\n{changed}/{len(md_files)} files had <Listing> tags removed")

if __name__ == '__main__':
    main()
