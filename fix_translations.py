#!/usr/bin/env python3
"""Auto-fix Gujarati translations: headings, terms, bilingual content, error formatting."""

import os
import re
import glob

GU_SRC = "/Users/himanshumistry/rustlings/gu_pipe/translations/gu/src"
EN_SRC = "/Users/himanshumistry/rustlings/book/src"

GU_CHARS = set(chr(c) for c in range(0x0A80, 0x0B00))

def has_gu(text):
    return any(c in GU_CHARS for c in text)

def first_gu_pos(text):
    for i, c in enumerate(text):
        if c in GU_CHARS:
            return i
    return -1

def last_gu_pos(text):
    last = -1
    for i, c in enumerate(text):
        if c in GU_CHARS:
            last = i
    return last

# ── Term replacements (outside backticks/code) ──
TERM_MAP = [
    ("ચલોને", "variable"),
    ("ચલોમાં", "variable"),
    ("ચલોથી", "variable"),
    ("ચલોના", "variable's"),
    ("ચલોની", "variable's"),
    ("ચલોનો", "variable's"),
    ("ચલો ", "variables "),
    ("ચલો.", "variables."),
    ("ચલો,", "variables,"),
    ("ચલો:", "variables:"),
    ("ચલને", "variable"),
    ("ચલમાં", "variable"),
    ("ચલથી", "variable"),
    ("ચલના", "variable's"),
    ("ચલની", "variable's"),
    ("ચલનો", "variable's"),
    ("પર્યાવર્ણ", "environment"),
    ("વપરાશકર્તા", "user"),
    ("નિર્દેશક", "pointer"),
    ("શામેલ", "સમાવિષ્ટ"),
    ("ફક્ત", "માત્ર"),
    ("ખાસ", "વિશેષ"),
    ("દલીલોનું", "Argument"),
    ("દલીલ", "Argument"),
    ("જનીન", "generic"),
]

BOUNDARY = r'[\s.,;:!?()\[\]{}"\'\-]'

def replace_in_prose(text):
    """Replace terms only outside backtick pairs."""
    parts = text.split('`')
    result = []
    for i, part in enumerate(parts):
        if i % 2 == 0:
            r = part
            for old, new in TERM_MAP:
                r = r.replace(old, new)
            r = re.sub(
                r'(?:^|(?<=' + BOUNDARY + r'))ચલ(?=' + BOUNDARY + r'|$)',
                'variable', r
            )
            result.append(r)
        else:
            result.append(part)
    return '`'.join(result)

def strip_bilingual(text):
    """Remove bilingual content - strips English before Gujarati."""
    if not has_gu(text):
        return text
    
    pos = first_gu_pos(text)
    if pos < 40:
        return text
    
    gu_part = text[pos:]
    if len(gu_part.strip()) < 20:
        return text
    
    # Extract backtick terms from English prefix that may be missing in Gujarati
    eng_prefix = text[:pos]
    backtick_terms = re.findall(r'`[^`]+`', eng_prefix)
    # Deduplicate and check if term (with or without backticks) appears in Gujarati
    seen = set()
    missing = []
    for bt in backtick_terms:
        term_text = bt.strip('`')
        if bt not in seen and bt not in gu_part and term_text not in gu_part:
            seen.add(bt)
            missing.append(bt)
    
    if missing:
        return ' '.join(missing) + ' ' + gu_part
    
    return gu_part

def strip_trailing_english(text):
    """Remove trailing English prose after Gujarati text."""
    if not has_gu(text):
        return text
    
    last = last_gu_pos(text)
    if last < 0 or last >= len(text) - 30:
        return text
    
    trailer = text[last+1:].strip()
    if not trailer or has_gu(trailer):
        return text
    if len(trailer) < 25:
        return text
    
    # Only strip if it looks like prose (starts with capital letter or common word)
    if trailer[0].isupper() or trailer.startswith('we ') or trailer.startswith('we\'') or trailer.startswith('the ') or trailer.startswith('this '):
        # Check there's not a backtick-ed term we'd lose
        backtick_terms = re.findall(r'`[^`]+`', trailer)
        if not backtick_terms:  # Only strip if no backtick content would be lost
            return text[:last+1].rstrip()
    
    return text

