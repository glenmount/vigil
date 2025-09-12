from __future__ import annotations
import json, os, subprocess
from pathlib import Path as P
from qa.canon import compute_hashes

def test_golden_hashes_match_bundle():
    # Which bundle are we testing?
    bundle = P(os.environ.get("VIGIL_BUNDLE", "qa/goldens/fixtures"))
    # Build with that bundle to refresh outputs
    env = os.environ.copy()
    env["VIGIL_BUNDLE"] = str(bundle)
    subprocess.check_call(["make","all"], env=env)

    # Compute canonical hashes of current outputs
    current = compute_hashes()

    # Load goldens
    golden_path = bundle / "hashes.json"
    assert golden_path.exists(), f"goldens missing for {bundle}: run scripts/update_goldens.py"
    golden = json.loads(golden_path.read_text(encoding="utf-8"))

    # Allow explicit bump via env (local only; CI should NOT set this)
    if os.environ.get("VIGIL_BUMP_GOLDENS") == "1":
        golden_path.write_text(json.dumps(current, sort_keys=True, separators=(",",":")), encoding="utf-8")
        print(f"[bumped] {golden_path}")
        return

    assert current == golden, f"canonical outputs changed for {bundle.name}\ncurrent={current}\ngolden={golden}"
