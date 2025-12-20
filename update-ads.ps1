param(
    [string]$filePath,
    [string]$title
)

$content = Get-Content $filePath -Raw

# Replace the top ad section
$topAdOld = '<div class="ad ad-top">\s*<ins class="adsbygoogle"[^>]*></ins>\s*</div>'
$topAdNew = @'
<div class="ad-container">
      <div class="ad-sidebar">
        <div class="ad ad-left">
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
      </div>

      <div class="ad-content">
        <div class="ad ad-top">
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
'@

$content = $content -replace $topAdOld, $topAdNew

# Add mid ad before download section
$midAdNew = @'
        <div class="ad ad-mid">
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

'@

# Look for pattern before downloadSection and insert mid ad
$beforeDownload = '    <div id="downloadSection"'
if ($content -match $beforeDownload) {
    $content = $content -replace '(\s+)<div id="downloadSection"', ($midAdNew + '        <div id="downloadSection"')
}

# Replace bottom ad and add right sidebar
$bottomAdOld = '<div class="ad ad-bottom">\s*<ins class="adsbygoogle"[^>]*></ins>\s*</div>\s*</main>'
$bottomAdNew = @'
        <div class="ad ad-bottom">
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

      <div class="ad-sidebar">
        <div class="ad ad-right">
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
      </div>
    </div>
  </main>
'@

$content = $content -replace $bottomAdOld, $bottomAdNew

# Write updated content
Set-Content -Path $filePath -Value $content
Write-Host "Updated: $filePath" -ForegroundColor Green
