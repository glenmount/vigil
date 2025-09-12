import json, datetime, hashlib, pathlib
p = pathlib.Path("receipts"); p.mkdir(exist_ok=True)
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
evt = {
  "observed_at": now,
  "kind":"label",
  "inputs":{"fixture":"stub"},
  "thresholds":{},
  "sha256":"stub"
}
(line:=json.dumps(evt, ensure_ascii=False))
pathlib.Path("receipts/events.jsonl").write_text(line+"\n", encoding="utf-8")
print("wrote receipts/events.jsonl")
