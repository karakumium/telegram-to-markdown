#!/usr/bin/env python3
import json
import shutil
import sys
from pathlib import Path
from typing import Dict, Any, List


# =========================
# Telegram export handling
# =========================

def extract_chats(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    if 'messages' in data and 'name' in data:
        return [data]

    if 'chats' in data and 'list' in data['chats']:
        return data['chats']['list']

    if 'dialogs' in data:
        return data['dialogs']

    raise ValueError('Unsupported Telegram export format')


# =========================
# Text rendering
# =========================

def render_text(text) -> str:
    if isinstance(text, str):
        return text.strip()

    if not isinstance(text, list):
        return ''

    out = []

    for part in text:
        if isinstance(part, str):
            out.append(part)
            continue

        if not isinstance(part, dict):
            continue

        t = part.get('type')
        v = part.get('text', '')

        if t == 'bold':
            out.append(f'**{v}**')
        elif t == 'italic':
            out.append(f'*{v}*')
        elif t == 'underline':
            out.append(f'__{v}__')
        elif t == 'strikethrough':
            out.append(f'~~{v}~~')
        elif t == 'code':
            out.append(f'`{v}`')
        elif t == 'pre':
            out.append(f'\n```\n{v}\n```\n')
        elif t == 'blockquote':
            for line in v.splitlines():
                out.append(f'> {line}')
            out.append('\n')
        else:
            out.append(v)

    return ''.join(out).strip()


# =========================
# Media (Obsidian-ready)
# =========================

MEDIA_FIELDS = [
    'photo',
    'video',
    'voice',
    'audio',
    'video_message',
    'animation',
    'sticker',
    'file',
]


def handle_media(message: Dict[str, Any], input_dir: Path, attach_dir: Path) -> str:
    for field in MEDIA_FIELDS:
        if field not in message:
            continue

        rel = message[field]
        if not isinstance(rel, str):
            continue

        src = input_dir / rel
        if not src.exists():
            return f'> ⚠️ media not found: {rel}\n'

        attach_dir.mkdir(parents=True, exist_ok=True)
        dst = attach_dir / src.name

        if not dst.exists():
            shutil.copy2(src, dst)

        # Obsidian embed
        return f'![[{dst.name}]]\n'

    return ''


# =========================
# Chat conversion
# =========================

def convert_chat(chat: Dict[str, Any], input_dir: Path, output_dir: Path):
    chat_name = chat.get('name', 'chat').replace('/', '_')
    md_path = output_dir / f'{chat_name}.md'
    attach_dir = output_dir / 'attachments'

    with md_path.open('w', encoding='utf-8') as md:
        md.write(f'# {chat_name}\n\n')

        for msg in chat.get('messages', []):
            if msg.get('type') == 'service':
                continue

            author = msg.get('from', 'Unknown')
            date = msg.get('date', '')

            md.write(f'## {author} — {date}\n\n')

            media_md = handle_media(msg, input_dir, attach_dir)
            text_md = render_text(msg.get('text'))

            if media_md:
                md.write(media_md)
                if text_md:
                    md.write(f'> {text_md}\n')

            else:
                if text_md:
                    md.write(text_md + '\n')

            md.write('\n---\n\n')


# =========================
# CLI
# =========================

def convert(input_dir: Path, output_dir: Path):
    result = input_dir / 'result.json'
    if not result.exists():
        raise FileNotFoundError('result.json not found')

    with result.open(encoding='utf-8') as f:
        data = json.load(f)

    chats = extract_chats(data)
    output_dir.mkdir(parents=True, exist_ok=True)

    for chat in chats:
        convert_chat(chat, input_dir, output_dir)


def main():
    if len(sys.argv) != 4 or sys.argv[1] != 'convert':
        print('Usage: python convert.py convert <input_dir> <output_dir>')
        sys.exit(1)

    convert(Path(sys.argv[2]), Path(sys.argv[3]))


if __name__ == '__main__':
    main()
