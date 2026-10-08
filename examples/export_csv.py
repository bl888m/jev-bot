"""Write every decision, and the gate's verdict on it, to decisions.csv.

    python examples/export_csv.py
"""
import csv
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from jev_bot import markets
from jev_bot.execution.paper import Book
from jev_bot.loop import run
from jev_bot.risk import Limits

records = run(markets.generate(n=10, seed=7), Book(), Limits())

with open("decisions.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["symbol", "asset_class", "action", "probability",
                "confidence", "engine", "verdict", "reason"])
    for st, d, gate in records:
        w.writerow([st.symbol, st.asset_class, d.action,
                    f"{d.probability:.2f}", f"{d.confidence:.2f}",
                    d.source, gate.verdict, gate.reason])

print(f"wrote decisions.csv ({len(records)} rows)")
