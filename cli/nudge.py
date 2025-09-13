import json, pathlib
from engine.nudge import nudge_from_labels
from engine.clock import now_iso

def main():
    labels = json.loads(pathlib.Path("receipts/labels.json").read_text(encoding="utf-8"))
    items = nudge_from_labels(labels)
    # determinism: sort each receipts array and the items list
    for it in items:
        it["receipts"] = sorted(it.get("receipts", []))
    items = sorted(items, key=lambda x: (x.get("id",""), x.get("title","")))
    out = {"generated_at": now_iso(), "items": items[:10]}
    pathlib.Path("web/queue.json").write_text(
        json.dumps(out, sort_keys=True, separators=(",",":")),
        encoding="utf-8"
    )
    print("queue generated")

if __name__=="__main__": main()
