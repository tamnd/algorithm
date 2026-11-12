# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/partition-function/. The authors are listed in prov/VFPG8P.jsonl.

"""The partition function of a discrete log-linear model, and its derivatives.

A model has variables 0 .. n-1 with domains 0 .. card[v]-1 and features. A
feature is a scope and a table from assignments of the scope to nonnegative
integers (counts). With parameters theta_k, the unnormalized weight of x is
exp(sum_k theta_k phi_k(x)). To stay exact we pass w_k = exp(theta_k) as a
positive Fraction; then each weight is a product of powers w_k ** phi_k(x), and

    Z(w) = sum_x prod_k w_k ** phi_k(x),      A = log Z.

The facts (Wainwright and Jordan 2008, Section 3): dA/dtheta_k = E[phi_k] and
the Hessian of A is the covariance of the features, so A is convex. The
function derivatives_along computes the first two derivatives of A along a
direction from values of Z alone, by exact polynomial interpolation, so they
can be compared with the moments.
"""

from fractions import Fraction
from itertools import product
from typing import Dict, List, NamedTuple, Sequence, Tuple

Assignment = Tuple[int, ...]


class Feature(NamedTuple):
    scope: Tuple[int, ...]
    table: Dict[Assignment, int]


def phi(features: Sequence[Feature], x: Sequence[int]) -> List[int]:
    return [f.table[tuple(x[v] for v in f.scope)] for f in features]


def weight(features: Sequence[Feature], w: Sequence[Fraction], x: Sequence[int]) -> Fraction:
    out = Fraction(1)
    for wk, c in zip(w, phi(features, x)):
        out *= wk ** c
    return out


def partition_function(features: Sequence[Feature], card: Sequence[int], w: Sequence[Fraction]) -> Fraction:
    """Z(w) by a sum over all joint assignments."""
    return sum((weight(features, w, x) for x in product(*(range(c) for c in card))), Fraction(0))


def moments(features: Sequence[Feature], card: Sequence[int],
            w: Sequence[Fraction]) -> Tuple[List[Fraction], List[List[Fraction]]]:
    """The mean vector E[phi] and the covariance matrix Cov(phi) under P_w."""
    z = partition_function(features, card, w)
    k = len(features)
    mean = [Fraction(0)] * k
    second = [[Fraction(0)] * k for _ in range(k)]
    for x in product(*(range(c) for c in card)):
        p = weight(features, w, x) / z
        f = phi(features, x)
        for i in range(k):
            mean[i] += p * f[i]
            for j in range(k):
                second[i][j] += p * f[i] * f[j]
    cov = [[second[i][j] - mean[i] * mean[j] for j in range(k)] for i in range(k)]
    return mean, cov


def _solve(a: List[List[Fraction]], b: List[Fraction]) -> List[Fraction]:
    """Gaussian elimination over the rationals; a is square and invertible."""
    n = len(b)
    m = [row[:] + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        p = next(r for r in range(c, n) if m[r][c] != 0)
        m[c], m[p] = m[p], m[c]
        for r in range(n):
            if r != c and m[r][c] != 0:
                t = m[r][c] / m[c][c]
                m[r] = [x - t * y for x, y in zip(m[r], m[c])]
    return [m[i][n] / m[i][i] for i in range(n)]


def derivatives_along(features: Sequence[Feature], card: Sequence[int], w: Sequence[Fraction],
                      u: Sequence[int]) -> Tuple[Fraction, Fraction]:
    """d/ds and d^2/ds^2 of A(theta + s u) at s = 0, for a direction u of nonnegative
    integers, using only values of Z.

    With t = exp(s), Z(theta + s u) = g(t) = sum_x c_x t^<u, phi(x)>, a polynomial
    of degree D = max_x <u, phi(x)>. We find g from its values at t = 1 .. D+1;
    then dA/ds = g'(1)/g(1) and d^2A/ds^2 = (g'(1) + g''(1))/g(1) - (g'(1)/g(1))^2.
    """
    deg = max(sum(a * b for a, b in zip(u, phi(features, x))) for x in product(*(range(c) for c in card)))
    pts = [Fraction(t) for t in range(1, deg + 2)]
    vals = [partition_function(features, card, [wk * t ** uk for wk, uk in zip(w, u)]) for t in pts]
    coef = _solve([[t ** i for i in range(deg + 1)] for t in pts], vals)
    g0 = sum(coef)
    g1 = sum(i * c for i, c in enumerate(coef))
    g2 = sum(i * (i - 1) * c for i, c in enumerate(coef))
    return g1 / g0, (g1 + g2) / g0 - (g1 / g0) ** 2
