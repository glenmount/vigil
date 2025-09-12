from __future__ import annotations
import json, pathlib

INDEX_PATH = pathlib.Path("policies/index.json")
MAP_PATH   = pathlib.Path("policies/citations.json")

def _load(path: pathlib.Path, fallback):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else fallback

def cite(kind: str):
    idx = _load(INDEX_PATH, {"entries": []})
    mapping = _load(MAP_PATH, {})
    rules = (mapping.get(kind) or [])[:2]
    out = []
    for rule in rules:
        match = rule.get("match", "")
        ent = next((e for e in idx["entries"]
                    if match in e.get("name", "") or match in e.get("path", "")), None)
        if ent:
            out.append({"doc_id": ent["path"], "sha256": ent["sha256"], "page": int(rule.get("page", 1))})
    return out[:2]
