# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tree-structured-csp/. The authors are listed in prov/G0H16E.jsonl.

"""Solve and count a binary CSP whose constraint graph is a forest, in O(n d^2) time.

A binary CSP has the variables 0 .. n-1. domains[i] is an iterable of the
values of variable i. constraints maps a pair (i, j), i != j, to the set of
allowed pairs (a, b), meaning x_i = a and x_j = b.
"""

from collections import deque
from collections.abc import Iterable, Mapping

Constraints = Mapping[tuple[int, int], Iterable[tuple[int, int]]]
Rel = dict[tuple[int, int], set[tuple[int, int]]]


def directed(constraints: Constraints) -> Rel:
    """Return the relation R_ij of each arc (i, j), for both directions."""
    rel: Rel = {}
    for (i, j), pairs in constraints.items():
        if i == j:
            raise ValueError("a binary constraint needs two different variables")
        fwd = set(pairs)
        bwd = {(b, a) for a, b in fwd}
        rel[(i, j)] = rel[(i, j)] & fwd if (i, j) in rel else fwd
        rel[(j, i)] = rel[(j, i)] & bwd if (j, i) in rel else bwd
    return rel


def parent_first_order(n: int, rel: Rel) -> tuple[list[int], list[int]]:
    """Return (order, parent) of a breadth-first search from a root in each tree.

    parent[v] is -1 for a root. Raise ValueError if the constraint graph has a cycle.
    """
    nbrs: list[list[int]] = [[] for _ in range(n)]
    for i, j in rel:
        nbrs[i].append(j)
    if len(rel) // 2 > max(n - 1, 0):
        raise ValueError("the constraint graph is not a forest")
    parent = [-1] * n
    seen = [False] * n
    order: list[int] = []
    for root in range(n):
        if seen[root]:
            continue
        seen[root] = True
        queue = deque([root])
        while queue:
            v = queue.popleft()
            order.append(v)
            for w in nbrs[v]:
                if w == parent[v]:
                    continue
                if seen[w]:
                    raise ValueError("the constraint graph is not a forest")
                seen[w] = True
                parent[w] = v
                queue.append(w)
    return order, parent


def solve_tree(domains: Iterable[Iterable[int]], constraints: Constraints) -> list[int] | None:
    """Return a solution, or None if the CSP has no solution."""
    dom = [set(d) for d in domains]
    rel = directed(constraints)
    n = len(dom)
    if any(not d for d in dom):  # @line L1
        return None
    order, parent = parent_first_order(n, rel)  # @line L2
    for v in reversed(order):  # @line L3
        p = parent[v]
        if p >= 0:  # @line L4
            r = rel[(p, v)]
            dom[p] = {a for a in dom[p] if any((a, b) in r for b in dom[v])}  # @line L5
            if not dom[p]:  # @line L6
                return None
    value = [0] * n
    for v in order:  # @line L7
        p = parent[v]
        if p < 0:
            value[v] = min(dom[v])  # @line L8
        else:
            r = rel[(p, v)]
            value[v] = min(b for b in dom[v] if (value[p], b) in r)  # @line L9
    return value  # @line L10


def count_tree(domains: Iterable[Iterable[int]], constraints: Constraints) -> int:
    """Return the number of solutions."""
    dom = [set(d) for d in domains]
    rel = directed(constraints)
    n = len(dom)
    order, parent = parent_first_order(n, rel)
    children: list[list[int]] = [[] for _ in range(n)]
    for v in order:
        if parent[v] >= 0:
            children[parent[v]].append(v)
    ways: list[dict[int, int]] = [{} for _ in range(n)]
    for v in reversed(order):  # @line L11
        for a in dom[v]:
            w = 1
            for c in children[v]:
                r = rel[(v, c)]
                w *= sum(ways[c][b] for b in dom[c] if (a, b) in r)
            ways[v][a] = w
    total = 1
    for v in order:  # @line L12
        if parent[v] < 0:
            total *= sum(ways[v].values())
    return total
