#!/usr/bin/env python3
"""Check that every AI translation (index.en-us.md) keeps the layout of its Chinese source (index.md).

The translation must map line-for-line onto the source:
- blank lines, headings (level + {#id}), list / quote markers and their exact indentation match;
- images point at the same files, shortcodes and `---` rules are identical, link count per line matches;
- code fences are byte-identical, except lines holding Chinese comments, which keep indentation and first token;
- no Chinese is left in the English body;
- front matter `translation.sourceHash` matches the current Chinese file (else the translation is stale).

Usage: python3 scripts/check_translation.py   (exit 1 on any problem)
"""
import hashlib
import re
import sys
from pathlib import Path

CJK = re.compile(r"[　-〿一-鿿＀-￯]")
MARKER = re.compile(r"^(\s*(?:>\s?)*(?:#{1,6} |[-*+] |\d+\. )?)")
IMAGE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)")
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(")
HEADING_ID = re.compile(r"\{#[\w-]+\}\s*$")
HASH = re.compile(r'sourceHash\s*=\s*"(\w+)"')


def split(text):
    _, front, body = text.split("+++", 2)  # TOML front matter: +++ ... +++
    return front, body.split("\n")


def shape(line):
    """What must survive translation on a prose line."""
    if not line.strip():
        return ""
    if line.startswith("{{<") or line.strip() == "---":
        return line
    heading_id = HEADING_ID.search(line)
    return (MARKER.match(line).group(1), heading_id and heading_id.group(), IMAGE.findall(line), len(LINK.findall(line)))


def compare(zh, en):
    if len(zh) != len(en):
        return [f"line count differs: zh {len(zh)} vs en {len(en)}"]
    errors, fence = [], False
    for n, (a, b) in enumerate(zip(zh, en), 1):
        if a.lstrip().startswith("```"):
            fence = not fence
            ok = a == b
        elif fence:
            same_start = re.match(r"\s*\S*", a).group() == re.match(r"\s*\S*", b).group()
            ok = a == b or (bool(CJK.search(a)) and same_start)
        else:
            ok = shape(a) == shape(b)
        if not ok:
            errors.append(f"body line {n}: layout differs\n    zh: {a!r}\n    en: {b!r}")
        elif CJK.search(b):
            errors.append(f"body line {n}: Chinese left in English: {b!r}")
    return errors


def main(root=Path(__file__).resolve().parent.parent / "content"):  # repo's content/, whatever the cwd
    failed = False
    for en_path in sorted(root.rglob("index.en-us.md")):
        zh_path = en_path.with_name("index.md")
        zh_text, en_text = zh_path.read_text(encoding="utf-8"), en_path.read_text(encoding="utf-8")
        en_front, en_body = split(en_text)
        errors = compare(split(zh_text)[1], en_body)
        want = hashlib.sha256(zh_text.encode()).hexdigest()[:12]
        got = HASH.search(en_front)
        if not got or got.group(1) != want:
            errors.append(f'stale or missing sourceHash: Chinese source changed, re-check translation, then set sourceHash = "{want}"')
        print(f"{'FAIL' if errors else 'ok  '} {en_path.relative_to(root.parent)}")
        for e in errors:
            print("  " + e)
        failed |= bool(errors)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
