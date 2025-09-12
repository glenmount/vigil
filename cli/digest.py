import json, datetime, pathlib
pathlib.Path("ledger").mkdir(exist_ok=True)
digest = {"generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()}
pathlib.Path(f"ledger/digest-{datetime.date.today().isoformat()}.json").write_text(
  json.dumps(digest), encoding="utf-8"
)
print("wrote ledger/digest-*.json")
