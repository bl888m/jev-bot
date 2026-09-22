"""Paper execution. The Robinhood-shaped slot, with no Robinhood behind it.

The architecture is: JEV decides, a risk gate approves, an execution layer
places the order. This is that execution layer, in paper. It records fills
and marks them, and it holds no key, signs nothing, and reaches no exchange.

Going live means replacing this one file with an adapter that speaks to a
real venue (Robinhood's agentic-trading workflow supports equities, options
and crypto). That adapter is deliberately not in this repo. Paper is the
default and the only mode shipped.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..types import Decision


@dataclass
class Fill:
    symbol: str
    action: str
    entry: float
    size: float          # notional in USD (paper)
    price_now: float

    def pnl(self) -> float:
        if self.entry <= 0:
            return 0.0
        move = (self.price_now - self.entry) / self.entry
        # a SELL profits when price falls
        direction = 1 if self.action == "BUY" else -1
        return round(self.size * move * direction, 2)


@dataclass
class Book:
    cash: float = 10_000.0
    per_trade: float = 1_000.0    # fixed paper size per fill
    fills: list = field(default_factory=list)
    log: list = field(default_factory=list)

    def open_positions(self) -> int:
        return len(self.fills)

    def execute(self, decision: Decision, price: float) -> Fill:
        f = Fill(symbol=decision.symbol, action=decision.action,
                 entry=price, size=self.per_trade, price_now=price)
        self.fills.append(f)
        self.log.append(
            f"EXECUTE  {decision.action:4} {decision.symbol:5} "
            f"${self.per_trade:,.0f}  p={decision.probability:.0%} "
            f"conf={decision.confidence:.0%}  ({decision.source})"
        )
        return f

    def mark(self, prices: dict) -> None:
        for f in self.fills:
            if f.symbol in prices:
                f.price_now = prices[f.symbol]

    def open_pnl(self) -> float:
        return round(sum(f.pnl() for f in self.fills), 2)

    def equity(self) -> float:
        return round(self.cash + self.open_pnl(), 2)
