# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cover-hart-theorem/. The authors are listed in prov/B8ZFXM.jsonl.

"""Exact and simulated checks of the Cover-Hart bound R* <= R <= R*(2 - M R*/(M - 1))."""

import bisect
import random
from fractions import Fraction
from typing import Sequence

# A finite distribution: a list of (P(X = x), (eta_1(x), ..., eta_M(x))).
Finite = Sequence[tuple[Fraction, Sequence[Fraction]]]


def bayes_risk(dist: Finite) -> Fraction:
    """R* = E[1 - max_i eta_i(X)]."""
    return sum((p * (1 - max(eta)) for p, eta in dist), Fraction(0))


def nn_asymptotic_risk(dist: Finite) -> Fraction:
    """R = E[1 - sum_i eta_i(X)^2], the large sample 1-NN risk."""
    return sum((p * (1 - sum(e * e for e in eta)) for p, eta in dist), Fraction(0))


def cover_hart_upper(r_star: Fraction, m: int) -> Fraction:
    """The upper bound R*(2 - M R*/(M - 1))."""
    return r_star * (2 - Fraction(m) * r_star / (m - 1))


def one_nn_error_uniform(n: int, m: int, rng: random.Random) -> float:
    """X ~ U[0, 1], P(Y = 1 | X = x) = x. Train 1-NN on n points, return the error on m test points."""
    train = sorted((x, int(rng.random() < x)) for x in (rng.random() for _ in range(n)))
    xs = [x for x, _ in train]
    wrong = 0
    for _ in range(m):
        x = rng.random()
        y = int(rng.random() < x)
        j = bisect.bisect_left(xs, x)
        if j == n or (j > 0 and x - xs[j - 1] <= xs[j] - x):
            j -= 1
        wrong += train[j][1] != y
    return wrong / m


def one_nn_risk_finite(dist: Finite, n: int, rng: random.Random) -> Fraction:
    """Draw n training pairs from a finite distribution and return the exact error
    P(g(X) != Y | training set) of the 1-NN rule g with the discrete metric. The
    neighbor of x is the first training point equal to x, or the first training
    point if none is equal."""
    weights = [float(p) for p, _ in dist]
    k = len(dist[0][1])
    train = []
    for _ in range(n):
        x = rng.choices(range(len(dist)), weights)[0]
        y = rng.choices(range(k), [float(e) for e in dist[x][1]])[0]
        train.append((x, y))
    first: dict[int, int] = {}
    for x, y in train:
        first.setdefault(x, y)
    return sum(
        (p * (1 - eta[first.get(x, train[0][1])]) for x, (p, eta) in enumerate(dist)), Fraction(0)
    )
