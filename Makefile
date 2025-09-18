# ---------- Config ----------
# Default bundle (can override: VIGIL_BUNDLE=qa/sandbox/hover_handover make all)
VIGIL_BUNDLE ?= qa/goldens/fixtures
PY := PYTHONPATH=.

# ---------- Core build (label → nudge → report → digest → scoreboard) ----------
policy-index:
	@$(PY) python -m engine.policy_index

label:
	@VIGIL_BUNDLE=$(VIGIL_BUNDLE) $(PY) python -m cli.label

nudge:
	@VIGIL_BUNDLE=$(VIGIL_BUNDLE) $(PY) python -m cli.nudge

report:
	@VIGIL_BUNDLE=$(VIGIL_BUNDLE) $(PY) python -m cli.report

digest:
	@VIGIL_BUNDLE=$(VIGIL_BUNDLE) $(PY) python -m cli.digest

scoreboard:
	@VIGIL_BUNDLE=$(VIGIL_BUNDLE) $(PY) python -m cli.scoreboard

all: policy-index label nudge report digest scoreboard
	@echo "[all] built with VIGIL_BUNDLE=$(VIGIL_BUNDLE)"

# ---------- Preflight & Postprocess ----------
preflight:
	@echo "[preflight] bundle=$(VIGIL_BUNDLE)"
	@python scripts/preflight.py --bundle $(VIGIL_BUNDLE) --json web/preflight_summary.json

report-explain:
	@python scripts/postprocess_report.py

# ---------- Deterministic publishers (viewer helpers; local only) ----------
emit-opportunities:
	@python scripts/emit_opportunities.py

# Prefer CSV-derived actions (handover windows) if present; fall back to labels-based script
# Copy local artifacts for drill-down (never published on Pages)
pilot-copy:
	@mkdir -p web/receipts
	@cp -f receipts/labels.json web/receipts/labels.json 2>/dev/null || true
	@[ -f receipts/events.jsonl ] && cp -f receipts/events.jsonl web/receipts.jsonl || true

# ---------- One-shot local pilot run ----------
pilot-day: preflight all report-explain emit-opportunities pilot-copy
	@echo "[pilot-day] Done. Serve locally with: python -m http.server -d web 8082"

.PHONY: policy-index label nudge report digest scoreboard all preflight report-explain emit-opportunities emit-actions pilot-copy pilot-day

sandbox-small:
	@python scripts/gen_sandbox.py --name small2u --units 2 --days 1 --seed 7 --breaches "Unit A:1,Unit B:0"
	@VIGIL_BUNDLE=qa/sandbox/small2u $(MAKE) pilot-day
	@echo "[sandbox-small] serve: python -m http.server -d web 8082"

sandbox-week:
	@python scripts/gen_sandbox.py --name week3u --units 3 --days 7 --seed 13 --breaches "Unit A:3,Unit C:1"
	@VIGIL_BUNDLE=qa/sandbox/week3u $(MAKE) pilot-day
	@echo "[sandbox-week] serve: python -m http.server -d web 8082"

sandbox-no-units:
	@VIGIL_BUNDLE=qa/sandbox/no_units $(MAKE) pilot-day
	@echo "[sandbox-no-units] serve: python -m http.server -d web 8082"

monday-report:
	@python scripts/monday_report.py

sandbox-random-week:
	@python scripts/gen_sandbox.py --name randw --units 4 --days 7 --seed 99 --breaches "Unit A:4,Unit B:2,Unit C:1"
	@VIGIL_BUNDLE=qa/sandbox/randw $(MAKE) pilot-day
	@$(MAKE) monday-report
	@echo "[sandbox-random-week] serve: python -m http.server -d web 8082"

ci-check:
	@echo "[ci-check] preflight (fixtures)"
	@VIGIL_BUNDLE=qa/goldens/fixtures $(MAKE) preflight || true
	@echo "[ci-check] build (fixtures)"
	@VIGIL_BUNDLE=qa/goldens/fixtures $(MAKE) all
	@echo "[ci-check] pytest"
	@PYTHONPATH=. pytest -q

standards:
	@python scripts/check_standards.py

