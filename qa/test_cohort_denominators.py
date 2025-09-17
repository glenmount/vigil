from engine.fairness import compute_fairness_gap

def test_denominator_rates_balance_gap_small():
    labels = {
        "handover_windows_per_unit": {"A": 10, "B": 10}
    }
    queue = {
        "items": [
            {"title": "Sterile Cockpit: ... — Unit A"},
            {"title": "Sterile Cockpit: ... — Unit A"},
            {"title": "Sterile Cockpit: ... — Unit B"},
            {"title": "Sterile Cockpit: ... — Unit B"},
        ]
    }
    gap, rates = compute_fairness_gap(labels, queue)
    assert gap == 0.0, f"expected 0 gap, got {gap:.2f} with rates {rates}"

def test_denominator_gap_detects_imbalance():
    labels = { "handover_windows_per_unit": {"A": 10, "B": 10} }
    queue  = { "items": [{"title":"Sterile Cockpit: ... — Unit A"}] }  # A:1/10, B:0/10
    gap, rates = compute_fairness_gap(labels, queue)
    assert gap == 10.0, f"expected 10.0pp gap, got {gap:.2f} with rates {rates}"
