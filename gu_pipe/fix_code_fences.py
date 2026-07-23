#!/usr/bin/env python3
"""Restore code fences in Gujarati translation files.

English code blocks (```console, ```text, ```powershell) lost their
fences during translation. This script matches them by finding the
same command/output lines in Gujarati files and wrapping them.
"""

import os
import re
import glob

EN_SRC = "/Users/himanshumistry/rustlings/book/src"
GU_SRC = "/Users/himanshumistry/rustlings/gu_pipe/translations/gu/src"

def get_en_code_blocks(filepath):
    """Extract (fence_type, [content_lines]) for each English code block."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    blocks = []
    i = 0
    while i < len(lines):
        stripped = lines[i].rstrip()
        m = re.match(r'^```(\w*)', stripped)
        if m:
            fence_type = m.group(1)
            content = []
            i += 1
            while i < len(lines) and not lines[i].rstrip().startswith('```'):
                content.append(lines[i].rstrip())
                i += 1
            if content:
                blocks.append((fence_type, content))
        i += 1
    return blocks


def is_code_line(line):
    """Check if a line is likely a code/command line."""
    s = line.strip()
    if not s:
        return False
    # Shell commands
    if s.startswith('$ '):
        return True
    # PowerShell/CMD prompt
    if s.startswith('> echo '):
        return True
    # Cargo commands
    if s.startswith('cargo ') or s.startswith('$cargo'):
        return True
    # Rust commands
    if s.startswith('rustc '):
        return True
    # Known output lines
    if s == 'Rust is installed now. Great!':
        return True
    if re.match(r'^rustc \d+\.\d+\.\d+', s):
        return True
    return False


def fix_file(fname):
    en_path = os.path.join(EN_SRC, fname)
    gu_path = os.path.join(GU_SRC, fname)
    
    if not os.path.exists(en_path) or not os.path.exists(gu_path):
        return f"SKIP {fname}: missing"
    
    en_blocks = get_en_code_blocks(en_path)
    if not en_blocks:
        return f"SKIP {fname}: no code blocks"
    
    with open(gu_path, 'r', encoding='utf-8') as f:
        gu_lines = f.readlines()
    
    # Build a flat list of "content items" from EN for paragraph-by-paragraph alignment
    # Then match code blocks by content signature
    
    already_fenced = set()
    
    for fence_type, en_content in en_blocks:
        # Get first non-empty EN content line as signature
        sig_lines = [cl.strip() for cl in en_content if cl.strip()]
        if not sig_lines:
            continue
        
        sig = sig_lines[0]
        
        # Find this signature in GU lines (searching forward from last position)
        found = -1
        for gi, gl in enumerate(gu_lines):
            if gi in already_fenced:
                continue
            if gl.rstrip().startswith('```'):
                continue
            if sig in gl.rstrip():
                found = gi
                break
        
        if found < 0:
            print(f"    WARN: signature not found: {sig[:50]}")
            continue
        
        # Determine how many GU lines to wrap
        # English code block has N content lines (including blank lines)
        # Gujarati may have fewer or more lines due to joining/splitting
        # Strategy: match each EN line to GU lines forward
        
        code_start = found
        code_end = found
        
        en_idx = 0
        while en_idx < len(en_content) and code_end < len(gu_lines):
            en_line = en_content[en_idx].strip()
            gu_line = gu_lines[code_end].rstrip()
            
            if gu_line.startswith('```') or gu_line.startswith('#'):
                break
            
            if not en_line:
                # Blank line in EN - skip blank lines in GU too
                while code_end < len(gu_lines) and not gu_lines[code_end].rstrip():
                    if gu_lines[code_end].rstrip().startswith('```'):
                        break
                    code_end += 1
                en_idx += 1
            elif en_line in gu_line or gu_line in en_line:
                code_end += 1
                en_idx += 1
            elif not gu_line:
                code_end += 1
            else:
                break
        
        # Ensure we captured at least the matching line
        if code_end <= found:
            code_end = found + 1
        
        # Wrap
        # Skip blank lines at start
        while code_start < code_end and not gu_lines[code_start].strip():
            code_start += 1
        
        if code_start < code_end and code_start not in already_fenced:
            gu_lines.insert(code_start, f'```{fence_type}\n')
            code_end += 1
            gu_lines.insert(code_end, '```\n')
            # Mark these lines as already fenced
            for fi in range(code_start, code_end + 1):
                already_fenced.add(fi)
    
    with open(gu_path, 'w', encoding='utf-8') as f:
        f.writelines(gu_lines)
    
    return f"OK   {fname}: {len(en_blocks)} code blocks"


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
