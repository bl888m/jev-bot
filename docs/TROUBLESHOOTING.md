# Troubleshooting

The three things that trip people up most.

## `unrecognized arguments: --engine jev`

```text
jev-bot: error: unrecognized arguments: --engine jev
```

Flags go **before** the subcommand, not after it.

```bash
# wrong
python -m jev_bot decisions --engine jev

# right
python -m jev_bot --engine jev decisions
```

The same goes for `--n`, `--seed` and `--min-confidence`.

## `No module named jev-bot`

```text
No module named jev-bot
```

The package name uses an underscore. The hyphen is only for the installed command.

```bash
python -m jev_bot decisions     # module, underscore
jev-bot decisions               # command, after `pip install -e .`
```

## `set TYPESAFE_API_KEY to use --engine jev`

The real JEV engine needs a key from TypeSafe AI. Access is early-access and gated. Without a key, use the default offline engine, which needs nothing:

```bash
python -m jev_bot decisions
```

If you do have a key:

```bash
export TYPESAFE_API_KEY=your_key_here
python -m jev_bot --engine jev decisions
```

## `card` says the symbol is not in this batch

`card` only knows the assets in the current batch. List them first, then pick one, using the same flags:

```bash
python -m jev_bot --seed 3 --n 5 decisions
python -m jev_bot --seed 3 --n 5 card TSLA
```

Still stuck? Open an issue with the command you ran and the full output.
