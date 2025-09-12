.PHONY: label nudge report digest all
label: ; PYTHONPATH=. python -m cli.label
nudge: ; PYTHONPATH=. python -m cli.nudge
report: ; PYTHONPATH=. python -m cli.report
digest: ; PYTHONPATH=. python -m cli.digest
all: label nudge report digest
