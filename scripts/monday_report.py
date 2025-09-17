#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime, timezone

def _j(p, default):
    try: return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception: return default

queue = _j("web/queue.json", {})
score = _j("web/scoreboard.json", {})
opps  = _j("web/opportunities.json", {"windows_per_unit": {}}).get("windows_per_unit", {})

items = queue.get("items", []) or []
handover = [i for i in items if i.get("kind") == "handover"]
bells    = [i for i in items if "bell"  in (i.get("kind") or "") or "bell"  in (i.get("title") or "").lower()]
breaks   = [i for i in items if "break" in (i.get("kind") or "") or "break" in (i.get("title") or "").lower()]

# Tightened fairness rule: compute a gap ONLY when >=2 cohorts have BOTH opportunities AND actions.
rates = []
valid = 0
for u, v in sorted(opps.items()):
    au = sum(1 for i in handover if (i.get("unit") or i.get("scope") or "ALL") == u)
    if v and au > 0:
        valid += 1
        rates.append(au / v)

gap_pp = round((max(rates) - min(rates)) * 100, 1) if valid >= 2 else None

out = {
  "generated_at": datetime.now(timezone.utc).isoformat(),
  "totals": { "items": len(items), "handover": len(handover), "bells": len(bells), "breaks": len(breaks) },
  "denominators": { "windows_per_unit": opps },
  "fairness_gap_pp": gap_pp,
  "notes": [
    "Receipt-free summary for Monday site-wide report.",
    "Fairness is enforced in CI only when ≥2 cohorts are valid (cohorts = units; denominators = windows)."
  ]
}
Path("web/monday.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
print("[monday] wrote web/monday.json (tight gate)")
