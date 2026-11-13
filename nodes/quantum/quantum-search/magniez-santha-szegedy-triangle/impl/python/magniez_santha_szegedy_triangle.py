# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/magniez-santha-szegedy-triangle/. The authors are listed in prov/A5A7MR.jsonl.
"""The Magniez-Santha-Szegedy triangle algorithm: its classical parts, its query count, and an
exact simulation of the outer quantum walk on small graphs.

The graph is a symmetric 0/1 adjacency matrix adj on the vertices 0..n-1. A query reads one
entry adj[u][v]. The outer walk of lines L2 to L6 is simulated exactly on the states |A>|x>
of Ambainis's walk; the check of line L4 is run classically there, and its quantum cost
c(r) = sqrt(n) r^(2/3) is counted by the formula. The same walk, with another marked set, is
the graph collision walk of line L8.
"""

import math
import random
from fractions import Fraction
from itertools import combinations

# ---------- brute force ----------


def triangles(adj) -> list[tuple[int, int, int]]:
    n = len(adj)
    return [(a, b, c) for a, b, c in combinations(range(n), 3) if adj[a][b] and adj[b][c] and adj[a][c]]


def random_graph(n: int, p: float, rng: random.Random) -> list[list[int]]:
    adj = [[0] * n for _ in range(n)]
    for u, v in combinations(range(n), 2):
        adj[u][v] = adj[v][u] = int(rng.random() < p)
    return adj


# ---------- the classical meaning of the check ----------


def graph_collision(adj, a_set, f) -> tuple[int, int] | None:
    """A pair u, u' in a_set with f(u) = f(u') = 1 and uu' an edge of G restricted to a_set."""
    for u, w in combinations(sorted(a_set), 2):
        if f(u) and f(w) and adj[u][w]:
            return u, w
    return None


def check(adj, a_set) -> tuple[int, int, int] | None:
    """CHECK(A): a triangle with an edge inside A, or None. Lines L7 to L9 do this with queries."""
    for v in range(len(adj)):  # @line L7
        pair = graph_collision(adj, a_set, lambda u: adj[u][v])  # @line L8
        if pair:
            return pair[0], pair[1], v  # @line L9
    return None


# ---------- the data structure and its query counts ----------


class Data:
    """D(A): the edges of G inside A, with a count of the queries that built it."""

    def __init__(self, adj, a_set):
        self.adj, self.a, self.queries = adj, set(a_set), 0
        self.edges = {}
        for u, w in combinations(sorted(self.a), 2):
            self.edges[(u, w)] = self.read(u, w)

    def read(self, u, w):
        self.queries += 1
        return self.adj[u][w]

    def add(self, x):
        for u in self.a:
            self.edges[(min(u, x), max(u, x))] = self.read(u, x)
        self.a.add(x)

    def remove(self, x):
        self.a.discard(x)
        for u in self.a:
            self.read(u, x)  # uncompute the stored bit, one more query
            del self.edges[(min(u, x), max(u, x))]


def setup_cost(r: int) -> int:
    return r * (r - 1) // 2


def step_cost(r: int) -> int:
    """One step of the walk adds a vertex (r queries) and removes one (r queries)."""
    return 2 * r


# ---------- Ambainis's walk on r-subsets, simulated exactly ----------


def _diffuse(state, n, key_set):
    """Diffusion of the coin x over key_set(mask), for every set register mask."""
    out = {}
    groups = {}
    for (mask, x), amp in state.items():
        groups.setdefault(mask, {})[x] = amp
    for mask, coins in groups.items():
        t = key_set(mask)
        total = sum(coins.get(y, 0) for y in t)
        for y in t:
            v = 2 * total / len(t) - coins.get(y, 0)
            if v:
                out[(mask, y)] = v
    return out


