from __future__ import annotations
import json, pathlib, datetime
from engine.receipts import write_event
from engine.citations import cite

POLICY = json.loads(pathlib.Path("engine/policy.json").read_text(encoding="utf-8")) if pathlib.Path("engine/policy.json").exists() else {
    "index_version":"v1",
    "thresholds":{
        "hours_14d":{"high":100,"med":80},
        "overtime_7d":{"high":8,"med":4},
        "doubles_10d":{"high":2,"med":1},
        "bells_p95":{"high":480,"med":240},
        "interruptions_per_hr":{"high":12,"med":8}
    }
}
TH = POLICY["thresholds"]

def risk_level(val: float, th: dict) -> str:
    if val >= th["high"]: return "HIGH"
    if val >= th["med"]:  return "MED"
    return "LOW"

def apply_playbook(name: str, reason: str, owner_default: str, due_iso: str, receipts:list):
    return {
      "id": f"{name.lower().replace(' ','-')}-{datetime.date.today().isoformat()}",
      "title": reason,
      "owner": owner_default,
      "due_by": due_iso,
      "receipts": receipts
    }

def nudge_from_labels(labels: dict) -> list:
    items = []
    # Doubles
    total_doubles = sum(labels["doubles_10d"].values()) if isinstance(labels["doubles_10d"], dict) else float(labels["doubles_10d"])
    dbl_lvl = risk_level(total_doubles, TH["doubles_10d"])
    if dbl_lvl in ("HIGH","MED"):
        receipts = []
        e = write_event("nudge", {"unit":"ALL"}, {"doubles_10d":labels["doubles_10d"]}, TH["doubles_10d"], None, cite("doubles"))
        receipts.append(e["sha256"])
        items.append(apply_playbook("Double-Shift Recovery", f"{dbl_lvl}: protect 48h rest window", "rostering",
                                    datetime.datetime.now(datetime.timezone.utc).isoformat(), receipts))
    # Breaks (hours)
    total_hours = sum(labels["hours_14d"].values()) if isinstance(labels["hours_14d"], dict) else float(labels["hours_14d"])
    brk_lvl = risk_level(total_hours, TH["hours_14d"])
    if brk_lvl in ("HIGH","MED"):
        receipts = []
        e = write_event("nudge", {"unit":"ALL"}, {"hours_14d":labels["hours_14d"]}, TH["hours_14d"], None, cite("breaks"))
        receipts.append(e["sha256"])
        items.append(apply_playbook("Break Guarantees", f"{brk_lvl}: schedule protected breaks", "unit_manager",
                                    datetime.datetime.now(datetime.timezone.utc).isoformat(), receipts))
    # Bells
    bell95 = float(labels["bells_p95"]) if not isinstance(labels["bells_p95"], dict) else 0.0
    if bell95 >= TH["bells_p95"]["med"]:
        receipts = []
        e = write_event("nudge", {"unit":"ALL"}, {"bells_p95":bell95}, TH["bells_p95"], None, cite("bells"))
        receipts.append(e["sha256"])
        items.append(apply_playbook("Hydration & Offload", "MED: long bells → offload docs + hydration rounds", "assistant",
                                    datetime.datetime.now(datetime.timezone.utc).isoformat(), receipts))
    return items
