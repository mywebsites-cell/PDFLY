#!/usr/bin/env python3
"""
Add Help & Tips sections to all tool HTML pages before the bottom banner.
"""
import re
import os

tips_map = {
    'pdf-to-image': [
        '<li><strong>DPI:</strong> Higher DPI yields sharper images; balance vs. file size.</li>',
        '<li><strong>Format:</strong> PNG for quality/transparency; JPG for smaller size.</li>',
        '<li><strong>Ranges:</strong> Export specific page ranges to save time.</li>',
        '<li><strong>Performance:</strong> Very large PDFs may render slowly—be patient.</li>',
        '<li><strong>Use:</strong> Ideal for previews, thumbnails, and sharing online.</li>',
    ],
    'merge-pdf': [
        '<li><strong>Reorder:</strong> Drag files to set merge order before combining.</li>',
        '<li><strong>Local:</strong> Merging is client‑side—files stay on your device.</li>',
        '<li><strong>Naming:</strong> Use clear filenames to track post‑merge content.</li>',
        '<li><strong>Size:</strong> Avoid merging extremely large files to keep outputs manageable.</li>',
        '<li><strong>Support:</strong> Questions? <a href="/contact" style="color: var(--primary); text-decoration: underline;">Contact us</a>.</li>',
    ],
    'split-pdf': [
        '<li><strong>Modes:</strong> Split all pages or choose ranges (e.g., 1‑3,5,7‑9).</li>',
        '<li><strong>Local:</strong> Runs client‑side; no uploads required.</li>',
        '<li><strong>Targeted:</strong> Extract only the sections you need.</li>',
        '<li><strong>Naming:</strong> Name outputs clearly for quick identification.</li>',
        '<li><strong>Privacy:</strong> Client‑side processing keeps files local.</li>',
    ],
    'compress-pdf': [
        '<li><strong>Images:</strong> Compression helps most on image‑heavy PDFs.</li>',
        '<li><strong>Balance:</strong> Try medium quality for size vs. readability.</li>',
        '<li><strong>Preview:</strong> Check pages to ensure text remains legible.</li>',
        '<li><strong>Version:</strong> Newer PDF versions may compress more efficiently.</li>',
        '<li><strong>Limits:</strong> Text‑only PDFs often see minimal gains.</li>',
    ],
    'rotate-pdf': [
        '<li><strong>Angles:</strong> Rotate by 90/180/270 degrees as needed.</li>',
        '<li><strong>Pages:</strong> Apply rotation to selected pages or all pages.</li>',
        '<li><strong>Local:</strong> Edits occur in‑browser; nothing uploaded.</li>',
        '<li><strong>Save:</strong> Export the rotated version when finished.</li>',
        '<li><strong>Backup:</strong> Keep originals in case you need to revert.</li>',
    ],
    'reorder-pages': [
        '<li><strong>Drag:</strong> Drag thumbnails to change page order.</li>',
        '<li><strong>Zoom:</strong> Zoom in for precise identification of pages.</li>',
        '<li><strong>Groups:</strong> Reorder in batches for long documents.</li>',
        '<li><strong>Export:</strong> Save when done to apply the new sequence.</li>',
        '<li><strong>Local:</strong> Runs client‑side for speed and privacy.</li>',
    ],
    'lock-pdf': [
        '<li><strong>Passwords:</strong> Add a password to restrict opening.</li>',
        '<li><strong>Strength:</strong> Use strong, unique passwords; store safely.</li>',
        '<li><strong>Sharing:</strong> Share passwords securely—not via plain text.</li>',
        '<li><strong>Limits:</strong> Some viewers handle encryption differently; test outputs.</li>',
        '<li><strong>Privacy:</strong> Server‑side; files auto‑delete. <a href="/privacy" style="color: var(--primary); text-decoration: underline;">Privacy Policy</a>.</li>',
    ],
    'unlock-pdf': [
        '<li><strong>Rights:</strong> Only unlock PDFs you are authorized to modify.</li>',
        '<li><strong>Limits:</strong> Strong encryption or policy locks may not be removable.</li>',
        '<li><strong>Legal:</strong> Respect licenses and terms when modifying PDFs.</li>',
        '<li><strong>Alternate:</strong> If unlock fails, try "Print to PDF" as a workaround.</li>',
        '<li><strong>Privacy:</strong> Server‑side; files auto‑delete. <a href="/privacy" style="color: var(--primary); text-decoration: underline;">Privacy Policy</a>.</li>',
    ],
    'excel-to-pdf': [
        '<li><strong>Layouts:</strong> Preserves tables and formatting from XLSX/XLS.</li>',
        '<li><strong>Breaks:</strong> Set page breaks for ideal pagination.</li>',
        '<li><strong>Fit:</strong> Use "Fit to page" scaling for wide sheets.</li>',
        '<li><strong>Orientation:</strong> Landscape works better for wide tables.</li>',
        '<li><strong>Print Area:</strong> Define print area to include only desired cells.</li>',
    ],
    'extract-images': [
        '<li><strong>Output:</strong> Extract embedded images as PNG/JPG files.</li>',
        '<li><strong>DPI:</strong> Higher DPI yields better quality for reuse.</li>',
        '<li><strong>Reuse:</strong> Ideal for graphics, figures, and illustrations.</li>',
        '<li><strong>Performance:</strong> Large PDFs may take longer to process.</li>',
        '<li><strong>Naming:</strong> Outputs are numbered—rename for clarity.</li>',
    ],
    'add-page-numbers': [
        '<li><strong>Placement:</strong> Choose header or footer positions.</li>',
        '<li><strong>Formats:</strong> Styles like "1", "1/10", or "Page 1".</li>',
        '<li><strong>Style:</strong> Set font size/color for readability.</li>',
        '<li><strong>Start:</strong> Start numbering at a specific page if needed.</li>',
        '<li><strong>Safety:</strong> Avoid overlapping content—preview before saving.</li>',
    ],
    'add-watermark': [
        '<li><strong>Opacity:</strong> Use light opacity to keep text readable.</li>',
        '<li><strong>Position:</strong> Center/diagonal placements are common.</li>',
        '<li><strong>Font:</strong> Choose clear, professional fonts for text marks.</li>',
        '<li><strong>Size:</strong> Scale watermark appropriately for page size.</li>',
        '<li><strong>Preview:</strong> Check placement before saving final PDF.</li>',
    ],
    'qr-code-pdf': [
        '<li><strong>Contrast:</strong> High contrast improves scan reliability.</li>',
        '<li><strong>Size:</strong> Use ≥2cm code size for printed materials.</li>',
        '<li><strong>Quiet Zone:</strong> Leave padding around the code for scanners.</li>',
        '<li><strong>Testing:</strong> Test with a phone camera before publishing.</li>',
        '<li><strong>Content:</strong> Store URLs, Wi‑Fi, contacts (vCard), or text.</li>',
    ],
}

