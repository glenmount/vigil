from __future__ import annotations
import json, hashlib
from pathlib import Path as P

def canon_events_bytes(path: P) -> bytes:
    """JSONL → list, drop computed fields, stable-sort, dump canonical bytes."""
    if not path.exists(): return b""
    objs = []
    for ln in path.read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if not ln: continue
        o = json.loads(ln)
        o.pop("sha256", None)
        o.pop("observed_at", None)
        objs.append(o)
    objs.sort(key=lambda o: (o.get("kind",""), json.dumps(o, sort_keys=True, separators=(",",":"))))
    return json.dumps(objs, sort_keys=True, separators=(",",":")).encode("utf-8")

def canon_queue_bytes(path: P) -> bytes:
    if not path.exists(): return b""
    obj = json.loads(path.read_text(encoding="utf-8"))
    for it in obj.get("items", []):
        it["receipts"] = sorted(it.get("receipts", []))
    obj["items"] = sorted(obj.get("items", []), key=lambda x: (x.get("id",""), x.get("title","")))
    return json.dumps(obj, sort_keys=True, separators=(",",":")).encode("utf-8")

def canon_json_bytes(path: P) -> bytes:
    if not path.exists(): return b""
    obj = json.loads(path.read_text(encoding="utf-8"))
    return json.dumps(obj, sort_keys=True, separators=(",",":")).encode("utf-8")

def sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def compute_hashes() -> dict:
    e = sha256_hex(canon_events_bytes(P("receipts/events.jsonl")))
    q = sha256_hex(canon_queue_bytes(P("web/queue.json")))
    r = sha256_hex(canon_json_bytes(P("web/report.json")))
    return {"events.jsonl": e, "queue.json": q, "report.json": r}
