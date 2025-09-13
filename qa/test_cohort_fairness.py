import json, pathlib, subprocess, os, pytest
from engine.fairness import compute_fairness_gap

def test_unit_cohort_fairness_gap_computes():
    # Build
    env = os.environ.copy()
    subprocess.check_call(["make","all"], env=env)
    labels = json.loads(pathlib.Path("receipts/labels.json").read_text(encoding="utf-8"))
    queue  = json.loads(pathlib.Path("web/queue.json").read_text(encoding="utf-8"))
    gap, rates = compute_fairness_gap(labels, queue)
    # If fewer than 2 units in rates, skip
    if len(rates) < 2 or sum(1 for v in rates.values() if v>0) < 2:
        pytest.skip("Not enough unit cohorts with actions to assert fairness")
    assert gap < 1.0, f"cohort fairness gap {gap:.2f}pp >= 1.0pp"
