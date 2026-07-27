#!/usr/bin/env python3
"""Restore reference-style markdown links lost during translation.

English source uses [text][ref-id] syntax with [ref-id]: url at bottom.
Translation pipeline stripped these to plain text. This script restores them.
"""

import os
import re
import glob

EN_SRC = "/Users/himanshumistry/rustlings/book/src"
GU_SRC = "/Users/himanshumistry/rustlings/gu_pipe/translations/gu/src"

# Link definitions pattern: [ref-id]: url
LINK_DEF_RE = re.compile(r'^\[([^\]]+)\]:\s*(.+)$')


def get_link_defs(filepath):
    """Extract reference link definitions from a markdown file.
    
    Returns dict: {ref_id: url} and list of (text, ref_id, url) tuples from body usage.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # Extract definitions from bottom of file
    defs = {}
    for line in lines:
        m = LINK_DEF_RE.match(line)
        if m:
            defs[m.group(1)] = m.group(2).strip()
    
    # Find all usages of [text][ref-id] in body
    usages = []
    # Match [text][ref] where text can include backticks and quotes
    usage_re = re.compile(r'\[([^\]]+)\]\[([^\]]+)\]')
    for m in usage_re.finditer(content):
        text = m.group(1)
        ref_id = m.group(2)
        if ref_id in defs:
            usages.append((text, ref_id))
    
    return defs, usages


def fix_file(fname):
    en_path = os.path.join(EN_SRC, fname)
    gu_path = os.path.join(GU_SRC, fname)
    
    if not os.path.exists(en_path) or not os.path.exists(gu_path):
        return f"SKIP {fname}: missing"
    
    en_defs, en_usages = get_link_defs(en_path)
    if not en_defs:
        return f"SKIP {fname}: no link defs"
    
    with open(gu_path, 'r', encoding='utf-8') as f:
        gu_content = f.read()
    gu_lines = gu_content.split('\n')
    
    changed = False

    for i, line in enumerate(gu_lines):
        stripped = line.rstrip()
        if '[Cargo][doccargo]' in stripped:
            new_stripped = re.sub(r'\[Cargo\]\[doccargo\]\.(toml|lock)', r'Cargo.\1', stripped)
            if new_stripped != stripped:
                gu_lines[i] = new_stripped
                changed = True
    
    for text, ref_id in en_usages:
        for line_idx in range(len(gu_lines)):
            stripped = gu_lines[line_idx].rstrip()
            if re.search(r'\]\[', stripped):
                continue
            if stripped.startswith('```') or stripped.startswith('#') or stripped.startswith('>') or stripped.startswith('{{#'):
                continue
            if text not in stripped:
                continue
            old_line = gu_lines[line_idx]
            if '`' in text:
                new_line = old_line.replace(text, f'[{text}][{ref_id}]', 1)
            else:
                new_line = re.sub(r'(?<![-\w])' + re.escape(text) + r'(?!(?:\w|\.(?:toml|lock|rs)))', f'[{text}][{ref_id}]', old_line, count=1)
            if new_line != old_line:
                gu_lines[line_idx] = new_line
                changed = True
    
    # Remove duplicate link definitions (keep last occurrence of each ref_id)
    seen_defs = {}
    def_indices = []
    for i, l in enumerate(gu_lines):
        m = LINK_DEF_RE.match(l)
        if m:
            seen_defs[m.group(1)] = i
            def_indices.append(i)
    
    # Remove earlier duplicates (keep only the last occurrence of each ref_id)
    keep_indices = set(seen_defs.values())
    if len(def_indices) > len(keep_indices):
        new_lines = []
        for i, l in enumerate(gu_lines):
            if i in def_indices and i not in keep_indices:
                changed = True
                continue  # Skip this duplicate definition
            new_lines.append(l)
        gu_lines = new_lines
    
    # Add any missing definitions
    existing_ids = set(seen_defs.keys())
    missing_defs = {}
    for text, ref_id in en_usages:
        url = en_defs.get(ref_id)
        if url and ref_id not in existing_ids:
            missing_defs[ref_id] = url
    missing_defs_list = list(missing_defs.items())
    
    if missing_defs_list:
        gu_lines.append('')
        for ref_id, url in missing_defs_list:
            gu_lines.append(f'[{ref_id}]: {url}')
        gu_lines.append('')
        changed = True
    
    if changed:
        with open(gu_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(gu_lines))
        return f"FIX  {fname}: {len(en_usages)} links restored"
    else:
        return f"OK   {fname}: {len(en_usages)} links (no changes needed)"


def main():
    md_files = sorted(glob.glob(os.path.join(GU_SRC, '*.md')))
    results = []
    for md_path in md_files:
        fname = os.path.basename(md_path)
        result = fix_file(fname)
        results.append(result)
    for r in results:
        print(r)


if __name__ == '__main__':
    main()
