from __future__ import annotations
import json, pathlib
from engine.receipts import write_event
from engine.citations import cite
from engine.clock import now_iso, today_iso_date

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
      "id": f"{name.lower().replace(' ','-')}-{today_iso_date()}",
      "title": reason,
      "owner": owner_default,
      "due_by": due_iso,
      "receipts": receipts
    }

def nudge_from_labels(labels: dict) -> list:
    items = []

    # Doubles → Recovery
    total_doubles = sum(labels.get("doubles_10d", {}).values()) if isinstance(labels.get("doubles_10d"), dict) else float(labels.get("doubles_10d",0))
    dbl_lvl = risk_level(total_doubles, TH["doubles_10d"])
    if dbl_lvl in ("HIGH","MED"):
        r=[]
        e=write_event("nudge", {"unit":"ALL"}, {"doubles_10d":labels.get("doubles_10d",{})}, TH["doubles_10d"], None, cite("doubles")); r.append(e["sha256"])
        items.append(apply_playbook("Double-Shift Recovery", f"{dbl_lvl}: protect 48h rest window","rostering", now_iso(), r))

    # Break Guarantees — trigger on hours OR interruptions
    total_hours = sum(labels.get("hours_14d", {}).values()) if isinstance(labels.get("hours_14d"), dict) else float(labels.get("hours_14d",0))
    brk_lvl = risk_level(total_hours, TH["hours_14d"])
    intr = float(labels.get("interruptions_per_hr", 0.0))
    intr_high_enough = intr >= TH["interruptions_per_hr"]["med"]
    if brk_lvl in ("HIGH","MED") or intr_high_enough:
        r=[]
        payload = {"hours_14d":labels.get("hours_14d",{}), "interruptions_per_hr":intr}
        e=write_event("nudge", {"unit":"ALL"}, payload, {"hours_14d":TH["hours_14d"], "interruptions_per_hr":TH["interruptions_per_hr"]}, None, cite("breaks")); r.append(e["sha256"])
        items.append(apply_playbook("Break Guarantees", "Schedule protected 15-min breaks", "unit_manager", now_iso(), r))

    # Bells → Hydration & Offload
    bell95 = float(labels.get("bells_p95",0.0)) if not isinstance(labels.get("bells_p95"), dict) else 0.0
    if bell95 >= TH["bells_p95"]["med"]:
        r=[]
        e=write_event("nudge", {"unit":"ALL"}, {"bells_p95":bell95}, TH["bells_p95"], None, cite("bells")); r.append(e["sha256"])
        items.append(apply_playbook("Hydration & Offload", "MED: long bells → offload docs + hydration rounds", "assistant", now_iso(), r))

    # Sterile Cockpit (Handover) — per-unit items when breached, else ALL fallback
    breaches_total = int(labels.get("handover_breaches_total", 0))
    breach_units = labels.get("handover_breach_units", {})
    if breaches_total >= 1:
        if breach_units:
            for u, c in sorted(breach_units.items()):
                r=[]
                e=write_event("nudge", {"unit":u}, {"handover_breaches_total":c}, {}, None, cite("handover")); r.append(e["sha256"])
                items.append(apply_playbook("Sterile Cockpit: protect 20-min handover window (no interruptions) — Unit {}".format(u),
                                            "Sterile Cockpit — Unit {}".format(u), "unit_manager", now_iso(), r))
        else:
            r=[]
            e=write_event("nudge", {"unit":"ALL"}, {"handover_breaches_total":breaches_total}, {}, None, cite("handover")); r.append(e["sha256"])
            items.append(apply_playbook("Sterile Cockpit: protect 20-min handover window (no interruptions)",
                                        "Sterile Cockpit", "unit_manager", now_iso(), r))
    return items
