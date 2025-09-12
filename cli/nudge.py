import json, pathlib, datetime
from engine.nudge import nudge_from_labels

def main():
    labels = json.loads(pathlib.Path("receipts/labels.json").read_text(encoding="utf-8"))
    items = nudge_from_labels(labels)
    out = {"generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(), "items": items[:10]}
    pathlib.Path("web/queue.json").write_text(json.dumps(out), encoding="utf-8")
    print("queue generated")

if __name__=="__main__": main()
