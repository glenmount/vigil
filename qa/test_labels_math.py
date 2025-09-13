from engine import labels as L

def test_hours_and_overtime_basic():
    t = [
        {"staff_id":"A","clock_in":"2025-01-01T00:00","clock_out":"2025-01-01T08:00"},
        {"staff_id":"A","clock_in":"2025-01-02T00:00","clock_out":"2025-01-02T04:00"},
        {"staff_id":"B","clock_in":"2025-01-01T00:00","clock_out":"2025-01-01T10:00"},
        {"staff_id":"C","clock_in":"2025-01-01T00:00","clock_out":"2025-01-03T00:00"}  # 48h
    ]
    h = L.hours_14d(t)
    assert round(h["A"],2) == 12.0
    assert round(h["B"],2) == 10.0
    assert round(h["C"],2) == 48.0
    ot = L.overtime_7d(t)
    assert round(ot["A"],2) == 0.0
    assert round(ot["B"],2) == 0.0
    assert round(ot["C"],2) == 10.0  # 48-38

def test_doubles_day_sum():
    r = [
        {"staff_id":"D","shift_start":"2025-02-01T07:00","shift_end":"2025-02-01T12:00"},
        {"staff_id":"D","shift_start":"2025-02-01T13:00","shift_end":"2025-02-01T23:00"},  # 15h
        {"staff_id":"E","shift_start":"2025-02-01T07:00","shift_end":"2025-02-01T14:00"}   # 7h
    ]
    d = L.doubles_10d(r)
    assert d["D"] == 1
    assert "E" not in d

def test_bells_stats():
    bells = [
        {"started_at":"2025-01-01T00:00","response_secs":"60"},
        {"started_at":"2025-01-01T01:00","response_secs":"120"},
        {"started_at":"2025-01-01T02:00","response_secs":"540"},
        {"started_at":"2025-01-01T03:00","response_secs":"600"},
    ]
    assert L.bells_p95(bells) == 600.0
    iphr = L.interruptions_per_hr(bells)  # 4 bells over ~3h span
    assert 1.3 < iphr < 1.4
