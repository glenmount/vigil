#!/usr/bin/env python3
import argparse, csv, re, sys, json
from pathlib import Path

REQS = {
    "roster": ["staff_id", "unit", "role", "shift_start", "shift_end"],
    "timeclock": ["staff_id", "clock_in", "clock_out"],
    "bells": ["resident_id", "started_at", "response_secs"],
    "incidents": ["resident_id", "kind", "occurred_at"],
}

# Very light PII-ish patterns (names/emails/phones). We keep this conservative.
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"\b(?:\+?\d[\s-]?){7,}\b")
NAMEY_RE = re.compile(r"\b([A-Z][a-z]{2,}\s+[A-Z][a-z]{2,})\b")  # "Jane Smith" (basic)

def die(msg):
    print(f"[preflight] ERROR: {msg}", file=sys.stderr)
    sys.exit(1)

def check_headers(path: Path, required_cols):
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            die(f"{path} is empty")
    missing = [c for c in required_cols if c not in header]
    return header, missing

def scan_pii(path: Path, header, max_rows=5000):
    hits = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i > max_rows:  # guard for huge files
                break
            for k, v in row.items():
                if not v:
                    continue
                s = str(v)
                if EMAIL_RE.search(s) or PHONE_RE.search(s) or NAMEY_RE.search(s):
                    hits.append({"row": i+2, "col": k, "sample": s[:80]})
                    if len(hits) >= 25:  # don't flood
                        return hits
    return hits

def load_bad_days(path: Path):
    if not path.exists():
        return []
    days = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            days.append(r)
    return days

def main():
    p = argparse.ArgumentParser(description="Preflight CSV contracts + PII scan + bad-day annotations")
    p.add_argument("--bundle", default="qa/sandbox/wingA", help="Folder containing CSVs")
    p.add_argument("--bad-days", default="qa/sandbox/bad_day_annotations.csv", help="Optional annotations CSV")
    p.add_argument("--json", default="", help="Optional: write a JSON summary here")
    args = p.parse_args()

    base = Path(args.bundle)
    if not base.exists():
        die(f"Bundle folder not found: {base}")

    report = {"bundle": str(base), "files": [], "bad_day_annotations": []}

    for kind, required in REQS.items():
        path = base / f"{kind}.csv"
        if not path.exists():
            die(f"Missing required file: {path}")
        header, missing = check_headers(path, required)
        if missing:
            die(f"{path} missing columns: {', '.join(missing)}")
        pii = scan_pii(path, header)
        report["files"].append({
            "kind": kind, "path": str(path), "missing": missing, "pii_hits": pii[:5], "pii_count": len(pii)
        })
        if pii:
            die(f"PII-like content found in {path}. Redact upstream or map IDs (e.g., replace names with staff_id). (e.g., row {pii[0]['row']} col {pii[0]['col']}). Redact upstream or map IDs.")

    # Optional: bad-day annotations
    bad = load_bad_days(Path(args.bad_days))
    report["bad_day_annotations"] = bad
    print(f"[preflight] OK: headers valid; no PII-like content; bad_day_annotations={len(bad)}")

    if args.json:
        Path(args.json).write_text(json.dumps(report, indent=2), encoding="utf-8")

if __name__ == "__main__":
    main()
