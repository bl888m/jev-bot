"""Same decisions, different gates: how the risk limits change what executes.

    python examples/custom_gate.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from jev_bot import markets
from jev_bot.execution.paper import Book
from jev_bot.loop import run
from jev_bot.risk import Limits

variants = {
    "loose    (conf >= 50%)": Limits(min_confidence=0.50),
    "default  (conf >= 70%)": Limits(),
    "strict   (conf >= 90%)": Limits(min_confidence=0.90),
    "tight    (2 positions)": Limits(max_positions=2),
}

states = markets.generate(n=10, seed=3)
for name, limits in variants.items():
    records = run(states, Book(), limits)
    n = sum(1 for _, _, g in records if g.verdict == "EXECUTE")
    print(f"{name:<24} -> {n} executed of {len(records)}")
