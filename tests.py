"""reflex checks. No network, no dependencies. Run: python tests.py

Each check is one fact about the decision loop. The real JEV engine is not
exercised here (it needs access and a key); the offline engine and the gate
are, because those are what run by default.
"""

from jev_bot import jev, markets
from jev_bot.types import MarketState, Decision, ACTIONS
from jev_bot.risk import Limits, check
from jev_bot.execution.paper import Book

PASS = FAIL = 0


def ok(name, cond):
    global PASS, FAIL
    if cond:
        PASS += 1
        print("  ok    " + name)
    else:
        FAIL += 1
        print("  FAIL  " + name)


def st(**kw):
    base = dict(symbol="X", asset_class="stock", price=100.0, change_24h=0.0,
                volume_delta=0.0, momentum=0.0, news=0.0, regime="neutral")
    base.update(kw)
    return MarketState(**base)


# --- decision engine (offline) ---------------------------------------------
d1 = jev.decide(st(momentum=0.6, change_24h=0.05, regime="bullish"))
ok("a strong bullish state decides BUY", d1.action == "BUY")

d2 = jev.decide(st(momentum=-0.6, change_24h=-0.05, regime="bearish"))
ok("a strong bearish stock decides SELL", d2.action == "SELL")

d3 = jev.decide(st(momentum=-0.6, change_24h=-0.05, asset_class="meme", regime="bearish"))
ok("a strong bearish meme decides AVOID, not SELL", d3.action == "AVOID")

ok("a flat state decides HOLD", jev.decide(st()).action == "HOLD")

ok("action is always one of the four", jev.decide(st()).action in ACTIONS)

ok("probability and confidence stay in range",
   0.4 <= d1.confidence <= 0.97 and 0.5 <= d1.probability <= 0.97)

ok("every offline decision is labelled offline", d1.source == "offline")

ok("the same state gives the same decision",
   jev.decide(st(momentum=0.4)).action == jev.decide(st(momentum=0.4)).action
   and jev.decide(st(momentum=0.4)).probability == jev.decide(st(momentum=0.4)).probability)

# --- the gate --------------------------------------------------------------
strong = Decision("X", "BUY", 0.80, 0.90, "offline")
ok("a clean decision executes", check(strong, 0, Limits()).verdict == "EXECUTE")

ok("HOLD never executes",
   check(Decision("X", "HOLD", 0.9, 0.9), 0, Limits()).verdict == "SKIP")

ok("AVOID never executes",
   check(Decision("X", "AVOID", 0.9, 0.9), 0, Limits()).verdict == "SKIP")

ok("low confidence is refused",
   check(Decision("X", "BUY", 0.9, 0.5), 0, Limits()).verdict == "SKIP")

ok("the position cap is enforced",
   check(strong, 5, Limits()).verdict == "SKIP")

# --- paper execution -------------------------------------------------------
b = Book()
b.execute(strong, 100.0)
ok("executing adds a paper fill", b.open_positions() == 1)

b.mark({"X": 110.0})
ok("a BUY profits when price rises", b.open_pnl() > 0)

b2 = Book()
b2.execute(Decision("X", "SELL", 0.8, 0.9), 100.0)
b2.mark({"X": 90.0})
ok("a SELL profits when price falls", b2.open_pnl() > 0)

# --- market source ---------------------------------------------------------
ok("the generator is deterministic",
   [m.symbol for m in markets.generate(6, 3)] == [m.symbol for m in markets.generate(6, 3)])

print(f"\n  {PASS} passed, {FAIL} failed")
raise SystemExit(1 if FAIL else 0)
