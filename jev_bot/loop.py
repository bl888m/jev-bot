"""The cycle: state -> JEV -> risk -> execution, once per market.

    for each market state:
        decision = jev.decide(state)      # BUY / SELL / HOLD / AVOID + prob
        gate     = risk.check(decision)   # may this execute?
        if gate is EXECUTE:
            book.execute(decision)        # paper

Returns one record per market so the renderer can show every decision and
the reason the gate did or did not let it through.
"""

from __future__ import annotations

from collections.abc import Iterable

from . import jev, risk
from .types import MarketState
from .execution.paper import Book


def run(states: Iterable[MarketState], book: Book, limits: risk.Limits,
        engine: str = "offline") -> list:
    records = []
    for st in states:
        decision = jev.decide(st, engine=engine)
        gate = risk.check(decision, book.open_positions(), limits)
        if gate.verdict == "EXECUTE":
            book.execute(decision, st.price)
        records.append((st, decision, gate))
    return records
