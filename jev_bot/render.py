"""Terminal output. A LIVE DECISIONS table and a single decision, unpacked.

Every block carries a label for what is real and what is not: the data, the
decision engine, the execution mode. That labelling is the point. A reader
should never have to guess whether a number was read, computed, or made up.
"""

from __future__ import annotations

from .execution.paper import Book

_W = 66
_ARROW = {"BUY": "up", "SELL": "dn", "HOLD": "--", "AVOID": "x "}


def rule(ch="-"):
    return ch * _W


def header(engine: str, n: int) -> str:
    dec = "JEV (live)" if engine == "jev" else "offline (deterministic)"
    return "\n".join([
        rule("="),
        "  JEV-BOT  ·  market decisions by JEV",
        rule("-"),
        f"  DATA        sim ({n} assets)",
        f"  DECISION    {dec}",
        f"  EXECUTION   paper",
        f"  PERFORMANCE simulated",
        rule("="),
    ])


def decisions_table(records) -> str:
    lines = ["  ASSET   CLASS    JEV      PROB   CONF   VERDICT", rule("-")]
    for st, d, gate in records:
        tag = "EXEC" if gate.verdict == "EXECUTE" else "skip"
        lines.append(
            f"  {st.symbol:<6}  {st.asset_class:<6}  {d.action:<5} "
            f"{_ARROW[d.action]:>2}  {d.probability:>4.0%}  {d.confidence:>4.0%}   "
            + (tag if gate.verdict == "EXECUTE" else f"{tag} · {gate.reason}")
        )
    return "\n".join(lines)


def decision_card(st, d, gate) -> str:
    lines = [
        rule("="),
        f"  {st.symbol}  ·  {st.asset_class}  ·  ${st.price:,.2f}",
        rule("-"),
        f"  MARKET STATE",
        f"    24h            {st.change_24h:>+7.2%}",
        f"    volume         {st.volume_delta:>+7.0%}",
        f"    momentum       {st.momentum:>+7.2f}",
        f"    news           {st.news:>+7.2f}",
        f"    regime         {st.regime:>7}",
        rule("-"),
        f"  JEV OUTPUT  ({d.source})",
        f"    decision       {d.action:>7}",
        f"    probability    {d.probability:>7.2f}",
        f"    confidence     {d.confidence:>7.2f}",
        rule("-"),
        f"  GATE           {gate.verdict}" + (f"  ·  {gate.reason}" if gate.reason else ""),
        rule("="),
    ]
    return "\n".join(lines)


def book_summary(book: Book) -> str:
    ret = (book.equity() / 10_000 - 1) if book.equity() else 0
    lines = [
        rule("="),
        "  PAPER BOOK",
        rule("-"),
        f"  equity     ${book.equity():>10,.2f}   ({ret:+.2%})",
        f"  open P&L   ${book.open_pnl():>+10,.2f}",
        f"  positions  {book.open_positions():>10}",
    ]
    if book.fills:
        lines.append(rule("-"))
        for f in book.fills:
            lines.append(f"    {f.action:<4} {f.symbol:<5}  ${f.size:,.0f}  "
                         f"{f.pnl():>+8,.2f}")
    lines.append(rule("="))
    lines.append("  paper only · JEV decides, execution is simulated · not advice")
    return "\n".join(lines)
