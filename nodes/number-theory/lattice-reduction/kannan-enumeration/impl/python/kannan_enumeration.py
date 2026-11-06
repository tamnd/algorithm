# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kannan-enumeration/. The authors are listed in prov/NY4D49.jsonl.

from fractions import Fraction
from math import floor, isqrt
from typing import Optional, Sequence, Union

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


def _lll_from(b: list[list[Fraction]], lo: int, delta: Fraction = Fraction(3, 4)) -> None:
    """LLL in place on the projected rows pi_lo(b_lo), ..., pi_lo(b_{n-1}).

    Rows before lo are not changed; rows from lo on are size-reduced against all earlier rows,
    and swaps happen only among positions >= lo.
    """
    n = len(b)
    k = lo + 1
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
            k = max(k - 1, lo + 1)


def _block_svp(
    mu: list[list[Fraction]], norms: list[Fraction], k: int, h: int, stats: Optional[dict] = None
) -> tuple[list[int], Fraction]:
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
        if stats is not None:
            stats["nodes"] += 1
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


def _size_reduce(b: list[list[Fraction]]) -> None:
    """Make |mu_ij| <= 1/2 for all j < i without changing the Gram-Schmidt vectors."""
    for i in range(1, len(b)):
        mu, _ = _gso(b[: i + 1])
        for j in range(i - 1, -1, -1):
            q = floor(mu[i][j] + Fraction(1, 2))
            if q:
                b[i] = [a - q * c for a, c in zip(b[i], b[j])]
                for l in range(j):
                    mu[i][l] -= q * mu[j][l]
                mu[i][j] -= q


def kannan_enumeration(basis: Sequence[Sequence[Number]], stats: Optional[dict] = None) -> list[list[Fraction]]:
    """Kannan's algorithm: an HKZ-reduced basis of the same lattice, in exact arithmetic.

    The first row of the result is a shortest nonzero lattice vector. The recursion of
    Kannan's algorithm on the projected lattices pi_k(L) runs on an explicit task stack:
    (k, start) LLL-reduces the projected rows k..n-1 and then HKZ-reduces pi_{k+1};
    (k, check) makes the block quasi-HKZ (N_k <= 4 N_{k+1}) by swaps, then enumerates a
    shortest vector of pi_k(L) with radius N_k and inserts it. If stats is a dict, it gets
    the counts 'nodes' (enumeration nodes) and 'swaps'. Raises ValueError on invalid input.
    """
    b = [[Fraction(c) for c in row] for row in basis]
    n = len(b)
    if n == 0 or any(len(row) != len(b[0]) for row in b):
        raise ValueError("need at least one basis row, all of the same length")
    _gso(b)
    if stats is not None:
        stats.setdefault("nodes", 0)
        stats.setdefault("swaps", 0)
    tasks: list[tuple[int, bool]] = [(0, True)]  # @line L1
    while tasks:  # @line L2
        k, start = tasks.pop()  # @line L3
        if k >= n - 1:
            continue
        if start:
            _lll_from(b, k)  # @line L4
            tasks += [(k, False), (k + 1, True)]
            continue
        mu, norms = _gso(b)
        q = floor(mu[k + 1][k] + Fraction(1, 2))  # @line L5
        if q:
            b[k + 1] = [a - q * c for a, c in zip(b[k + 1], b[k])]
        if norms[k] > 4 * norms[k + 1]:  # @line L6
            b[k], b[k + 1] = b[k + 1], b[k]
            tasks += [(k, False), (k + 1, True)]
            if stats is not None:
                stats["swaps"] += 1
            continue
        mu, norms = _gso(b)
        x, length = _block_svp(mu, norms, k, n - 1, stats)  # @line L7
        if length < norms[k]:  # @line L8
            _insert(b, k, x)
            tasks.append((k + 1, True))
    _size_reduce(b)  # @line L9
    return b
