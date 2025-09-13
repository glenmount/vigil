import os, json, hashlib, pathlib, subprocess, shutil, datetime

ROOT = pathlib.Path(__file__).resolve().parents[1]
BUNDLES = [p for p in (ROOT/"qa/goldens").iterdir() if p.is_dir() and p.name.startswith("fixtures")]
WEB = ROOT/"web"; DEST = WEB/"bundles"; DEST.mkdir(parents=True, exist_ok=True)

def sha(p: pathlib.Path): return hashlib.sha256(p.read_bytes()).hexdigest()

def run_bundle(bdir: pathlib.Path):
    env = os.environ.copy(); env["VIGIL_BUNDLE"] = str(bdir)
    subprocess.check_call(["make","all"], cwd=ROOT, env=env)
    # copy artifacts to bundle folder
    out = DEST/bdir.name; out.mkdir(parents=True, exist_ok=True)
    for fn in ["queue.json","report.json"]: shutil.copy2(WEB/fn, out/fn)
    # snapshot receipt hash only (not full file to avoid duplication)
    rpath = ROOT/"receipts"/"events.jsonl"
    return {"bundle": bdir.name,
            "generated_at": datetime.datetime.utcnow().isoformat()+"Z",
            "hashes": {
              "queue.json": sha(WEB/"queue.json"),
              "report.json": sha(WEB/"report.json"),
              "receipts.jsonl": sha(rpath) if rpath.exists() else None
            }}

def main():
    results = [run_bundle(b) for b in sorted(BUNDLES)]
    (WEB/"bundles.json").write_text(json.dumps({"results":results}, indent=2), encoding="utf-8")
    print(json.dumps({"processed": [r["bundle"] for r in results]}, indent=2))

if __name__ == "__main__": main()
