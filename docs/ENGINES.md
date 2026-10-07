# Engines

jev-bot has two decision engines behind one function, decide(state, engine).
Both return the same Decision object. The source field says which one ran.

## offline (default)

A small scoring function in jev_bot/jev.py. No key, no network, and the same
input always gives the same output.

It adds up five readable contributions:

    momentum   0.9 x momentum
    trend      4.0 x the 24h change
    volume     0.4 x volume delta, clamped between -1 and 1
    news       0.5 x news score
    regime     +0.25 bullish, 0 neutral, -0.25 bearish

The sum is the net score, and its size is the strength.

    strength below 0.15   HOLD
    net above 0           BUY
    net below 0           SELL for stocks and crypto, AVOID for memes

Probability and confidence are smooth functions of strength, capped at 97%. A
stronger signal gives higher numbers, and a HOLD stays near 50%.

Every contribution is stored on the decision in its reasons field, so you can
see exactly what moved it.

## jev (the real model)

Used with --engine jev and TYPESAFE_API_KEY set. It describes the state in one
sentence, asks one question with four options (BUY, SELL, HOLD, AVOID), and
reads back the chosen option with its probability and confidence. If the answer
is not one of the four, the engine falls back to HOLD.

Settings come from the environment:

    TYPESAFE_API_KEY    required
    TYPESAFE_API_BASE   optional, defaults to https://api.typesafe.ai/v1/decide

JEV is in gated early access. The request and response shapes in jev.py follow
the expected format, and if the API you get access to differs, the _jev()
function is the one place to change.

## Why two

The offline engine lets anyone run and test the whole loop without access. The
real engine is the point of the project. Keeping both behind one shape means
the gate, the book and the renderer never need to know which one ran.
