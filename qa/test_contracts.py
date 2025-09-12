import json, pathlib
from jsonschema import validate, Draft202012Validator

def _read(p): return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))
def _each_jsonl(p):
    for line in pathlib.Path(p).read_text(encoding="utf-8").splitlines():
        if line.strip(): yield json.loads(line)

def test_queue_schema():
    schema = _read("schemas/queue.json"); data = _read("web/queue.json")
    Draft202012Validator(schema).validate(data)

def test_report_schema():
    schema = _read("schemas/report.json"); data = _read("web/report.json")
    Draft202012Validator(schema).validate(data)

def test_events_schema():
    schema = _read("schemas/events.json")
    for obj in _each_jsonl("receipts/events.jsonl"):
        Draft202012Validator(schema).validate(obj)
