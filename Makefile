.PHONY: label nudge report digest all
label: ; PYTHONPATH=. python -m cli.label
nudge: ; PYTHONPATH=. python -m cli.nudge
report: ; PYTHONPATH=. python -m cli.report
index: ; PYTHONPATH=. python -m engine.policy_index
digest: ; PYTHONPATH=. python -m cli.digest
all: index label nudge report digest
