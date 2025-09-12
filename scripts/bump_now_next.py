#!/usr/bin/env python3
import re
from pathlib import Path
from datetime import datetime
try:
    from zoneinfo import ZoneInfo
    TZ = ZoneInfo("Australia/Brisbane")
except Exception:
    TZ = None

DOC = Path("docs/NOW_NEXT.md")
HDR = re.compile(r"^Updated:\s.*$", re.MULTILINE)

def main():
    if not DOC.exists():
        print("NOW_NEXT.md missing"); return
    text = DOC.read_text(encoding="utf-8")
    stamp = (datetime.now(TZ) if TZ else datetime.now()).strftime("%d %b %Y %H:%M")
    line = f"Updated: {stamp} (AEST)"
    if HDR.search(text):
        text = HDR.sub(line, text, count=1)
    else:
        text = line + "\n\n" + text
    DOC.write_text(text, encoding="utf-8")
    print("NOW/NEXT timestamp updated.")

if __name__ == "__main__":
    main()
