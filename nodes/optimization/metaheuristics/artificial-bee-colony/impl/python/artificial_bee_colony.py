# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/artificial-bee-colony/. The authors are listed in prov/DVD07D.jsonl.

import math
import random
from collections.abc import Callable, Sequence

Vector = list[float]


def abc_fitness(fx: float) -> float:
    """Karaboga's fitness for minimization: 1 / (1 + f) if f >= 0, else 1 + |f|. It is positive and decreases in f."""
    return 1.0 / (1.0 + fx) if fx >= 0 else 1.0 + abs(fx)


def roulette(weights: Sequence[float], u: float) -> int:
    """The index i with prefix(i - 1) <= u * total < prefix(i), for u in [0, 1) and positive weights."""
    target = u * sum(weights)
    acc = 0.0
    for i, wt in enumerate(weights):
        acc += wt
        if target < acc:
            return i
    return len(weights) - 1  # only through rounding


def neighbor(x: Sequence[Vector], i: int, k: int, j: int, phi: float, lower: Sequence[float], upper: Sequence[float]) -> Vector:
    """A copy of x[i] with coordinate j set to x_ij + phi (x_ij - x_kj), clipped to [lower_j, upper_j]."""
    v = list(x[i])
    v[j] = min(upper[j], max(lower[j], x[i][j] + phi * (x[i][j] - x[k][j])))
    return v


def artificial_bee_colony(
    f: Callable[[Sequence[float]], float],
    lower: Sequence[float],
    upper: Sequence[float],
    sources: int,
    limit: int,
    cycles: int,
    rng: random.Random,
    on_cycle: Callable[[int, list[Vector], list[float], list[int], int], None] | None = None,
) -> tuple[Vector, float, list[float]]:
    """Artificial bee colony (Karaboga 2005) for minimizing f on the box [lower, upper].

    Each cycle: every employed bee tries one neighbor of its source; the
    onlooker bees pick sources by a roulette wheel on abc_fitness and try a
    neighbor each; a source kept for more than `limit` failed tries is
    replaced by a random point (scout). Replacement is greedy and strict.
    Precondition: sources >= 2, lower[j] < upper[j].
    Returns (best point, its value, history of the best value per cycle).
    Cost: O(cycles * sources * (D + c + sources)) time for D variables and
    evaluation cost c, and O(sources * D) space.
    """
    d = len(lower)

    def random_point() -> Vector:
        return [rng.uniform(lower[j], upper[j]) for j in range(d)]

    x = [random_point() for _ in range(sources)]  # @line L1
    fx = [f(p) for p in x]
    trial = [0] * sources
    b = min(range(sources), key=lambda i: fx[i])
    best, best_f = list(x[b]), fx[b]
    history: list[float] = []

    def try_neighbor(i: int) -> None:
        k = rng.choice([s for s in range(sources) if s != i])
        j = rng.randrange(d)
        v = neighbor(x, i, k, j, rng.uniform(-1.0, 1.0), lower, upper)
        fv = f(v)
        if abc_fitness(fv) > abc_fitness(fx[i]):  # greedy selection
            x[i], fx[i], trial[i] = v, fv, 0
        else:
            trial[i] += 1

    for c in range(cycles):  # @line L2
        for i in range(sources):  # @line L3
            try_neighbor(i)
        fit = [abc_fitness(v) for v in fx]  # @line L4
        for _ in range(sources):  # @line L5
            try_neighbor(roulette(fit, rng.random()))
        for i in range(sources):  # @line L6
            if fx[i] < best_f:
                best, best_f = list(x[i]), fx[i]
        scout = -1
        s = max(range(sources), key=lambda i: trial[i])
        if trial[s] > limit:  # @line L7
            x[s] = random_point()
            fx[s], trial[s], scout = f(x[s]), 0, s
            if fx[s] < best_f:
                best, best_f = list(x[s]), fx[s]
        history.append(best_f)
        if on_cycle is not None:
            on_cycle(c, [list(p) for p in x], list(fx), list(trial), scout)
    return best, best_f, history  # @line L8


def sphere(x: Sequence[float]) -> float:
    return sum(v * v for v in x)


def rastrigin(x: Sequence[float]) -> float:
    return 10.0 * len(x) + sum(v * v - 10.0 * math.cos(2 * math.pi * v) for v in x)
