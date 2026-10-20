"""Check which engine would run in this shell. Prints nothing secret.

    python examples/env_check.py
"""
import os

key = os.environ.get("TYPESAFE_API_KEY")
base = os.environ.get("TYPESAFE_API_BASE")

print("TYPESAFE_API_KEY :", "set" if key else "not set")
print("TYPESAFE_API_BASE:", base if base else "not set")
print()
if key:
    print("--engine jev is available (early access key found)")
else:
    print("--engine jev will refuse to start, the offline engine needs nothing")
print("paper execution is always on, there is no live mode")
