# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ac-4/. The authors are listed in prov/ZP1QQ8.jsonl.

"""AC-4 (Mohr and Henderson 1986): arc consistency with support counters.

A binary CSP has the variables 0 .. n-1. domains[i] is an iterable of the
values of variable i. constraints maps a pair (i, j), i != j, to the set of
allowed pairs (a, b), meaning x_i = a and x_j = b. Two entries for the same
two variables both apply.
"""

from collections import deque
from collections.abc import Iterable, Mapping

Constraints = Mapping[tuple[int, int], Iterable[tuple[int, int]]]


def directed(constraints: Constraints) -> dict[tuple[int, int], set[tuple[int, int]]]:
    """Return the relation R_ij of each arc (i, j), for both directions."""
    rel: dict[tuple[int, int], set[tuple[int, int]]] = {}
    for (i, j), pairs in constraints.items():
        if i == j:
            raise ValueError("a binary constraint needs two different variables")
        fwd = set(pairs)
        bwd = {(b, a) for a, b in fwd}
        rel[(i, j)] = rel[(i, j)] & fwd if (i, j) in rel else fwd
        rel[(j, i)] = rel[(j, i)] & bwd if (j, i) in rel else bwd
    return rel


def ac4(domains: Iterable[Iterable[int]], constraints: Constraints,
        stats: dict[str, int] | None = None) -> tuple[bool, list[set[int]]]:
    """Return (ok, D), where D is the arc consistency closure.

    ok is False when the closure has an empty domain; then the CSP has no solution.
    stats, when given, receives the number of constraint checks and of counter decrements.
    """
    if stats is None:
        stats = {}
    stats["checks"] = stats["decrements"] = 0
    dom = [set(d) for d in domains]
    rel = directed(constraints)
    counter: dict[tuple[int, int, int], int] = {}
    support: dict[tuple[int, int], list[tuple[int, int]]] = {}
    start = [set(d) for d in dom]  # the counters are set on the initial domains
    deleted: deque[tuple[int, int]] = deque()  # @line L1
    for (i, j), r in rel.items():  # @line L2
        for a in start[i]:  # @line L3
            total = 0
            for b in start[j]:  # @line L4
                stats["checks"] += 1
                if (a, b) in r:
                    total += 1
                    support.setdefault((j, b), []).append((i, a))  # @line L5
            counter[(i, j, a)] = total
            if total == 0 and a in dom[i]:  # @line L6
                dom[i].discard(a)
                deleted.append((i, a))
    while deleted:  # @line L7
        j, b = deleted.popleft()  # @line L8
        for i, a in support.get((j, b), ()):  # @line L9
            if a in dom[i]:
                stats["decrements"] += 1
                counter[(i, j, a)] -= 1  # @line L10
                if counter[(i, j, a)] == 0:  # @line L11
                    dom[i].discard(a)
                    deleted.append((i, a))
    return all(dom), dom  # @line L12
