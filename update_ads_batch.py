import os
import re

# Files to update
files_to_update = [
    'unlock-pdf.html',
    'rotate-pdf.html',
    'reorder-pages.html',
    'qr-code-pdf.html',
    'lock-pdf.html',
    'compress-pdf.html',
    'add-watermark.html',
    'add-page-numbers.html'
]

base_path = 'D:\\webs\\pdf-tools-website'

ad_left_sidebar = '''<div class="ad-container">
      <div class="ad ad-left-sidebar">
          <script type="text/javascript">
            atOptions = {
              'key' : '6055f7e32563fba0867266619119fb48',
              'format' : 'iframe',
              'height' : 600,
              'width' : 160,
              'params' : {}
            };
          </script>
          <script type="text/javascript" src="https://www.highperformanceformat.com/6055f7e32563fba0867266619119fb48/invoke.js"></script>
      </div>
      <div class="ad-content">
        <div class="ad ad-top-banner">
          <script type="text/javascript">
            atOptions = {
              'key' : '3f0207e61000b922d449a7a10ac84d14',
              'format' : 'iframe',
              'height' : 90,
              'width' : 728,
              'params' : {}
            };
          </script>
          <script type="text/javascript" src="https://www.highperformanceformat.com/3f0207e61000b922d449a7a10ac84d14/invoke.js"></script>
        </div>'''

ad_middle_banner = '''        <div class="ad ad-middle-banner">
          <script type="text/javascript">
            atOptions = {
              'key' : '3f0207e61000b922d449a7a10ac84d14',
              'format' : 'iframe',
              'height' : 90,
              'width' : 728,
              'params' : {}
            };
          </script>
          <script type="text/javascript" src="https://www.highperformanceformat.com/3f0207e61000b922d449a7a10ac84d14/invoke.js"></script>
        </div>'''

ad_bottom_and_right = '''        <div class="ad ad-bottom-banner">
          <script type="text/javascript">
            atOptions = {
              'key' : '3f0207e61000b922d449a7a10ac84d14',
              'format' : 'iframe',
              'height' : 90,
              'width' : 728,
              'params' : {}
            };
          </script>
          <script type="text/javascript" src="https://www.highperformanceformat.com/3f0207e61000b922d449a7a10ac84d14/invoke.js"></script>
        </div>
      </div>
      <div class="ad ad-right-sidebar">
        <script type="text/javascript">
          atOptions = {
            'key' : '6055f7e32563fba0867266619119fb48',
            'format' : 'iframe',
            'height' : 600,
            'width' : 160,
            'params' : {}
          };
        </script>
        <script type="text/javascript" src="https://www.highperformanceformat.com/6055f7e32563fba0867266619119fb48/invoke.js"></script>
      </div>
    </div>'''

for filename in files_to_update:
    filepath = os.path.join(base_path, filename)
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filename}")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern 1: Replace the top ad
    content = re.sub(
        r'<div class="ad ad-top">\s*<ins class="adsbygoogle"[^>]*></ins>\s*</div>',
        ad_left_sidebar,
        content
    )
    
    # Pattern 2: Look for convertBtn and insert middle ad before downloadSection
    content = re.sub(
        r'(\s+)<button class="btn" id="convertBtn"[^>]*>[\s\S]*?</button>\s*\n\s*</div>\s*\n\s*<div id="downloadSection"',
        r'\1<button class="btn" id="convertBtn" style="display:none;" onclick="convertFile()">\n\1  🔄 Convert\n\1</button>\n\1</div>\n\n' + ad_middle_banner + r'\n\n\1<div id="downloadSection"',
        content,
        flags=re.MULTILINE
    )
    
    # Pattern 3: Replace bottom ad with right sidebar
    content = re.sub(
        r'<div class="ad ad-bottom">\s*<ins class="adsbygoogle"[^>]*></ins>\s*</div>\s*</main>',
        ad_bottom_and_right + r'\n  </main>',
        content
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Updated: {filename}")

print("\n✅ All files updated!")
