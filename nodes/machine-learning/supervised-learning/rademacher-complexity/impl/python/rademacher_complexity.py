# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rademacher-complexity/. The authors are listed in prov/3MG65J.jsonl.

"""The empirical Rademacher complexity of a finite set of vectors A in R^n,

    R(A) = E_sigma [ max_{a in A} (1/n) sum_i sigma_i a_i ],

with sigma uniform on {-1, +1}^n. For a class F and a sample z_1 .. z_n, take
A = {(f(z_1), ..., f(z_n)) : f in F}.
"""

from fractions import Fraction
from itertools import product
from math import log, sqrt


def _value(A, sigma):
    return max(sum(s * x for s, x in zip(sigma, a)) for a in A)


def rademacher_exact(A):
    """Exact value by enumeration of all 2^n sign vectors. Exact for rational entries."""
    n = len(A[0])
    total = sum(_value(A, sigma) for sigma in product((-1, 1), repeat=n))
    if isinstance(total, float):
        return total / (n * 2 ** n)
    return Fraction(total) / (n * 2 ** n)


def rademacher_monte_carlo(A, draws, rng):
    """Mean of max_a (1/n) sigma . a over `draws` independent sign vectors from rng."""
    n = len(A[0])
    total = 0.0  # @line L1
    for _ in range(draws):  # @line L2
        sigma = [1 if rng.random() < 0.5 else -1 for _ in range(n)]  # @line L3
        total += float(_value(A, sigma)) / n  # @line L4
    return total / draws  # @line L5


def monte_carlo_tolerance(A, draws, delta):
    """Hoeffding: each draw lies in [-r, r] with r = max_a (1/n) sum |a_i|, so the mean
    of `draws` draws is within this distance of R(A) with probability >= 1 - delta."""
    n = len(A[0])
    r = max(sum(abs(float(x)) for x in a) for a in A) / n
    return 2 * r * sqrt(log(2 / delta) / (2 * draws))


def massart_bound(A):
    """Massart's lemma: R(A) <= max_a ||a - mean(A)|| sqrt(2 ln N) / n, with N = |A|."""
    n, N = len(A[0]), len(A)
    mean = [sum(float(a[i]) for a in A) / N for i in range(n)]
    r = max(sqrt(sum((float(a[i]) - mean[i]) ** 2 for i in range(n))) for a in A)
    return r * sqrt(2 * log(N)) / n


def threshold_vectors(points):
    """The +1/-1 vectors of the thresholds x -> sign(x - t) on sorted distinct points:
    the prefix 0..k-1 gets -1 and the rest +1, for k = 0 .. n."""
    n = len(points)
    return [tuple(-1 if i < k else 1 for i in range(n)) for k in range(n + 1)]


def linear_unit_ball_exact(xs):
    """R of {x -> <w, x> : ||w||_2 <= 1} on the points xs. The max over w of
    sigma . (<w, x_i>)_i is ||sum_i sigma_i x_i||, so R = E ||sum sigma_i x_i|| / n."""
    n, dim = len(xs), len(xs[0])
    total = 0.0
    for sigma in product((-1, 1), repeat=n):
        v = [sum(s * x[j] for s, x in zip(sigma, xs)) for j in range(dim)]
        total += sqrt(sum(c * c for c in v))
    return total / (n * 2 ** n)


def linear_unit_ball_bound(xs):
    """sqrt(sum ||x_i||^2) / n <= max ||x_i|| / sqrt(n), from Jensen's inequality."""
    n = len(xs)
    return sqrt(sum(sum(c * c for c in x) for x in xs)) / n


def apply_coordinatewise(phi, A):
    """phi o A = {(phi(a_1), ..., phi(a_n)) : a in A}."""
    return [tuple(phi(x) for x in a) for a in A]
