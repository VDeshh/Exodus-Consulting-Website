# Exodus Consulting - one-command publish to Netlify (live URL)
# Usage:  powershell -ExecutionPolicy Bypass -File C:\Users\shive\fennec-consulting\deploy.ps1
$ErrorActionPreference = 'Stop'
$src  = "C:\Users\shive\fennec-consulting"
$dist = "$src\dist"

Write-Host "Building dist..." -ForegroundColor Cyan
Remove-Item $dist -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path $dist | Out-Null
Copy-Item "$src\index.html","$src\about.html","$src\styles.css","$src\script.js" $dist
Copy-Item "$src\assets" $dist -Recurse

Write-Host "Publishing to Netlify..." -ForegroundColor Cyan
Set-Location $src
netlify deploy --dir=dist --prod --message="deploy via script"

Write-Host "Done. Live at https://exodus-consulting.netlify.app" -ForegroundColor Green
