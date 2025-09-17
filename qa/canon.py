from __future__ import annotations
import json, hashlib
from pathlib import Path as P

def _canon_events_bytes(path: P) -> bytes:
    if not path.exists(): return b""
    objs=[]
    for ln in path.read_text(encoding="utf-8").splitlines():
        ln=ln.strip()
        if not ln: continue
        o=json.loads(ln)
        o.pop("sha256",None)
        o.pop("observed_at",None)
        objs.append(o)
    objs.sort(key=lambda o:(o.get("kind",""), json.dumps(o,sort_keys=True,separators=(",",":"))))
    return json.dumps(objs,sort_keys=True,separators=(",",":")).encode("utf-8")

def _norm_queue_items(path: P):
    if not path.exists(): return []
    src=json.loads(path.read_text(encoding="utf-8"))
    norm=[]
    for it in src.get("items",[]):
        title=(it.get("title","") or "").strip()
        owner=(it.get("owner","") or "").strip()
        receipts=sorted(set(it.get("receipts",[])))
        norm.append((title, owner, tuple(receipts)))
    norm.sort()
    return norm

def _canon_queue_bytes(path: P) -> bytes:
    norm=_norm_queue_items(path)
    return json.dumps({"items": norm}, separators=(",",":")).encode("utf-8")

def _canon_json_bytes(path: P) -> bytes:
    if not path.exists(): return b""
    return json.dumps(json.loads(path.read_text(encoding="utf-8")),
                      sort_keys=True,separators=(",",":")).encode("utf-8")

def sha256_hex(b: bytes) -> str: return hashlib.sha256(b).hexdigest()

def compute_hashes() -> dict:
    e = sha256_hex(_canon_events_bytes(P("receipts/events.jsonl")))
    q = sha256_hex(_canon_queue_bytes(P("web/queue.json")))
    r = sha256_hex(_canon_json_bytes(P("web/report.json")))
    return {"events.jsonl": e, "queue.json": q, "report.json": r}
