import json, pathlib, subprocess, os

def action_gap_pp(items):
    if not items: return 0.0
    a = [it for i,it in enumerate(items) if i%2==0]
    b = [it for i,it in enumerate(items) if i%2==1]
    total = max(1, len(a)+len(b))
    return abs(len(a)/total - len(b)/total) * 100.0

def build_for_bundle(bundle):
    env = os.environ.copy(); env["VIGIL_BUNDLE"] = str(bundle)
    subprocess.check_call(["make","all"], env=env)

def test_equal_risk_equal_action_across_bundles():
    root = pathlib.Path(".").resolve()
    for b in sorted((root/"qa/goldens").iterdir()):
        if not b.is_dir() or not b.name.startswith("fixtures"): continue
        build_for_bundle(b)
        q = json.loads((root/"web"/"queue.json").read_text(encoding="utf-8"))
        gap = action_gap_pp(q.get("items",[]))
        assert gap < 1.0, f"{b.name}: equal-risk action gap {gap:.2f}pp >= 1.0pp (freeze)"
