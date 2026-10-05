# FAQ

**Does jev-bot trade real money?**
No. Paper by default and paper only. There is no wallet in the repo, no key
handling for exchanges and no --live flag. The execution layer is a stub that
records fills and reaches no market.

**Is JEV an LLM?**
No. JEV is TypeSafe AI's System One model. It takes a state and a typed
question and returns one option with a calibrated probability in a single
fast pass. It writes no text.

**What does the offline engine do?**
It is a small local scoring function, used by default so the bot runs with no
key and gives the same result every time. Every decision is labelled offline
or jev, so you always know which one made the call.

**How do I use the real JEV model?**
Pass --engine jev and set TYPESAFE_API_KEY. JEV is in gated early access, so
the endpoint comes from your environment, not from the code.

**Why does the gate skip so many decisions?**
That is its job. It refuses low confidence, low probability, HOLD and AVOID
actions, and anything past the position cap, and it names the rule on every
skip.

**Does it predict markets?**
No claim is made that it does. This is an experiment in what happens when a
decision model gets market state and a risk gate. All data and results here
are simulated and labelled that way.

**Where do I start?**
python -m jev_bot decisions, then python -m jev_bot card BTC, then read
docs/ARCHITECTURE.md.
