#!/usr/bin/env python3
"""
Remove duplicate Help & Tips sections, keeping only the one before the bottom banner.
"""
import re
import os

root_dir = os.path.dirname(os.path.abspath(__file__))
tool_pages = [
    'word-to-pdf.html',
    'pdf-to-word.html',
    'image-to-pdf.html',
    'pdf-to-image.html',
    'merge-pdf.html',
    'split-pdf.html',
    'compress-pdf.html',
    'rotate-pdf.html',
    'reorder-pages.html',
    'lock-pdf.html',
    'unlock-pdf.html',
    'excel-to-pdf.html',
    'extract-images.html',
    'add-page-numbers.html',
    'add-watermark.html',
    'qr-code-pdf.html',
]

for page in tool_pages:
    filepath = os.path.join(root_dir, page)
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find and remove ALL <section class="help">...</section> blocks EXCEPT the one before ad-bottom-banner
    # We'll keep only the last occurrence which should be before the bottom banner
    
    # Count how many help sections exist
    help_count = len(re.findall(r'<section class="help">', content))
    
    if help_count <= 1:
        print(f"{page}: OK (0 or 1 help section)")
        continue
    
    print(f"{page}: Found {help_count} help sections, removing duplicates...")
    
    # Split by help sections
    parts = re.split(r'(<section class="help">.*?</section>)', content, flags=re.DOTALL)
    
    # Reconstruct: keep only the last help section
    new_content = ""
    help_sections = []
    for i, part in enumerate(parts):
        if part.startswith('<section class="help">'):
            help_sections.append(part)
        else:
            new_content += part
    
    # Reinsert only the last help section
    if help_sections:
        new_content = new_content + help_sections[-1]
    
    # Make sure the help section is right before ad-bottom-banner, not inside it
    # Move it out if it's nested inside
    if '<div class="ad ad-bottom-banner">' in new_content and '<section class="help">' in new_content:
        # Check if help is inside the bottom banner div
        match = re.search(r'(<div class="ad ad-bottom-banner">\s*<section class="help">.*?</section>)', new_content, re.DOTALL)
        if match:
            # Extract the help section and move it out
            help_match = re.search(r'<section class="help">.*?</section>', match.group(1), re.DOTALL)
            if help_match:
                help_section = help_match.group(0)
                # Remove from inside the bottom banner
                new_content = new_content.replace(help_section + '\n\n', '')
                # Add it before the bottom banner
                new_content = new_content.replace(
                    '<div class="ad ad-bottom-banner">',
                    help_section + '\n\n    <div class="ad ad-bottom-banner">'
                )
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  ✓ Cleaned up {page}")
    else:
        print(f"  No changes needed for {page}")

print("\nDone!")
