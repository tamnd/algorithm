# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pc-2/. The authors are listed in prov/JNRB9Z.jsonl.

"""PC-2 (Mackworth 1977): enforce path consistency on a binary CSP.

A binary CSP has the variables 0 .. n-1. domains[i] is an iterable of the
values of variable i. constraints maps a pair (i, j), i != j, to the set of
allowed pairs (a, b), meaning x_i = a and x_j = b. A pair of variables with no
constraint has the full relation D_i x D_j.
"""

from collections import deque
from collections.abc import Iterable, Mapping

Constraints = Mapping[tuple[int, int], Iterable[tuple[int, int]]]
Relations = dict[tuple[int, int], set[tuple[int, int]]]


def full_relations(dom: list[set[int]], constraints: Constraints) -> Relations:
    """Return R_ij for each pair i < j, inside D_i x D_j."""
    n = len(dom)
    rel: Relations = {}
    for i in range(n):
        for j in range(i + 1, n):
            rel[(i, j)] = {(a, b) for a in dom[i] for b in dom[j]}
    for (i, j), pairs in constraints.items():
        if i == j:
            raise ValueError("a binary constraint needs two different variables")
        p = set(pairs) if i < j else {(b, a) for a, b in pairs}
        key = (min(i, j), max(i, j))
        rel[key] &= p
    return rel


def get(rel: Relations, i: int, j: int) -> set[tuple[int, int]]:
    """R_ij for any order of i and j."""
    if i < j:
        return rel[(i, j)]
    return {(b, a) for a, b in rel[(j, i)]}


def revise_path(rel: Relations, dom: list[set[int]], i: int, k: int, j: int,
                stats: dict[str, int]) -> bool:
    """Keep only the pairs of R_ij that extend to x_k. True if R_ij changed."""
    rik, rkj = get(rel, i, k), get(rel, k, j)
    keep = set()
    for a, b in rel[(i, j)]:  # @line L10
        for c in dom[k]:
            stats["checks"] += 1
            if (a, c) in rik and (c, b) in rkj:
                keep.add((a, b))
                break
    if keep == rel[(i, j)]:  # @line L11
        return False
    rel[(i, j)] = keep  # @line L12
    return True


def pc2(domains: Iterable[Iterable[int]], constraints: Constraints,
        stats: dict[str, int] | None = None) -> tuple[bool, list[set[int]], Relations]:
    """Return (ok, D, R): the strongly path consistent closure, R_ij for i < j.

    ok is False when a relation or a domain becomes empty; then the CSP has no solution.
    """
    if stats is None:
        stats = {}
    stats["revisions"] = stats["checks"] = 0
    dom = [set(d) for d in domains]
    n = len(dom)
    rel = full_relations(dom, constraints)
    queue = deque((i, k, j) for i in range(n) for j in range(i + 1, n)
                  for k in range(n) if k != i and k != j)  # @line L1
    in_queue = set(queue)
    while queue:  # @line L2
        t = queue.popleft()  # @line L3
        in_queue.discard(t)
        i, k, j = t
        stats["revisions"] += 1
        if revise_path(rel, dom, i, k, j, stats):  # @line L4
            if not rel[(i, j)]:  # @line L5
                return False, dom, rel
            for m in range(n):  # @line L6
                if m == i or m == j:
                    continue
                for u in ((min(i, m), j, max(i, m)), (min(j, m), i, max(j, m))):  # @line L7
                    if u not in in_queue:
                        queue.append(u)
                        in_queue.add(u)
    for i in range(n):  # @line L8
        for j in range(n):
            if i != j:
                used = {a for a, _ in get(rel, i, j)}
                dom[i] &= used
    for key in rel:
        i, j = key
        rel[key] = {(a, b) for a, b in rel[key] if a in dom[i] and b in dom[j]}
    return all(dom), dom, rel  # @line L9
