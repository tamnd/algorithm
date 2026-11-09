# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/npga/. The authors are listed in prov/H04GPP.jsonl.

"""NPGA, the niched Pareto genetic algorithm of Horn, Nafpliotis and Goldberg (1994), on real vectors.

All objectives are minimized. Each parent is the winner of a Pareto domination
tournament: two candidates are checked against a random comparison set of t
members. If exactly one candidate is dominated by the set, the other wins.
Otherwise the candidate with the smaller niche count wins, where the niche
count is taken over the images already in the mating pool (continuously
updated sharing).
"""

import math
import random
from fractions import Fraction
from math import comb
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


def dominated_by_set(y: Vector, comparison: Sequence[Vector]) -> bool:
    return any(dominates(z, y) for z in comparison)


def niche_count(y: Vector, pool: Sequence[Vector], sigma: float, lo: Sequence[float], span: Sequence[float]) -> float:
    """Sum of sh(d) = 1 - d/sigma over pool images closer than sigma, in the normalized objective space."""
    def scale(v):
        return [(v[k] - lo[k]) / span[k] if span[k] > 0 else 0.0 for k in range(len(v))]

    a = scale(y)
    m = 0.0
    for z in pool:
        d = math.dist(a, scale(z))
        if d < sigma:
            m += 1 - d / sigma
    return m


def tournament(
    images: Sequence[Vector], pool: Sequence[Vector], t: int, sigma: float, rng: random.Random,
    lo: Sequence[float], span: Sequence[float],
) -> int:
    """Return the index of the winner of one Pareto domination tournament."""
    n = len(images)
    a, b = rng.randrange(n), rng.randrange(n)  # @line L5
    comp = [images[i] for i in rng.sample(range(n), min(t, n))]
    da = dominated_by_set(images[a], comp)  # @line L6
    db = dominated_by_set(images[b], comp)
    if da and not db:  # @line L7
        return b
    if db and not da:  # @line L8
        return a
    ma = niche_count(images[a], pool, sigma, lo, span)  # @line L9
    mb = niche_count(images[b], pool, sigma, lo, span)
    if ma != mb:
        return a if ma < mb else b
    return rng.choice((a, b))


def prob_found_dominated(n: int, k: int, t: int) -> Fraction:
    """Probability that a member with k dominators is dominated by a random t-subset of n members."""
    return 1 - Fraction(comb(n - k, t), comb(n, t))


def npga(
    f: Callable[[Vector], Vector],
    n: int,
    lower: Sequence[float],
    upper: Sequence[float],
    t: int,
    sigma: float,
    generations: int,
    rng: random.Random,
    mutation_sigma: float = 0.1,
    on_generation: Callable[[list], None] | None = None,
) -> list[tuple[tuple, tuple]]:
    """Run NPGA in the box [lower, upper]. Return the non-dominated (x, f(x)) of the last population."""
    d = len(lower)

    def clip(v: float, i: int) -> float:
        return min(upper[i], max(lower[i], v))

    pop = []
    for _ in range(n):  # @line L1
        x = tuple(rng.uniform(lower[i], upper[i]) for i in range(d))
        pop.append((x, tuple(f(x))))
    for _ in range(generations):  # @line L2
        images = [y for _, y in pop]
        p = len(images[0])
        lo = [min(y[k] for y in images) for k in range(p)]
        span = [max(y[k] for y in images) - lo[k] for k in range(p)]
        pool: list[int] = []  # @line L3
        while len(pool) < n:  # @line L4
            pool.append(tournament(images, [images[i] for i in pool], t, sigma, rng, lo, span))
        off = []
        for k in range(n):  # @line L10
            u, v = pop[pool[k]][0], pop[pool[(k + 1) % n]][0]
            w = rng.random()
            c = [w * a + (1 - w) * b for a, b in zip(u, v)]
            x = tuple(clip(c[i] + rng.gauss(0, mutation_sigma) * (upper[i] - lower[i]), i) for i in range(d))
            off.append((x, tuple(f(x))))
        pop = off
        if on_generation is not None:
            on_generation(pop)
    return [(x, y) for x, y in pop if not any(dominates(z, y) for _, z in pop)]  # @line L11
