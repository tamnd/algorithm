# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ant-colony-optimization/. The authors are listed in prov/H2R48A.jsonl.

import random
from collections.abc import Callable, Sequence

Matrix = list[list[float]]


def tour_length(dist: Sequence[Sequence[float]], tour: Sequence[int]) -> float:
    """The length of the closed tour, the last city joined back to the first."""
    return sum(dist[tour[k]][tour[(k + 1) % len(tour)]] for k in range(len(tour)))


def choice_probabilities(
    i: int, candidates: Sequence[int], tau: Matrix, dist: Sequence[Sequence[float]], alpha: float, beta: float
) -> list[float]:
    """The probability of each candidate j: tau_ij^alpha eta_ij^beta over the sum, with eta_ij = 1 / d_ij."""
    weights = [tau[i][j] ** alpha * (1.0 / dist[i][j]) ** beta for j in candidates]
    total = sum(weights)
    return [wt / total for wt in weights]


def choose(probs: Sequence[float], u: float) -> int:
    """The index k with prefix(k - 1) <= u < prefix(k), for u in [0, 1)."""
    acc = 0.0
    for k, p in enumerate(probs):
        acc += p
        if u < acc:
            return k
    return max(k for k, p in enumerate(probs) if p > 0)  # only through rounding


def build_tour(tau: Matrix, dist: Sequence[Sequence[float]], alpha: float, beta: float, rng: random.Random) -> list[int]:
    """One ant: start at a random city and add unvisited cities by choice_probabilities."""
    n = len(dist)
    tour = [rng.randrange(n)]
    unvisited = [j for j in range(n) if j != tour[0]]
    while unvisited:
        probs = choice_probabilities(tour[-1], unvisited, tau, dist, alpha, beta)
        j = unvisited.pop(choose(probs, rng.random()))
        tour.append(j)
    return tour


def ant_colony_optimization(
    dist: Sequence[Sequence[float]],
    ants: int,
    alpha: float,
    beta: float,
    rho: float,
    tau0: float,
    tau_min: float,
    tau_max: float,
    iterations: int,
    rng: random.Random,
    on_iteration: Callable[[int, Matrix, list[int], float], None] | None = None,
) -> tuple[list[int], float, list[float]]:
    """MAX-MIN Ant System for the symmetric traveling salesman problem.

    Each iteration, `ants` ants build tours; the pheromone evaporates by the
    factor 1 - rho; the best-so-far tour deposits 1 / L on its edges; and
    every value is clamped to [tau_min, tau_max]. With tau_min = 0 and
    tau_max = inf there is no clamp. Precondition: n >= 3, d_ij > 0 for
    i != j and symmetric, 0 < rho <= 1, tau_min <= tau0 <= tau_max.
    Returns (best tour, its length, history of the best length).
    Cost: O(iterations * ants * n^2) time and O(n^2) space.
    """
    n = len(dist)
    tau = [[tau0] * n for _ in range(n)]  # @line L1
    best: list[int] = []
    best_len = float("inf")
    history: list[float] = []
    for t in range(iterations):  # @line L2
        tours = [build_tour(tau, dist, alpha, beta, rng) for _ in range(ants)]  # @line L3
        lengths = [tour_length(dist, s) for s in tours]
        k = min(range(ants), key=lambda a: lengths[a])  # @line L4
        if lengths[k] < best_len:  # @line L5
            best, best_len = tours[k], lengths[k]
        for i in range(n):
            for j in range(n):
                tau[i][j] *= 1.0 - rho  # @line L6
        for a in range(n):
            i, j = best[a], best[(a + 1) % n]
            tau[i][j] += 1.0 / best_len  # @line L7
            tau[j][i] = tau[i][j]
        for i in range(n):
            for j in range(n):
                tau[i][j] = min(tau_max, max(tau_min, tau[i][j]))  # @line L8
        history.append(best_len)
        if on_iteration is not None:
            on_iteration(t, [row[:] for row in tau], list(best), best_len)
    return best, best_len, history  # @line L9
