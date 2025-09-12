import json, pathlib, datetime, hashlib
def h(p): 
    pth = pathlib.Path(p)
    return hashlib.sha256(pth.read_bytes()).hexdigest() if pth.exists() else None

def main():
    d = {
      "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
      "hashes": {
        "receipts/events.jsonl": h("receipts/events.jsonl"),
        "web/queue.json": h("web/queue.json"),
        "web/report.json": h("web/report.json")
      }
    }
    pathlib.Path(f"ledger/digest-{datetime.date.today().isoformat()}.json").write_text(json.dumps(d), encoding="utf-8")
    print("digest written")

if __name__=="__main__": main()
