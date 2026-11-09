# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vega/. The authors are listed in prov/3S4BQF.jsonl.

"""VEGA, the vector evaluated genetic algorithm of Schaffer (1985), on real vectors.

All objectives are minimized. Each generation fills p parts of the mating pool,
part i by selection on objective i alone, shuffles the pool, and replaces the
population by the offspring. Selection here is a binary tournament on one
objective; Schaffer used proportional selection, whose expected shares are
given by proportional_shares.
"""

import random
from fractions import Fraction
from typing import Callable, Sequence

Vector = Sequence[float]


def dominates(a: Vector, b: Vector) -> bool:
    """Return True when a dominates b (minimization)."""
    strict = False
    for u, v in zip(a, b):
        if u > v:
            return False
        if u < v:
            strict = True
    return strict


def part_sizes(n: int, p: int) -> list[int]:
    """Sizes of the p parts of a pool of n; the first n mod p parts get one more."""
    return [n // p + (1 if i < n % p else 0) for i in range(p)]


def vega(
    f: Callable[[Vector], Vector],
    p: int,
    n: int,
    lower: Sequence[float],
    upper: Sequence[float],
    generations: int,
    rng: random.Random,
    crossover_rate: float = 0.9,
    sigma: float = 0.1,
    on_generation: Callable[[list], None] | None = None,
) -> list[tuple[tuple, tuple]]:
    """Run VEGA in the box [lower, upper]. Return the non-dominated (x, f(x)) of the last population."""
    d = len(lower)

    def clip(v: float, i: int) -> float:
        return min(upper[i], max(lower[i], v))

    pop = []
    for _ in range(n):  # @line L1
        x = tuple(rng.uniform(lower[i], upper[i]) for i in range(d))
        pop.append((x, tuple(f(x))))
    for _ in range(generations):  # @line L2
        pool = []  # @line L3
        for obj, size in enumerate(part_sizes(n, p)):  # @line L4
            for _ in range(size):  # @line L5
                a, b = rng.choice(pop), rng.choice(pop)
                pool.append(a[0] if a[1][obj] <= b[1][obj] else b[0])
        rng.shuffle(pool)  # @line L6
        off = []
        for k in range(0, n, 2):  # @line L7
            u = pool[k]
            v = pool[k + 1] if k + 1 < n else pool[0]
            if rng.random() < crossover_rate:
                t = rng.random()
                c1 = tuple(t * a + (1 - t) * b for a, b in zip(u, v))
                c2 = tuple((1 - t) * a + t * b for a, b in zip(u, v))
            else:
                c1, c2 = tuple(u), tuple(v)
            for c in (c1, c2)[: min(2, n - k)]:
                x = tuple(clip(c[i] + rng.gauss(0, sigma) * (upper[i] - lower[i]), i) for i in range(d))
                off.append((x, tuple(f(x))))
        pop = off  # @line L8
        if on_generation is not None:
            on_generation(pop)
    return [(x, y) for x, y in pop if not any(dominates(z, y) for _, z in pop)]  # @line L9


def proportional_shares(g: Sequence[Sequence[Fraction]], n: int) -> list[Fraction]:
    """Expected number of copies of each member in a VEGA pool with proportional selection.

    g[k][i] > 0 is the fitness (to maximize) of member k for objective i. Part i
    has n / p slots, and each slot picks k with probability g[k][i] / S_i.
    """
    p = len(g[0])
    sums = [sum(row[i] for row in g) for i in range(p)]
    return [sum(Fraction(n, p) * row[i] / sums[i] for i in range(p)) for row in g]


def weighted_sum_shares(g: Sequence[Sequence[Fraction]], n: int) -> list[Fraction]:
    """Expected copies under proportional selection on h_k = sum_i g[k][i] / S_i."""
    p = len(g[0])
    sums = [sum(row[i] for row in g) for i in range(p)]
    h = [sum(Fraction(row[i]) / sums[i] for i in range(p)) for row in g]
    total = sum(h)
    return [n * v / total for v in h]
