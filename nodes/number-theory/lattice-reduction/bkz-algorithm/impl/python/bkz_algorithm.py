# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bkz-algorithm/. The authors are listed in prov/TQ85KA.jsonl.

from fractions import Fraction
from math import floor, isqrt
from typing import Sequence, Union

Number = Union[int, Fraction]


def _dot(u: Sequence[Fraction], v: Sequence[Fraction]) -> Fraction:
    return sum((a * b for a, b in zip(u, v)), Fraction(0))


def _gso(b: list[list[Fraction]]) -> tuple[list[list[Fraction]], list[Fraction]]:
    """Gram-Schmidt coefficients mu[i][j] (j < i) and squared norms N_i; ValueError if dependent."""
    n = len(b)
    stars: list[list[Fraction]] = []
    norms: list[Fraction] = []
    mu = [[Fraction(0)] * n for _ in range(n)]
    for i, row in enumerate(b):
        w = row[:]
        for j in range(i):
            mu[i][j] = _dot(row, stars[j]) / norms[j]
            w = [a - mu[i][j] * c for a, c in zip(w, stars[j])]
        nw = _dot(w, w)
        if nw == 0:
            raise ValueError("the basis vectors are linearly dependent")
        stars.append(w)
        norms.append(nw)
    return mu, norms


def _lll(b: list[list[Fraction]], delta: Fraction) -> None:
    """Exact LLL in place (size reduction plus Lovasz swaps)."""
    n = len(b)
    k = 1
    while k < n:
        mu, norms = _gso(b[: k + 1])
        for j in range(k - 1, -1, -1):
            q = floor(mu[k][j] + Fraction(1, 2))
            if q:
                b[k] = [a - q * c for a, c in zip(b[k], b[j])]
                for l in range(j):
                    mu[k][l] -= q * mu[j][l]
                mu[k][j] -= q
        if norms[k] + mu[k][k - 1] ** 2 * norms[k - 1] >= delta * norms[k - 1]:
            k += 1
        else:
            b[k - 1], b[k] = b[k], b[k - 1]
            k = max(k - 1, 1)


def _block_svp(mu: list[list[Fraction]], norms: list[Fraction], k: int, h: int) -> tuple[list[int], Fraction]:
    """Shortest nonzero vector of pi_k(L(b_k..b_h)) by exact enumeration (iterative).

    Returns block coefficients x (length h - k + 1) and the squared length
    sum_j (x_j + sum_{i>j} x_i mu_ij)^2 N_j. The radius shrinks to the best length found.
    """
    d = h - k + 1
    best_x = [1] + [0] * (d - 1)
    best = norms[k]
    x = [0] * d
    c = [Fraction(0)] * d
    rho = [Fraction(0)] * (d + 1)
    i, new = d - 1, True
    while i < d:
        if new:
            c[i] = -sum((x[j] * mu[k + j][k + i] for j in range(i + 1, d)), Fraction(0))
            q = max(best - rho[i + 1], Fraction(0)) / norms[k + i]
            x[i] = floor(c[i]) - isqrt(floor(q)) - 1
        else:
            x[i] += 1
        while (x[i] - c[i]) ** 2 * norms[k + i] + rho[i + 1] > best and x[i] <= c[i]:
            x[i] += 1
        val = rho[i + 1] + (x[i] - c[i]) ** 2 * norms[k + i]
        if val > best:
            i, new = i + 1, False
            continue
        rho[i] = val
        if i == 0:
            if val < best and any(x):
                best, best_x = val, x[:]
            new = False
        else:
            i, new = i - 1, True
    return best_x, best


def _ext_gcd(a: int, b: int) -> tuple[int, int, int]:
    """(g, s, t) with s a + t b = g = gcd(a, b) >= 0."""
    s0, s1, t0, t1 = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a - q * b
        s0, s1 = s1, s0 - q * s1
        t0, t1 = t1, t0 - q * t1
    if a < 0:
        a, s0, t0 = -a, -s0, -t0
    return a, s0, t0


def _insert(b: list[list[Fraction]], k: int, x: list[int]) -> None:
    """Replace b_k..b_{k+d-1} by a basis of the same lattice whose first vector is sum x_i b_{k+i}.

    Needs gcd(x) = 1. Each step applies a 2 x 2 unimodular matrix to adjacent rows.
    """
    x = x[:]
    for j in range(len(x) - 2, -1, -1):
        if x[j] == 0 and x[j + 1] == 0:
            continue
        g, s, t = _ext_gcd(x[j], x[j + 1])
        p, q = x[j] // g, x[j + 1] // g
        u, w = b[k + j], b[k + j + 1]
        b[k + j] = [p * a + q * c for a, c in zip(u, w)]
        b[k + j + 1] = [-t * a + s * c for a, c in zip(u, w)]
        x[j], x[j + 1] = g, 0


def bkz(basis: Sequence[Sequence[Number]], block_size: int, delta: Number = Fraction(99, 100)) -> list[list[Fraction]]:
    """BKZ reduction (Schnorr-Euchner form) with an exact enumeration SVP oracle.

    Input: n >= 1 linearly independent rows (int or Fraction), block size beta >= 2
    and 1/4 < delta <= 1. Output: a basis of the same lattice that is LLL-reduced and
    satisfies delta ||b_k*||^2 <= lambda_1(pi_k(L(b_k..b_h)))^2 with h = min(k + beta - 1, n)
    for every k. Cost per step: one block enumeration (at most prod (2 sqrt(N_k / N_i) + 1)
    nodes per level) and, after an insertion, one LLL call; the number of steps is finite
    but has no known polynomial bound. Raises ValueError on invalid input.
    """
    d = Fraction(delta)
    if not Fraction(1, 4) < d <= 1:
        raise ValueError("delta must satisfy 1/4 < delta <= 1")
    if block_size < 2:
        raise ValueError("the block size must be at least 2")
    b = [[Fraction(c) for c in row] for row in basis]
    n = len(b)
    if n == 0 or any(len(row) != len(b[0]) for row in b):
        raise ValueError("need at least one basis row, all of the same length")
    _gso(b)
    _lll(b, d)  # @line L1
    z, k = 0, -1
    while z < n - 1:  # @line L2
        k = (k + 1) % (n - 1)  # @line L3
        h = min(k + block_size - 1, n - 1)
        mu, norms = _gso(b)
        x, length = _block_svp(mu, norms, k, h)  # @line L4
        if length < d * norms[k]:  # @line L5
            _insert(b, k, x)  # @line L6
            _lll(b, d)  # @line L7
            z = 0
        else:
            z += 1  # @line L8
    return b  # @line L9
