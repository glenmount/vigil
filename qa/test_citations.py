import json, pathlib, subprocess, os

def test_nudges_have_citations_when_present():
    # rebuild (ensures policy index exists)
    env = os.environ.copy()
    subprocess.check_call(["make","all"], env=env)
    events = []
    p = pathlib.Path("receipts/events.jsonl")
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            events.append(json.loads(line))
    nudges = [e for e in events if e.get("kind") == "nudge"]
    for n in nudges:
        cits = n.get("citations", [])
        assert all(("doc_id" in c and "sha256" in c and "page" in c) for c in cits), f"bad citation structure: {cits}"
        assert 0 <= len(cits) <= 2, f"too many citations: {len(cits)}"
