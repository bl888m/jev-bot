# jev-bot dev shortcuts. Run `make help` to list them.

.PHONY: help install test decisions run card clean

help:
	@echo "jev-bot — common tasks"
	@echo ""
	@echo "  make install     pip install -e . (editable, for the CLI on PATH)"
	@echo "  make test        run the offline test suite (17 checks, no network)"
	@echo "  make decisions   one cycle: state -> JEV -> risk, show the table"
	@echo "  make run         ... and execute the approved ones on paper"
	@echo "  make card SYM=BTC  unpack a single decision"
	@echo "  make clean       remove __pycache__ and build artifacts"

install:
	pip install -e .

test:
	python tests.py

decisions:
	python -m jev_bot decisions

run:
	python -m jev_bot run

card:
	python -m jev_bot card $(or $(SYM),BTC)

clean:
	find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true
	rm -rf *.egg-info build dist
