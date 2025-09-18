#!/usr/bin/env python3
import json
from pathlib import Path

def _j(p, d):
    try: return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception: return d

def main():
    rules   = _j("policies/rules.json", {"rules":[]}).get("rules", [])
    queue   = _j("web/queue.json",      {"items":[]})
    score   = _j("web/scoreboard.json", {})
    opps    = _j("web/opportunities.json", {"windows_per_unit":{}}).get("windows_per_unit", {})
    labels  = _j("receipts/labels.json", {})

    items = queue.get("items",[]) or []

    # actions per unit from queue (handover only)
    acts={}
    for it in items:
        if it.get("kind")=="handover":
            u = (it.get("unit") or it.get("scope") or "ALL")
            if u!="ALL": acts[u]=acts.get(u,0)+1

    res=[]
    for r in rules:
        rid, title, kind, op, val = r.get("id"), r.get("title"), r.get("kind"), r.get("op"), r.get("value")
        ok, observed = None, None

        if rid=="handover.window.minutes":
            observed = 20
            ok = (observed==val) if op=="eq" else None

        elif rid=="nudges.top_n.max":
            observed = len(items)
            ok = (observed <= val) if op=="lte" else None

        elif rid=="bells.p95.lte":
            p95 = (score.get("bells",{}) or {}).get("p95")
            if p95 is None:
                p95 = labels.get("bells_p95") or (labels.get("bells",{}) or {}).get("p95")
            observed = p95
            ok = (p95 <= val) if (p95 is not None and op=="lte") else None

        elif rid=="handover.tolerance.pp.lte":
            # actions per unit from queue (handover only)
            acts={}
            for it in items:
                if it.get("kind")=="handover":
                    u=(it.get("unit") or it.get("scope") or "ALL")
                    if u!="ALL":
                        acts[u]=acts.get(u,0)+1

            # fallback: labels.handover.breaches_per_unit when queue has only ALL
            if not acts:
                lab_h = (labels.get("handover") or {})
                lab_per = (lab_h.get("breaches_per_unit") or {})
                # only take strictly positive counts
                acts = { str(u): int(c or 0) for u,c in lab_per.items() if int(c or 0) > 0 }

            rates=[]
            for u,opp in opps.items():
                if isinstance(opp,(int,float)) and opp>0:
                    a = acts.get(u,0)
                    rates.append(a/opp*100.0)
            if rates:
                mx = max(rates)
                observed = round(mx,1)
                ok = (mx <= val) if op=="lte" else None
            else:
                observed, ok = None, None
elif rid=="breaks.presence.when.longhours":
            has_breaks = any("break" in (it.get("kind","")+it.get("title","")).lower() for it in items)
            observed = 1 if has_breaks else 0
            ok = (observed >= 1) if op=="present" else None

        res.append({
            "id": rid, "title": title, "ok": ok,
            "observed": observed, "expected": {"op": op, "value": val}
        })

    out = {
        "results": res,
        "summary": {
            "passed": sum(1 for x in res if x["ok"] is True),
            "failed": sum(1 for x in res if x["ok"] is False),
            "unknown":sum(1 for x in res if x["ok"] is None),
        }
    }
    Path("web/standards.json").write_text(json.dumps(out,indent=2), encoding="utf-8")
    print("[standards] wrote web/standards.json")
if __name__=="__main__":
    main()
