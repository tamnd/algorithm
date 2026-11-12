# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lossy-compression/. The authors are listed in prov/JRTS3R.jsonl.

"""Distortion measures, closed-form rate distortion functions, and the
Blahut-Arimoto algorithm that computes a point of R(D) for a discrete
memoryless source.

Rates are in bits per source symbol (log base 2). A source is a list of
probabilities p[x]; a distortion measure is a matrix d[x][y] >= 0 over the
source alphabet (rows) and the reproduction alphabet (columns).
"""

import math
from typing import List, Sequence, Tuple

Matrix = List[List[float]]


def mse(x: Sequence[float], y: Sequence[float]) -> float:
    """Mean squared error of two sequences of the same nonzero length."""
    if len(x) != len(y) or not x:
        raise ValueError("need two sequences of the same nonzero length")
    return sum((a - b) * (a - b) for a, b in zip(x, y)) / len(x)


def psnr(x: Sequence[float], y: Sequence[float], peak: float = 255.0) -> float:
    """Peak signal to noise ratio in dB: 10 log10(peak^2 / MSE).

    Returns math.inf when the two sequences are equal.
    """
    e = mse(x, y)
    if e == 0:
        return math.inf
    return 10.0 * math.log10(peak * peak / e)


def binary_entropy(p: float) -> float:
    """h(p) = -p log2 p - (1 - p) log2 (1 - p), with h(0) = h(1) = 0."""
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log2(p) - (1.0 - p) * math.log2(1.0 - p)


def rd_bernoulli(p: float, dist: float) -> float:
    """R(D) of a Bernoulli(p) source under Hamming distortion.

    R(D) = h(p) - h(D) for 0 <= D <= min(p, 1 - p), and 0 above that.
    """
    if dist >= min(p, 1.0 - p):
        return 0.0
    return binary_entropy(p) - binary_entropy(dist)


def rd_gaussian(var: float, dist: float) -> float:
    """R(D) of a Gaussian source of variance var under squared error.

    R(D) = (1/2) log2(var / D) for 0 < D <= var, and 0 above that.
    """
    if dist >= var:
        return 0.0
    return 0.5 * math.log2(var / dist)


def hamming_matrix(k: int) -> Matrix:
    """The Hamming distortion d(x, y) = [x != y] on an alphabet of size k."""
    return [[0.0 if i == j else 1.0 for j in range(k)] for i in range(k)]


def squared_error_matrix(xs: Sequence[float], ys: Sequence[float]) -> Matrix:
    """d(x, y) = (x - y)^2 for source points xs and reproduction points ys."""
    return [[(a - b) * (a - b) for b in ys] for a in xs]


def blahut_arimoto(
    p: Sequence[float], d: Matrix, beta: float, iters: int = 2000, tol: float = 1e-12
) -> Tuple[float, float, List[float]]:
    """Blahut-Arimoto iteration for the rate distortion function.

    For a slope parameter beta > 0 it returns (R, D, q): a point of the
    R(D) curve where the slope is -beta / ln 2 in bits, and the output
    distribution q. Each iteration costs O(|X| |Y|) arithmetic operations.
    """
    nx, ny = len(p), len(d[0])
    a = [[math.exp(-beta * d[x][y]) for y in range(ny)] for x in range(nx)]
    q = [1.0 / ny] * ny  # @line L1
    for _ in range(iters):  # @line L2
        z = [sum(q[y] * a[x][y] for y in range(ny)) for x in range(nx)]  # @line L3
        new_q = [q[y] * sum(p[x] * a[x][y] / z[x] for x in range(nx)) for y in range(ny)]  # @line L4
        change = max(abs(u - v) for u, v in zip(new_q, q))
        q = new_q
        if change < tol:  # @line L5
            break
    z = [sum(q[y] * a[x][y] for y in range(ny)) for x in range(nx)]
    rate = dist = 0.0
    for x in range(nx):  # @line L6
        if p[x] == 0:
            continue
        for y in range(ny):
            w = q[y] * a[x][y] / z[x]  # the test channel Q(y | x)
            if w > 0:
                dist += p[x] * w * d[x][y]
                rate += p[x] * w * math.log2(w / q[y])
    return rate, dist, q  # @line L7


def rd_point_at(p: Sequence[float], d: Matrix, target: float, iters: int = 2000) -> Tuple[float, float]:
    """Find (R, D) on the curve with D close to target, by bisection on beta."""
    lo, hi = 0.0, 1.0
    while blahut_arimoto(p, d, hi, iters)[1] > target:
        lo, hi = hi, 2.0 * hi
    best = blahut_arimoto(p, d, hi, iters)
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        r, dd, _ = blahut_arimoto(p, d, mid, iters)
        if dd > target:
            lo = mid
        else:
            hi, best = mid, (r, dd, None)
    return best[0], best[1]
