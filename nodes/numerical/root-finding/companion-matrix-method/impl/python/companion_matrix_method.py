# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/companion-matrix-method/. The authors are listed in prov/4VFJZ5.jsonl.

"""Polynomial roots as the eigenvalues of the companion matrix.

The companion matrix is balanced (Parlett-Reinsch, powers of 2) and its
eigenvalues are computed by the shifted QR iteration on the upper
Hessenberg form, with Givens rotations in complex arithmetic, Wilkinson
shifts, an exceptional shift every 10 steps, and deflation of negligible
subdiagonal entries. Coefficients are listed highest degree first.
"""

import cmath
import math
from dataclasses import dataclass
from typing import List, Sequence

EPS = 2.0 ** -52


@dataclass
class CompanionResult:
    roots: List[complex]
    sweeps: int  # QR steps on the active block
    status: str  # "converged" or "failed"


def companion(a: Sequence[complex]) -> List[List[complex]]:
    """Upper Hessenberg companion matrix: first row -a_1/a_0, ..., -a_n/a_0, ones below the diagonal."""
    n = len(a) - 1
    C = [[0j] * n for _ in range(n)]
    for j in range(n):
        C[0][j] = complex(-a[j + 1] / a[0])
    for i in range(1, n):
        C[i][i - 1] = 1 + 0j
    return C


def balance(A: List[List[complex]]) -> None:
    """In place D^-1 A D with D a diagonal of powers of 2 (exact in floating point)."""
    n = len(A)
    radix = 2.0
    done = False
    while not done:
        done = True
        for i in range(n):
            c = sum(abs(A[j][i]) for j in range(n) if j != i)
            r = sum(abs(A[i][j]) for j in range(n) if j != i)
            if c == 0 or r == 0:
                continue
            g, f, s = r / radix, 1.0, c + r
            while c < g:
                f *= radix
                c *= radix * radix
            g = r * radix
            while c > g:
                f /= radix
                c /= radix * radix
            if (c + r) / f < 0.95 * s:
                done = False
                for j in range(n):
                    A[i][j] /= f
                for j in range(n):
                    A[j][i] *= f


def _wilkinson_shift(a, b, c, d):
    """Eigenvalue of [[a, b], [c, d]] closer to d."""
    h = (a - d) / 2
    disc = cmath.sqrt(h * h + b * c)
    m1, m2 = (a + d) / 2 + disc, (a + d) / 2 - disc
    return m1 if abs(m1 - d) <= abs(m2 - d) else m2


def hessenberg_eigenvalues(H: List[List[complex]], max_iter: int = 60):
    """Eigenvalues of an upper Hessenberg matrix (modified in place).
    Returns (eigenvalues, sweeps, status)."""
    n = len(H)
    eig = []
    sweeps = 0
    hi = n - 1
    its = 0
    while hi >= 0:  # @line L4
        lo = hi  # @line L5
        while lo > 0:
            s = abs(H[lo - 1][lo - 1]) + abs(H[lo][lo])
            if s == 0:
                s = sum(abs(H[i][j]) for i in range(hi + 1) for j in range(hi + 1))
            if abs(H[lo][lo - 1]) <= EPS * s:
                H[lo][lo - 1] = 0j
                break
            lo -= 1
        if lo == hi:  # @line L6
            eig.append(H[hi][hi])
            hi -= 1
            its = 0
            continue
        if its >= max_iter:  # @line L9
            return eig, sweeps, "failed"
        its += 1
        sweeps += 1
        if its % 10 == 0:  # @line L7
            mu = H[hi][hi] + abs(H[hi][hi - 1]) * (0.75 + 0.5j)
        else:
            mu = _wilkinson_shift(H[hi - 1][hi - 1], H[hi - 1][hi], H[hi][hi - 1], H[hi][hi])
        for i in range(lo, hi + 1):  # @line L8
            H[i][i] -= mu
        rots = []
        for k in range(lo, hi):
            x, y = H[k][k], H[k + 1][k]
            r = math.hypot(abs(x), abs(y))
            if r == 0:
                c, s = 1 + 0j, 0j
            else:
                c, s = x / r, y / r
            rots.append((c, s))
            for j in range(k, hi + 1):
                u, v = H[k][j], H[k + 1][j]
                H[k][j] = c.conjugate() * u + s.conjugate() * v
                H[k + 1][j] = -s * u + c * v
        for k, (c, s) in zip(range(lo, hi), rots):
            for i in range(lo, min(k + 2, hi) + 1):
                u, v = H[i][k], H[i][k + 1]
                H[i][k] = u * c + v * s
                H[i][k + 1] = -u * s.conjugate() + v * c.conjugate()
        for i in range(lo, hi + 1):
            H[i][i] += mu
    return eig, sweeps, "converged"  # @line L10


def companion_roots(coeffs: Sequence[float], balanced: bool = True, max_iter: int = 60) -> CompanionResult:
    """All roots of the polynomial, with multiplicity, as companion matrix eigenvalues."""
    a = [complex(x) for x in coeffs]
    if not all(math.isfinite(z.real) and math.isfinite(z.imag) for z in a):
        raise ValueError("coefficients must be finite")
    while a and a[0] == 0:  # @line L1
        a.pop(0)
    if not a:
        raise ValueError("the zero polynomial has every number as a root")
    zeros = 0
    while len(a) > 1 and a[-1] == 0:
        a.pop()
        zeros += 1
    if len(a) == 1:
        return CompanionResult([0j] * zeros, 0, "converged")
    C = companion(a)  # @line L2
    if balanced:
        balance(C)  # @line L3
    eig, sweeps, status = hessenberg_eigenvalues(C, max_iter)
    return CompanionResult(eig + [0j] * zeros, sweeps, status)
