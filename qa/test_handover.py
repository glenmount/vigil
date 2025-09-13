from engine import labels as L
from engine.nudge import nudge_from_labels

def test_handover_windows_exist_with_roster():
    roster = [
        {"staff_id":"X","unit":"A","role":"carer","shift_start":"2025-09-01T07:00","shift_end":"2025-09-01T15:00"},
        {"staff_id":"Y","unit":"B","role":"carer","shift_start":"2025-09-01T15:00","shift_end":"2025-09-01T23:00"},
    ]
    wins = L.handover_windows(roster)
    assert len(wins) == 2
    assert wins[0]["unit"] in ("A","B")
    assert wins[0]["end"] > wins[0]["start"]

def test_handover_nudge_on_breach():
    labels = {
        "hours_14d": {},
        "interruptions_per_hr": 0.0,
        "bells_p95": 0.0,
        "doubles_10d": {},
        "handover_breaches_total": 1
    }
    items = nudge_from_labels(labels)
    titles = [it["title"] for it in items]
    assert any("Sterile Cockpit" in t for t in titles), f"no handover nudge in {titles}"
