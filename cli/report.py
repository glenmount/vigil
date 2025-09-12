import json, datetime, pathlib
pathlib.Path("web").mkdir(exist_ok=True)
report = {
  "week_of": datetime.date.today().isoformat(),
  "dm_percent": 0.0,
  "calls_over_8m": 0,
  "interruptions_per_hr": 0.0,
  "charting_minutes": 0.0,
  "fixes": []
}
pathlib.Path("web/report.json").write_text(json.dumps(report), encoding="utf-8")
print("wrote web/report.json")
