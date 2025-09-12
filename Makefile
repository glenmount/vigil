.PHONY: index label nudge report digest all clean bundles

PY := PYTHONPATH=.

index: ; $(PY) python -m engine.policy_index
label: ; $(PY) python -m cli.label
nudge: ; $(PY) python -m cli.nudge
report: ; $(PY) python -m cli.report
digest: ; $(PY) python -m cli.digest

all: index label nudge report digest

bundles:
	@$(PY) python qa/run_all.py

clean:
	@rm -f receipts/events.jsonl web/queue.json web/report.json ledger/digest-*.json policies/index.json