delta:
	@[ -f web/standards.json ] && cp -f web/standards.json web/standards.prev.json || true
	@python scripts/check_standards.py
	@python scripts/delta_intel.py

publish-gh-pages:
	@echo "[publish] build receipt-free site to gh-pages"
	@rm -f web/receipts.jsonl && rm -rf web/receipts 2>/dev/null || true
	@git fetch origin
	@{ git show-ref --verify --quiet refs/heads/gh-pages || git branch gh-pages origin/gh-pages 2>/dev/null || true; }
	@git worktree remove gh-pages 2>/dev/null || true
	@git worktree add gh-pages gh-pages
	@rsync -av --delete web/ gh-pages/
	@cd gh-pages && git add -A && git commit -m "publish: update static site" && git push origin gh-pages && cd ..
	@git worktree remove gh-pages

opps-from-labels:
	@python scripts/emit_windows_from_labels.py

pilot-day: preflight all report-explain opps-from-labels pilot-copy
	@echo "[pilot-day] Done."

sandbox-handover-fail:
	@mkdir -p qa/sandbox/handover_fail
	@cat > qa/sandbox/handover_fail/roster.csv <<\"CSV\"
staff_id,unit,role,shift_start,shift_end
A1,Unit A,carer,2025-09-14T07:00:00+00:00,2025-09-14T15:00:00+00:00
B1,Unit B,carer,2025-09-14T07:30:00+00:00,2025-09-14T15:30:00+00:00
C1,Unit C,carer,2025-09-14T08:00:00+00:00,2025-09-14T16:00:00+00:00
CSV
	@cat > qa/sandbox/handover_fail/timeclock.csv <<\"CSV\"
staff_id,clock_in,clock_out
A1,2025-09-14T06:55:00+00:00,2025-09-14T15:05:00+00:00
B1,2025-09-14T07:25:00+00:00,2025-09-14T15:35:00+00:00
C1,2025-09-14T07:55:00+00:00,2025-09-14T16:05:00+00:00
CSV
	@cat > qa/sandbox/handover_fail/bells.csv <<\"CSV\"
resident_id,started_at,response_secs
RC1,2025-09-14T08:02:00+00:00,90
RC2,2025-09-14T08:10:00+00:00,120
CSV
	@echo "resident_id,kind,occurred_at" > qa/sandbox/handover_fail/incidents.csv
	@VIGIL_BUNDLE=qa/sandbox/handover_fail $(MAKE) all standards delta
	@echo "[handover-fail] serve: python -m http.server -d web 8082"

# --- demo: force per-unit handover breaches in Unit C (should FAIL tolerance) ---
sandbox-handover-fail:
	@mkdir -p qa/sandbox/handover_fail
	@cat > qa/sandbox/handover_fail/roster.csv <<'CSV'
staff_id,unit,role,shift_start,shift_end
A1,Unit A,carer,2025-09-14T07:00:00+00:00,2025-09-14T15:00:00+00:00
B1,Unit B,carer,2025-09-14T07:30:00+00:00,2025-09-14T15:30:00+00:00
C1,Unit C,carer,2025-09-14T08:00:00+00:00,2025-09-14T16:00:00+00:00
CSV
	@cat > qa/sandbox/handover_fail/timeclock.csv <<'CSV'
staff_id,clock_in,clock_out
A1,2025-09-14T06:55:00+00:00,2025-09-14T15:05:00+00:00
B1,2025-09-14T07:25:00+00:00,2025-09-14T15:35:00+00:00
C1,2025-09-14T07:55:00+00:00,2025-09-14T16:05:00+00:00
CSV
	@cat > qa/sandbox/handover_fail/bells.csv <<'CSV'
resident_id,started_at,response_secs
RC1,2025-09-14T08:02:00+00:00,90
RC2,2025-09-14T08:10:00+00:00,120
CSV
	@echo "resident_id,kind,occurred_at" > qa/sandbox/handover_fail/incidents.csv
	@VIGIL_BUNDLE=qa/sandbox/handover_fail $(MAKE) all standards delta
	@echo "[handover-fail] serve: python -m http.server -d web 8082"
