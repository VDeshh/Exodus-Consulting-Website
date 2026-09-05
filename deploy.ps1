# Exodus Consulting - build dist/ and publish.
# Copies the whole 16-page site plus css, js and assets, and deliberately
# excludes internal reference docs and raw app captures (which contain guest PII).
$ErrorActionPreference = 'Stop'
$src  = "C:\Users\shive\fennec-consulting"
$dist = "$src\dist"

Write-Host "Building dist..." -ForegroundColor Cyan
Remove-Item $dist -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path $dist | Out-Null

# every site page
Get-ChildItem "$src\*.html" | Where-Object {
  $_.Name -notmatch '^(Exodus-|oc-email|exodus-standalone|train-animation)'
} | Copy-Item -Destination $dist

Copy-Item "$src\css","$src\js","$src\assets" $dist -Recurse
if (Test-Path "$src\vercel.json") { Copy-Item "$src\vercel.json" $dist }

# never publish these
Remove-Item "$dist\assets\product\raw" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$dist\assets\product\prep.py","$dist\assets\product\index.jpg","$dist\assets\product\contact-sheet.jpg" -Force -ErrorAction SilentlyContinue
Remove-Item "$dist\css\*.md","$dist\css\PARTIALS.html" -Force -ErrorAction SilentlyContinue

$pages = (Get-ChildItem "$dist\*.html").Count
Write-Host "dist built: $pages pages" -ForegroundColor Green

Write-Host "Verifying no client-internal material..." -ForegroundColor Cyan
# Gate on dist, not on $src. dist is what actually ships; the working folder
# also holds gitignored internal drafts that are never copied into a build.
python "$src\tools\check-client-internals.py" --dir "$dist"
if ($LASTEXITCODE -ne 0) { Write-Host "BLOCKED: fix the findings above before deploying." -ForegroundColor Red; exit 1 }

Write-Host "Publishing to Netlify..." -ForegroundColor Cyan
Set-Location $src
netlify deploy --dir=dist --prod --message="deploy via script"
