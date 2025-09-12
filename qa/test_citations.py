import json, os, pathlib, subprocess

FILES_TO_RESET = [
    "receipts/events.jsonl",
    "web/queue.json",
    "web/report.json",
]

def test_nudges_have_citations_when_present():
    # Reset any stale artifacts from pre-index runs
    for fp in FILES_TO_RESET:
        pathlib.Path(fp).unlink(missing_ok=True)

    # Rebuild (ensures policy index exists and receipts are fresh)
    env = os.environ.copy()
    subprocess.check_call(["make", "all"], env=env)

    p = pathlib.Path("receipts/events.jsonl")
    events = []
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                events.append(json.loads(line))

    nudges = [e for e in events if e.get("kind") == "nudge"]
    for n in nudges:
        cits = n.get("citations", [])
        assert len(cits) <= 2, f"too many citations: {len(cits)}"
        for c in cits:
            assert isinstance(c, dict) and all(k in c for k in ("doc_id","sha256","page")), f"bad citation: {c}"
