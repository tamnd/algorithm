# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simulated-annealing/. The authors are listed in prov/R8R2C0.jsonl.

import math
import random
from typing import Callable, Sequence, TypeVar

S = TypeVar("S")


def acceptance_probability(delta: float, temperature: float) -> float:
    """The Metropolis rule: 1 for a move that does not go up, else exp(-delta / T)."""
    if delta <= 0:
        return 1.0
    if temperature <= 0:
        return 0.0
    return math.exp(-delta / temperature)


def geometric_schedule(t0: float, alpha: float) -> Callable[[int], float]:
    """T(k) = t0 * alpha^(k - 1) for k = 1, 2, ..."""
    return lambda k: t0 * alpha ** (k - 1)


def logarithmic_schedule(c: float) -> Callable[[int], float]:
    """T(k) = c / ln(k + 1) for k = 1, 2, ... (the schedule of Hajek's theorem)."""
    return lambda k: c / math.log(k + 1)


def simulated_annealing(
    x0: S,
    energy: Callable[[S], float],
    neighbor: Callable[[S, random.Random], S],
    schedule: Callable[[int], float],
    steps: int,
    rng: random.Random,
    trace: list | None = None,
) -> tuple[S, float]:
    """Minimize energy by simulated annealing. Return (best state, best energy).

    If trace is a list, append (k, T, current energy, best energy) after each step.
    """
    x, ex = x0, energy(x0)  # @line L1
    best, eb = x, ex
    for k in range(1, steps + 1):  # @line L2
        t = schedule(k)
        y = neighbor(x, rng)  # @line L3
        ey = energy(y)
        delta = ey - ex  # @line L4
        if delta <= 0 or rng.random() < acceptance_probability(delta, t):  # @line L5
            x, ex = y, ey  # @line L6
            if ex < eb:  # @line L7
                best, eb = x, ex
        if trace is not None:
            trace.append((k, t, ex, eb))
    return best, eb  # @line L8


# The Metropolis chain at a fixed temperature on a small state space.


def boltzmann(energies: Sequence[float], temperature: float) -> list[float]:
    """The Boltzmann distribution pi(i) = exp(-E(i)/T) / Z."""
    m = min(energies)
    w = [math.exp(-(e - m) / temperature) for e in energies]
    z = sum(w)
    return [x / z for x in w]


def metropolis_matrix(
    energies: Sequence[float], neighbors: Sequence[Sequence[int]], temperature: float
) -> list[list[float]]:
    """Transition matrix of the Metropolis chain with a uniform neighbor proposal.

    Every state must have the same number of neighbors, so that the proposal is symmetric.
    """
    n = len(energies)
    p = [[0.0] * n for _ in range(n)]
    for i in range(n):
        r = 1.0 / len(neighbors[i])
        for j in neighbors[i]:
            p[i][j] += r * acceptance_probability(energies[j] - energies[i], temperature)
        p[i][i] += 1.0 - sum(p[i])
    return p


def metropolis_visits(
    energies: Sequence[float],
    neighbors: Sequence[Sequence[int]],
    temperature: float,
    start: int,
    steps: int,
    rng: random.Random,
) -> list[int]:
    """Run the Metropolis chain at a fixed temperature and count the visits to each state."""
    counts = [0] * len(energies)
    x = start
    for _ in range(steps):
        y = rng.choice(neighbors[x])
        if rng.random() < acceptance_probability(energies[y] - energies[x], temperature):
            x = y
        counts[x] += 1
    return counts


def cycle_neighbors(n: int) -> list[list[int]]:
    return [[(i - 1) % n, (i + 1) % n] for i in range(n)]


def tour_length(tour: Sequence[int], dist: Sequence[Sequence[float]]) -> float:
    return sum(dist[tour[i - 1]][tour[i]] for i in range(len(tour)))


def two_opt_neighbor(tour: tuple, rng: random.Random) -> tuple:
    """Reverse a random segment tour[i..j] with 1 <= i < j <= n - 1 (city tour[0] stays first)."""
    n = len(tour)
    i, j = sorted(rng.sample(range(1, n), 2))
    return tour[:i] + tour[i : j + 1][::-1] + tour[j + 1 :]
