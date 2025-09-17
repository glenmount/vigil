import json, pathlib
from engine.fairness import compute_fairness_gap

def _load_json(p): return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))
def _load_jsonl(p):
    out=[]; q=pathlib.Path(p)
    if not q.exists(): return out
    for line in q.read_text(encoding="utf-8").splitlines():
        if line.strip(): out.append(json.loads(line))
    return out

def main():
    queue=_load_json("web/queue.json") if pathlib.Path("web/queue.json").exists() else {"items":[]}
    labels=_load_json("receipts/labels.json") if pathlib.Path("receipts/labels.json").exists() else {}
    events=_load_jsonl("receipts/events.jsonl")
    gap_pp, _rates = compute_fairness_gap(labels, queue)
    nudges=[e for e in events if e.get("kind")=="nudge"]
    cits_avg = (sum(len(e.get("citations",[])) for e in nudges)/len(nudges)) if nudges else 0.0
    sb = {
        "items": len(queue.get("items",[])),
        "nudges": len(nudges),
        "fairness_gap_pp": round(gap_pp,2),
        "citations_avg_per_nudge": round(cits_avg,2),
        "receipts_lines": len(events),
        "handover_breaches": int(labels.get("handover_breaches_total", 0))
    }
    pathlib.Path("web/scoreboard.json").write_text(
        json.dumps(sb, sort_keys=True, separators=(",",":")), encoding="utf-8"
    )
    print("wrote web/scoreboard.json")

if __name__=="__main__": main()
