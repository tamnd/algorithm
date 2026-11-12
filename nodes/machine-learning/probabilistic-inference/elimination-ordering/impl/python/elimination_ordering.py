# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/elimination-ordering/. The authors are listed in prov/BG2816.jsonl.

"""Elimination orderings of an undirected graph: width, fill, two greedy
heuristics (min-degree and min-fill) and the exact minimum width.

A graph is given by its number of vertices n (labelled 0 .. n-1) and a list of
edges. Eliminating a vertex joins all its remaining neighbours to each other
(the fill edges) and deletes it. The width of an order is the largest number of
remaining neighbours of a vertex when it is eliminated. Ties in the heuristics
go to the smallest label, so the results are deterministic.
"""

from itertools import combinations
from typing import Dict, Iterable, List, Sequence, Set, Tuple

Edge = Tuple[int, int]


def adjacency(n: int, edges: Iterable[Edge]) -> Dict[int, Set[int]]:
    adj: Dict[int, Set[int]] = {v: set() for v in range(n)}
    for u, v in edges:
        if u != v:
            adj[u].add(v)
            adj[v].add(u)
    return adj


def eliminate(n: int, edges: Iterable[Edge], order: Sequence[int]) -> Tuple[int, List[Edge]]:
    """Return (width, fill edges) of the order. O(n^3) time."""
    if sorted(order) != list(range(n)):
        raise ValueError("the order must hold each vertex once")
    adj = adjacency(n, edges)
    width, fill = 0, []
    for z in order:
        nb = adj.pop(z)
        width = max(width, len(nb))
        for u, v in combinations(sorted(nb), 2):
            if v not in adj[u]:
                adj[u].add(v)
                adj[v].add(u)
                fill.append((u, v))
        for u in nb:
            adj[u].discard(z)
    return width, fill


def induced_width(n: int, edges: Iterable[Edge], order: Sequence[int]) -> int:
    return eliminate(n, edges, order)[0]


def _fill_count(adj: Dict[int, Set[int]], z: int) -> int:
    nb = sorted(adj[z])
    return sum(1 for u, v in combinations(nb, 2) if v not in adj[u])


def greedy_order(n: int, edges: Iterable[Edge], score: str) -> List[int]:
    """Greedy elimination: at each step take a vertex of least score.

    score is "degree" (min-degree) or "fill" (min-fill). O(n^3) per step for
    min-fill in this simple form, O(n^4) in total; O(n^2) per step for min-degree.
    """
    adj = adjacency(n, edges)
    order: List[int] = []
    while adj:
        if score == "degree":
            z = min(adj, key=lambda v: (len(adj[v]), v))
        elif score == "fill":
            z = min(adj, key=lambda v: (_fill_count(adj, v), v))
        else:
            raise ValueError("score must be 'degree' or 'fill'")
        nb = adj.pop(z)
        for u, v in combinations(nb, 2):
            adj[u].add(v)
            adj[v].add(u)
        for u in nb:
            adj[u].discard(z)
        order.append(z)
    return order


def min_degree_order(n: int, edges: Iterable[Edge]) -> List[int]:
    return greedy_order(n, edges, "degree")


def min_fill_order(n: int, edges: Iterable[Edge]) -> List[int]:
    return greedy_order(n, edges, "fill")


def exact_min_width(n: int, edges: Iterable[Edge]) -> Tuple[int, List[int]]:
    """The minimum width over all n! orders, and an order that reaches it.

    Dynamic programming over the set S of vertices eliminated first: the degree
    of v when it is eliminated right after S is the number of vertices outside
    S and v that v reaches by a path whose inner vertices all lie in S. Time
    O(2^n n^3); use it for small n only.
    """
    adj = adjacency(n, edges)

    def degree_after(s: int, v: int) -> int:
        seen = {v}
        stack = [v]
        out = 0
        while stack:
            x = stack.pop()
            for y in adj[x]:
                if y in seen:
                    continue
                seen.add(y)
                if s >> y & 1:
                    stack.append(y)
                else:
                    out += 1
        return out

    full = (1 << n) - 1
    best = [0] * (1 << n)
    choice = [-1] * (1 << n)
    for s in range(1, 1 << n):
        best[s] = n
        for v in range(n):
            if s >> v & 1:
                rest = s & ~(1 << v)
                w = max(best[rest], degree_after(rest, v))
                if w < best[s]:
                    best[s], choice[s] = w, v
    order: List[int] = []
    s = full
    while s:
        v = choice[s]
        order.append(v)
        s &= ~(1 << v)
    order.reverse()
    return (best[full] if n else 0), order
