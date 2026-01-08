# telegram-to-markdown (Telegram Desktop 2026 fork)

This repository is a fork of  
https://github.com/alexlyzhov/telegram-to-markdown

The original project converts Telegram Desktop chat exports into Markdown adopted for Obsidian Vault.
This fork modernizes the converter to support **new Telegram Desktop export formats (2024–2026)**.

---

## What’s changed in this fork

Compared to the original project, this fork introduces:

### Support for new Telegram Desktop export format
- Handles exports where `result.json` represents a **single chat**
- Compatible with Telegram Desktop 2024–2026
- Backward-compatible with older exports

### Obsidian-ready Markdown output
- One chat → one `.md` file
- Media stored in `attachments/`
- Obsidian-native embeds:
  ```md
  ![[image.jpg]]
  ```

### Inline captions for media

Media captions are rendered inline using blockquotes:
```md
![[photo.jpg]]
> Caption text
```


### Robust text rendering

- Correct handling of rich Telegram text entities:
  - bold
  - italic
  - blockquotes
  - code blocks
- Service messages are safely skipped

### Media handling

- Photos, videos, files, voice messages, stickers, etc.
- Media files are copied automatically
- Missing media does not break conversion

### Fixed CLI interface
`python convert.py convert <input_dir> <output_dir>`

Usage
```bash
python convert.py convert ChatExport_2026-01-07 OutputDir
```

Result:
```
OutputDir/
├── Chat name.md
└── attachments/
    ├── photo_123.jpg
    └── file_456.pdf
```
License

This project is distributed under the MIT License, same as the original project.
See the LICENSE file for details.

Original author:
Alexey Lyzhov — https://github.com/alexlyzhov
