#!/usr/bin/env python3
import json, math
from pathlib import Path

def _j(path, default):
    try: return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception: return default

def pp(x):
    return None if x is None else round(x, 1)

def rates_from(opps, actions):
    rates = {}
    for u, opp in opps.items():
        a = actions.get(u, 0)
        rates[u] = (a/opp*100.0) if (isinstance(opp,(int,float)) and opp>0) else None
    return rates

def main():
    # previous/current standards
    prev = _j("web/standards.prev.json", {"results":[],"summary":{}})
    curr = _j("web/standards.json",      {"results":[],"summary":{}})

    # viewer denominators + actions from engine queue for per-unit handover rates
    opps = _j("web/opportunities.json", {"windows_per_unit":{}}).get("windows_per_unit",{})
    q    = _j("web/queue.json", {"items":[]})
    acts = {}
    for it in q.get("items",[]):
        if it.get("kind")=="handover":
            u = (it.get("unit") or it.get("scope") or "ALL")
            if u!="ALL":
                acts[u] = acts.get(u,0)+1
    rates = rates_from(opps, acts)

    # diff: rules
    prev_idx = {r["id"]: r for r in prev.get("results",[])}
    rule_changes = []
    for r in curr.get("results",[]):
        rid = r["id"]
        before = prev_idx.get(rid, {})
        if (before.get("ok") != r.get("ok")) or (before.get("observed") != r.get("observed")):
            rule_changes.append({
                "id": rid,
                "title": r.get("title"),
                "ok_before": before.get("ok"),
                "ok_after": r.get("ok"),
                "observed_before": before.get("observed"),
                "observed_after": r.get("observed"),
                "expected": r.get("expected")
            })

    # diff: top-N size (items count)
    topn_before = _j("web/delta.prev.meta.json", {}).get("topn")
    topn_after  = len(q.get("items",[]))
    topn_change = None
    if topn_before is not None and topn_before != topn_after:
        topn_change = {"before": int(topn_before), "after": int(topn_after), "delta": int(topn_after-topn_before)}

    # diff: cohort rates (pp)
    prev_rates = _j("web/delta.prev.meta.json", {}).get("rates") or {}
    rate_changes = []
    for u, r in rates.items():
        old = prev_rates.get(u)
        if (r is not None) and (old is not None):
            d = r - old
            if abs(d) >= 0.1:
                rate_changes.append({"unit": u, "before_pp": pp(old), "after_pp": pp(r), "delta_pp": pp(d)})

    out = {
        "summary": {
            "rules_changed": len(rule_changes),
            "topn_changed": bool(topn_change),
            "units_rate_changed": len(rate_changes)
        },
        "rules": rule_changes,
        "topn": topn_change,
        "cohort_rates": sorted(rate_changes, key=lambda x: -abs(x["delta_pp"]))
    }
    Path("web/delta.json").write_text(json.dumps(out, indent=2), encoding="utf-8")

    # persist current meta as "previous" for next run
    meta = {"topn": topn_after, "rates": {k: (None if v is None else float(v)) for k,v in rates.items()}}
    Path("web/delta.prev.meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print("[delta] wrote web/delta.json and updated web/delta.prev.meta.json")

if __name__ == "__main__":
    main()
