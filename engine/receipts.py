from __future__ import annotations
import json, hashlib, pathlib, datetime

RECEIPTS = pathlib.Path("receipts"); RECEIPTS.mkdir(exist_ok=True)

def _sha256(obj) -> str:
    data = json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(data).hexdigest()

def write_event(kind: str, subject: dict, inputs: dict, thresholds: dict, action: dict|None=None, citations=list()):
    evt = {
        "observed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "kind": kind,
        "subject": subject,
        "inputs": inputs,
        "thresholds": thresholds,
        "action": action,
        "citations": citations,
        "sha256": ""
    }
    evt["sha256"] = _sha256({"inputs":inputs,"thresholds":thresholds,"action":action})
    with (RECEIPTS/"events.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(evt, ensure_ascii=False)+"\n")
    return evt
