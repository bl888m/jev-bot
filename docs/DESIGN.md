# Design principles

The rules jev-bot is built around. When a change is in question, these decide
it.

## One decision, typed

A state goes in. An action, a probability and a confidence come out. No free
text to parse, no hidden chain of steps. If a stage needs a new field, it goes
on the typed object, not into a string.

## The model and the gate are separate jobs

JEV decides what it thinks is right. The gate decides whether that may act.
They live in different files so neither can quietly do the other's work.

## Every decision is labelled

Each decision says which engine made it, offline or jev. A reader should never
have to guess whether a number came from the model or from the local stand in.

## Paper is the floor

There is no live flag and no wallet. Execution is a paper book in one file.
Going live means writing an adapter yourself, deliberately outside this repo.

## Honest about what is simulated

Data is generated, performance is paper. Nothing here claims the model
predicts markets. Anything simulated says so where it appears.

## Standard library only

Zero runtime dependencies means fewer things to audit before you trust the
loop.
