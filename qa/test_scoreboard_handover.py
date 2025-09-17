import json, subprocess, os, pathlib
def test_scoreboard_has_handover_breaches():
    subprocess.check_call(["make","all"], env=os.environ.copy())
    sb = json.loads(pathlib.Path("web/scoreboard.json").read_text(encoding="utf-8"))
    assert "handover_breaches" in sb
    assert isinstance(sb["handover_breaches"], int)
