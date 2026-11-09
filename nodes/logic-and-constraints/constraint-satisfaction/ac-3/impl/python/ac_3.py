# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ac-3/. The authors are listed in prov/QXMHYC.jsonl.

"""AC-3 (Mackworth 1977): enforce arc consistency on a binary CSP.

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


def revise(dom: list[set[int]], rel: dict[tuple[int, int], set[tuple[int, int]]],
           i: int, j: int, stats: dict[str, int]) -> bool:
    """Delete the values of x_i that have no support in D_j. True if one was deleted."""
    r, dj = rel[(i, j)], dom[j]
    gone = []  # @line L10
    for a in dom[i]:  # @line L11
        supported = False
        for b in dj:  # @line L12
            stats["checks"] += 1
            if (a, b) in r:
                supported = True
                break
        if not supported:
            gone.append(a)  # @line L13
    for a in gone:
        dom[i].discard(a)
    return bool(gone)  # @line L14


def ac3(domains: Iterable[Iterable[int]], constraints: Constraints,
        stats: dict[str, int] | None = None) -> tuple[bool, list[set[int]]]:
    """Return (ok, D). D is the arc consistency closure when ok is True.

    ok is False when some domain becomes empty; then the CSP has no solution.
    stats, when given, receives the number of revisions and of constraint checks.
    """
    if stats is None:
        stats = {}
    stats["revisions"] = stats["checks"] = 0
    dom = [set(d) for d in domains]
    rel = directed(constraints)
    if any(not d for d in dom):  # @line L1
        return False, dom
    nbrs: list[list[int]] = [[] for _ in dom]
    for i, j in rel:
        nbrs[i].append(j)
    queue = deque(rel)  # @line L2
    in_queue = set(rel)
    while queue:  # @line L3
        i, j = queue.popleft()  # @line L4
        in_queue.discard((i, j))
        stats["revisions"] += 1
        if revise(dom, rel, i, j, stats):  # @line L5
            if not dom[i]:  # @line L6
                return False, dom
            for k in nbrs[i]:  # @line L7
                if k != j and (k, i) not in in_queue:
                    queue.append((k, i))  # @line L8
                    in_queue.add((k, i))
    return True, dom  # @line L9
