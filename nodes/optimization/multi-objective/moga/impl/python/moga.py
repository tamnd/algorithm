# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/moga/. The authors are listed in prov/0EWQ9V.jsonl.

"""MOGA, the multi-objective genetic algorithm of Fonseca and Fleming (1993), on real vectors.

All objectives are minimized. The rank of a member is one plus the number of
members that dominate it. Raw fitness is linear in the position of the sorted
population, averaged inside each rank, then shared inside each rank by the
niche count in the normalized objective space, and scaled so that the total
fitness of each rank does not change. Parents are drawn by stochastic
universal sampling.
"""

import math
import random
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


def ff_rank(images: Sequence[Vector]) -> list[int]:
    """Fonseca-Fleming rank: 1 + the number of members that dominate each member."""
    return [1 + sum(1 for z in images if dominates(z, y)) for y in images]


def raw_fitness(ranks: Sequence[int]) -> list[int]:
    """Sort by rank (stable) and give positions 1, 2, ..., N the values N, N-1, ..., 1."""
    n = len(ranks)
    order = sorted(range(n), key=lambda i: ranks[i])
    raw = [0] * n
    for pos, i in enumerate(order):
        raw[i] = n - pos
    return raw


def average_by_rank(raw: Sequence[float], ranks: Sequence[int]) -> list:
    """Replace the raw fitness of each member by the mean over the members of its rank."""
    groups: dict[int, list[int]] = {}
    for i, r in enumerate(ranks):
        groups.setdefault(r, []).append(i)
    out = [0] * len(raw)
    for members in groups.values():
        mean = sum(raw[i] for i in members) / len(members)
        for i in members:
            out[i] = mean
    return out


def niche_counts(images: Sequence[Vector], ranks: Sequence[int], sigma: float) -> list[float]:
    """m(i) = sum over members j of the same rank of sh(d(i, j)), sh(d) = 1 - d/sigma for d < sigma.

    Distances are Euclidean after scaling each objective by its range in the population.
    """
    p = len(images[0])
    lo = [min(y[k] for y in images) for k in range(p)]
    span = [max(y[k] for y in images) - lo[k] for k in range(p)]
    scaled = [[(y[k] - lo[k]) / span[k] if span[k] > 0 else 0.0 for k in range(p)] for y in images]
    out = []
    for i, a in enumerate(scaled):
        m = 0.0
        for j, b in enumerate(scaled):
            if ranks[j] == ranks[i]:
                d = math.dist(a, b)
                if d < sigma:
                    m += 1 - d / sigma
        out.append(m)
    return out


def share_and_scale(base: Sequence[float], m: Sequence[float], ranks: Sequence[int]) -> list[float]:
    """Divide by the niche count, then scale each rank back to its old total."""
    shared = [b / c for b, c in zip(base, m)]
    out = [0.0] * len(base)
    for r in set(ranks):
        members = [i for i in range(len(base)) if ranks[i] == r]
        scale = sum(base[i] for i in members) / sum(shared[i] for i in members)
        for i in members:
            out[i] = shared[i] * scale
    return out


def moga_fitness(images: Sequence[Vector], sigma: float) -> list[float]:
    ranks = ff_rank(images)
    base = average_by_rank(raw_fitness(ranks), ranks)
    return share_and_scale(base, niche_counts(images, ranks, sigma), ranks)


def sus(weights: Sequence[float], k: int, rng: random.Random) -> list[int]:
    """Stochastic universal sampling of k indices with probabilities proportional to weights."""
    total = sum(weights)
    step = total / k
    start = rng.random() * step
    out, acc, i = [], weights[0], 0
    for t in range(k):
        point = start + t * step
        while acc <= point and i < len(weights) - 1:
            i += 1
            acc += weights[i]
        out.append(i)
    return out


def moga(
    f: Callable[[Vector], Vector],
    n: int,
    lower: Sequence[float],
    upper: Sequence[float],
    sigma: float,
    generations: int,
    rng: random.Random,
    mutation_sigma: float = 0.1,
    on_generation: Callable[[list], None] | None = None,
) -> list[tuple[tuple, tuple]]:
    """Run MOGA in the box [lower, upper]. Return the non-dominated (x, f(x)) of the last population."""
    d = len(lower)

    def clip(v: float, i: int) -> float:
        return min(upper[i], max(lower[i], v))

    pop = []
    for _ in range(n):  # @line L1
        x = tuple(rng.uniform(lower[i], upper[i]) for i in range(d))
        pop.append((x, tuple(f(x))))
    for _ in range(generations):  # @line L2
        images = [y for _, y in pop]
        ranks = ff_rank(images)  # @line L3
        raw = raw_fitness(ranks)  # @line L4
        base = average_by_rank(raw, ranks)  # @line L5
        m = niche_counts(images, ranks, sigma)  # @line L6
        phi = share_and_scale(base, m, ranks)  # @line L7
        parents = [pop[i][0] for i in sus(phi, n, rng)]  # @line L8
        rng.shuffle(parents)
        off = []
        for k in range(n):  # @line L9
            u, v = parents[k], parents[(k + 1) % n]
            t = rng.random()
            c = [t * a + (1 - t) * b for a, b in zip(u, v)]
            x = tuple(clip(c[i] + rng.gauss(0, mutation_sigma) * (upper[i] - lower[i]), i) for i in range(d))
            off.append((x, tuple(f(x))))
        pop = off
        if on_generation is not None:
            on_generation(pop)
    return [(x, y) for x, y in pop if not any(dominates(z, y) for _, z in pop)]  # @line L10
