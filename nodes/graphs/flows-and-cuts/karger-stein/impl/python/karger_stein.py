# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/karger-stein/. The authors are listed in prov/QPM3H8.jsonl.

import itertools
import math
import random


def karger_stein(
    n: int,
    edges: list[tuple[int, int, float]],
    runs: int | None = None,
    rng: random.Random | None = None,
) -> tuple[float, set[int]]:
    """Global minimum cut of an undirected graph by recursive contraction.

    Vertices are 0 .. n-1 with n >= 2, and edges (u, v, w) are undirected with
    weight w >= 0, an integer or a real number. Parallel edges add up and
    self-loops are ignored. Returns (value, S): S is a nonempty proper subset of
    the vertices and value is the exact weight of its cut. The value is a
    minimum with high probability; it is never below the minimum. The default
    number of runs is ceil(log2(n))^2 + 1.
    """
    if n < 2:
        raise ValueError("need at least two vertices")
    rng = rng or random.Random()
    w = [[0] * n for _ in range(n)]
    for u, v, c in edges:
        if c < 0:
            raise ValueError("weights must be nonnegative")
        if u != v:
            w[u][v] += c
            w[v][u] += c
    if runs is None:
        runs = math.ceil(math.log2(n)) ** 2 + 1
    groups = [frozenset([v]) for v in range(n)]
    best, best_set = None, set()  # @line L1
    for _ in range(runs):  # @line L2
        value, side = recursive_contract([row[:] for row in w], list(groups), rng)  # @line L3
        if best is None or value < best:
            best, best_set = value, set(side)
    return best, best_set  # @line L4


def recursive_contract(w: list[list[float]], groups: list[frozenset[int]], rng: random.Random) -> tuple[float, frozenset[int]]:
    """One run on the graph with weight matrix w; vertex i stands for groups[i]."""
    k = len(groups)  # @line L5
    if k <= 6:  # @line L6
        return brute_force_cut(w, groups)
    t = math.ceil(1 + k / math.sqrt(2))  # @line L7
    results = []
    for _ in range(2):  # @line L8
        w2, g2 = contract(w, groups, t, rng)
        if w2 is None:  # no edge left: g2 is a side whose cut has weight 0
            results.append((0, g2))
        else:
            results.append(recursive_contract(w2, g2, rng))
    return min(results, key=lambda r: r[0])  # @line L9


def contract(w, groups, t, rng):
    """Contract random edges, chosen with probability proportional to weight, down to t vertices.

    Returns a new (matrix, groups). If no edge of positive weight is left while
    more than t vertices remain, the graph is disconnected and the group of any
    vertex is a cut of weight 0; then (None, that group) is returned.
    """
    w = [row[:] for row in w]
    groups = list(groups)
    alive = list(range(len(groups)))
    deg = [sum(row) for row in w]
    while len(alive) > t:  # @line L10
        total = sum(deg[v] for v in alive)
        if total == 0:
            return None, groups[alive[0]]
        u = pick(alive, [deg[v] for v in alive], total, rng)  # @line L11
        v = pick(alive, [w[u][x] for x in alive], deg[u], rng)
        groups[u] = groups[u] | groups[v]
        for x in alive:
            w[u][x] += w[v][x]
            w[x][u] = w[u][x]
        deg[u] += deg[v] - 2 * w[u][u]
        w[u][u] = 0
        alive.remove(v)
    w2 = [[w[a][b] for b in alive] for a in alive]  # @line L12
    return w2, [groups[a] for a in alive]


def pick(items, weights, total, rng):
    """An item chosen with probability weight / total; total is positive."""
    if all(isinstance(x, int) for x in weights):
        r = rng.randrange(total)
    else:
        r = rng.random() * total
    acc = 0
    last = None
    for item, x in zip(items, weights):
        if x > 0:
            acc += x
            last = item
            if r < acc:
                return item
    return last


def brute_force_cut(w, groups):
    """The exact minimum cut of a graph with at most six vertices."""
    k = len(groups)
    best, best_side = None, None
    for r in range(k - 1):
        for extra in itertools.combinations(range(1, k), r):
            side = {0, *extra}
            value = sum(w[a][b] for a in side for b in range(k) if b not in side)
            if best is None or value < best:
                best, best_side = value, side
    return best, frozenset().union(*(groups[a] for a in best_side))
