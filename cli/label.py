import json, pathlib
from adapters.loaders import load_bundle
from engine import labels as L
from engine.receipts import write_event

FIX = pathlib.Path("qa/goldens/fixtures")

def main():
    b = load_bundle(FIX)
    hours = L.hours_14d(b["timeclock"])
    doubles = L.doubles_10d(b["roster"])
    overtime = L.overtime_7d(b["timeclock"])
    bells95 = L.bells_p95(b["bells"])
    intr = L.interruptions_per_hr(b["bells"])

    write_event("label", {"cohort":"ALL"}, {"hours_14d":hours}, {}, None, [])
    write_event("label", {"cohort":"ALL"}, {"doubles_10d":doubles}, {}, None, [])
    write_event("label", {"cohort":"ALL"}, {"overtime_7d":overtime}, {}, None, [])
    write_event("label", {"cohort":"ALL"}, {"bells_p95":bells95}, {}, None, [])
    write_event("label", {"cohort":"ALL"}, {"interruptions_per_hr":intr}, {}, None, [])

    snapshot = {
        "hours_14d": hours, "doubles_10d": doubles, "overtime_7d": overtime,
        "bells_p95": bells95, "interruptions_per_hr": intr
    }
    pathlib.Path("receipts/labels.json").write_text(json.dumps(snapshot), encoding="utf-8")
    print("labels computed")

if __name__=="__main__": main()