help_template = '''    <section class="help">
      <h2>Help & Tips</h2>
      <ul>
{tips}      </ul>
    </section>

    <script type="text/javascript">
      atOptions = {{
        'key' : '3f0207e61000b922d449a7a10ac84d14',
        'format' : 'iframe',
        'height' : 90,
        'width' : 728,
        'params' : {{}}
      }};
    </script>
    <div class="ad ad-bottom-banner">
      <script type="text/javascript" src="https://www.highperformanceformat.com/3f0207e61000b922d449a7a10ac84d14/invoke.js"></script>
    </div>'''

root_dir = os.path.dirname(os.path.abspath(__file__))
tool_pages = [
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
    tool_name = page.replace('.html', '')
    if tool_name not in tips_map:
        print(f"Skipping {page} - no tips defined")
        continue

    filepath = os.path.join(root_dir, page)
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # If tips section already exists, skip
    if '<section class="help">' in content:
        print(f"Tips already in {page}, skipping")
        continue

    # Find the last occurrence of '<script type="text/javascript">' followed by atOptions before closing </div>
    # We want to insert the help section before this pattern
    pattern = r'(\s+)<script type="text/javascript">\s+atOptions = \{\s+\'key\' : \'3f0207e61000b922d449a7a10ac84d14\','
    
    if not re.search(pattern, content):
        print(f"Could not find insertion point in {page}")
        continue

    # Build the tips section
    tips_html = '\n'.join([f"        {tip}" for tip in tips_map[tool_name]])
    help_section = help_template.format(tips=tips_html)

    # Replace: find the pattern and insert before it
    new_content = re.sub(
        pattern,
        r'\1<section class="help">\n\1  <h2>Help & Tips</h2>\n\1  <ul>\n' + tips_html + f'\n\1  </ul>\n\1</section>\n\n\1<script type="text/javascript">\n\1  atOptions = {{\n\1    \'key\' : \'3f0207e61000b922d449a7a10ac84d14\',',
        content
    )

    if new_content == content:
        print(f"No changes made to {page}")
        continue

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"✓ Added tips to {page}")

print("\nDone!")
