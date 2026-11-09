# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multi-objective-simulated-annealing/. The authors are listed in prov/DTW645.jsonl.

"""Multi-objective simulated annealing with an archive (Serafini 1994; Ulungu et al. 1999).

All objectives are minimized. One current solution moves to a random
neighbour with probability pi(delta, T), where delta = f(y) - f(x) and the
rule combines the objectives with weights w >= 0:

    sum rule:     pi = min(1, exp(-sum_m w_m delta_m / T))
    product rule: pi = prod_m min(1, exp(-w_m delta_m / T))

The archive holds the non-dominated images of all solutions evaluated.
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


def weakly_dominates(a: Vector, b: Vector) -> bool:
    return all(u <= v for u, v in zip(a, b))


def accept_probability(fx: Vector, fy: Vector, w: Vector, temp: float, rule: str = "sum") -> float:
    """Probability of the move from image fx to image fy at temperature temp > 0."""
    if rule == "sum":
        s = sum(wm * (b - a) for wm, a, b in zip(w, fx, fy))
        return 1.0 if s <= 0 else math.exp(-s / temp)
    if rule == "product":
        s = sum(max(0, wm * (b - a)) for wm, a, b in zip(w, fx, fy))
        return 1.0 if s == 0 else math.exp(-s / temp)
    raise ValueError(rule)


def archive_update(archive: list, y: tuple) -> None:
    """Remove the members that y dominates; add y = (x, f(x)) if no member weakly dominates it."""
    if any(weakly_dominates(z, y[1]) for _, z in archive):
        return
    archive[:] = [(x, z) for x, z in archive if not dominates(y[1], z)]
    archive.append(y)


def mosa(
    init: Callable[[random.Random], object],
    f: Callable,
    neighbour: Callable[[object, random.Random], object],
    w: Vector,
    t0: float,
    alpha: float,
    steps: int,
    rng: random.Random,
    rule: str = "sum",
    on_step: Callable[[tuple, tuple, list, float], None] | None = None,
) -> list:
    """Run MOSA with weights w, start temperature t0 and geometric cooling factor alpha. Return the archive."""
    x0 = init(rng)
    cur = (x0, tuple(f(x0)))  # @line L1
    archive = [cur]
    temp = t0
    for _ in range(steps):  # @line L2
        xy = neighbour(cur[0], rng)
        y = (xy, tuple(f(xy)))  # @line L3
        archive_update(archive, y)  # @line L4
        pi = accept_probability(cur[1], y[1], w, temp, rule)  # @line L5
        if pi >= 1 or rng.random() < pi:  # @line L6
            cur = y
        if on_step is not None:
            on_step(cur, y, archive, temp)
        temp *= alpha  # @line L7
    return archive  # @line L8
