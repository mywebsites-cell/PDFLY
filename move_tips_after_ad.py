import re
import os

# List of tool pages
pages = [
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
    'qr-code-pdf.html'
]

for page in pages:
    filepath = page
    if not os.path.exists(filepath):
        print(f"{page}: NOT FOUND")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and extract the Help & Tips section
    help_pattern = r'(\s*<section class="help">.*?</section>\s*)'
    help_match = re.search(help_pattern, content, re.DOTALL)
    
    if not help_match:
        print(f"{page}: No Help & Tips section found")
        continue
    
    help_section = help_match.group(1)
    
    # Remove the Help & Tips section from its current position
    content_without_help = content.replace(help_section, '', 1)
    
    # Find the bottom ad banner closing div
    # Look for the pattern: </script>\n    </div> that closes the ad-bottom-banner
    # Then insert the Help & Tips section after the closing </div> of the ad-content wrapper
    
    # Pattern: find </div> that closes ad-bottom-banner, then the </div> that closes ad-content
    # Insert Help & Tips after ad-content closing but before </main>
    
    # Look for the pattern: ad-bottom-banner script closing, then </div> (ad-bottom-banner), then closing divs
    pattern = r'(</script>\s*</div>\s*</div>\s*<div class="ad-sidebar">.*?</div>\s*</div>\s*</div>\s*</main>)'
    
    # Try to find where to insert - after the main content wrapper closes but before </main>
    # Simpler approach: find </main> and insert before it
    if '</main>' in content_without_help:
        # Insert Help & Tips section right before </main>
        content_new = content_without_help.replace('</main>', help_section.strip() + '\n\n  </main>', 1)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content_new)
        print(f"{page}: Moved Help & Tips after bottom ad")
    else:
        print(f"{page}: Could not find </main> tag")

print("\nDone!")