def get_english_headings(en_path):
    """Extract heading (level, text) tuples from English source."""
    headings = []
    try:
        with open(en_path, 'r', encoding='utf-8') as f:
            for line in f:
                stripped = line.rstrip()
                if not stripped.startswith('#'):
                    continue
                if stripped.startswith('<!--'):
                    continue
                m = re.match(r'^(#+)\s+(.*)', stripped)
                if m:
                    level = len(m.group(1))
                    text = m.group(2).strip()
                    headings.append((level, text))
    except FileNotFoundError:
        pass
    return headings

def fix_ch17_04(content_lines):
    """Wrap the compiler error block in ```text ... ``` for ch17-04."""
    result = []
    in_error = False
    error_started = False
    error_lines = []
    
    for line in content_lines:
        stripped = line.rstrip()
        
        if not error_started and re.match(r'error\[E0599\]', stripped):
            error_started = True
            in_error = True
            error_lines = [line]
        elif in_error:
            if (stripped == '' or 
                stripped.startswith('  ') or 
                stripped.startswith('   ') or 
                stripped.startswith('=') or 
                stripped.startswith('help:') or
                stripped.startswith('1') or
                stripped.startswith('10') or
                stripped.startswith('|')):
                error_lines.append(line)
            else:
                in_error = False
                result.append('```text\n')
                for el in error_lines:
                    result.append(el)
                result.append('```\n')
                result.append(line)
        else:
            result.append(line)
    
    if in_error and error_lines:
        result.append('```text\n')
        for el in error_lines:
            result.append(el)
        result.append('```\n')
    
    return result

def process_file(gu_path, en_headings):
    """Process a single Gujarati translation file."""
    with open(gu_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    heading_idx = 0
    in_code_block = False
    
    for line in lines:
        stripped = line.rstrip()
        
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            new_lines.append(line)
            continue
        
        if in_code_block:
            new_lines.append(line)
            continue
        
        # ── Heading restoration ──
        if stripped.startswith('#') and not stripped.startswith('<!--'):
            m = re.match(r'^(#+)\s+(.*)', stripped)
            if m:
                level = len(m.group(1))
                while heading_idx < len(en_headings):
                    en_level, en_text = en_headings[heading_idx]
                    heading_idx += 1
                    if en_level == level:
                        new_lines.append('#' * level + ' ' + en_text + '\n')
                        break
                    elif en_level < level:
                        continue
                    else:
                        new_lines.append(line)
                        break
                else:
                    new_lines.append(line)
                continue
        
        # ── Term replacements + bilingual stripping ──
        line_replaced = replace_in_prose(stripped)
        line_cleaned = strip_bilingual(line_replaced)
        line_cleaned = strip_trailing_english(line_cleaned)
        
        new_lines.append(line_cleaned + '\n')
    
    basename = os.path.basename(gu_path)
    if basename == 'ch17-04-streams.md':
        new_lines = fix_ch17_04(new_lines)
    
    with open(gu_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

def main():
    gu_files = sorted(glob.glob(os.path.join(GU_SRC, '*.md')))
    print(f"Found {len(gu_files)} Gujarati files")
    
    for i, gu_path in enumerate(gu_files):
        basename = os.path.basename(gu_path)
        en_path = os.path.join(EN_SRC, basename)
        
        en_headings = get_english_headings(en_path)
        
        if not os.path.exists(en_path):
            print(f"  [{i+1}/{len(gu_files)}] SKIP {basename} (no English source)")
            continue
        
        try:
            process_file(gu_path, en_headings)
            status = f"{len(en_headings)} headings" if en_headings else "no headings"
            print(f"  [{i+1}/{len(gu_files)}] OK  {basename} ({status})")
        except Exception as e:
            print(f"  [{i+1}/{len(gu_files)}] ERR {basename}: {e}")
    
    print("\nDone!")

if __name__ == '__main__':
    main()
