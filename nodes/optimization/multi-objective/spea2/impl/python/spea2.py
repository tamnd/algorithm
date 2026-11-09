# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spea2/. The authors are listed in prov/3QZDDW.jsonl.

"""SPEA2 of Zitzler, Laumanns and Thiele (2001).

All objectives are minimized. Each member i of U = P + A gets the strength
S(i), the number of members it dominates, the raw fitness R(i), the sum of
the strengths of its dominators, and the density D(i) = 1 / (sigma_k + 2),
where sigma_k is the distance to its k-th nearest neighbour in objective
space. F = R + D, smaller is better, and F < 1 exactly for the non-dominated
members. The archive keeps exactly m members.
"""

import bisect
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


def fitness(images: Sequence[Vector], k: int) -> tuple[list[int], list[int], list[float], list[float]]:
    """Strength S, raw fitness R, density D and fitness F = R + D of each member."""
    n = len(images)
    dom = [[dominates(images[i], images[j]) for j in range(n)] for i in range(n)]
    s = [sum(row) for row in dom]  # @line L4
    r = [sum(s[j] for j in range(n) if dom[j][i]) for i in range(n)]  # @line L5
    d = []
    for i in range(n):
        dist = sorted(math.dist(images[i], images[j]) for j in range(n) if j != i)
        sigma = dist[min(k, len(dist)) - 1] if dist else 0.0
        d.append(1 / (sigma + 2))
    return s, r, d, [r[i] + d[i] for i in range(n)]  # @line L6


def truncate(images: Sequence[Vector], members: Sequence[int], m: int) -> list[int]:
    """Remove, one at a time, the member whose sorted distances to the others are lexicographically smallest."""
    left = list(members)
    dd = {(i, j): math.dist(images[i], images[j]) for i in left for j in left}
    near = {i: sorted((dd[i, j], j) for j in left if j != i) for i in left}
    while len(left) > m:  # @line L9
        victim = min(left, key=lambda i: ([x for x, _ in near[i]], i))
        left.remove(victim)
        del near[victim]
        for i in left:
            lst = near[i]
            lst.pop(bisect.bisect_left(lst, (dd[i, victim], victim)))
    return left


def environmental_selection(images: Sequence[Vector], f: Sequence[float], m: int) -> list[int]:
    """Indices of the next archive: all members with F < 1, filled up by F or cut by truncation."""
    keep = [i for i in range(len(images)) if f[i] < 1]  # @line L7
    if len(keep) < m:  # @line L8
        rest = sorted((i for i in range(len(images)) if f[i] >= 1), key=lambda i: (f[i], i))
        keep += rest[: m - len(keep)]
    return truncate(images, keep, m)


def spea2(
    init: Callable[[random.Random], object],
    f: Callable,
    vary: Callable[[list, random.Random], list],
    n: int,
    m: int,
    generations: int,
    rng: random.Random,
    on_generation: Callable[[list, list], None] | None = None,
) -> list:
    """Run SPEA2 with population size n and archive size m. Return the non-dominated archive members."""
    pop = []
    for _ in range(n):  # @line L1
        x = init(rng)
        pop.append((x, tuple(f(x))))
    archive: list = []
    k = math.isqrt(n + m)
    for t in range(generations + 1):  # @line L2
        union = pop + archive  # @line L3
        images = [y for _, y in union]
        _, _, _, fit = fitness(images, k)
        keep = environmental_selection(images, fit, m)
        archive = [union[i] for i in keep]
        afit = [fit[i] for i in keep]
        if on_generation is not None:
            on_generation(pop, archive)
        if t == generations:  # @line L10
            return [(x, y) for x, y in archive if not any(dominates(z, y) for _, z in archive)]
        pool = []
        for _ in range(n):  # @line L11
            a, b = rng.randrange(len(archive)), rng.randrange(len(archive))
            if afit[a] == afit[b]:
                a = rng.choice((a, b))
            pool.append(archive[a if afit[a] <= afit[b] else b][0])
        pop = [(x, tuple(f(x))) for x in vary(pool, rng)[:n]]
    return archive


def blend_gauss(lower: Sequence[float], upper: Sequence[float], sigma: float = 0.1):
    """A simple real-valued variation: blend crossover of neighbours, Gaussian mutation, clipping."""

    def vary(parents: list, r: random.Random) -> list:
        out = []
        k = len(parents)
        for i in range(k):
            u, v = parents[i], parents[(i + 1) % k]
            w = r.random()
            out.append(
                tuple(
                    min(hi, max(lo, w * a + (1 - w) * b + r.gauss(0, sigma) * (hi - lo)))
                    for a, b, lo, hi in zip(u, v, lower, upper)
                )
            )
        return out

    return vary
