#!/usr/bin/env python3
"""Restore bullet list markers (- ) in Gujarati translations using position-based matching.

English source has bullet items like "- text". Gujarati translation drops
the "- " prefix. This script uses relative line positions to locate the
right paragraphs and re-adds "- ".
"""

import os
import re
import glob

EN_SRC = "/Users/himanshumistry/rustlings/book/src"
GU_SRC = "/Users/himanshumistry/rustlings/gu_pipe/translations/gu/src"

def code_spans(text):
    return re.findall(r'`([^`]+)`', text)

def find_bullet_lists(lines):
    """Return [(lead_in_line, en_line_number, [bullet_text, ...]), ...]"""
    lists = []
    i = 0
    while i < len(lines):
        stripped = lines[i].rstrip()
        if not stripped.startswith('- '):
            i += 1
            continue

        lead_in = ''
        lead_in_lineno = 0
        for j in range(i - 1, -1, -1):
            prev = lines[j].rstrip()
            if prev and not prev.startswith('- ') and not prev.startswith('#'):
                lead_in = prev
                lead_in_lineno = j
                break

        bullets = []
        first_lineno = i
        while i < len(lines):
            line = lines[i].rstrip()
            if not line.startswith('- '):
                break
            item = line[2:]
            i += 1
            while i < len(lines) and lines[i].rstrip() and not lines[i].rstrip().startswith('- ') and not lines[i].rstrip().startswith('#'):
                item += ' ' + lines[i].rstrip()
                i += 1
            bullets.append(item)

        if bullets:
            lists.append((lead_in, lead_in_lineno, first_lineno, bullets))
    return lists

def find_paragraphs_after(lines, start_line, count):
    """Find `count` paragraphs starting near `start_line` in the file.
    Returns list of line indices (first line of each paragraph)."""
    result = []
    i = start_line
    while i < len(lines) and len(result) < count:
        stripped = lines[i].rstrip()

        skip = (stripped.startswith('#') or stripped.startswith('```')
                or stripped.startswith('<') or stripped.startswith('[')
                or stripped.startswith('</') or not stripped)
        if skip:
            i += 1
            continue

        if stripped.startswith('- '):
            result.append(i)
            i += 1
            continue

        result.append(i)
        i += 1
        while i < len(lines) and lines[i].rstrip():
            if lines[i].rstrip().startswith('- '):
                break
            i += 1

        i += 1

    return result

def find_lead_in_line(lead_in, gu_lines, approx_pos):
    """Find the lead-in line in Gujarati text near approx_pos."""
    spans = code_spans(lead_in)
    if spans:
        for offset in range(0, 20):
            for idx in [approx_pos + offset, approx_pos - offset]:
                if 0 <= idx < len(gu_lines):
                    if all(s in gu_lines[idx] for s in spans):
                        return idx + 1

    words = [w.strip('*_`[](),.') for w in lead_in.split()
             if len(w.strip('*_`[](),.')) > 3]
    if words:
        for offset in range(0, 20):
            for idx in [approx_pos + offset, approx_pos - offset]:
                if 0 <= idx < len(gu_lines):
                    if any(w.lower() in gu_lines[idx].lower() for w in words[:3]):
                        return idx + 1

    return None

def fix_file(fname):
    en_path = os.path.join(EN_SRC, fname)
    gu_path = os.path.join(GU_SRC, fname)

    if not os.path.exists(en_path) or not os.path.exists(gu_path):
        return f"SKIP {fname}: missing"

    with open(en_path, 'r', encoding='utf-8') as f:
        en_lines = f.readlines()

    with open(gu_path, 'r', encoding='utf-8') as f:
        gu_lines = f.readlines()

    en_lists = find_bullet_lists(en_lines)
    if not en_lists:
        return f"OK   {fname}: no bullet lists"

    if any(l.rstrip().startswith('- ') for l in gu_lines):
        return f"OK   {fname}: bullets already present"

    ratio = len(gu_lines) / len(en_lines) if en_lines else 1
    modified = False

    for lead_in, lead_lineno, first_lineno, en_bullets in en_lists:
        approx_pos = int(first_lineno * ratio)

        gu_start = find_lead_in_line(lead_in, gu_lines, approx_pos)
        if gu_start is None:
            first_spans = code_spans(en_bullets[0])
            if first_spans:
                for offset in range(0, 15):
                    for idx in [approx_pos + offset, approx_pos - offset]:
                        if 0 <= idx < len(gu_lines):
                            if all(s in gu_lines[idx] for s in first_spans):
                                gu_start = idx
                                break
                    if gu_start is not None:
                        break

        if gu_start is None:
            gu_start = max(0, approx_pos - 5)

        targets = find_paragraphs_after(gu_lines, gu_start, len(en_bullets))

        for gi in targets:
            stripped = gu_lines[gi].rstrip()
            if stripped.startswith('> '):
                inner = stripped[2:]
                gu_lines[gi] = '> - ' + inner + '\n'
            elif stripped.startswith('>'):
                inner = stripped[1:]
                gu_lines[gi] = '> - ' + inner + '\n'
            elif not stripped.startswith('- '):
                gu_lines[gi] = '- ' + gu_lines[gi]
            modified = True

    if modified:
        with open(gu_path, 'w', encoding='utf-8') as f:
            f.writelines(gu_lines)
        total = sum(len(b) for _, _, _, b in en_lists)
        return f"FIXED {fname}: {len(en_lists)} lists, {total} items"
    return f"OK   {fname}: no changes made"

def main():
    md_files = sorted(glob.glob(os.path.join(GU_SRC, '*.md')))
    results = []
    for md_path in md_files:
        fname = os.path.basename(md_path)
        result = fix_file(fname)
        results.append(result)
        print(result)
    fixed = sum(1 for r in results if r.startswith('FIXED'))
    print(f"\n{fixed}/{len(results)} files fixed")

if __name__ == '__main__':
    main()
