# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/goemans-williamson-steiner-forest/. The authors are listed in prov/AWBKWN.jsonl.

from fractions import Fraction
from typing import Sequence

Number = int | Fraction


def _connects_all(n: int, edges: Sequence[tuple[int, int, Number]], chosen: Sequence[int],
                  pairs: Sequence[tuple[int, int]]) -> bool:
    parent = list(range(n))

    def find(u: int) -> int:
        while parent[u] != u:
            parent[u] = parent[parent[u]]
            u = parent[u]
        return u

    for e in chosen:
        u, v, _ = edges[e]
        parent[find(u)] = find(v)
    return all(find(s) == find(t) for s, t in pairs)


def goemans_williamson_steiner_forest(n: int, edges: Sequence[tuple[int, int, Number]],
                                      pairs: Sequence[tuple[int, int]], added: list[int] | None = None):
    """Primal-dual 2 - 2/k approximation for Steiner forest (Goemans and Williamson 1995).

    The graph has vertices 0 .. n - 1 and edges (u, v, cost) with cost >= 0. Each pair (s, t)
    must be connected. Returns (forest, y): forest lists the indices of the chosen edges in
    the order of addition, and y maps each raised vertex set (a frozenset) to its dual value.
    If added is a list, it receives all edges of the growth phase in the order of addition.
    The cost of the forest is at most (2 - 2/k) times the sum of y, where k is the number
    of terminals, and y is feasible for the dual of the cut LP.
    Raises ValueError if some pair cannot be connected. Time O(n m) with exact arithmetic.
    """
    pairs = [(s, t) for s, t in pairs if s != t]
    comp = list(range(n))  # @line L1
    members = {v: {v} for v in range(n)}
    d = [Fraction(0)] * n  # d[v] is the sum of y_S over the raised sets S that hold v
    y: dict[frozenset, Fraction] = {}
    if added is None:
        added = []

    def active(label: int) -> bool:
        return any((comp[s] == label) != (comp[t] == label) for s, t in pairs)

    while True:
        act = {label for label in members if active(label)}
        if not act:  # @line L2
            break
        best = None
        for k, (u, v, w) in enumerate(edges):  # @line L3
            if comp[u] == comp[v]:
                continue
            rate = (comp[u] in act) + (comp[v] in act)
            if rate:
                eps = (Fraction(w) - d[u] - d[v]) / rate
                if best is None or eps < best[0]:
                    best = (eps, k)
        if best is None:
            raise ValueError("some pair is not connected in the graph")
        eps, k = best  # @line L4
        for label in act:  # @line L5
            if eps:
                s = frozenset(members[label])
                y[s] = y.get(s, Fraction(0)) + eps
                for v in members[label]:
                    d[v] += eps
        u, v, _ = edges[k]  # @line L6
        added.append(k)
        keep, gone = comp[u], comp[v]
        for x in members[gone]:
            comp[x] = keep
        members[keep] |= members.pop(gone)
    forest = list(added)
    for k in reversed(added):  # @line L7
        rest = [e for e in forest if e != k]
        if _connects_all(n, edges, rest, pairs):  # @line L8
            forest = rest
    return forest, y  # @line L9
