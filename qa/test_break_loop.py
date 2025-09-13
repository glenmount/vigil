from engine.nudge import nudge_from_labels
def test_breaks_trigger_on_interruptions_only():
    labels = {
        "hours_14d": {},          # low hours
        "interruptions_per_hr": 9.0,  # >= med (8)
        "bells_p95": 0.0,
        "doubles_10d": {}
    }
    items = nudge_from_labels(labels)
    titles = [it["title"] for it in items]
    assert any("Schedule protected 15" in t or "Break" in t for t in titles), f"no break nudge: {titles}"
