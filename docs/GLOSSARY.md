# Glossary

Plain definitions for the terms jev-bot uses.

**JEV** , TypeSafe AI's first System One model. It takes a state and a typed
question and returns one option with a calibrated probability, in a single
fast pass, with no text to parse.

**System One** , the fast, intuitive kind of decision, as opposed to slow
step by step reasoning. The name comes from the System 1 and System 2 idea.

**State** , one snapshot of a market: price, 24h change, volume, momentum,
news score and regime.

**Decision** , what JEV returns for a state: an action, a probability and a
confidence.

**Action** , one of BUY, SELL, HOLD or AVOID.

**Probability** , how likely the chosen action is to be the right one.

**Confidence** , how sure the engine is that it should act at all.

**Calibrated** , a probability that means what it says. Of everything scored
at 70%, about 70% should turn out right.

**Gate** , the risk check between a decision and execution. It can refuse a
decision and always names the rule that stopped it.

**Offline engine** , the default local scoring function. Transparent and
reproducible, and labelled "offline" on every decision so it is never mistaken
for the real model.

**Paper** , trades recorded as if real, with no money and no orders. The only
execution mode jev-bot ships.

**Regime** , the broad market mood for an asset: bullish, neutral or bearish.
