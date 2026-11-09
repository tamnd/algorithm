# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dpll/. The authors are listed in prov/V4WR4Y.jsonl.

"""The Davis-Putnam-Logemann-Loveland procedure (DPLL) for CNF satisfiability.

A clause is a list of nonzero ints in DIMACS style: v is the variable v and
-v is its negation. dpll(n, clauses) returns a model as a list of n literals
(entry i is i + 1 or -(i + 1)), or None when the formula has no model.

Each node of the search applies unit propagation, then the pure literal
rule, then splits on a literal of a shortest clause, true branch first. The
recursion of the textbook procedure is replaced by an explicit stack of
pending branches.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence

Clause = frozenset[int]


def assign(f: list[Clause], lit: int) -> list[Clause]:
    """F|lit: drop the clauses that contain lit, and remove -lit from the rest."""
    return [c - {-lit} if -lit in c else c for c in f if lit not in c]


def dpll(
    n: int,
    clauses: Iterable[Sequence[int]],
    log: list[tuple[str, int]] | None = None,
) -> list[int] | None:
    """Return a model of the CNF formula over 1..n, or None if it has none.

    Precondition: n >= 0 and each literal l of each clause has 1 <= |l| <= n.
    If log is a list, the run appends ("unit", l), ("pure", l), ("split", l),
    ("conflict", 0) and ("sat", 0) events in order.
    Cost: at most 2^(n+1) - 1 nodes, each in O(n |F|) time, so O(2^n n |F|)
    time in the worst case, where |F| is the number of literal occurrences.
    The stack holds at most n + 1 formulas, so the space is O(n |F|).
    """
    f0 = []
    for c in clauses:
        s = frozenset(c)
        if not any(-q in s for q in s):  # a tautology is always true
            f0.append(s)
    stack: list[tuple[list[Clause], list[int]]] = [(f0, [])]
    while stack:
        f, alpha = stack.pop()
        while True:  # @line L1
            unit = next((c for c in f if len(c) == 1), None)
            if unit is None:
                break
            (lit,) = unit
            if log is not None:
                log.append(("unit", lit))
            alpha = alpha + [lit]  # @line L2
            f = assign(f, lit)
        if any(len(c) == 0 for c in f):  # @line L3
            if log is not None:
                log.append(("conflict", 0))
            continue
        while True:  # @line L4
            occurs = {q for c in f for q in c}
            pure = next((q for q in sorted(occurs, key=abs) if -q not in occurs), None)
            if pure is None:
                break
            if log is not None:
                log.append(("pure", pure))
            alpha = alpha + [pure]  # @line L5
            f = assign(f, pure)
        if not f:  # @line L6
            if log is not None:
                log.append(("sat", 0))
            value = {abs(q): q > 0 for q in alpha}
            return [v if value.get(v, False) else -v for v in range(1, n + 1)]
        shortest = min(f, key=len)
        lit = min(shortest, key=lambda q: (abs(q), -q))  # @line L7
        if log is not None:
            log.append(("split", lit))
        stack.append((assign(f, -lit), alpha + [-lit]))  # @line L9
        stack.append((assign(f, lit), alpha + [lit]))  # @line L8
    return None
