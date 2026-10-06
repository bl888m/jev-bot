# The gate

JEV returns a calibrated answer. The gate decides whether that answer may
execute. The developer, not the model, is responsible for acting on a
decision, and the gate is where that responsibility lives in code.

## Rules, in the order they are checked

1. Action. HOLD and AVOID never execute, whatever the confidence.
2. Confidence. Below 70% the decision is skipped.
3. Probability. Below 60% the decision is skipped, because the action has to
   beat a coin flip.
4. Exposure. With 5 positions already open, nothing new opens.

The first rule that fails is the one reported. Every skip names it, for
example: confidence 68% < 70% floor.

## Why this order

Cheap, absolute checks come first. Whether an action is allowed at all does
not depend on any number, so it goes first. Then the two thresholds on the
model's own output, then the check on the state of the book.

## Changing a limit

The defaults live in jev_bot/risk.py in the Limits dataclass. From the command
line, --min-confidence overrides the confidence floor:

    python -m jev_bot --min-confidence 0.85 decisions

## Adding a rule

A rule is a few lines in check() that returns a skip with a reason. Add the
rule, then add a test in tests.py that proves it refuses and proves a clean
decision still passes.
