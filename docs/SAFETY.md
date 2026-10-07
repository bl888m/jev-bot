# Safety

What jev-bot can and cannot do.

## What it cannot do

- It holds no wallet and no exchange keys.
- It places no orders. The execution layer is a paper book.
- There is no live flag. Going live is code you would write yourself.

## What it does

- Generates simulated market states offline.
- Asks an engine for a decision on each one.
- Passes every decision through the gate.
- Records approved decisions as paper fills.

## What leaves your machine

- With the default offline engine: nothing.
- With --engine jev: a one sentence description of each state (symbol, asset
  class, price, 24h change, volume, momentum, news, regime) goes to the
  TypeSafe API under your own key. With the built in generator that data is
  simulated.

There is no telemetry and no analytics.

## Keys

The only secret jev-bot reads is TYPESAFE_API_KEY, and only with --engine jev.
Keep it in your shell environment or a local .env file, and never commit it.

## Not advice

All data is simulated and all results are paper. Nothing here is financial
advice or a claim of returns.
