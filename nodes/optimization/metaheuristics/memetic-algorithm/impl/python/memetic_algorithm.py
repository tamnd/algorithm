# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/memetic-algorithm/. The authors are listed in prov/P2XYTJ.jsonl.

import random
from collections.abc import Callable, Sequence

Dist = Sequence[Sequence[float]]
EPS = 1e-12


def tour_length(dist: Dist, tour: Sequence[int]) -> float:
    """The length of the closed tour, the last city joined back to the first."""
    return sum(dist[tour[k]][tour[(k + 1) % len(tour)]] for k in range(len(tour)))


def canonical(tour: Sequence[int]) -> tuple[int, ...]:
    """The same cycle written from city 0, in the direction whose second city is smaller."""
    n = len(tour)
    s = list(tour).index(0)
    fwd = tuple(tour[(s + k) % n] for k in range(n))
    bwd = tuple(tour[(s - k) % n] for k in range(n))
    return min(fwd, bwd)


def order_crossover(a: Sequence[int], b: Sequence[int], i: int, j: int) -> list[int]:
    """OX: keep a[i..j]; fill the other positions, from j + 1 on and wrapping, with the missing cities in b's order from j + 1."""
    n = len(a)
    child = list(a)
    kept = set(a[i : j + 1])
    rest = [b[(j + 1 + k) % n] for k in range(n) if b[(j + 1 + k) % n] not in kept]
    for k, city in enumerate(rest):
        child[(j + 1 + k) % n] = city
    return child


def two_opt_delta(dist: Dist, tour: Sequence[int], i: int, j: int) -> float:
    """The change of length when tour[i+1..j] is reversed, that is, edges (i, i+1) and (j, j+1) become (i, j) and (i+1, j+1)."""
    n = len(tour)
    a, b, c, d = tour[i], tour[i + 1], tour[j], tour[(j + 1) % n]
    return dist[a][c] + dist[b][d] - dist[a][b] - dist[c][d]


def two_opt(dist: Dist, tour: Sequence[int]) -> list[int]:
    """First-improvement 2-opt: apply improving moves until none has delta < -EPS. Cost: O(n^2) per pass, n >= 4."""
    t = list(tour)
    n = len(t)
    improved = True
    while improved:
        improved = False
        for i in range(n - 1):
            for j in range(i + 2, n if i > 0 else n - 1):
                if two_opt_delta(dist, t, i, j) < -EPS:
                    t[i + 1 : j + 1] = reversed(t[i + 1 : j + 1])
                    improved = True
    return t


def is_two_opt_optimal(dist: Dist, tour: Sequence[int]) -> bool:
    """True when no 2-opt move shortens the tour by more than EPS."""
    n = len(tour)
    return all(two_opt_delta(dist, tour, i, j) >= -EPS for i in range(n - 1) for j in range(i + 2, n if i > 0 else n - 1))


def memetic_algorithm(
    dist: Dist,
    pop_size: int,
    steps: int,
    p_m: float,
    rng: random.Random,
    on_step: Callable[[int, list[list[int]], list[float]], None] | None = None,
) -> tuple[list[int], float, list[float]]:
    """Steady-state memetic algorithm for the symmetric TSP.

    The initial tours and every child are improved by 2-opt, and the improved
    tour is kept (Lamarckian). A child from order crossover of two random
    parents, with a random swap of two cities with probability p_m, replaces
    the worst tour if it is shorter and not already in the population.
    Precondition: n >= 4, symmetric distances, pop_size >= 2.
    Returns (best tour, its length, history of the best length).
    Cost: O((pop_size + steps) * I * n^2 + steps * pop_size * n) time, I the
    number of 2-opt passes per local search, and O(pop_size * n) space.
    """
    n = len(dist)
    pop = [two_opt(dist, rng.sample(range(n), n)) for _ in range(pop_size)]  # @line L1
    lengths = [tour_length(dist, t) for t in pop]
    history = [min(lengths)]
    for s in range(steps):  # @line L2
        p, q = rng.sample(range(pop_size), 2)  # @line L3
        i, j = sorted(rng.sample(range(n), 2))
        c = order_crossover(pop[p], pop[q], i, j)  # @line L4
        if rng.random() < p_m:  # @line L5
            u, v = rng.sample(range(n), 2)
            c[u], c[v] = c[v], c[u]
        c = two_opt(dist, c)  # @line L6
        lc = tour_length(dist, c)
        w = max(range(pop_size), key=lambda k: lengths[k])  # @line L7
        if lc < lengths[w] - EPS and canonical(c) not in {canonical(t) for t in pop}:  # @line L8
            pop[w], lengths[w] = c, lc
        history.append(min(lengths))
        if on_step is not None:
            on_step(s, [list(t) for t in pop], list(lengths))
    b = min(range(pop_size), key=lambda k: lengths[k])
    return pop[b], lengths[b], history  # @line L9
