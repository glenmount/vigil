from __future__ import annotations
import datetime
from typing import Dict, List
from adapters.loaders import parse_dt

def hours_14d(timeclock: List[dict]) -> Dict[str, float]:
    totals: Dict[str, float] = {}
    for row in timeclock:
        sid = row["staff_id"]
        start = parse_dt(row["clock_in"])
        end = parse_dt(row["clock_out"])
        hrs = (end - start).total_seconds() / 3600.0
        totals[sid] = totals.get(sid, 0.0) + hrs
    return totals

def doubles_10d(roster: List[dict]) -> Dict[str, int]:
    per_day_hours: Dict[tuple, float] = {}
    for r in roster:
        sid = r["staff_id"]
        start = parse_dt(r["shift_start"])
        end = parse_dt(r["shift_end"])
        day = start.date()
        span = (end - start).total_seconds() / 3600.0
        per_day_hours[(sid, day)] = per_day_hours.get((sid, day), 0.0) + span
    counts: Dict[str, int] = {}
    for (sid, _day), total in per_day_hours.items():
        if total >= 15.0:
            counts[sid] = counts.get(sid, 0) + 1
    return counts

def overtime_7d(timeclock: List[dict]) -> Dict[str, float]:
    totals = hours_14d(timeclock)
    return {sid: max(0.0, hrs - 38.0) for sid, hrs in totals.items()}

def bells_p95(bells: List[dict]) -> float:
    if not bells:
        return 0.0
    vals = sorted(int(b["response_secs"]) for b in bells)
    idx = int(round(0.95 * (len(vals) - 1)))
    return float(vals[idx])

def interruptions_per_hr(bells: List[dict]) -> float:
    if not bells:
        return 0.0
    first = min(parse_dt(b["started_at"]) for b in bells)
    last = max(parse_dt(b["started_at"]) for b in bells)
    span_hours = max(1.0, (last - first).total_seconds() / 3600.0)
    return len(bells) / span_hours

# ---- Sterile Cockpit / Handover helpers (v1) ----
from typing import Tuple
from adapters.loaders import parse_dt

def handover_windows(roster: List[dict]) -> List[dict]:
    """
    v1: every shift_start creates a [start, start+20m] window per unit.
    Returns sorted list of {"unit", "start", "end"} (ISO strings, UTC-naive as per fixtures).
    """
    seen = set()
    wins: List[dict] = []
    for r in roster:
        unit = r.get("unit","ALL")
        start = parse_dt(r["shift_start"])
        end = parse_dt(r["shift_end"])
        win_start = start
        win_end = start + datetime.timedelta(minutes=20)
        key = (unit, win_start.isoformat())
        if key in seen:
            continue
        seen.add(key)
        wins.append({
            "unit": unit,
            "start": win_start.isoformat(),
            "end": win_end.isoformat()
        })
    wins.sort(key=lambda w: (w["unit"], w["start"]))
    return wins

def handover_breaches(bells: List[dict], windows: List[dict]) -> Tuple[int, Dict[str,int]]:
    """
    Counts how many handover windows had ≥1 bell inside the window.
    Returns (total_breaches, breaches_per_unit).
    """
    # Pre-parse bell times once
    bts = [(b.get("resident_id",""), parse_dt(b["started_at"])) for b in bells]
    per_unit = {}
    total = 0
    for w in windows:
        u = w["unit"]
        ws = parse_dt(w["start"])
        we = parse_dt(w["end"])
        hit = any(ws <= t <= we for (_rid, t) in bts)
        if hit:
            per_unit[u] = per_unit.get(u, 0) + 1
            total += 1
    return total, per_unit
