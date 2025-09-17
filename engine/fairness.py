from __future__ import annotations
from typing import Dict, List, Tuple

def _units_from_labels(labels: dict) -> List[str]:
    m = labels.get("handover_windows_per_unit") or {}
    units = sorted([u for u,c in m.items() if c and c > 0])
    return units or ["ALL"]

def _unit_of_item(it: dict) -> str:
    t = (it.get("title") or "")
    if "Unit " in t:
        try:
            after = t.split("Unit ",1)[1]
            u = after.split()[0].strip("—:-,)")
            return u
        except Exception:
            pass
    return "ALL"

def unit_opportunities(labels: dict, units: List[str]) -> Dict[str, float]:
    per = labels.get("handover_windows_per_unit") or {}
    return {u: float(per.get(u, 0.0)) for u in units}

def unit_items(queue: dict, units: List[str]) -> Dict[str, float]:
    items = queue.get("items", [])
    counts = {u: 0.0 for u in units}
    for it in items:
        u = _unit_of_item(it)
        if u in counts: counts[u] += 1.0
    return counts

def unit_action_rates(queue: dict, labels: dict) -> Dict[str, float]:
    units = _units_from_labels(labels)
    opp = unit_opportunities(labels, units)
    cnt = unit_items(queue, units)
    rates = {}
    for u in units:
        den = opp.get(u, 0.0)
        # Only count rates where we have non-zero opportunities
        rates[u] = (cnt[u] / den) if den > 0 else 0.0
    return rates

def gap_pp_from_rates(rates: Dict[str,float]) -> float:
    if len(rates) < 2:
        return 0.0
    vals = list(rates.values())
    return abs(max(vals) - min(vals)) * 100.0

def compute_fairness_gap(labels: dict, queue: dict) -> Tuple[float, Dict[str,float]]:
    rates = unit_action_rates(queue, labels)
    return gap_pp_from_rates(rates), rates
