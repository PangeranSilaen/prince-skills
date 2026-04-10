---
name: glm-ocr
description: "Use when needing to OCR images or PDFs - extract text, tables, formulas, handwriting from screenshots, photos, scanned documents. Triggers: OCR, extract text from image, read screenshot, parse PDF, screenshot to text, GLM-OCR, ocr.z.ai, document parsing, image to text, pdf to text, read this image, what does this say"
---

# GLM-OCR: Free OCR via ocr.z.ai

## Overview

GLM-OCR is a free, high-accuracy OCR powered by Z.AI's GLM-OCR model (0.9B params, SOTA on OmniDocBench). This skill calls the ocr.z.ai REST API directly via a PowerShell script -- no browser needed, lightweight, fast.

**Capabilities:** Text, tables, formulas, handwriting, code blocks, invoices, multilingual (CN/EN/FR/ES/RU/DE/JA/KO)
**Formats:** PNG, JPG, JPEG, PDF (image ≤10MB, PDF ≤50MB, max 100 pages)
**Output:** Markdown (default) or JSON with layout/bounding box details

## Setup (one-time)

If `~/.glm-ocr-token` does not exist, tell the user:

1. Open https://ocr.z.ai/ and log in with Google
2. Press F12 > Application > Local Storage > `https://ocr.z.ai`
3. Find key `auth-storage`, copy the `token` value (the JWT string)
4. Run: `Set-Content -Path "$env:USERPROFILE\.glm-ocr-token" -Value 'PASTE_TOKEN_HERE' -NoNewline`

## Workflow

### Step 1: Resolve the file path

Resolve the user's file reference to an **absolute path**. If the user gives a URL, download it first:

```powershell
Invoke-WebRequest -Uri "https://example.com/image.png" -OutFile "$env:TEMP\ocr-download.png"
```

### Step 2: Ask user about output preference

Before running the script, use the **question tool** to ask the user where they want the output:

```
Question: "Hasil OCR mau ditaruh di mana?"
Options:
  - "Tampilkan di chat" (default -- just print to terminal)
  - "Simpan ke file" (save to working directory, suggest filename based on input)
```

If user picks "Simpan ke file", suggest a filename like `<input-name>-ocr.md` in the current working directory. Let user customize the name/path.

### Step 3: Run the OCR script

```powershell
# Print result to terminal
powershell -File "C:\Users\hi\.agents\skills\glm-ocr\scripts\ocr.ps1" -FilePath "ABSOLUTE_PATH_HERE"

# Save result to a file in the current working directory
powershell -File "C:\Users\hi\.agents\skills\glm-ocr\scripts\ocr.ps1" -FilePath "ABSOLUTE_PATH_HERE" -OutputFile "result.md"

# JSON output (includes layout details and bounding boxes)
powershell -File "C:\Users\hi\.agents\skills\glm-ocr\scripts\ocr.ps1" -FilePath "ABSOLUTE_PATH_HERE" -Format json -OutputFile "result.json"
```

**Path rules:**
- `-FilePath`: the input file to OCR. Can be relative (resolved from cwd) or absolute. Files do NOT need to be in the current directory.
- `-OutputFile`: where to save. Relative paths resolve from the **current working directory** (the user's project folder). Do NOT save to home directory unless explicitly asked.

### Step 4: Present results

If printed to stdout, present the Markdown to the user in chat. The output may contain `<div>` image tags for detected images/icons -- these can be ignored or mentioned.

If saved to file, confirm the path to the user.

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

## API Reference (for manual use)

```
Base URL: https://ocr.z.ai/api/v1/z-ocr
Auth: Bearer token from localStorage key "auth-storage"

POST /tasks/process     -- Upload file (multipart/form-data, field: "file")
GET  /tasks/list        -- List past OCR tasks
GET  /tasks/detail/:id  -- Get result by task ID
POST /tasks/delete      -- Delete task (body: {"task_id": "..."})
```
