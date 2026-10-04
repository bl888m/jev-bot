# Architecture

How a market state moves through jev-bot, and where each piece lives. The whole
path is a few hundred lines. This is the map.

## The flow

    markets  ->  JEV  ->  gate  ->  paper book
    state       decide    check     execute

1. A source yields MarketState objects (symbol, price, 24h change, volume,
   momentum, news, regime).
2. JEV turns a state into a Decision: BUY, SELL, HOLD or AVOID, plus a
   probability and a confidence.
3. The gate approves or refuses the decision and names the binding rule.
4. The paper book records approved decisions as fills. No money moves.

## Where things live

- jev_bot/types.py       the two typed shapes: MarketState and Decision
- jev_bot/markets.py     the offline generator, plus stubs for live feeds
- jev_bot/jev.py         the decision engine, offline or the real TypeSafe API
- jev_bot/risk.py        the gate: confidence, probability, action, exposure
- jev_bot/execution/     the paper book (the slot where an adapter would go)
- jev_bot/loop.py        wires the four stages together, one pass per market
- jev_bot/render.py      terminal tables and the single-decision card
- jev_bot/cli.py         the commands: decisions, run, card

## Two engines, one shape

Both engines return the same Decision object. The only difference is the
source field: "offline" for the local scoring function, "jev" for the real
model. Nothing downstream can tell them apart except by reading that field,
which is the point. Every decision is labelled by what made it.

## The gate defaults

- confidence below 70% is refused
- probability below 60% is refused
- HOLD and AVOID never execute
- more than 5 open positions is refused

## Design constraints

- Standard library only. Zero runtime dependencies.
- No wallet, no signing, no live flag. Paper is the only mode shipped.
- The model decides. The gate decides whether the decision may act. Those are
  two jobs in two files, on purpose.
