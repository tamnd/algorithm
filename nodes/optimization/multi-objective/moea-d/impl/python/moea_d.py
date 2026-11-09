# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/moea-d/. The authors are listed in prov/EZEF0D.jsonl.

"""MOEA/D of Zhang and Li (2007) with the Tchebycheff approach.

All objectives are minimized. Subproblem i minimizes
g(x | w_i, z) = max_m w_i[m] * |f_m(x) - z_m|, where z is the best value of
each objective found so far. A child made from two neighbours of i replaces
the current solution of each neighbour subproblem j that it does not make
worse. The external population E keeps the non-dominated images of all
points evaluated.
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


def weakly_dominates(a: Vector, b: Vector) -> bool:
    return all(u <= v for u, v in zip(a, b))


def simplex_weights(p: int, h: int) -> list[tuple[Fraction, ...]]:
    """All weight vectors with p coordinates in multiples of 1/h that sum to 1, for h >= 1."""
    out = []

    def rec(prefix: list[int], left: int) -> None:
        if len(prefix) == p - 1:
            out.append(tuple(Fraction(v, h) for v in prefix + [left]))
            return
        for v in range(left + 1):
            rec(prefix + [v], left - v)

    rec([], h)
    return out


def tchebycheff(y: Vector, w: Vector, z: Vector):
    """g(x | w, z) for the image y = f(x)."""
    return max(wm * abs(ym - zm) for ym, wm, zm in zip(y, w, z))


def neighbourhoods(weights: Sequence[Vector], t: int) -> list[list[int]]:
    """B(i): the indices of the t weight vectors nearest to weight i (itself first), ties by index."""
    out = []
    for i, wi in enumerate(weights):
        d = sorted(range(len(weights)), key=lambda j: (sum((a - b) ** 2 for a, b in zip(wi, weights[j])), j != i, j))
        out.append(d[:t])
    return out


def update_neighbours(pop: list, child: tuple, nb: Sequence[int], weights: Sequence[Vector], z: Vector) -> list[int]:
    """Replace x_j by the child for each j in nb where the child is no worse for subproblem j."""
    done = []
    for j in nb:  # @line L7
        if tchebycheff(child[1], weights[j], z) <= tchebycheff(pop[j][1], weights[j], z):  # @line L8
            pop[j] = child
            done.append(j)
    return done


def update_external(ext: list, y: Vector) -> None:
    """Remove the images that y dominates; add y if no image weakly dominates it."""
    if any(weakly_dominates(e, y) for e in ext):
        return
    ext[:] = [e for e in ext if not dominates(y, e)]
    ext.append(tuple(y))


def moea_d(
    init: Callable[[random.Random], object],
    f: Callable,
    vary: Callable[[object, object, random.Random], object],
    weights: Sequence[Vector],
    t: int,
    generations: int,
    rng: random.Random,
    on_child: Callable[[int, tuple, list, list, list], None] | None = None,
) -> tuple[list, list]:
    """Run MOEA/D. Return the external population and the final (x, f(x)) of each subproblem."""
    n = len(weights)
    b = neighbourhoods(weights, t)  # @line L1
    pop = []
    for _ in range(n):  # @line L2
        x = init(rng)
        pop.append((x, tuple(f(x))))
    p = len(pop[0][1])
    z = [min(y[m] for _, y in pop) for m in range(p)]
    ext: list = []
    for _, y in pop:
        update_external(ext, y)
    for _ in range(generations):  # @line L3
        for i in range(n):  # @line L4
            k, l = rng.choice(b[i]), rng.choice(b[i])
            xy = vary(pop[k][0], pop[l][0], rng)  # @line L5
            child = (xy, tuple(f(xy)))
            for m in range(p):  # @line L6
                z[m] = min(z[m], child[1][m])
            before = list(pop)
            update_neighbours(pop, child, b[i], weights, z)
            update_external(ext, child[1])  # @line L9
            if on_child is not None:
                on_child(i, child, list(z), before, pop)
    return ext, pop  # @line L10


def blend_gauss(lower: Sequence[float], upper: Sequence[float], sigma: float = 0.1):
    """A simple real-valued variation: blend crossover of two parents, Gaussian mutation, clipping."""

    def vary(u, v, r: random.Random):
        w = r.random()
        return tuple(
            min(hi, max(lo, w * a + (1 - w) * c + r.gauss(0, sigma) * (hi - lo)))
            for a, c, lo, hi in zip(u, v, lower, upper)
        )

    return vary


def zdt1(x: Vector) -> tuple:
    g = 1 + 9 * sum(x[1:]) / (len(x) - 1)
    return (x[0], g * (1 - math.sqrt(x[0] / g)))
