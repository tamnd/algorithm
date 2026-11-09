# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/davis-putnam-elimination/. The authors are listed in prov/1EV788.jsonl.

"""The Davis-Putnam procedure (1960): decide CNF satisfiability by the
unit rule, the pure literal rule and the elimination of variables by
resolution, with no search.

A clause is a list of nonzero ints in DIMACS style. davis_putnam(n, clauses)
returns a model as a list of n literals, or None when there is none. The
model is rebuilt from a record of the steps, in reverse order.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence

Clause = frozenset[int]


def resolvents(pos: Iterable[Clause], neg: Iterable[Clause], x: int) -> set[Clause]:
    """All resolvents on x of a clause with x and a clause with -x, except
    the tautologies."""
    out: set[Clause] = set()
    negs = list(neg)
    for c in pos:
        for d in negs:
            r = (c - {x}) | (d - {-x})
            if not any(-q in r for q in r):
                out.add(r)
    return out


def eliminate(f: set[Clause], x: int) -> tuple[set[Clause], list[Clause]]:
    """Replace the clauses with x or -x by their resolvents on x. Return the
    new formula and the removed clauses."""
    pos = [c for c in f if x in c]
    neg = [c for c in f if -x in c]
    removed = pos + neg
    rest = {c for c in f if x not in c and -x not in c}
    return rest | resolvents(pos, neg, x), removed


def davis_putnam(
    n: int,
    clauses: Iterable[Sequence[int]],
    log: list[tuple[str, int, int]] | None = None,
) -> list[int] | None:
    """Return a model of the CNF formula over 1..n, or None if it has none.

    Precondition: n >= 0 and each literal l of each clause has 1 <= |l| <= n.
    If log is a list, each step appends (rule, literal or variable, number of
    clauses after the step), with rule "unit", "pure" or "eliminate".
    Cost: at most n steps. Duplicate clauses are merged, so the formula has
    at most 3^n clauses, and the time is O(n^2 9^n) and the space O(n 3^n)
    in the worst case.
    """
    f: set[Clause] = set()
    for c in clauses:
        s = frozenset(c)
        if not any(-q in s for q in s):
            f.add(s)
    record: list[tuple[str, int, list[Clause]]] = []
    while True:  # @line L1
        if frozenset() in f:  # @line L2
            return None
        if not f:  # @line L3
            break
        unit = next((c for c in f if len(c) == 1), None)
        if unit is not None:  # @line L4
            (lit,) = unit
            record.append(("fix", lit, []))
            f = {c - {-lit} for c in f if lit not in c}
            if log is not None:
                log.append(("unit", lit, len(f)))
            continue
        occurs = {q for c in f for q in c}
        pure = next((q for q in sorted(occurs, key=abs) if -q not in occurs), None)
        if pure is not None:  # @line L5
            record.append(("fix", pure, []))
            f = {c for c in f if pure not in c}
            if log is not None:
                log.append(("pure", pure, len(f)))
            continue
        count: dict[int, int] = {}
        for q in occurs:
            count[q] = sum(1 for c in f if q in c)
        x = min({abs(q) for q in occurs}, key=lambda v: (count[v] * count[-v], v))  # @line L6
        pos = [c for c in f if x in c]  # @line L7
        neg = [c for c in f if -x in c]
        res = resolvents(pos, neg, x)  # @line L8
        f = {c for c in f if x not in c and -x not in c} | res  # @line L9
        record.append(("elim", x, pos))
        if log is not None:
            log.append(("eliminate", x, len(f)))
    value = [False] * (n + 1)
    for kind, a, pos in reversed(record):
        if kind == "fix":
            value[abs(a)] = a > 0
        else:
            # x false satisfies the clauses with -x; that is safe exactly when
            # every clause with x is already true without x.
            ok = all(any(value[abs(q)] == (q > 0) for q in c if q != a) for c in pos)
            value[a] = not ok
    return [v if value[v] else -v for v in range(1, n + 1)]
