"""Count why the gate skipped decisions, grouped by rule.

    python examples/skip_reasons.py
"""
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from jev_bot import markets
from jev_bot.execution.paper import Book
from jev_bot.loop import run
from jev_bot.risk import Limits


def rule(reason):
    if "does not execute" in reason:
        return "HOLD / AVOID never executes"
    if reason.startswith("confidence"):
        return "below the confidence floor"
    if reason.startswith("probability"):
        return "below the probability floor"
    return "position cap reached"


records = run(markets.generate(n=10, seed=7), Book(), Limits())
skipped = Counter(rule(g.reason) for _, _, g in records if g.verdict == "SKIP")

print(f"{sum(skipped.values())} skipped of {len(records)}\n")
for name, n in skipped.most_common():
    print(f"  {n}x  {name}")
