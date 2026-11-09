# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/differential-evolution/. The authors are listed in prov/R0J5VG.jsonl.

"""Differential evolution, the DE/rand/1/bin strategy of Storn and Price, with box bounds."""

import math
import random
from typing import Callable, Sequence

Vector = list[float]


def random_population(lo: Sequence[float], hi: Sequence[float], size: int, rng: random.Random) -> list[Vector]:
    """size points drawn uniformly from the box [lo, hi]."""
    return [[rng.uniform(a, b) for a, b in zip(lo, hi)] for _ in range(size)]


def repair(v: Vector, base: Sequence[float], lo: Sequence[float], hi: Sequence[float]) -> Vector:
    """Move each coordinate of v that leaves the box halfway from the base vector to the bound.

    If base is in the box, the result is in the box.
    """
    out = []
    for vj, bj, a, b in zip(v, base, lo, hi):
        if vj < a:
            vj = (a + bj) / 2
        elif vj > b:
            vj = (b + bj) / 2
        out.append(vj)
    return out


def binomial_crossover(x: Sequence[float], v: Sequence[float], cr: float, rng: random.Random) -> Vector:
    """Take each coordinate from v with probability cr, and coordinate jrand always."""
    n = len(x)
    jrand = rng.randrange(n)
    return [v[j] if (j == jrand or rng.random() < cr) else x[j] for j in range(n)]


def differential_evolution(
    f: Callable[[Sequence[float]], float],
    pop0: Sequence[Sequence[float]],
    F: float,
    cr: float,
    generations: int,
    rng: random.Random,
    bounds: tuple[Sequence[float], Sequence[float]] | None = None,
    trace: list | None = None,
) -> tuple[Vector, float]:
    """Minimize f with DE/rand/1/bin from the population pop0. Return (best point, its value).

    With bounds = (lo, hi) and pop0 inside the box, every point stays inside the box.
    If trace is a list, append a copy of (population, values) after each generation.
    """
    pop = [list(x) for x in pop0]  # @line L1
    fit = [f(x) for x in pop]
    size = len(pop)
    for _ in range(generations):  # @line L2
        new_pop, new_fit = [], []
        for i in range(size):  # @line L3
            r1, r2, r3 = rng.sample([j for j in range(size) if j != i], 3)  # @line L4
            v = [a + F * (b - c) for a, b, c in zip(pop[r1], pop[r2], pop[r3])]  # @line L5
            if bounds is not None:
                v = repair(v, pop[r1], bounds[0], bounds[1])  # @line L6
            u = binomial_crossover(pop[i], v, cr, rng)  # @line L7
            fu = f(u)
            if fu <= fit[i]:  # @line L8
                new_pop.append(u)
                new_fit.append(fu)
            else:
                new_pop.append(pop[i])
                new_fit.append(fit[i])
        pop, fit = new_pop, new_fit  # @line L9
        if trace is not None:
            trace.append(([x[:] for x in pop], fit[:]))
    k = min(range(size), key=lambda i: fit[i])
    return pop[k], fit[k]  # @line L10


def sphere(x: Sequence[float]) -> float:
    return sum(t * t for t in x)


def rastrigin(x: Sequence[float]) -> float:
    return 10 * len(x) + sum(t * t - 10 * math.cos(2 * math.pi * t) for t in x)
