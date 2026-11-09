# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nsga-ii/. The authors are listed in prov/736BVW.jsonl.

"""NSGA-II of Deb, Pratap, Agarwal and Meyarivan (2002).

All objectives are minimized. The generic loop works on any representation:
make_offspring(parents, rng) returns new solutions. The real-coded version
uses simulated binary crossover and polynomial mutation, both in their simple
forms with clipping to the bounds.
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


def fast_non_dominated_sort(images: Sequence[Vector]) -> list[list[int]]:
    """Return the fronts F1, F2, ... as lists of indices. O(p N^2) time."""
    n = len(images)
    beats: list[list[int]] = [[] for _ in range(n)]
    count = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            if dominates(images[i], images[j]):
                beats[i].append(j)
                count[j] += 1
            elif dominates(images[j], images[i]):
                beats[j].append(i)
                count[i] += 1
    fronts = [[i for i in range(n) if count[i] == 0]]
    while fronts[-1]:
        nxt = []
        for i in fronts[-1]:
            for j in beats[i]:
                count[j] -= 1
                if count[j] == 0:
                    nxt.append(j)
        fronts.append(nxt)
    fronts.pop()
    return fronts


def crowding_distance(images: Sequence[Vector], front: Sequence[int]) -> dict[int, float]:
    """Crowding distance of each index of one front. Extremes get infinity."""
    d = {i: 0.0 for i in front}
    if len(front) <= 2:
        return {i: math.inf for i in front}
    for m in range(len(images[front[0]])):
        order = sorted(front, key=lambda i: images[i][m])
        lo, hi = images[order[0]][m], images[order[-1]][m]
        d[order[0]] = d[order[-1]] = math.inf
        if hi == lo:
            continue
        for k in range(1, len(order) - 1):
            d[order[k]] += (images[order[k + 1]][m] - images[order[k - 1]][m]) / (hi - lo)
    return d


def rank_and_crowding(images: Sequence[Vector]) -> tuple[list[int], list[float]]:
    """Front number and crowding distance (inside its front) of each index."""
    rank = [0] * len(images)
    dist = [0.0] * len(images)
    for r, front in enumerate(fast_non_dominated_sort(images), start=1):
        cd = crowding_distance(images, front)
        for i in front:
            rank[i], dist[i] = r, cd[i]
    return rank, dist


def survival(images: Sequence[Vector], n: int) -> list[int]:
    """Indices of the n members of R kept by NSGA-II: whole fronts first, then the least crowded of the next front."""
    kept: list[int] = []
    fronts = fast_non_dominated_sort(images)  # @line L6
    k = 0  # @line L7
    while k < len(fronts) and len(kept) + len(fronts[k]) <= n:  # @line L8
        kept.extend(fronts[k])  # @line L9
        k += 1
    if len(kept) < n:
        cd = crowding_distance(images, fronts[k])  # @line L10
        order = sorted(fronts[k], key=lambda i: -cd[i])
        kept.extend(order[: n - len(kept)])  # @line L11
    return kept


def crowded_tournament(rank: Sequence[int], dist: Sequence[float], rng: random.Random) -> int:
    """Binary tournament on (lower rank, then larger crowding distance); ties at random."""
    a, b = rng.randrange(len(rank)), rng.randrange(len(rank))
    if (rank[a], -dist[a]) < (rank[b], -dist[b]):
        return a
    if (rank[b], -dist[b]) < (rank[a], -dist[a]):
        return b
    return rng.choice((a, b))


def nsga_ii_loop(
    pop: list,
    f: Callable,
    make_offspring: Callable[[list, random.Random], list],
    n: int,
    generations: int,
    rng: random.Random,
    on_generation: Callable[[list, list], None] | None = None,
) -> list:
    """Run NSGA-II from a population of n pairs (x, f(x)). Return the first front of the last population."""
    rank, dist = rank_and_crowding([y for _, y in pop])  # @line L2
    for _ in range(generations):  # @line L3
        parents = [pop[crowded_tournament(rank, dist, rng)][0] for _ in range(n)]  # @line L4
        off = [(x, tuple(f(x))) for x in make_offspring(parents, rng)][:n]
        union = pop + off  # @line L5
        keep = survival([y for _, y in union], n)
        pop = [union[i] for i in keep]
        rank, dist = rank_and_crowding([y for _, y in pop])
        if on_generation is not None:
            on_generation(pop, union)
    return [pop[i] for i in range(len(pop)) if rank[i] == 1]  # @line L12


def sbx(x1: Vector, x2: Vector, eta: float, lower: Vector, upper: Vector, rng: random.Random):
    """Simulated binary crossover of two real vectors, each variable with probability 1/2, then clipping."""
    c1, c2 = list(x1), list(x2)
    for i in range(len(x1)):
        if rng.random() < 0.5:
            u = rng.random()
            beta = (2 * u) ** (1 / (eta + 1)) if u <= 0.5 else (1 / (2 * (1 - u))) ** (1 / (eta + 1))
            a, b = x1[i], x2[i]
            c1[i] = 0.5 * ((1 + beta) * a + (1 - beta) * b)
            c2[i] = 0.5 * ((1 - beta) * a + (1 + beta) * b)
        c1[i] = min(upper[i], max(lower[i], c1[i]))
        c2[i] = min(upper[i], max(lower[i], c2[i]))
    return tuple(c1), tuple(c2)


def polynomial_mutation(x: Vector, eta: float, pm: float, lower: Vector, upper: Vector, rng: random.Random):
    """Polynomial mutation of each variable with probability pm, then clipping."""
    out = list(x)
    for i in range(len(x)):
        if rng.random() < pm:
            u = rng.random()
            delta = (2 * u) ** (1 / (eta + 1)) - 1 if u < 0.5 else 1 - (2 * (1 - u)) ** (1 / (eta + 1))
            out[i] = min(upper[i], max(lower[i], x[i] + delta * (upper[i] - lower[i])))
    return tuple(out)


def nsga_ii(
    f: Callable[[Vector], Vector],
    n: int,
    lower: Sequence[float],
    upper: Sequence[float],
    generations: int,
    rng: random.Random,
    eta_c: float = 15.0,
    eta_m: float = 20.0,
    crossover_rate: float = 0.9,
    on_generation: Callable[[list, list], None] | None = None,
) -> list:
    """Real-coded NSGA-II in the box [lower, upper]."""
    d = len(lower)
    pm = 1 / d

    def make_offspring(parents, r):
        out = []
        for k in range(0, len(parents), 2):
            u, v = parents[k], parents[(k + 1) % len(parents)]
            if r.random() < crossover_rate:
                u, v = sbx(u, v, eta_c, lower, upper, r)
            out.append(polynomial_mutation(u, eta_m, pm, lower, upper, r))
            out.append(polynomial_mutation(v, eta_m, pm, lower, upper, r))
        return out

    pop = []
    for _ in range(n):  # @line L1
        x = tuple(rng.uniform(lower[i], upper[i]) for i in range(d))
        pop.append((x, tuple(f(x))))
    return nsga_ii_loop(pop, f, make_offspring, n, generations, rng, on_generation)
