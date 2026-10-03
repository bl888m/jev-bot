# Changelog

## v0.2.0
- Added a `Makefile` with common dev shortcuts (`make test`, `make decisions`,
  `make card SYM=BTC`, `make run`, `make clean`).
- Added `scripts/setup.sh`, a one-shot dev setup that installs the CLI
  editable and runs the test suite.
- Added a `Dockerfile` so the bot runs the same way anywhere: `docker build
  -t jev-bot . && docker run --rm jev-bot decisions`.
- No changes to the decision loop, the gate, or paper execution. All 17 tests
  still pass unchanged.

## v0.1.0
- The decision loop: market state -> JEV -> risk gate -> paper execution.
- Two engines: `offline` (deterministic, default) and `jev` (the real
  TypeSafe API, behind `--engine jev` and `TYPESAFE_API_KEY`).
- `decisions`, `run`, and `card SYMBOL` commands.
- 17 offline tests, zero runtime dependencies.
