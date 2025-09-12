.PHONY: label nudge report digest all
label: ; PYTHONPATH=. python -m cli.label
nudge: ; PYTHONPATH=. python -m cli.nudge
report: ; PYTHONPATH=. python -m cli.report
index: ; PYTHONPATH=. python -m engine.policy_index
index: ; PYTHONPATH=. python -m engine.policy_index
digest: ; PYTHONPATH=. python -m cli.digest
all: index label nudge report digest

bundles:
	@PYTHONPATH=. python qa/run_all.py

bump:
	@python scripts/bump_now_next.py --touch
