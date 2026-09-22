"""Where a market state comes from.

The default is an offline generator so the loop runs with no keys and is
reproducible: same seed, same states. It spans the asset classes JEV would
see through a Robinhood agentic-trading workflow, stocks, crypto and meme
stocks, so the decision layer is exercised across all of them.

Real feeds (a quotes API, an on-chain price, a news score) plug in here,
behind the same MarketState shape the rest of the loop consumes. They are
left as clearly marked stubs, the same way the live decision engine is: the
harness runs today, and each feed is a small adapter you add when you have
the key.
"""

from __future__ import annotations

import random

from .types import MarketState

_UNIVERSE = [
    ("HOOD", "stock"), ("NVDA", "stock"), ("AAPL", "stock"), ("TSLA", "stock"),
    ("BTC", "crypto"), ("ETH", "crypto"), ("SOL", "crypto"),
    ("GME", "meme"), ("AMC", "meme"), ("DOGE", "meme"),
]

_REGIMES = ["bullish", "neutral", "bearish"]


def generate(n: int = 8, seed: int = 7) -> list[MarketState]:
    rng = random.Random(seed)
    picks = rng.sample(_UNIVERSE, min(n, len(_UNIVERSE)))
    out: list[MarketState] = []
    for sym, cls in picks:
        base = {"stock": 150, "crypto": 2000, "meme": 12}[cls]
        price = round(base * rng.uniform(0.4, 2.4), 2)
        change = round(rng.gauss(0.01, 0.05), 4)
        out.append(MarketState(
            symbol=sym,
            asset_class=cls,
            price=price,
            change_24h=change,
            volume_delta=round(rng.gauss(0.2, 0.6), 3),
            momentum=round(max(-1, min(1, rng.gauss(change * 6, 0.4))), 3),
            news=round(max(-1, min(1, rng.gauss(0.1, 0.5))), 3),
            regime=rng.choices(_REGIMES, weights=[0.4, 0.35, 0.25])[0],
        ))
    return out


# --- live feed adapters (stubs) --------------------------------------------
# Each returns MarketState objects for its asset class. They are intentionally
# not implemented: point them at the quotes source you have access to, keep
# the MarketState shape, and the decision loop works unchanged.

def from_stocks(symbols):     # e.g. a quotes API
    raise NotImplementedError("wire a live quotes source, then map to MarketState")


def from_crypto(symbols):     # e.g. an exchange or on-chain price
    raise NotImplementedError("wire a live crypto source, then map to MarketState")
