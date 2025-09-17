import json, subprocess, pathlib, time

FILES = ["receipts/events.jsonl","receipts/labels.json","web/queue.json","web/report.json"]

def _norm_queue_items(path: pathlib.Path):
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

def _canon_events_list(path: pathlib.Path):
    if not path.exists(): return []
    out=[]
    for line in path.read_text(encoding="utf-8").splitlines():
        line=line.strip()
        if not line: continue
        o=json.loads(line)
        o.pop("sha256",None); o.pop("observed_at",None)
        out.append(o)
    out.sort(key=lambda o:(o.get("kind",""), json.dumps(o,sort_keys=True,separators=(",",":"))))
    return out

def canon_struct():
    e = _canon_events_list(pathlib.Path("receipts/events.jsonl"))
    q = _norm_queue_items(pathlib.Path("web/queue.json"))
    r = json.loads(pathlib.Path("web/report.json").read_text(encoding="utf-8")) if pathlib.Path("web/report.json").exists() else {}
    return {"events": e, "queue_items": q, "report": r}

def test_deterministic_build():
    for p in FILES: pathlib.Path(p).unlink(missing_ok=True)
    subprocess.check_call(["make","all"])
    s1 = canon_struct()
    time.sleep(0.05)
    for p in FILES: pathlib.Path(p).unlink(missing_ok=True)
    subprocess.check_call(["make","all"])
    s2 = canon_struct()
    assert s1 == s2, f"semantic drift:\n{s1}\nvs\n{s2}"
