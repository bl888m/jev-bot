"""Show the asset universe the offline generator draws from.

    python examples/universe.py
"""
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from jev_bot import markets

by_class = defaultdict(set)
for seed in range(1, 40):
    for s in markets.generate(n=10, seed=seed):
        by_class[s.asset_class].add(s.symbol)

for cls in sorted(by_class):
    print(f"{cls:<7} {', '.join(sorted(by_class[cls]))}")
