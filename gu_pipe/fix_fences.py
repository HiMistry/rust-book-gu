#!/usr/bin/env python3
"""Fix code fence structural corruption in Gujarati translations.

Handles two patterns:
1. Gujarati prose wrapped inside ```lang ... ``` code blocks
2. Inline ``` used in prose lines (should be separate code blocks)

Also fixes corrupted include paths like [Cargo][doccargo] -> Cargo.toml
"""

import os
import re
import glob

GU_SRC = "/Users/himanshumistry/rustlings/gu_pipe/translations/gu/src"

HAS_GUJARATI = re.compile(r'[\u0A80-\u0AFF]')

def has_gujarati(text):
    return bool(HAS_GUJARATI.search(text))

def fix_inline_fences(line):
    """Split inline ```rust...``` from a prose line into proper fence format."""
    m = re.search(r'(```\w*\s*.+?```)', line)
    if not m:
        return [line]

    inline_block = m.group(1)
    before = line[:m.start()].strip()
    after = line[m.end():].strip()

    result = []
    if before:
        result.append(before + '\n')
    result.append('\n')

    fence_match = re.match(r'(```(\w*))\s*(.*?)```', inline_block, re.DOTALL)
    if fence_match:
        fence_type = fence_match.group(1)
        code = fence_match.group(3).strip()
        result.append(fence_type + '\n')
        result.append(code + '\n')
        result.append('```\n')
    result.append('\n')

    if after:
        result.append(after.rstrip() + '\n')

    return result

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    modified = False
    new_lines = []
    i = 0

    while i < len(lines):
        stripped = lines[i].rstrip()

        in_fence = stripped.startswith('```')
        if not in_fence:
            if '```' in stripped:
                fence_markers = re.findall(r'```\w*', stripped)
                if fence_markers:
                    has_gu = has_gujarati(stripped[:stripped.find('```')])
                    if has_gu:
                        parts = fix_inline_fences(stripped)
                        new_lines.extend(parts)
                        modified = True
                        i += 1
                        continue
            new_lines.append(lines[i])
            i += 1
            continue

        fence_line = stripped
        fence_lang = ''
        lang_match = re.match(r'```(\w*)', fence_line)
        if lang_match:
            fence_lang = lang_match.group(1)

        fence_start = i
        i += 1
        content_lines = []
        while i < len(lines) and not lines[i].rstrip().startswith('```'):
            content_lines.append(lines[i].rstrip())
            i += 1

        if i < len(lines):
            i += 1

        if fence_lang == '' or fence_lang == 'text':
            total_content = '\n'.join(content_lines)
            if has_gujarati(total_content) and len(total_content) > 20:
                for cl in content_lines:
                    if '```' in cl and has_gujarati(cl[:cl.find('```')]):
                        parts = fix_inline_fences(cl)
                        new_lines.extend(parts)
                        modified = True
                    else:
                        new_lines.append(cl + '\n')
                if new_lines and new_lines[-1].strip():
                    new_lines.append('\n')
                modified = True
                continue

        contains_only_prose = False
        total_nonempty = sum(1 for c in content_lines if c.strip())
        if total_nonempty > 0:
            gu_count = sum(1 for c in content_lines if has_gujarati(c))
            if gu_count == total_nonempty and total_nonempty > 0:
                contains_only_prose = True

        first_nonempty = next((c for c in content_lines if c.strip()), '')
        starts_with_gu = has_gujarati(first_nonempty) if first_nonempty else False

        first_code_line = next((c for c in content_lines if c.strip() and not has_gujarati(c)), '')

        if contains_only_prose or (starts_with_gu and not first_code_line):
            for cl in content_lines:
                if '```' in cl and has_gujarati(cl[:cl.find('```')]):
                    parts = fix_inline_fences(cl)
                    new_lines.extend(parts)
                    modified = True
                else:
                    new_lines.append(cl + '\n')
            if new_lines and new_lines[-1].strip():
                new_lines.append('\n')
            modified = True
            continue

        new_lines.append(fence_line + '\n')

        inside_inline_fence = False
        for cl in content_lines:
            if '```' in cl and has_gujarati(cl):
                parts = fix_inline_fences(cl)
                new_lines.extend(parts)
                modified = True
            else:
                new_lines.append(cl + '\n')

        if content_lines and not content_lines[-1].strip().startswith('```'):
            new_lines.append('```\n')

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        return True
    return False

def fix_include_paths():
    """Fix corrupted [Cargo][doccargo] in include paths only."""
    for md_path in glob.glob(os.path.join(GU_SRC, '*.md')):
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        original = content
        content = re.sub(r'\{\{(#include|#rustdoc_include)[^}]*?\[Cargo\]\[doccargo\][^}]*?\}\}',
                         lambda m: m.group(0).replace('[Cargo][doccargo]', 'Cargo'),
                         content)
        if content != original:
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"FIXED_INCLUDE {os.path.basename(md_path)}")

def main():
    fix_include_paths()

    md_files = sorted(glob.glob(os.path.join(GU_SRC, '*.md')))
    changed = 0
    for md_path in md_files:
        fname = os.path.basename(md_path)
        if fix_file(md_path):
            print(f"FIXED_FENCE {fname}")
            changed += 1
    print(f"\n{changed}/{len(md_files)} files had fence corruption fixed")

if __name__ == '__main__':
    main()
