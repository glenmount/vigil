from engine.metrics import dm_percent_v0
def test_dm_percent_monotonic_interruptions():
    labels1 = {"interruptions_per_hr": 2.0, "bells_p95": 300}
    labels2 = {"interruptions_per_hr": 6.0, "bells_p95": 300}
    assert dm_percent_v0(labels1) > dm_percent_v0(labels2)
def test_dm_percent_bounds_and_rounding():
    labels = {"interruptions_per_hr": 0.0, "bells_p95": 0}
    v = dm_percent_v0(labels)
    assert 0.0 <= v <= 100.0
    assert abs(v - round(v,1)) < 1e-9
