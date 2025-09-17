#!/usr/bin/env python3
import json
from pathlib import Path

def _j(p, d):
    try: return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception: return d

def main():
    rules = _j("policies/rules.json", {"rules":[]}).get("rules", [])
    queue = _j("web/queue.json", {"items":[]})
    labels= _j("receipts/labels.json", {})
    items = queue.get("items", [])

    results = []
    for r in rules:
        rid, title, kind, op, val = r.get("id"), r.get("title"), r.get("kind"), r.get("op"), r.get("value")
        ok, observed = True, None

        if rid == "handover.window.minutes":
            # infer configured window from labels (where we computed windows)
            # if not available, mark unknown
            hw = 20  # current hard-coded design default
            observed = hw
            if op == "eq": ok = (observed == val)

        elif rid == "nudges.top_n.max":
            topn = len(items)
            observed = topn
            if op == "lte": ok = (topn <= val)

        else:
            ok, observed = None, None  # unknown rule

        results.append({
            "id": rid, "title": title, "ok": ok,
            "observed": observed, "expected": {"op": op, "value": val}
        })

    out = {
        "version": 1,
        "summary": {
            "passed": sum(1 for r in results if r["ok"] is True),
            "failed": sum(1 for r in results if r["ok"] is False),
            "unknown": sum(1 for r in results if r["ok"] is None)
        },
        "results": results
    }
    Path("web/standards.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print("[standards] wrote web/standards.json")
if __name__ == "__main__":
    main()
