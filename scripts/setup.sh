#!/usr/bin/env bash
# One-shot dev setup for jev-bot. No dependencies to install, the core is
# standard library only; this just gets the CLI on PATH and runs the tests
# so you know the checkout is good.
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

echo "==> python version"
python3 --version

echo "==> installing jev-bot in editable mode"
pip install -e . --quiet

echo "==> running the test suite"
python3 tests.py

echo "==> try it:"
echo "    python -m jev_bot decisions"
echo "    python -m jev_bot card BTC"
