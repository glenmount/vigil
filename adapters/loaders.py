from __future__ import annotations
import csv, pathlib, datetime
from typing import List, Dict

ISO = "%Y-%m-%dT%H:%M"

def read_csv(path: pathlib.Path) -> List[Dict[str,str]]:
    with path.open("r", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def parse_dt(s: str) -> datetime.datetime:
    try:
        return datetime.datetime.fromisoformat(s)
    except ValueError:
        return datetime.datetime.strptime(s, ISO)

def load_bundle(root: pathlib.Path) -> dict:
    return {
        "roster": read_csv(root/"roster.csv"),
        "timeclock": read_csv(root/"timeclock.csv"),
        "bells": read_csv(root/"bells.csv") if (root/"bells.csv").exists() else [],
        "incidents": read_csv(root/"incidents.csv") if (root/"incidents.csv").exists() else [],
    }
