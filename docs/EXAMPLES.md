# Examples

Flags go before the command: python -m jev_bot [flags] decisions.

## One cycle over the default batch

    python -m jev_bot decisions

## A smaller batch with a fixed seed

    python -m jev_bot --seed 3 --n 5 decisions

Output:

      ASSET   CLASS    JEV      PROB   CONF   VERDICT
    ------------------------------------------------------------------
      TSLA    stock   SELL  dn   74%   70%   EXEC
      AMC     meme    AVOID x    92%   87%   skip · AVOID does not execute
      AAPL    stock   BUY   up   92%   88%   EXEC
      GME     meme    BUY   up   71%   68%   skip · confidence 68% < 70% floor
      BTC     crypto  BUY   up   76%   72%   EXEC

The same seed always gives the same batch and the same decisions.

## A stricter gate

    python -m jev_bot --min-confidence 0.9 decisions

With a 90% floor, decisions that cleared at 70% now skip, and the reason names
the new floor, for example: confidence 84% < 90% floor.

## Run the approved decisions on paper

    python -m jev_bot run

Prints the table, then the paper book: equity, open P&L and each fill.

## Unpack one decision

    python -m jev_bot card BTC

Shows the market state that went in, the decision that came out, and the gate
verdict.

## Use the real JEV model

    export TYPESAFE_API_KEY=your_key
    python -m jev_bot --engine jev decisions

Needs gated early access. Every decision is labelled jev instead of offline.

## With make

    make test
    make decisions
    make card SYM=ETH
