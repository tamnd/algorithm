# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-influence-maximization/. The authors are listed in prov/DDTH3Z.jsonl.

import random
from collections.abc import Callable, Hashable, Iterable


def greedy_influence_maximization(
    vertices: Iterable[int], k: int, sigma: Callable[[frozenset[int]], float]
) -> list[int]:
    """Return k seeds chosen greedily for the spread function sigma, in the order picked.

    sigma maps a frozenset of vertices to its (expected or estimated) spread.
    Each round adds the vertex with the largest marginal gain
    sigma(S + v) - sigma(S); ties go to the smallest vertex. If k exceeds the
    number of vertices, every vertex is returned. The function makes at most
    k * n + 1 calls to sigma, and is a (1 - 1/e)-approximation whenever sigma
    is monotone and submodular with sigma(empty set) = 0 and the calls are exact.
    """
    pool = sorted(set(vertices))
    if k < 0:
        raise ValueError("k must be non-negative")
    seeds: list[int] = []  # @line L1
    chosen: set[int] = set()
    base = sigma(frozenset())
    for _ in range(min(k, len(pool))):  # @line L2
        best, best_gain, best_value = -1, 0.0, base
        for v in pool:  # @line L3
            if v in chosen:
                continue
            value = sigma(frozenset(chosen | {v}))
            gain = value - base  # @line L4
            if best < 0 or gain > best_gain:  # @line L5
                best, best_gain, best_value = v, gain, value
        seeds.append(best)  # @line L6
        chosen.add(best)
        base = best_value
    return seeds  # @line L7


def _out_lists(n: int, arcs: Iterable[tuple[int, int, float]]) -> list[list[tuple[int, float]]]:
    out: list[list[tuple[int, float]]] = [[] for _ in range(n)]
    for u, v, p in arcs:
        if not (0 <= u < n and 0 <= v < n):
            raise ValueError("arc end out of range")
        if not 0 <= p <= 1:
            raise ValueError("probability or weight outside [0, 1]")
        out[u].append((v, p))
    return out


def ic_spread(
    n: int, arcs: list[tuple[int, int, float]], seeds: Iterable[int], runs: int, rng: random.Random
) -> float:
    """Monte Carlo estimate of the expected spread under the independent cascade model.

    arcs holds (u, v, p): when u becomes active it activates v with probability p,
    once. Each run is a breadth-first cascade; the result is the mean number of
    active vertices over the runs, seeds included. Time O(runs * (n + m)).
    """
    out = _out_lists(n, arcs)
    start = sorted(set(seeds))
    if runs <= 0 or not start:
        return 0.0
    total = 0
    for _ in range(runs):
        active = [False] * n
        for s in start:
            active[s] = True
        frontier = list(start)
        count = len(start)
        while frontier:
            nxt = []
            for u in frontier:
                for v, p in out[u]:
                    if not active[v] and rng.random() < p:
                        active[v] = True
                        nxt.append(v)
                        count += 1
            frontier = nxt
        total += count
    return total / runs


def lt_spread(
    n: int, arcs: list[tuple[int, int, float]], seeds: Iterable[int], runs: int, rng: random.Random
) -> float:
    """Monte Carlo estimate of the expected spread under the linear threshold model.

    arcs holds (u, v, b): u pushes v with weight b, and the weights into each
    vertex sum to at most 1. Each run draws a uniform threshold in [0, 1] for
    every vertex; a vertex turns active once the weight from its active
    in-neighbours reaches its threshold. Time O(runs * (n + m)).
    """
    out = _out_lists(n, arcs)
    into = [0.0] * n
    for _, v, b in arcs:
        into[v] += b
    if any(x > 1 + 1e-9 for x in into):
        raise ValueError("the weights into a vertex sum to more than 1")
    start = sorted(set(seeds))
    if runs <= 0 or not start:
        return 0.0
    total = 0
    for _ in range(runs):
        theta = [rng.random() for _ in range(n)]
        pressure = [0.0] * n
        active = [False] * n
        for s in start:
            active[s] = True
        frontier = list(start)
        count = len(start)
        while frontier:
            nxt = []
            for u in frontier:
                for v, b in out[u]:
                    if active[v]:
                        continue
                    pressure[v] += b
                    if pressure[v] >= theta[v]:
                        active[v] = True
                        nxt.append(v)
                        count += 1
            frontier = nxt
        total += count
    return total / runs


def memoized(sigma: Callable[[frozenset[int]], float]) -> Callable[[frozenset[int]], float]:
    """Wrap a spread function so that each seed set is evaluated once."""
    cache: dict[Hashable, float] = {}

    def f(s: frozenset[int]) -> float:
        if s not in cache:
            cache[s] = sigma(s)
        return cache[s]

    return f
