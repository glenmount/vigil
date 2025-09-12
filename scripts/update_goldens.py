#!/usr/bin/env python3
from __future__ import annotations
import os, subprocess, json
from pathlib import Path as P
from qa.canon import compute_hashes

BUNDLES = [
    P("qa/goldens/fixtures"),
    P("qa/goldens/fixtures_b"),
    P("qa/goldens/fixtures_c"),
]

def run(bundle: P):
    env = os.environ.copy()
    env["VIGIL_BUNDLE"] = str(bundle)
    subprocess.check_call(["make","all"], env=env)
    hs = compute_hashes()
    out = bundle / "hashes.json"
    out.write_text(json.dumps(hs, sort_keys=True, separators=(",",":")), encoding="utf-8")
    print(f"wrote {out}")

def main():
    for b in BUNDLES:
        assert b.exists(), f"missing bundle dir: {b}"
        run(b)

if __name__ == "__main__":
    main()
