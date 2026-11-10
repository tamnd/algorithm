# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/streaming-triangle-counting/. The authors are listed in prov/1HBVC8.jsonl.
"""Neighborhood sampling for triangle counting (Pavan, Tangwongsan, Tirthapura, Wu 2013).

One estimator reads the edge stream once and keeps O(1) words:

- r1, a uniform random edge of the stream (a reservoir of size 1);
- c, the number of edges after r1 that share an endpoint with r1;
- r2, a uniform random edge among those c edges (a second reservoir);
- found, whether the edge that closes the wedge r1, r2 came after r2.

The estimate is m * c if found, else 0. It is unbiased for the number of
triangles. The mean of s independent estimators has variance at most
m * C * T / s, where C is the largest c over the edges.
"""

from __future__ import annotations

import random
from typing import Callable


def norm(e) -> tuple:
    u, v = e
    return (u, v) if u < v else (v, u)


def closing_edge(a, b):
    """The third edge of the triangle on the wedge a, b (they share one endpoint)."""
    shared = set(a) & set(b)
    if len(shared) != 1:
        return None
    x = (set(a) - shared).pop()
    y = (set(b) - shared).pop()
    return norm((x, y))


class NeighborhoodSampler:
    """One estimator. coin(p) must return True with probability p."""

    def __init__(self, coin: Callable[[float], bool]) -> None:
        self.coin = coin
        self.i = 0
        self.r1 = None
        self.r2 = None
        self.c = 0
        self.found = False

    def state(self) -> tuple:
        return (self.i, self.r1, self.r2, self.c, self.found)

    def process(self, e) -> None:
        e = norm(e)
        if e[0] == e[1]:
            raise ValueError("self-loops are not edges")
        self.i += 1  # @line L1
        if self.i == 1 or self.coin(1 / self.i):  # @line L2
            self.r1, self.r2, self.c, self.found = e, None, 0, False
            return
        if set(e) & set(self.r1):  # @line L3
            if self.r2 is not None and e == closing_edge(self.r1, self.r2):  # @line L4
                self.found = True
            self.c += 1  # @line L5
            if self.coin(1 / self.c):  # @line L6
                self.r2, self.found = e, False

    def estimate(self) -> int:
        return self.i * self.c if self.found else 0  # @line L7


def estimate_triangles(stream, s: int, rng: random.Random) -> float:
    """The mean of s independent neighborhood sampling estimators, in one pass."""
    coin = lambda p: p >= 1 or rng.random() < p
    samplers = [NeighborhoodSampler(coin) for _ in range(s)]
    for e in stream:
        for sm in samplers:
            sm.process(e)
    return sum(sm.estimate() for sm in samplers) / s  # @line L8


def count_triangles(edges) -> int:
    """Exact count by checking common neighbors, for the tests."""
    adj: dict = {}
    for u, v in edges:
        adj.setdefault(u, set()).add(v)
        adj.setdefault(v, set()).add(u)
    t = 0
    for u, v in {norm(e) for e in edges}:
        t += len(adj[u] & adj[v])
    return t // 3


def neighborhood_sizes(stream) -> list[int]:
    """c(e_j): the number of later edges that share an endpoint with e_j."""
    stream = [norm(e) for e in stream]
    return [sum(1 for f in stream[j + 1 :] if set(f) & set(e)) for j, e in enumerate(stream)]


def second_moment(stream) -> int:
    """E[X^2] = sum over triangles of m * c(first edge of the triangle in stream order)."""
    stream = [norm(e) for e in stream]
    pos = {e: j for j, e in enumerate(stream)}
    c = neighborhood_sizes(stream)
    m = len(stream)
    total = 0
    verts = sorted({x for e in stream for x in e})
    for a in range(len(verts)):
        for b in range(a + 1, len(verts)):
            for d in range(b + 1, len(verts)):
                tri = [norm((verts[a], verts[b])), norm((verts[a], verts[d])), norm((verts[b], verts[d]))]
                if all(t in pos for t in tri):
                    first = min(pos[t] for t in tri)
                    total += m * c[first]
    return total
