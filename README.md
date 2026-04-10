# prince-skills

Custom AI agent skills for [OpenCode](https://opencode.ai/).

## Skills

### glm-ocr

Free OCR powered by [GLM-OCR](https://ocr.z.ai/) (Z.AI). Extract text, tables, formulas, and handwriting from images and PDFs directly from the terminal.

- **No API key needed** -- uses ocr.z.ai's free web API with your login session
- **Lightweight** -- pure `curl` calls, no browser automation
- **Formats:** PNG, JPG, JPEG, PDF

#### Setup

1. Log in to https://ocr.z.ai/ with Google
2. F12 > Application > Local Storage > `auth-storage` > copy `token`
3. `Set-Content -Path "$env:USERPROFILE\.glm-ocr-token" -Value 'YOUR_TOKEN' -NoNewline`

#### Install

Copy the `glm-ocr` folder to your skills directory:

```
# OpenCode
~/.agents/skills/glm-ocr/

# Claude Code
~/.claude/skills/glm-ocr/
```

## License

MIT
