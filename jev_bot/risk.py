"""The gate. JEV decides; this decides whether the decision may execute.

This is the line TypeSafe itself draws: the model returns a calibrated
answer, and the developer, not the model, is responsible for acting on it.
So a decision is never executed on JEV's word alone. It has to clear a
confidence floor and the book's own limits first, and when it does not, the
gate names the single rule that stopped it.
"""

from __future__ import annotations

from dataclasses import dataclass

from .types import Decision


@dataclass
class Limits:
    min_confidence: float = 0.70    # do not act below this, send to a human
    min_probability: float = 0.60   # the action must be better than a coin flip
    max_positions: int = 5          # cap concurrent exposure
    block_actions: tuple = ("AVOID",)  # AVOID and HOLD never execute


@dataclass
class Gate:
    verdict: str    # "EXECUTE" or "SKIP"
    reason: str     # binding rule when SKIP, else ""


def check(decision: Decision, open_positions: int, limits: Limits) -> Gate:
    if decision.action in limits.block_actions or decision.action == "HOLD":
        return Gate("SKIP", f"{decision.action} does not execute")
    if decision.confidence < limits.min_confidence:
        return Gate("SKIP", f"confidence {decision.confidence:.0%} < "
                            f"{limits.min_confidence:.0%} floor")
    if decision.probability < limits.min_probability:
        return Gate("SKIP", f"probability {decision.probability:.0%} < "
                            f"{limits.min_probability:.0%} floor")
    if open_positions >= limits.max_positions:
        return Gate("SKIP", f"{limits.max_positions} positions already open")
    return Gate("EXECUTE", "")
