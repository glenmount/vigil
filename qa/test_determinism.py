import hashlib, subprocess, pathlib, time
FILES = ["receipts/events.jsonl","web/queue.json","web/report.json"]
def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def test_deterministic_build():
    for p in FILES: pathlib.Path(p).unlink(missing_ok=True)
    subprocess.check_call(["make","all"])
    h1 = {p: sha(p) for p in FILES}
    time.sleep(0.2)
    subprocess.check_call(["make","all"])
    h2 = {p: sha(p) for p in FILES}
    assert h1 == h2, f"hash drift: {h1} vs {h2}"
