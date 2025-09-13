import json, pathlib
from engine.clock import today_iso_date
from engine.metrics import dm_percent_v0

def main():
    labels = json.loads(pathlib.Path("receipts/labels.json").read_text(encoding="utf-8"))
    dm = dm_percent_v0(labels)
    report = {
      "week_of": today_iso_date(),
      "dm_percent": dm,
      "calls_over_8m":  1 if (isinstance(labels.get("bells_p95"), (int,float)) and labels["bells_p95"]>480) else 0,
      "interruptions_per_hr": labels.get("interruptions_per_hr", 0.0),
      "charting_minutes": 0.0,
      "fixes": [
        {"title":"Protect 15-min breaks","cost_estimate":0.0,"owner":"unit_manager"},
        {"title":"Offload charting 20m","cost_estimate":0.0,"owner":"assistant"}
      ]
    }
    pathlib.Path("web/report.json").write_text(
        json.dumps(report, sort_keys=True, separators=(",",":")),
        encoding="utf-8"
    )
    print("report generated")

if __name__=="__main__": main()
