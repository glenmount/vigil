from __future__ import annotations
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
