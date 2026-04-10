<#
.SYNOPSIS
    OCR a file using GLM-OCR via ocr.z.ai REST API.
.DESCRIPTION
    Uploads a local file (image or PDF) to ocr.z.ai and returns the OCR result.
    Requires a Bearer token stored in ~/.glm-ocr-token.
.PARAMETER FilePath
    Path to the image or PDF file to OCR.
.PARAMETER Format
    Output format: "markdown" (default) or "json".
.EXAMPLE
    powershell -File ocr.ps1 -FilePath "C:\Users\hi\document.pdf"
    powershell -File ocr.ps1 -FilePath "screenshot.png" -Format json
#>
param(
    [Parameter(Mandatory=$true)]
    [string]$FilePath,

    [ValidateSet("markdown", "json")]
    [string]$Format = "markdown"
)

$ErrorActionPreference = "Stop"

# Resolve to absolute path
$FilePath = (Resolve-Path $FilePath).Path

# Validate file exists
if (-not (Test-Path $FilePath)) {
    Write-Error "File not found: $FilePath"
    exit 1
}

# Check file size
$fileSize = (Get-Item $FilePath).Length
$ext = [System.IO.Path]::GetExtension($FilePath).ToLower()
if ($ext -eq ".pdf" -and $fileSize -gt 50MB) {
    Write-Error "PDF file too large (max 50MB). File size: $([math]::Round($fileSize/1MB, 1))MB"
    exit 1
}
if ($ext -ne ".pdf" -and $fileSize -gt 10MB) {
    Write-Error "Image file too large (max 10MB). File size: $([math]::Round($fileSize/1MB, 1))MB"
    exit 1
}

# Read token
$tokenFile = Join-Path $env:USERPROFILE ".glm-ocr-token"
if (-not (Test-Path $tokenFile)) {
    Write-Error @"
Token file not found at $tokenFile.

To set up:
1. Open https://ocr.z.ai/ in your browser and log in with Google
2. Press F12 > Application > Local Storage > https://ocr.z.ai
3. Find key 'auth-storage' and copy the 'token' value
4. Run: Set-Content -Path '$tokenFile' -Value 'YOUR_TOKEN' -NoNewline
"@
    exit 1
}
$token = (Get-Content $tokenFile -Raw).Trim()

# Upload file
Write-Host "Uploading $(Split-Path $FilePath -Leaf) ($([math]::Round($fileSize/1KB, 1))KB)..." -ForegroundColor Cyan

$response = curl.exe -s -w "`n%{http_code}" -X POST "https://ocr.z.ai/api/v1/z-ocr/tasks/process" `
    -H "Authorization: Bearer $token" `
    -H "Accept-Language: en" `
    -F "file=@$FilePath"

# Split response body and status code
$lines = $response -split "`n"
$httpCode = $lines[-1]
$body = ($lines[0..($lines.Length-2)]) -join "`n"

# Check for auth errors
if ($httpCode -eq "401") {
    Write-Error @"
Token expired or invalid (HTTP 401).

Please refresh your token:
1. Open https://ocr.z.ai/ in your browser (make sure you're logged in)
2. Press F12 > Application > Local Storage > https://ocr.z.ai
3. Find key 'auth-storage' and copy the 'token' value
4. Run: Set-Content -Path '$tokenFile' -Value 'YOUR_TOKEN' -NoNewline
"@
    exit 1
}

if ($httpCode -ne "200") {
    Write-Error "API error (HTTP $httpCode): $body"
    exit 1
}

# Parse response
$result = $body | ConvertFrom-Json

if ($result.code -ne 200) {
    Write-Error "API error: $($result.message)"
    exit 1
}

$task = $result.data

# Output based on format
if ($Format -eq "json") {
    # Output the raw JSON content (layout details, bounding boxes, etc.)
    $task.json_content
} else {
    # Output clean markdown
    $task.markdown_content
}
