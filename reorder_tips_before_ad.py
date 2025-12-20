import re
import os

# List of tool pages (exclude the 3 already fixed)
pages = [
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
    'qr-code-pdf.html'
]

for page in pages:
    filepath = page
    if not os.path.exists(filepath):
        print(f"{page}: NOT FOUND")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and extract the Help & Tips section (likely after </div> or </main>)
    help_pattern = r'(\s*<section class="help">.*?</section>\s*\n*)'
    help_match = re.search(help_pattern, content, re.DOTALL)
    
    if not help_match:
        print(f"{page}: No Help & Tips section found")
        continue
    
    help_section = help_match.group(1)
    
    # Remove the Help & Tips section from its current position
    content_without_help = content.replace(help_section, '', 1)
    
    # Find the ad-bottom-banner div and insert Help & Tips BEFORE it
    ad_pattern = r'(\s*<div class="ad ad-bottom-banner">)'
    
    if re.search(ad_pattern, content_without_help):
        content_new = re.sub(
            ad_pattern,
            '\n' + help_section.strip() + r'\1',
            content_without_help,
            count=1
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content_new)
        print(f"{page}: Moved Help & Tips before bottom ad")
    else:
        print(f"{page}: Could not find ad-bottom-banner div")

print("\nDone!")
