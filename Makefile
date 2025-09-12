.PHONY: label nudge report digest all
label: ; python -m cli.label
nudge: ; python -m cli.nudge
report: ; python -m cli.report
digest: ; python -m cli.digest
all: label nudge report digest
