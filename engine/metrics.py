from __future__ import annotations
def _clamp(x: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, x))
def dm_percent_v0(labels: dict) -> float:
    """Deterministic proxy: penalize interruptions and long tail of bell responses."""
    intr = float(labels.get("interruptions_per_hr", 0.0))
    p95  = float(labels.get("bells_p95", 0.0))  # seconds
    score = 100.0 - 3.0*intr - 0.05*p95  # -30 at 600s p95, -3 per extra intr/hr
    return round(_clamp(score), 1)
