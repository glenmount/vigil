from __future__ import annotations
def cite(kind: str):
    table = {
        "breaks": [{"doc_id":"policies/breaks.pdf","page":3}],
        "doubles": [{"doc_id":"policies/rostering.pdf","page":5}],
        "bells": [{"doc_id":"policies/call-bells.pdf","page":2}],
    }
    return table.get(kind, [])[:2]
