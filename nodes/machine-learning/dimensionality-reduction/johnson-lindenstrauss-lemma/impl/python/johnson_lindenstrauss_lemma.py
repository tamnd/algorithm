# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/johnson-lindenstrauss-lemma/. The authors are listed in prov/E6QYBH.jsonl.
"""The Johnson-Lindenstrauss lemma with the constant of Dasgupta and Gupta (2003),
and the Gaussian projection that proves it."""

import math


def jl_dimension(n, eps):
    """The least integer k with k >= 4 ln n / (eps^2/2 - eps^3/3), for n >= 2 and 0 < eps < 1."""
    if n < 2 or not 0 < eps < 1:
        raise ValueError("need n >= 2 and 0 < eps < 1")
    return math.ceil(4 * math.log(n) / (eps * eps / 2 - eps ** 3 / 3))


def tail_bound(k, eps):
    """The bound exp(-(k/2)(eps^2/2 - eps^3/3)) on each tail of ||f(u)||^2 for a unit u."""
    return math.exp(-(k / 2) * (eps * eps / 2 - eps ** 3 / 3))


def gaussian_matrix(k, d, rng):
    return [[rng.gauss(0.0, 1.0) for _ in range(d)] for _ in range(k)]


def project(r, x):
    """f(x) = R x / sqrt(k)."""
    c = 1.0 / math.sqrt(len(r))
    return [c * sum(a * b for a, b in zip(row, x)) for row in r]


def sq_dist(x, y):
    return sum((a - b) ** 2 for a, b in zip(x, y))


def distortion_ratios(points, images):
    """The ratios ||f(u) - f(v)||^2 / ||u - v||^2 over all pairs."""
    out = []
    n = len(points)
    for i in range(n):
        for j in range(i + 1, n):
            out.append(sq_dist(images[i], images[j]) / sq_dist(points[i], points[j]))
    return out


def bad_fraction(points, images, eps):
    """The fraction of pairs whose squared distance moves outside [1 - eps, 1 + eps]."""
    rs = distortion_ratios(points, images)
    return sum(1 for r in rs if not 1 - eps <= r <= 1 + eps) / len(rs)
