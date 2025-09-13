#!/usr/bin/env python3
from __future__ import annotations
import argparse, re, sys
from pathlib import Path
from datetime import datetime
try:
    from zoneinfo import ZoneInfo
    TZ = ZoneInfo("Australia/Brisbane")
except Exception:
    TZ = None

DOC = Path("docs/NOW_NEXT.md")
HDR_RE = re.compile(r"^Updated:\s.*$", re.MULTILINE)
SEC_RE = {"now": re.compile(r"(?ms)^## NOW.*?(?=^## |\Z)"),
          "next": re.compile(r"(?ms)^## NEXT.*?(?=^## |\Z)")}

def update_timestamp(text: str) -> str:
    now = datetime.now(TZ) if TZ else datetime.now()
    line = f"Updated: {now.strftime('%d %b %Y %H:%M')} (AEST)"
    if HDR_RE.search(text):
        return HDR_RE.sub(line, text, count=1)
    # if header missing, insert at top
    return line + "\n\n" + text

def mark_done(text: str, pattern: str) -> str:
    # turns "- [ ] ..." into "- [x] ..." for the first matching bullet
    return re.sub(rf"^- \[ \] (.*{re.escape(pattern)}.*)$",
                  r"- [x] \1", text, count=1, flags=re.MULTILINE)

def append_item(text: str, section: str, item: str) -> str:
    m = SEC_RE[section].search(text)
    if not m:  # no section? append at end
        return text + f"\n- [ ] {item}\n"
    block = m.group(0)
    # insert just before the next blank line or end of section
    insert_at = block.rfind("\n")
    new_block = block + f"- [ ] {item}\n"
    return text[:m.start()] + new_block + text[m.end():]

def main():
    ap = argparse.ArgumentParser(description="Bump NOW/NEXT: timestamp, check items, append bullets.")
    ap.add_argument("--touch", action="store_true", help="Update the Updated: timestamp only.")
    ap.add_argument("--check", action="append", default=[], help="Mark the first matching bullet as done (regex literal).")
    ap.add_argument("--add-now", action="append", default=[], help="Append a new unchecked bullet under NOW.")
    ap.add_argument("--add-next", action="append", default=[], help="Append a new unchecked bullet under NEXT.")
    args = ap.parse_args()

    text = DOC.read_text(encoding="utf-8")

    # always update timestamp unless file is empty
    if text.strip():
        text = update_timestamp(text)

    for pat in args.check:
        text = mark_done(text, pat)

    for it in args.add_now:
        text = append_item(text, "now", it)

    for it in args.add_next:
        text = append_item(text, "next", it)

    DOC.write_text(text, encoding="utf-8")
    print("NOW/NEXT updated.")

if __name__ == "__main__":
    main()
