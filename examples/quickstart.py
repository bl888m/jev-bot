"""Run JEV as a library in a few lines (paper only).

    python examples/quickstart.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from jev_bot import markets
from jev_bot.execution.paper import Book
from jev_bot.loop import run
from jev_bot.risk import Limits

states = markets.generate(n=8, seed=7)
records = run(states, Book(), Limits())

executed = [(st, d) for st, d, gate in records if gate.verdict == "EXECUTE"]
print(f"{len(executed)} executed of {len(records)} decided\n")
for st, d in executed:
    print(f"  {d.action:<4}  {st.symbol:<5}  p={d.probability:.0%}  conf={d.confidence:.0%}")
