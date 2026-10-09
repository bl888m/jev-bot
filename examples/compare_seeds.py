"""Same seed, same decisions. Different seed, different market.

    python examples/compare_seeds.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from jev_bot import jev, markets


def actions(seed):
    return [jev.decide(s).action for s in markets.generate(n=6, seed=seed)]


print("seed 7 :", actions(7))
print("seed 7 :", actions(7), " (identical, the offline engine is deterministic)")
print("seed 11:", actions(11))
