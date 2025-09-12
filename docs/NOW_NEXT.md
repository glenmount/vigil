# NOW / NEXT — Vigil (living)
Updated: 12 Sep 2025 (AEST)

## NOW (this sprint, 4 days)
- [ ] Freeze CSV contracts + fixtures (14d): `adapters/contracts.md`, `qa/goldens/fixtures/*`.
- [ ] Implement Label → Nudge → Audit:
      - labels: `doubles_10d`, `hours_14d`, `overtime_7d`, `bells_p95`, `interruptions_per_hr`.
      - receipts: append JSONL lines with sha256 over {inputs, thresholds, index_version}.
- [ ] Policy thresholds + action ladders:
      - `engine/policy.json` (traffic-light thresholds).
      - `playbooks/{breaks.yaml,doubles.yaml,recovery.yaml}`.
- [ ] Minimal viewer: `web/index.html` rendering `web/queue.json`, `web/report.json`, link receipts.
- [ ] CI rails: block outbound network; determinism + fairness tests.
- [ ] Publish first `ledger/digest-YYYY-MM-DD.json` and baseline scoreboard.

**Acceptance (must be green):**
- Determinism: clean checkout → `make all` twice → identical hashes.
- Fairness: equal-risk cohorts gap < 1.0 pp (freeze if violated).
- 3-Guarantee: non-empty Live Queue; Stress Report with 2 costed fixes; each nudge has ≤2 citations.

## NEXT (7–14 days)
- [ ] DM% calc + Stress Report HTML template.
- [ ] Policy Indexer: hash + page anchors for citations (`policies/*`).
- [ ] Family Receipts (opt-in): non-PII weekly digest snapshot.
- [ ] Expand fixtures to 3 bundles; tighten schema validation.
- [ ] Scoreboard page: DM%, calls>8m, interruptions/hr, charting minutes, nudge completion/time-to-act.

**Targets:** calls>8m −25%; interruptions/hr −30%; charting minutes −40–60% on a pilot wing.
