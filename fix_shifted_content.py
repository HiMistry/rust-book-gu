#!/usr/bin/env python3
"""Fix 'shifted by one' content in Gujarati translation files.

When the translation pipeline processed markdown, blockquotes (>) were stripped.
If a blockquote contained a heading (e.g. > ### Command Line Notation), that
heading was lost entirely, causing ALL subsequent content to shift down by one
heading — each section's content ended up under the WRONG heading.

This script realigns content:
  - Reads English markdown to get correct heading structure
  - Reads current Gujarati markdown
  - Maps each English section heading to the correct Gujarati content block
  - Writes the fixed Gujarati file
"""

import os
import re
import glob

EN_SRC = "/Users/himanshumistry/rustlings/book/src"
GU_SRC = "/Users/himanshumistry/rustlings/gu_pipe/translations/gu/src"

def parse_sections(filepath, include_blockquote_headings=False):
    """Split markdown into (heading_is_blockquote, heading_level, heading_text, content_lines) tuples.
    
    heading_level is the number of '#' characters (2 for ##, 3 for ###, etc.).
    Returns list of (is_bq, level, heading, [content_lines]).
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    sections = []
    current_heading = None
    current_level = 0
    current_is_bq = False
    current_content = []
    
    for line in lines:
        stripped = line.rstrip()
        
        # Detect heading (normal or blockquote)
        m = re.match(r'^(>)?\s*(#{1,6})\s+(.*)', stripped)
        if m:
            is_bq = m.group(1) is not None
            if include_blockquote_headings or not is_bq:
                # Save previous section
                if current_heading is not None:
                    sections.append((current_is_bq, current_level, current_heading, current_content))
                current_heading = m.group(3).strip()
                current_level = len(m.group(2))
                current_is_bq = is_bq
                current_content = []
                continue
        
        # Skip HTML comments and hidden anchors
        if stripped.startswith('<!--') or stripped.startswith('<a id'):
            continue
        
        if current_heading is not None:
            current_content.append(line)
    
    # Save last section
    if current_heading is not None:
        sections.append((current_is_bq, current_level, current_heading, current_content))
    
    return sections


def is_blank(line):
    """Check if a line is blank (empty, or blockquote-only with no content)."""
    s = line.strip()
    return not s or s == '>'


def count_paragraphs(lines):
    """Count paragraphs (contiguous non-blank regions) in content lines."""
    count = 0
    in_para = False
    for line in lines:
        if not is_blank(line):
            if not in_para:
                count += 1
                in_para = True
        else:
            in_para = False
    return count


def split_content_at_paragraph(gu_content, num_paras):
    """Split gu_content after num_paras paragraphs.
    
    Returns (bq_lines, remaining_lines).
    """
    para_count = 0
    in_para = False
    split_idx = len(gu_content)
    
    for i, line in enumerate(gu_content):
        if not is_blank(line):
            if not in_para:
                para_count += 1
                in_para = True
                if para_count > num_paras:
                    split_idx = i
                    break
        else:
            in_para = False
    
    return gu_content[:split_idx], gu_content[split_idx:]





def fix_file(fname):
    en_path = os.path.join(EN_SRC, fname)
    gu_path = os.path.join(GU_SRC, fname)
    
    if not os.path.exists(en_path) or not os.path.exists(gu_path):
        print(f"  SKIP {fname}: missing EN or GU file")
        return
    
    # Parse English sections (include blockquote headings)
    en_sections = parse_sections(en_path, include_blockquote_headings=True)
    
    # Parse current Gujarati sections (regular headings only)
    gu_sections = parse_sections(gu_path, include_blockquote_headings=False)
    
    print(f"\n  {fname}: EN={len(en_sections)} sections, GU={len(gu_sections)} sections")
    
    en_non_bq = sum(1 for is_bq, _, _, _ in en_sections if not is_bq)
    if en_non_bq != len(gu_sections):
        print(f"    NOTE: heading count differs (EN non-BQ={en_non_bq} vs GU={len(gu_sections)})")
    
    en_heading_count = len(en_sections)
    gu_heading_count = len(gu_sections)
    
    # Build output
    output_lines = []
    carryover = []  # content lines carried over from previous blockquote section
    
    for i, (is_bq, level, heading, en_content) in enumerate(en_sections):
        # Determine which GU section contributes content
        if i < gu_heading_count:
            gu_idx = i
        else:
            gu_idx = gu_heading_count - 1
        
        # Get GU content (prepend any carryover from previous blockquote)
        if gu_idx < len(gu_sections):
            _, _, _, gu_content = gu_sections[gu_idx]
        else:
            gu_content = []
        
        if carryover:
            # A previous blockquote section had excess content; prepend to this section
            gu_content = carryover + gu_content
            carryover = []
        
        # Write heading
        heading_prefix = '#' * level
        if is_bq:
            output_lines.append(f'> {heading_prefix} {heading}\n')
        else:
            output_lines.append(f'{heading_prefix} {heading}\n')
        
        # Write content
        if is_bq:
            # Count paragraphs in English blockquote content only
            # (only lines that START with '>' are actual blockquote content;
            #  lines after the blockquote end, without '>', are NOT part of it)
            bq_en_lines = [l for l in en_content if l.strip().startswith('>')]
            en_paras = count_paragraphs(bq_en_lines)
            
            # Skip leading blank lines in GU content
            seen_non_empty = False
            skip_end = 0
            for cl in gu_content:
                if not seen_non_empty and not cl.rstrip():
                    skip_end += 1
                else:
                    break
            gu_content_trimmed = gu_content[skip_end:]
            
            # Split GU content after the same number of paragraphs as English BQ
            bq_part, remaining = split_content_at_paragraph(gu_content_trimmed, en_paras)
            carryover = remaining
            
            # Write blockquote lines
            bq_lines = [f'>\n']  # blank line after heading
            for cl in bq_part:
                stripped_cl = cl.rstrip()
                if stripped_cl:
                    bq_lines.append(f'> {stripped_cl}\n')
                else:
                    bq_lines.append('>\n')
            if not bq_lines:
                bq_lines.append('>\n')
            output_lines.extend(bq_lines)
        else:
            # Skip leading blank lines in content for non-BQ sections too
            non_bq_content = []
            seen_content = False
            for cl in gu_content:
                if not seen_content and not cl.rstrip():
                    continue
                seen_content = True
                non_bq_content.append(cl)
            output_lines.extend(non_bq_content)
    
    # Append any remaining carryover at the end (shouldn't happen, but be safe)
    if carryover:
        output_lines.extend(carryover)
    
    # Ensure file ends with newline
    if output_lines and not output_lines[-1].endswith('\n'):
        output_lines[-1] += '\n'
    
    # Write output
    with open(gu_path, 'w', encoding='utf-8') as f:
        f.writelines(output_lines)
    
    print(f"    DONE: {len(en_sections)} sections written")


def main():
    # All files with the "shifted by one" content issue
    affected = [
        'ch01-01-installation.md',
        'ch03-00-introduction.md',
        'ch03-02-data-types.md',
        'ch04-01-what-is-ownership.md',
        'ch05-01-defining-structs.md',
        'ch07-03-paths-referring-to-an-item-in-the-module-tree.md',
        'ch07-05-separating-modules-into-different-files.md',
        'ch09-01-unrecoverable-errors-with-panic.md',
        'ch09-02-recoverable-errors-with-result.md',
        'ch12-01-accepting-command-line-arguments.md',
        'ch12-03-improving-error-handling-and-modularity.md',
        'ch18-01-what-is-oo.md',
        'ch18-03-oo-design-patterns.md',
    ]
    
    for fname in affected:
        fix_file(fname)


if __name__ == '__main__':
    main()
