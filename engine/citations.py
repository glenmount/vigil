from __future__ import annotations
import json, pathlib
INDEX_PATH=pathlib.Path("policies/index.json")
MAP_PATH=pathlib.Path("policies/citations.json")
def _load(p, fb): return json.loads(p.read_text(encoding="utf-8")) if p.exists() else fb
def cite(kind: str):
    idx=_load(INDEX_PATH, {"entries":[]}); mapping=_load(MAP_PATH, {})
    rules=(mapping.get(kind) or [])[:2]; out=[]
    for r in rules:
        m=r.get("match","")
        ent=next((e for e in idx["entries"] if m in e.get("name","") or m in e.get("path","")), None)
        if ent: out.append({"doc_id":ent["path"], "sha256":ent["sha256"], "page":int(r.get("page",1))})
    return out[:2]
