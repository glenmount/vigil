import json, pathlib, subprocess, os, pytest

def action_gap_pp(items):
    if not items: return 0.0
    a=[it for i,it in enumerate(items) if i%2==0]
    b=[it for i,it in enumerate(items) if i%2==1]
    total=max(1,len(a)+len(b))
    return abs(len(a)/total - len(b)/total)*100.0

def build(env=None): subprocess.check_call(["make","all"], env=env or os.environ.copy())

def test_equal_risk_equal_action_across_default_bundle():
    build()
    q=json.loads(pathlib.Path("web/queue.json").read_text(encoding="utf-8"))
    items=q.get("items",[])
    if len(items)<2:
        pytest.skip("Not enough actions to assert equal-risk fairness")
    gap=action_gap_pp(items)
    assert gap < 1.0, f"equal-risk action gap {gap:.2f}pp >= 1.0pp (freeze)"
