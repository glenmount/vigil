import json, datetime, pathlib
pathlib.Path("web").mkdir(exist_ok=True)
queue = {
  "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
  "items": []
}
pathlib.Path("web/queue.json").write_text(json.dumps(queue), encoding="utf-8")
print("wrote web/queue.json")
