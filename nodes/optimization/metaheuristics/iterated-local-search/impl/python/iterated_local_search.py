# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterated-local-search/. The authors are listed in prov/AVNAXF.jsonl.

import math
import random
from collections.abc import Callable, Iterable
from typing import TypeVar

S = TypeVar("S")


def iterated_local_search(
    x0: S,
    f: Callable[[S], float],
    local_search: Callable[[S], S],
    perturb: Callable[[S, random.Random], S],
    iterations: int,
    rng: random.Random,
    accept: str = "better",
) -> tuple[S, float, list[tuple[S, float, bool]]]:
    """Minimize f by iterated local search.

    Each iteration perturbs the current local optimum, runs the local search
    from the result, and decides by the acceptance rule which local optimum
    to keep: "better" accepts it if f is strictly lower, "always" accepts it
    every time (a random walk over local optima). Returns (best, f(best), log)
    with one (new local optimum, its value, accepted) entry per iteration.
    Cost: `iterations` + 1 runs of the local search and `iterations` perturbations.
    """
    if accept not in ("better", "always"):
        raise ValueError("accept must be 'better' or 'always'")
    x = local_search(x0)  # @line L1
    fx = f(x)
    best, f_best = x, fx
    log: list[tuple[S, float, bool]] = []
    for _ in range(iterations):  # @line L2
        y = perturb(x, rng)  # @line L3
        z = local_search(y)  # @line L4
        fz = f(z)
        ok = accept == "always" or fz < fx  # @line L5
        if ok:
            x, fx = z, fz
        if fx < f_best:  # @line L6
            best, f_best = x, fx
        log.append((z, fz, ok))
    return best, f_best, log  # @line L7


def double_bridge(tour: tuple[int, ...], rng: random.Random) -> tuple[int, ...]:
    """The double-bridge kick: cut the tour into A B C D and reconnect as A D C B.

    The cut points 1 <= p1 < p2 < p3 <= n - 1 are uniform; needs n >= 4.
    """
    p1, p2, p3 = sorted(rng.sample(range(1, len(tour)), 3))
    return double_bridge_at(tour, p1, p2, p3)


def double_bridge_at(tour: tuple[int, ...], p1: int, p2: int, p3: int) -> tuple[int, ...]:
    """A = tour[:p1], B = tour[p1:p2], C = tour[p2:p3], D = tour[p3:]; return A D C B."""
    return tour[:p1] + tour[p3:] + tour[p2:p3] + tour[p1:p2]


def two_opt_neighbors(tour: tuple[int, ...]) -> Iterable[tuple[int, ...]]:
    """The 2-opt neighborhood: reverse tour[i..j] for 1 <= i < j <= n - 1, (i, j) != (1, n - 1)."""
    n = len(tour)
    for i in range(1, n - 1):
        for j in range(i + 1, n):
            if i == 1 and j == n - 1:
                continue
            yield tour[:i] + tour[i : j + 1][::-1] + tour[j + 1 :]


def two_opt_descent(f: Callable[[tuple[int, ...]], float]) -> Callable[[tuple[int, ...]], tuple[int, ...]]:
    """Best-improvement 2-opt local search, ending at a 2-opt local minimum."""

    def run(tour: tuple[int, ...]) -> tuple[int, ...]:
        ft = f(tour)
        while True:
            nxt = min(two_opt_neighbors(tour), key=f, default=None)
            if nxt is None or f(nxt) >= ft:
                return tour
            tour, ft = nxt, f(nxt)

    return run


def distance_matrix(points: list[tuple[int, int]]) -> list[list[int]]:
    """Euclidean distances rounded to the nearest integer."""
    return [[round(math.dist(p, q)) for q in points] for p in points]


def tour_length(d: list[list[int]], tour: tuple[int, ...]) -> int:
    """The length of the closed tour under the distance matrix d."""
    return sum(d[tour[k]][tour[(k + 1) % len(tour)]] for k in range(len(tour)))
