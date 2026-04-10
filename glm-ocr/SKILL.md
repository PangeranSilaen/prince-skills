---
name: glm-ocr
description: "Use when needing to OCR images or PDFs - extract text, tables, formulas, handwriting from screenshots, photos, scanned documents. Triggers: OCR, extract text from image, read screenshot, parse PDF, screenshot to text, GLM-OCR, ocr.z.ai, document parsing, image to text, pdf to text, read this image, what does this say"
---

# GLM-OCR: Free OCR via ocr.z.ai

## Overview

GLM-OCR is a free, high-accuracy OCR powered by Z.AI's GLM-OCR model. This skill calls the ocr.z.ai REST API directly via a PowerShell script -- no browser, no Python libraries, no dependencies. Just curl.

**Use this instead of** installing pymupdf, pdfplumber, pytesseract, poppler, etc. This is faster and more accurate.

**Capabilities:** Text, tables, formulas, handwriting, code blocks, invoices, multilingual (CN/EN/FR/ES/RU/DE/JA/KO)
**Formats:** PNG, JPG, JPEG, PDF (image ≤10MB, PDF ≤50MB, max 100 pages)

## Setup (one-time)

If `~/.glm-ocr-token` does not exist, tell the user:

1. Open https://ocr.z.ai/ and log in with Google
2. Press F12 > Application > Local Storage > `https://ocr.z.ai`
3. Find key `auth-storage`, copy the `token` value (the JWT string)
4. Run: `Set-Content -Path "$env:USERPROFILE\.glm-ocr-token" -Value 'PASTE_TOKEN_HERE' -NoNewline`

## Workflow

### Step 1: Resolve the file path

Resolve the user's file reference to an **absolute path**. The file can be anywhere on the filesystem -- it does NOT need to be in the current working directory.

If the user gives a URL, download it first:
```powershell
Invoke-WebRequest -Uri "https://example.com/image.png" -OutFile "$env:TEMP\ocr-download.png"
```

### Step 2: Run the OCR script

```powershell
powershell -File "C:\Users\hi\.agents\skills\glm-ocr\scripts\ocr.ps1" -FilePath "ABSOLUTE_PATH_HERE"
```

The script outputs the OCR result as Markdown text directly to stdout. You can read it immediately -- no file I/O needed.

### Step 3: Use the result

The stdout output IS the OCR result. Read it and use it to answer the user's question, summarize the document, extract data, etc.

**Do NOT** ask the user where to save the output unless they explicitly ask to export/save it. The primary use case is: user gives you a file, you read it, you understand it.

If the user explicitly asks to save the result to a file, use `-OutputFile`:
```powershell
powershell -File "C:\Users\hi\.agents\skills\glm-ocr\scripts\ocr.ps1" -FilePath "INPUT" -OutputFile "output.md"
```

If the script exits with an error about token expiry (401), guide the user through the setup steps above to refresh their token.

## Quick Reference

| Input | Supported |
|-------|-----------|
| PNG/JPG/JPEG images | Yes, ≤10MB |
| PDF documents | Yes, ≤50MB, ≤100 pages |
| Remote URLs | Download first, then OCR |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Token file not found" | Run setup steps above |
| HTTP 401 / token expired | Refresh token from browser localStorage |
| "File too large" | Image max 10MB, PDF max 50MB |
| Slow response | Large PDFs take longer. The API has a ~60s timeout. |
