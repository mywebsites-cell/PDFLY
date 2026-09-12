# submit-indexnow.ps1
# Submits all URLs from sitemap.xml to Bing/Yandex/Seznam via IndexNow.
# Usage: .\submit-indexnow.ps1
$key = "252f5789e0624ee4abee6c2bde5df017"
$hostUrl = "https://pdfly.live"

$sitemap = Join-Path $PSScriptRoot "sitemap.xml"
if (-not (Test-Path $sitemap)) {
    Write-Error "sitemap.xml not found next to this script."
    exit 1
}

[xml]$xml = Get-Content $sitemap
$urls = $xml.urlset.url | ForEach-Object { $_.loc }

Write-Host "Found $($urls.Count) URLs. Submitting to IndexNow..."
$ok = 0
$fail = 0

foreach ($u in $urls) {
    $endpoint = "https://www.bing.com/indexnow?url=$([uri]::EscapeDataString($u))&key=$key"
    try {
        $resp = Invoke-WebRequest -Uri $endpoint -UseBasicParsing -TimeoutSec 30
        if ($resp.StatusCode -eq 200) {
            Write-Host "  OK   $u"
            $ok++
        } else {
            Write-Host "  FAIL $u (HTTP $($resp.StatusCode))"
            $fail++
        }
    } catch {
        Write-Host "  FAIL $u ($($_.Exception.Message))"
        $fail++
    }
}

Write-Host ""
Write-Host "Done. Success: $ok, Failed: $fail"
