# Cheatsheet

Flags go **before** the subcommand. Run from the repo root.

| Command | What it does |
| ------- | ------------ |
| `python -m jev_bot decisions` | one cycle, show the decision table |
| `python -m jev_bot run` | same, and execute approved decisions on paper |
| `python -m jev_bot card TSLA` | unpack one decision (symbol must be in the batch) |
| `python -m jev_bot --seed 3 --n 5 decisions` | 5 assets, seed 3, reproducible |
| `python -m jev_bot --min-confidence 0.8 run` | stricter gate |
| `python -m jev_bot --engine jev decisions` | real JEV API (needs `TYPESAFE_API_KEY`) |

## Flags

| Flag | Default | Meaning |
| ---- | ------- | ------- |
| `--engine` | `offline` | `offline` or `jev` |
| `--n` | `8` | how many assets in the batch |
| `--seed` | `7` | same seed, same market |
| `--min-confidence` | `0.70` | gate floor for confidence |

## Make shortcuts

```bash
make test
make decisions
make run
make card SYM=TSLA
```

## Gate defaults

min confidence 70%, min probability 60%, max 5 open positions. HOLD and AVOID never execute.

Paper only. Not financial advice.
