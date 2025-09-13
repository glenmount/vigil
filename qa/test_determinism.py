import json, hashlib, subprocess, pathlib, time

FILES = ["receipts/events.jsonl","receipts/labels.json","web/queue.json","web/report.json"]

def _sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def _canon_events_jsonl(path: pathlib.Path) -> bytes:
    """Parse JSONL -> list, drop computed fields, sort, dump canonical JSON bytes."""
    if not path.exists(): return b""
    objs = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line: continue
        o = json.loads(line)
        # ignore computed / time fields
        o.pop("sha256", None)
        o.pop("observed_at", None)
        objs.append(o)
    # stable order: by kind then a stable string of the payload
    def key(o):
        payload = json.dumps(o, sort_keys=True, separators=(",",":"))
        return (o.get("kind",""), payload)
    objs.sort(key=key)
    return json.dumps(objs, sort_keys=True, separators=(",",":")).encode("utf-8")

def _canon_json(path: pathlib.Path) -> bytes:
    if not path.exists(): return b""
    obj = json.loads(path.read_text(encoding="utf-8"))
    if path.as_posix().endswith("queue.json"):
        for it in obj.get("items", []):
            it["receipts"] = sorted(it.get("receipts", []))
        obj["items"] = sorted(obj.get("items", []), key=lambda x: (x.get("id",""), x.get("title","")))
    return json.dumps(obj, sort_keys=True, separators=(",",":")).encode("utf-8")

def canon_hashes():
    e = _sha_bytes(_canon_events_jsonl(pathlib.Path("receipts/events.jsonl")))
    q = _sha_bytes(_canon_json(pathlib.Path("web/queue.json")))
    r = _sha_bytes(_canon_json(pathlib.Path("web/report.json")))
    return {"receipts/events.jsonl": e, "web/queue.json": q, "web/report.json": r}

def test_deterministic_build():
    for p in FILES: pathlib.Path(p).unlink(missing_ok=True)
    subprocess.check_call(["make","all"])
    h1 = canon_hashes()
    time.sleep(0.05)
    for p in FILES: pathlib.Path(p).unlink(missing_ok=True)
    subprocess.check_call(["make","all"])
    h2 = canon_hashes()
    assert h1 == h2, f"hash drift: {h1} vs {h2}"
