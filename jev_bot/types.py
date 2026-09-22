"""Typed shapes. State in, a decision out.

The whole project is built around one idea: a market state goes in, and a
typed decision with a calibrated probability comes out. These two
dataclasses are that contract. Nothing downstream re-parses text; every
stage reads typed fields.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

ACTIONS = ("BUY", "SELL", "HOLD", "AVOID")


@dataclass
class MarketState:
    """One snapshot of a market, the input JEV evaluates."""

    symbol: str
    asset_class: str          # "stock", "crypto", "meme", "option"
    price: float
    change_24h: float         # fraction, e.g. +0.048 for +4.8%
    volume_delta: float       # fraction vs its own average
    momentum: float           # -1..1
    news: float               # -1..1 sentiment
    regime: str               # "bullish", "neutral", "bearish"


@dataclass
class Decision:
    """What JEV returned for a state: a typed action and two numbers.

    `source` is "jev" when the real model produced it and "offline" when the
    deterministic local engine did. It is never hidden: the desk labels
    which one made the call, the same way it labels live vs simulated data.
    """

    symbol: str
    action: str               # one of ACTIONS
    probability: float        # calibrated P(action is right), 0..1
    confidence: float         # how sure JEV is it should act at all, 0..1
    source: str = "offline"   # "jev" or "offline"
    reasons: dict = field(default_factory=dict)   # feature -> signed weight
