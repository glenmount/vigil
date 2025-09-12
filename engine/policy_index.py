from __future__ import annotations
import hashlib, json, pathlib
def _sha256(p: pathlib.Path) -> str: return hashlib.sha256(p.read_bytes()).hexdigest()
def build_index():
    root = pathlib.Path("policies"); entries=[]
    for p in sorted(root.glob("*")):
        if p.is_file() and p.suffix.lower() in (".pdf",".html",".htm"):
            entries.append({"path": p.as_posix(), "name": p.name, "sha256": _sha256(p)})
    (root/"index.json").write_text(json.dumps({"version":"v1","entries":entries}, separators=(",",":")), encoding="utf-8")
    print(f"indexed {len(entries)} policy docs")
if __name__=="__main__": build_index()
