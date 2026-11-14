# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bayesian-online-changepoint-detection/. The authors are listed in prov/KJZYAX.jsonl.
"""Bayesian online changepoint detection (Adams and MacKay 2007).

Model: the series is cut into segments by a renewal process. A segment that
has run for r points ends after its r-th point with probability H(r) (the
hazard). Each segment draws its own parameter from a prior, independently of
the other segments, and the points of a segment are i.i.d. given the
parameter. The run length r_t is the number of points in the current segment,
x_t included, so r_t is in 1..t.

The joint J_t(r) = P(r_t = r, x_1..x_t) obeys
    J_1(1) = p(x_1 | no data),
    J_t(1) = p(x_t | no data) * sum_r J_(t-1)(r) H(r),
    J_t(r + 1) = p(x_t | the last r points) * J_(t-1)(r) (1 - H(r)).
The code keeps the normalized posterior P(r_t = r | x_1..x_t) and the
evidence. Cost O(t) at step t, O(n^2) in total, O(n) memory per step; the
optional pruning drops run lengths with posterior below a threshold.
"""

import math
from collections.abc import Callable, Iterable
from fractions import Fraction
from typing import Any


class BetaBernoulli:
    """Coin flips with a Beta(a, b) prior on the head probability. Exact with Fraction a, b."""

    def __init__(self, a: Fraction | int = 1, b: Fraction | int = 1) -> None:
        self.a, self.b = Fraction(a), Fraction(b)

    def empty(self) -> tuple[int, int]:
        return (0, 0)

    def predictive(self, stats: tuple[int, int], x: int) -> Fraction:
        h, t = stats
        p1 = (self.a + h) / (self.a + self.b + h + t)
        return p1 if x else 1 - p1

    def update(self, stats: tuple[int, int], x: int) -> tuple[int, int]:
        h, t = stats
        return (h + 1, t) if x else (h, t + 1)


class GaussianKnownVariance:
    """N(mu, sigma^2) points with sigma known and the prior mu ~ N(mu0, sigma0^2)."""

    def __init__(self, mu0: float, sigma0: float, sigma: float) -> None:
        self.mu0, self.v0, self.v = mu0, sigma0 * sigma0, sigma * sigma

    def empty(self) -> tuple[int, float]:
        return (0, 0.0)

    def predictive(self, stats: tuple[int, float], x: float) -> float:
        n, s = stats
        prec = 1.0 / self.v0 + n / self.v
        mean = (self.mu0 / self.v0 + s / self.v) / prec
        var = 1.0 / prec + self.v
        return math.exp(-0.5 * (x - mean) ** 2 / var) / math.sqrt(2.0 * math.pi * var)

    def update(self, stats: tuple[int, float], x: float) -> tuple[int, float]:
        return (stats[0] + 1, stats[1] + x)


def constant_hazard(lam: Any) -> Callable[[int], Any]:
    """H(r) = 1 / lam for every r: geometric segment lengths with mean lam."""
    return lambda r: 1 / lam


def bocpd(xs: Iterable[Any], model: Any, hazard: Callable[[int], Any],
          prune: float = 0.0) -> tuple[list[dict[int, Any]], Any]:
    """Run-length posteriors P(r_t = r | x_1..x_t) for t = 1..n, and the evidence p(x_1..x_n).

    Each posterior is a dict from run length r to probability. With prune > 0,
    run lengths whose posterior falls below prune are dropped (an
    approximation); prune = 0 gives the exact recursion.
    """
    post: dict[int, Any] = {}  # @line L1
    stats: dict[int, Any] = {}  # @line L1
    evidence: Any = 1
    out = []
    for t, x in enumerate(xs, 1):  # @line L2
        pred = {r: model.predictive(stats[r], x) for r in post}  # @line L3
        pred0 = model.predictive(model.empty(), x)  # @line L3
        joint = {r + 1: post[r] * pred[r] * (1 - hazard(r)) for r in post}  # @line L4
        joint[1] = pred0 * (sum(post[r] * hazard(r) for r in post) if t > 1 else 1)  # @line L5
        stats = {r + 1: model.update(stats[r], x) for r in post}  # @line L6
        stats[1] = model.update(model.empty(), x)  # @line L6
        z = sum(joint.values())  # @line L7
        evidence = evidence * z  # @line L7
        post = {r: v / z for r, v in joint.items()}  # @line L7
        if prune > 0:
            keep = {r: v for r, v in post.items() if v >= prune}
            total = sum(keep.values())
            post = {r: v / total for r, v in keep.items()}
            stats = {r: stats[r] for r in post}
        out.append(dict(sorted(post.items())))
    return out, evidence  # @line L8


def map_run_lengths(posteriors: list[dict[int, Any]]) -> list[int]:
    """The most probable run length at each step (ties go to the smaller r)."""
    return [min(p, key=lambda r: (-p[r], r)) for p in posteriors]
