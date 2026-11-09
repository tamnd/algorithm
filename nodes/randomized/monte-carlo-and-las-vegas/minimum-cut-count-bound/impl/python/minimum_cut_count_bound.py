# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimum-cut-count-bound/. The authors are listed in prov/7P1NFC.jsonl.

"""Exact checks of the bound n(n-1)/2 on the number of minimum cuts.

A multigraph has vertices 0..n-1 and a list of edges (u, v) with u != v;
parallel edges are repeated in the list. A cut is a partition {S, V - S}
with both sides nonempty; we name it by the side S that contains vertex 0.
"""

import random
from fractions import Fraction
from itertools import combinations
from typing import Sequence

Edge = tuple[int, int]
Cut = frozenset[int]


def cut_size(edges: Sequence[Edge], side: Cut) -> int:
    """The number of edges with one end in `side` and one end outside."""
    return sum(1 for u, v in edges if (u in side) != (v in side))


def all_cuts(n: int) -> list[Cut]:
    """All 2^(n-1) - 1 cuts of a vertex set of size n, as the side that contains 0."""
    out = []
    for mask in range(1 << (n - 1)):
        side = frozenset([0] + [v for v in range(1, n) if mask >> (v - 1) & 1])
        if len(side) < n:
            out.append(side)
    return out


def minimum_cuts(n: int, edges: Sequence[Edge]) -> tuple[int, list[Cut]]:
    """The size of a minimum cut and the list of all minimum cuts, by brute force."""
    sizes = [(cut_size(edges, s), s) for s in all_cuts(n)]
    best = min(c for c, _ in sizes)
    return best, [s for c, s in sizes if c == best]


def is_connected(n: int, edges: Sequence[Edge]) -> bool:
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    seen = {0}
    stack = [0]
    while stack:
        u = stack.pop()
        for w in adj[u]:
            if w not in seen:
                seen.add(w)
                stack.append(w)
    return len(seen) == n


def contract(n: int, edges: Sequence[Edge], rng: random.Random) -> Cut:
    """One run of Karger's contraction; returns the cut it outputs. Needs a connected graph."""
    label = list(range(n))  # label[v] is the super-vertex of v

    def find(v: int) -> int:
        while label[v] != v:
            label[v] = label[label[v]]
            v = label[v]
        return v

    groups = n
    while groups > 2:
        u, v = edges[rng.randrange(len(edges))]
        ru, rv = find(u), find(v)
        if ru == rv:
            continue  # a loop; drawing again makes the choice uniform over non-loop edges
        label[rv] = ru
        groups -= 1
    root = find(0)
    return frozenset(v for v in range(n) if find(v) == root)


def contraction_distribution(n: int, edges: Sequence[Edge]) -> dict[Cut, Fraction]:
    """The exact probability of each output cut of one contraction run, by dynamic programming."""
    start = tuple(range(n))  # a partition as the tuple of the least vertex of each block
    layer: dict[tuple[int, ...], Fraction] = {start: Fraction(1)}
    for _ in range(n - 2):
        nxt: dict[tuple[int, ...], Fraction] = {}
        for part, pr in layer.items():
            live = [(part[u], part[v]) for u, v in edges if part[u] != part[v]]
            for a, b in live:
                lo, hi = min(a, b), max(a, b)
                new = tuple(lo if x == hi else x for x in part)
                nxt[new] = nxt.get(new, Fraction(0)) + pr / len(live)
        layer = nxt
    out: dict[Cut, Fraction] = {}
    for part, pr in layer.items():
        side = frozenset(v for v in range(n) if part[v] == part[0])
        out[side] = out.get(side, Fraction(0)) + pr
    return out


def cycle(n: int) -> list[Edge]:
    return [(i, (i + 1) % n) for i in range(n)]


def all_simple_graphs(n: int) -> list[list[Edge]]:
    pairs = list(combinations(range(n), 2))
    return [[pairs[i] for i in range(len(pairs)) if mask >> i & 1] for mask in range(1 << len(pairs))]
