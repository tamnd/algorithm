# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spea/. The authors are listed in prov/Y5WMKW.jsonl.

"""SPEA, the strength Pareto evolutionary algorithm of Zitzler and Thiele (1999).

All objectives are minimized. The external archive holds the non-dominated
solutions found so far, cut to at most m members by average-linkage
clustering in objective space. A solution of the archive has a strength, the
share of the population it covers; a member of the population has fitness 1
plus the strengths of the archive members that cover it. Smaller is better.
"""

import math
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


def covers(a: Vector, b: Vector) -> bool:
    """Return True when a weakly dominates b: a is no worse in every objective."""
    return all(u <= v for u, v in zip(a, b))


def update_archive(archive: list, pop: list) -> list:
    """Add the non-dominated members of pop, then drop dominated members and repeated images."""
    new = [s for s in pop if not any(dominates(z, s[1]) for _, z in pop)]  # @line L3
    cand = archive + new
    out: list = []
    for x, y in cand:  # @line L4
        if any(dominates(z, y) for _, z in cand):
            continue
        if any(z == y for _, z in out):
            continue
        out.append((x, y))
    return out


def cluster_reduce(archive: list, m: int) -> list:
    """Average-linkage clustering to m clusters; keep from each the member nearest on average to the rest."""
    k = len(archive)
    if k <= m:
        return list(archive)
    pts = [y for _, y in archive]
    base = [[math.dist(pts[i], pts[j]) for j in range(k)] for i in range(k)]
    clusters = {i: [i] for i in range(k)}
    dist = {(i, j): base[i][j] for i in range(k) for j in range(i + 1, k)}
    while len(clusters) > m:  # @line L5
        (a, b) = min(dist, key=lambda e: (dist[e], e))
        na, nb = len(clusters[a]), len(clusters[b])
        for c in clusters:
            if c in (a, b):
                continue
            dac = dist[(min(a, c), max(a, c))]
            dbc = dist[(min(b, c), max(b, c))]
            dist[(min(a, c), max(a, c))] = (na * dac + nb * dbc) / (na + nb)
            del dist[(min(b, c), max(b, c))]
        del dist[(a, b)]
        clusters[a] += clusters.pop(b)
    out = []
    for members in clusters.values():
        rep = min(members, key=lambda i: (sum(base[i][j] for j in members), i))
        out.append(archive[rep])
    return out


def strengths(archive_images: Sequence[Vector], pop_images: Sequence[Vector]) -> list[Fraction]:
    """s(a) = number of population members that a covers, divided by N + 1."""
    n = len(pop_images)
    return [Fraction(sum(1 for y in pop_images if covers(a, y)), n + 1) for a in archive_images]  # @line L6


def population_fitness(archive_images: Sequence[Vector], s: Sequence[float], pop_images: Sequence[Vector]) -> list[float]:
    """F(x) = 1 + the sum of the strengths of the archive members that cover x."""
    return [1 + sum(si for a, si in zip(archive_images, s) if covers(a, y)) for y in pop_images]  # @line L7


def spea(
    init: Callable[[random.Random], object],
    f: Callable,
    vary: Callable[[list, random.Random], list],
    n: int,
    m: int,
    generations: int,
    rng: random.Random,
    on_generation: Callable[[list, list], None] | None = None,
) -> list:
    """Run SPEA with population size n and archive bound m. Return the archive as (x, f(x)) pairs."""
    pop = []
    for _ in range(n):  # @line L1
        x = init(rng)
        pop.append((x, tuple(f(x))))
    archive: list = []
    for _ in range(generations):  # @line L2
        archive = cluster_reduce(update_archive(archive, pop), m)
        if on_generation is not None:
            on_generation(pop, archive)
        a_img = [y for _, y in archive]
        s = strengths(a_img, [y for _, y in pop])
        fit = population_fitness(a_img, s, [y for _, y in pop])
        both = [(x, v) for (x, _), v in zip(archive, s)] + [(x, v) for (x, _), v in zip(pop, fit)]
        pool = []
        for _ in range(n):  # @line L8
            u, w = rng.choice(both), rng.choice(both)
            if u[1] == w[1]:
                u = rng.choice((u, w))
            pool.append(u[0] if u[1] <= w[1] else w[0])
        pop = [(x, tuple(f(x))) for x in vary(pool, rng)[:n]]  # @line L9
    archive = cluster_reduce(update_archive(archive, pop), m)  # @line L10
    if on_generation is not None:
        on_generation(pop, archive)
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
