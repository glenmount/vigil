#!/usr/bin/env python3
import csv, json, os
from pathlib import Path

bundle = Path(os.environ.get("VIGIL_BUNDLE", "qa/goldens/fixtures"))
roster = bundle / "roster.csv"
out = Path("web/opportunities.json")

ops = {}
if roster.exists():
    with roster.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            unit = (row.get("unit") or "ALL").strip()
            ops[unit] = ops.get(unit, 0) + 1  # one 20-min window per shift_start per unit
else:
    ops = {}

out.write_text(json.dumps({"windows_per_unit": ops}, indent=2), encoding="utf-8")
print(f"[emit_opportunities] wrote {out} from {roster}")