def walk_step(state, n):
    """Diffuse x over S - A, add x to A, diffuse x over A, remove x from A."""
    outside = lambda m: [y for y in range(n) if not m >> y & 1]
    inside = lambda m: [y for y in range(n) if m >> y & 1]
    state = _diffuse(state, n, outside)
    state = {(m | 1 << x, x): a for (m, x), a in state.items()}
    state = _diffuse(state, n, inside)
    return {(m & ~(1 << x), x): a for (m, x), a in state.items()}


def johnson_search(n: int, r: int, marked, t1: int, t2: int) -> dict[int, float]:
    """Lines L2 to L6 with marked(A) for the phase flip. Returns the distribution of the measured A."""
    sets = [sum(1 << i for i in c) for c in combinations(range(n), r)]
    amp = 1 / math.sqrt(len(sets) * (n - r))
    state = {(m, x): amp for m in sets for x in range(n) if not m >> x & 1}  # @line L2
    flip = {m for m in sets if marked(frozenset(i for i in range(n) if m >> i & 1))}
    for _ in range(t1):  # @line L3
        state = {(m, x): (-a if m in flip else a) for (m, x), a in state.items()}  # @line L4
        for _ in range(t2):
            state = walk_step(state, n)  # @line L5
    dist = {}
    for (m, _), a in state.items():
        dist[m] = dist.get(m, 0) + abs(a) ** 2
    return dist


def mss_triangle(adj, t1: int, t2: int, r: int | None, rng: random.Random):
    """The whole algorithm on a small graph. Returns (a triangle or None, the query count)."""
    n = len(adj)
    r = r or mss_r(n)
    dist = johnson_search(n, r, lambda a: check(adj, a) is not None, t1, t2)
    masks = sorted(dist)
    m = rng.choices(masks, weights=[dist[k] for k in masks])[0]
    a_set = {i for i in range(n) if m >> i & 1}
    queries = setup_cost(r) + t1 * t2 * step_cost(r) + (t1 + 1) * check_cost(n, r)
    return check(adj, a_set), queries  # @line L6


# ---------- the query count ----------


def mss_r(n: int) -> int:
    return max(2, math.ceil(n ** 0.6))  # @line L1


def check_cost(n: int, r: int) -> float:
    """c(r) = sqrt(n) r^(2/3): Grover over v, each round a graph collision walk on A."""
    return math.sqrt(n) * r ** (2 / 3)


def graph_collision_cost(r: int, q: int) -> float:
    """Ambainis's walk on q-subsets of A: setup q, update 1, check 0."""
    return q + (r / q) * math.sqrt(q)


def total_cost(n: int, r: int, c=None) -> float:
    """s(r) + (n/r) (c(r) + sqrt(r) u(r)) with s = r^2, u = r and c = sqrt(n) r^(2/3) by default."""
    c = check_cost(n, r) if c is None else c
    return r * r + (n / r) * (c + math.sqrt(r) * r)


def best_exponent(terms) -> tuple[Fraction, Fraction]:
    """Minimize max over the terms (c0 + c1 a) for a in [0, 1], exactly. Each term is (c0, c1)."""
    cands = {Fraction(0), Fraction(1)}
    for (p0, p1), (q0, q1) in combinations(terms, 2):
        if p1 != q1:
            a = (q0 - p0) / (p1 - q1)
            if 0 <= a <= 1:
                cands.add(a)
    return min(((max(c0 + c1 * a for c0, c1 in terms), a) for a in cands))[::-1]


# exponents of n in s(r), (n/r) c(r) and (n/r) sqrt(r) u(r) with r = n^a
MSS_TERMS = [(Fraction(0), Fraction(2)), (Fraction(3, 2), Fraction(-1, 3)), (Fraction(1), Fraction(1, 2))]
# the same walk with the plain check c(r) = sqrt(n) r (Grover over v and the pairs of A)
PLAIN_TERMS = [(Fraction(0), Fraction(2)), (Fraction(3, 2), Fraction(0)), (Fraction(1), Fraction(1, 2))]
