# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/online-gradient-descent/. The authors are listed in prov/X8NYQC.jsonl.

"""Online gradient descent (Zinkevich 2003) on an interval K = [lo, hi].

In round t the learner plays x_t, the adversary answers with the loss
f_t(x_t) and a subgradient g_t of f_t at x_t, and the learner moves to
x_{t+1} = clip(x_t - eta_t * g_t, lo, hi). The adversary is a function
adversary(t, x) -> (loss, subgradient), so it may depend on the point x_t.
Points and losses may be Fractions (exact) or floats.
"""

import math
from fractions import Fraction
from typing import Callable

Number = Fraction | float


def project(y: Number, lo: Number, hi: Number) -> Number:
    """Euclidean projection onto [lo, hi]."""
    if y < lo:
        return lo
    if y > hi:
        return hi
    return y


def online_gradient_descent(
    adversary: Callable[[int, Number], tuple[Number, Number]],
    rounds: int,
    lo: Number,
    hi: Number,
    step: Callable[[int], Number],
    x1: Number | None = None,
) -> tuple[list[Number], Number, list[Number]]:
    """Run OGD for the given number of rounds.

    Return the points x_1 .. x_T, the total loss, and the subgradients.
    Cost: O(1) per round plus the cost of the adversary.
    """
    if lo > hi:
        raise ValueError("empty interval")
    x = (Fraction(lo) + hi) / 2 if x1 is None else x1  # @line L1
    if not lo <= x <= hi:
        raise ValueError("x1 must lie in [lo, hi]")
    xs: list[Number] = []
    grads: list[Number] = []
    total: Number = 0
    for t in range(1, rounds + 1):  # @line L2
        xs.append(x)  # @line L3
        loss, g = adversary(t, x)  # @line L4
        total += loss
        grads.append(g)  # @line L5
        y = x - step(t) * g  # @line L6
        x = project(y, lo, hi)  # @line L7
    return xs, total, grads


def sqrt_step(diameter: float, lipschitz: float) -> Callable[[int], float]:
    """The step eta_t = D / (G sqrt t), which gives regret at most (3/2) G D sqrt T."""
    return lambda t: diameter / (lipschitz * math.sqrt(t))


def strongly_convex_step(lam: Number) -> Callable[[int], Number]:
    """The step eta_t = 1 / (lam t) for lam-strongly convex losses."""
    return lambda t: Fraction(1) / (lam * t)


def absolute_losses(zs: list[Number]) -> Callable[[int, Number], tuple[Number, Number]]:
    """The oblivious adversary f_t(x) = |x - z_t|, with subgradient sign(x - z_t)."""

    def adversary(t: int, x: Number) -> tuple[Number, Number]:
        z = zs[t - 1]
        g = 1 if x > z else (-1 if x < z else 0)
        return abs(x - z), g

    return adversary


def squared_losses(zs: list[Number]) -> Callable[[int, Number], tuple[Number, Number]]:
    """The oblivious adversary f_t(x) = (x - z_t)^2, which is 2-strongly convex."""

    def adversary(t: int, x: Number) -> tuple[Number, Number]:
        z = zs[t - 1]
        return (x - z) ** 2, 2 * (x - z)

    return adversary


def best_fixed_absolute(zs: list[Number], lo: Number, hi: Number) -> Number:
    """min over x in [lo, hi] of sum |x - z_t|. The sum is convex and piecewise
    linear, so the minimum is at an endpoint or at a projected z_t."""
    cands = [lo, hi] + [project(z, lo, hi) for z in zs]
    return min(sum(abs(c - z) for z in zs) for c in cands)


def best_fixed_squared(zs: list[Number], lo: Number, hi: Number) -> Number:
    """min over x in [lo, hi] of sum (x - z_t)^2, attained at the clipped mean."""
    c = project(sum(zs) / len(zs), lo, hi)
    return sum((c - z) ** 2 for z in zs)
