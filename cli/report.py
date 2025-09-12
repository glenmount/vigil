import json, pathlib, datetime
def main():
    labels = json.loads(pathlib.Path("receipts/labels.json").read_text(encoding="utf-8"))
    report = {
      "week_of": datetime.date.today().isoformat(),
      "dm_percent": 0.0,
      "calls_over_8m":  1 if (isinstance(labels["bells_p95"], (int,float)) and labels["bells_p95"]>480) else 0,
      "interruptions_per_hr": labels["interruptions_per_hr"],
      "charting_minutes": 0.0,
      "fixes": [
        {"title":"Protect 15-min breaks","cost_estimate":0.0,"owner":"unit_manager"},
        {"title":"Offload charting 20m","cost_estimate":0.0,"owner":"assistant"}
      ]
    }
    pathlib.Path("web/report.json").write_text(json.dumps(report), encoding="utf-8")
    print("report generated")

if __name__=="__main__": main()
