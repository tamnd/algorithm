# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kleinberg-impossibility-theorem/. The authors are listed in prov/TFYKXG.jsonl.
"""Single linkage with Kleinberg's three stopping conditions, and checks of the three axioms.

A distance function on the points 0..n-1 is a dict {(i, j): value} for i < j with values > 0.
No triangle inequality is needed. A partition is a frozenset of frozensets.
"""

from itertools import combinations
from typing import Callable

Dist = dict
Partition = frozenset


def _components(n: int, edges) -> Partition:
    """The connected components of the graph on 0..n-1 with the given edges (union-find)."""
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i, j in edges:
        parent[find(i)] = find(j)
    groups: dict = {}
    for x in range(n):
        groups.setdefault(find(x), set()).add(x)
    return frozenset(frozenset(g) for g in groups.values())


def single_linkage_k(n: int, d: Dist, k: int) -> Partition:
    """k-cluster stopping condition: add edges in order of (weight, pair) until k components remain.

    The pair breaks ties, so the order is total. This is Kruskal's algorithm stopped early.
    """
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    comps = n
    used = []
    for (i, j) in sorted(d, key=lambda e: (d[e], e)):
        if comps <= k:
            break
        a, b = find(i), find(j)
        if a != b:
            parent[a] = b
            comps -= 1
            used.append((i, j))
    return _components(n, used)


def single_linkage_r(n: int, d: Dist, r) -> Partition:
    """Distance-r stopping condition: the components of the graph of edges with weight <= r."""
    return _components(n, [e for e in d if d[e] <= r])


def single_linkage_alpha(n: int, d: Dist, alpha) -> Partition:
    """Scale-alpha stopping condition: the components of the edges with weight <= alpha * max weight."""
    rho = max(d.values())
    return _components(n, [e for e in d if d[e] <= alpha * rho])


def all_partitions(n: int) -> set:
    out = set()

    def grow(i: int, blocks: list) -> None:
        if i == n:
            out.add(frozenset(frozenset(b) for b in blocks))
            return
        for b in blocks:
            b.append(i)
            grow(i + 1, blocks)
            b.pop()
        blocks.append([i])
        grow(i + 1, blocks)
        blocks.pop()

    grow(0, [])
    return out


def same_block(p: Partition, i: int, j: int) -> bool:
    return any(i in b and j in b for b in p)


def is_transformation(p: Partition, d: Dist, d2: Dist) -> bool:
    """d2 is a p-transformation of d: no larger inside blocks of p, no smaller across blocks."""
    return all(d2[e] <= d[e] if same_block(p, *e) else d2[e] >= d[e] for e in d)


def refines(p: Partition, q: Partition) -> bool:
    """Each block of p lies inside a block of q."""
    return all(any(b <= c for c in q) for b in p)


def grid_distances(n: int, values) -> list:
    pairs = list(combinations(range(n), 2))
    out = []

    def rec(i: int, cur: dict) -> None:
        if i == len(pairs):
            out.append(dict(cur))
            return
        for v in values:
            cur[pairs[i]] = v
            rec(i + 1, cur)

    rec(0, {})
    return out


def check_scale_invariance(f: Callable, n: int, grid: list, scales) -> list:
    """Return the counterexamples (d, alpha) with f(alpha d) != f(d)."""
    bad = []
    for d in grid:
        for a in scales:
            if f(n, {e: a * v for e, v in d.items()}) != f(n, d):
                bad.append((d, a))
    return bad


def check_consistency(f: Callable, n: int, grid: list) -> list:
    """Return the counterexamples (d, d2): d2 is an f(d)-transformation of d but f(d2) != f(d)."""
    outs = [f(n, d) for d in grid]
    bad = []
    for d, p in zip(grid, outs):
        for d2, p2 in zip(grid, outs):
            if p2 != p and is_transformation(p, d, d2):
                bad.append((d, d2))
    return bad


def check_richness(f: Callable, n: int, grid: list) -> set:
    """Return the partitions that f does not output on the grid."""
    return all_partitions(n) - {f(n, d) for d in grid}
