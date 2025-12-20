import os
import re

files_to_check = [
    'word-to-pdf.html',
    'pdf-to-word.html',
    'pdf-to-image.html',
    'image-to-pdf.html',
    'excel-to-pdf.html',
    'extract-images.html',
    'merge-pdf.html',
    'split-pdf.html',
    'compress-pdf.html',
    'rotate-pdf.html',
    'reorder-pages.html',
    'lock-pdf.html',
    'unlock-pdf.html',
    'add-page-numbers.html',
    'add-watermark.html',
    'qr-code-pdf.html'
]

base_path = 'D:\\webs\\pdf-tools-website'

print("Checking ad structure in all tool pages:\n")

for filename in files_to_check:
    filepath = os.path.join(base_path, filename)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for both old and new naming conventions
    has_container = 'ad-container' in content
    has_left = ('ad-left-sidebar' in content or 'ad ad-left' in content)
    has_top = ('ad-top-banner' in content or 'ad ad-top' in content)
    has_bottom = ('ad-bottom-banner' in content or 'ad ad-bottom' in content)
    has_right = ('ad-right-sidebar' in content or 'ad ad-right' in content)
    
    all_present = has_container and has_left and has_top and has_bottom and has_right
    
    if all_present:
        print(f"✅ {filename}")
    else:
        missing = []
        if not has_container: missing.append('container')
        if not has_left: missing.append('left')
        if not has_top: missing.append('top')
        if not has_bottom: missing.append('bottom')
        if not has_right: missing.append('right')
        print(f"❌ {filename} - Missing: {', '.join(missing)}")

print("\nDone!")
