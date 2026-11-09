# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/guided-local-search/. The authors are listed in prov/0JTKYZ.jsonl.

import math
from collections.abc import Callable, Hashable, Iterable
from dataclasses import dataclass
from fractions import Fraction
from typing import Generic, TypeVar

S = TypeVar("S")


@dataclass
class Step(Generic[S]):
    """One iteration: the features penalized, then the new local minimum of the augmented objective."""

    penalized: list[Hashable]
    x: S
    g: float
    h: Fraction


def guided_local_search(
    x0: S,
    g: Callable[[S], float],
    features: Callable[[S], Iterable[Hashable]],
    cost: Callable[[Hashable], float],
    local_search: Callable[[S, Callable[[S], Fraction]], S],
    a: Fraction,
    iterations: int,
) -> tuple[S, float, dict[Hashable, int], list[Step[S]]]:
    """Minimize g by guided local search (Voudouris and Tsang).

    features(x) lists the features present in x, and cost(e) is the cost of
    feature e. After each local minimum x, every feature of x with the
    largest utility cost(e) / (1 + p[e]) gets one more penalty point. The
    local search then minimizes h(y) = g(y) + lam * (sum of p[e] over the
    features of y), with lam = a * g(x1) / (number of features of x1) for
    the first local minimum x1. Returns (best, g(best), penalties, log).
    Exact rational arithmetic keeps ties exact. Cost: `iterations` + 1 runs
    of the local search plus O(m) per iteration for m features in x.
    """
    if iterations < 0:
        raise ValueError("iterations must be non-negative")
    p: dict[Hashable, int] = {}  # @line L1
    x = local_search(x0, lambda y: Fraction(g(y)))
    best, g_best = x, g(x)
    lam = Fraction(a) * Fraction(g(x)) / max(1, len(list(features(x))))  # @line L2

    def h(y: S) -> Fraction:
        return Fraction(g(y)) + lam * sum(p.get(e, 0) for e in features(y))

    log: list[Step[S]] = []
    for _ in range(iterations):  # @line L3
        util = {e: Fraction(cost(e)) / (1 + p.get(e, 0)) for e in features(x)}  # @line L4
        top = max(util.values(), default=None)
        penalized = [e for e, u in util.items() if u == top]
        for e in penalized:  # @line L5
            p[e] = p.get(e, 0) + 1
        x = local_search(x, h)  # @line L6
        if g(x) < g_best:  # @line L7
            best, g_best = x, g(x)
        log.append(Step(penalized, x, g(x), h(x)))
    return best, g_best, dict(p), log  # @line L8


def two_opt_neighbors(tour: tuple[int, ...]) -> Iterable[tuple[int, ...]]:
    """The 2-opt neighborhood: reverse tour[i..j] for 1 <= i < j <= n - 1, (i, j) != (1, n - 1)."""
    n = len(tour)
    for i in range(1, n - 1):
        for j in range(i + 1, n):
            if i == 1 and j == n - 1:
                continue
            yield tour[:i] + tour[i : j + 1][::-1] + tour[j + 1 :]


def two_opt_descent(tour: tuple[int, ...], h: Callable[[tuple[int, ...]], Fraction]) -> tuple[int, ...]:
    """Best-improvement 2-opt on the objective h; ends at a 2-opt local minimum of h."""
    ht = h(tour)
    while True:
        nxt = min(two_opt_neighbors(tour), key=h, default=None)
        if nxt is None or h(nxt) >= ht:
            return tour
        tour, ht = nxt, h(nxt)


def tour_edges(tour: tuple[int, ...]) -> list[tuple[int, int]]:
    """The features of a tour: its edges, each written (smaller city, larger city)."""
    n = len(tour)
    return [(min(tour[k], tour[(k + 1) % n]), max(tour[k], tour[(k + 1) % n])) for k in range(n)]


def distance_matrix(points: list[tuple[int, int]]) -> list[list[int]]:
    """Euclidean distances rounded to the nearest integer."""
    return [[round(math.dist(p, q)) for q in points] for p in points]


def tour_length(d: list[list[int]], tour: tuple[int, ...]) -> int:
    """The length of the closed tour under the distance matrix d."""
    return sum(d[tour[k]][tour[(k + 1) % len(tour)]] for k in range(len(tour)))
