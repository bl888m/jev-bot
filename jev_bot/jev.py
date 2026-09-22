"""The decision. Two ways to make it, both honest about which one ran.

JEV is TypeSafe AI's System One model: you hand it a state and a typed
question with fixed options, and it returns one option with a calibrated
probability, in about a tenth of a second. This module wraps that into a
single call, `decide(state)`, and gives you two backends:

- offline (default): a small, transparent scoring function that turns the
  state features into an action, a probability and a confidence. It runs
  with no key and no network, and every decision is labelled source
  "offline" so it is never mistaken for the model.

- jev: the real TypeSafe API. Off unless you pass mode="jev" and set
  TYPESAFE_API_KEY. It sends the state and the four typed options and reads
  back the chosen action and its probability. Access is early-access and
  gated, so the endpoint and key come from the environment, not the code.

Either way the output is the same typed Decision. The rest of the loop
cannot tell which backend ran, except by reading `decision.source`.
"""

from __future__ import annotations

import json
import os
from urllib.request import urlopen, Request

from .types import MarketState, Decision, ACTIONS

# --- offline engine --------------------------------------------------------

def _score(state: MarketState) -> dict:
    """A readable feature score. This is not JEV; it is a stand-in that lets
    the loop run offline, and it is deliberately simple so you can audit it.
    """
    r = {
        "momentum": round(0.9 * state.momentum, 3),
        "trend_24h": round(4.0 * state.change_24h, 3),
        "volume": round(0.4 * min(max(state.volume_delta, -1), 1), 3),
        "news": round(0.5 * state.news, 3),
    }
    regime = {"bullish": 0.25, "neutral": 0.0, "bearish": -0.25}.get(state.regime, 0.0)
    r["regime"] = regime
    return r


def _sigmoid(x: float) -> float:
    from math import exp
    return 1 / (1 + exp(-x))


def _offline(state: MarketState) -> Decision:
    reasons = _score(state)
    net = sum(reasons.values())
    strength = abs(net)

    if strength < 0.15:
        action = "HOLD"
    elif net > 0:
        action = "BUY"
    else:
        # a strong negative on a name you would not short is an AVOID, not a SELL
        action = "SELL" if state.asset_class in ("crypto", "stock") else "AVOID"

    from math import tanh
    if action == "HOLD":
        probability = round(0.50 + 0.15 * strength, 3)
        confidence = round(0.45 + 0.20 * tanh(2.0 * strength), 3)
    else:
        probability = round(0.55 + 0.42 * tanh(1.6 * strength), 3)
        confidence = round(0.55 + 0.40 * tanh(1.3 * strength), 3)

    return Decision(symbol=state.symbol, action=action,
                    probability=min(0.97, max(0.50, probability)),
                    confidence=min(0.97, max(0.40, confidence)),
                    source="offline", reasons=reasons)


# --- real JEV adapter ------------------------------------------------------

def _jev(state: MarketState) -> Decision:
    """Call the real TypeSafe JEV API. Requires access and a key.

    JEV takes a block of state and a typed question, and returns the chosen
    option with a calibrated probability. We ask one Choice question over the
    four actions. The endpoint is read from the environment because JEV is in
    gated early access; point it at the API you were given.
    """
    key = os.environ.get("TYPESAFE_API_KEY")
    base = os.environ.get("TYPESAFE_API_BASE", "https://api.typesafe.ai/v1/decide")
    if not key:
        raise SystemExit("set TYPESAFE_API_KEY to use --engine jev "
                         "(the default offline engine needs no key)")

    state_text = (
        f"{state.symbol} ({state.asset_class}) at {state.price}. "
        f"24h change {state.change_24h:+.2%}, volume delta {state.volume_delta:+.0%}, "
        f"momentum {state.momentum:+.2f}, news {state.news:+.2f}, "
        f"regime {state.regime}."
    )
    body = json.dumps({
        "state": state_text,
        "questions": [{
            "id": "action",
            "type": "choice",
            "prompt": "What is the right action on this asset right now?",
            "options": list(ACTIONS),
        }],
    }).encode()

    req = Request(base, data=body, headers={
        "content-type": "application/json",
        "authorization": f"Bearer {key}",
    })
    with urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode())

    # Expected shape: {"answers": {"action": {"value": "BUY", "probability": 0.78,
    #                  "confidence": 0.91}}}. Read defensively.
    ans = (data.get("answers") or {}).get("action") or {}
    action = ans.get("value", "HOLD")
    if action not in ACTIONS:
        action = "HOLD"
    return Decision(
        symbol=state.symbol,
        action=action,
        probability=float(ans.get("probability", 0.5)),
        confidence=float(ans.get("confidence", ans.get("probability", 0.5))),
        source="jev",
        reasons={"engine": "typesafe-jev"},
    )


# --- one entry point -------------------------------------------------------

def decide(state: MarketState, engine: str = "offline") -> Decision:
    if engine == "jev":
        return _jev(state)
    return _offline(state)
