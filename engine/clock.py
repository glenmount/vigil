from __future__ import annotations
import os, datetime
_FIXED = os.environ.get("VIGIL_FIXED_NOW")

def _fixed():
    if not _FIXED: return None
    try: return datetime.datetime.fromisoformat(_FIXED)
    except Exception: return None

def now_iso() -> str:
    dt = _fixed()
    if dt is None:
        dt = datetime.datetime(1970,1,1,tzinfo=datetime.timezone.utc)
    return dt.isoformat()

def today_iso_date() -> str:
    dt = _fixed()
    if dt is None:
        return datetime.date(1970,1,1).isoformat()
    return dt.date().isoformat()
