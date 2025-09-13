import json, pathlib

def _load_json(p):
    return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))

def _load_jsonl(p):
    out=[]; q=pathlib.Path(p)
    if not q.exists(): return out
    for line in q.read_text(encoding="utf-8").splitlines():
        if line.strip(): out.append(json.loads(line))
    return out

def _gap_pp(items):
    if not items: return 0.0
    a=[it for i,it in enumerate(items) if i%2==0]
    b=[it for i,it in enumerate(items) if i%2==1]
    total=max(1,len(a)+len(b))
    return abs(len(a)/total - len(b)/total) * 100.0

def main():
    queue=_load_json("web/queue.json") if pathlib.Path("web/queue.json").exists() else {"items":[]}
    items=queue.get("items",[])
    events=_load_jsonl("receipts/events.jsonl")
    nudges=[e for e in events if e.get("kind")=="nudge"]
    cits_avg = (sum(len(e.get("citations",[])) for e in nudges)/len(nudges)) if nudges else 0.0
    sb = {
        "items": len(items),
        "nudges": len(nudges),
        "citations_avg_per_nudge": round(cits_avg,2),
        "fairness_gap_pp": round(_gap_pp(items), 2),
        "receipts_lines": len(events)
    }
    pathlib.Path("web/scoreboard.json").write_text(
        json.dumps(sb, sort_keys=True, separators=(",",":")), encoding="utf-8"
    )
    print("wrote web/scoreboard.json")

if __name__=="__main__": main()
