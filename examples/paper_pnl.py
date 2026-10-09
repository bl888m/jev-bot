"""Open a paper book, move the prices, read the PnL.

    python examples/paper_pnl.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from jev_bot import markets
from jev_bot.execution.paper import Book
from jev_bot.loop import run
from jev_bot.risk import Limits

states = markets.generate(n=8, seed=7)
book = Book()
run(states, book, Limits())

print(f"open positions: {book.open_positions()}")
print(f"equity at entry: ${book.equity():,.2f}")

# pretend every symbol moved +2%
book.mark({s.symbol: s.price * 1.02 for s in states})
print(f"equity after +2%: ${book.equity():,.2f}  (open pnl ${book.open_pnl():,.2f})")
print("\nsimulated, paper only, not a result")
