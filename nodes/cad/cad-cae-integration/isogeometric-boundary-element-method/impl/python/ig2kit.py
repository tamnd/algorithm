# SPDX-License-Identifier: MIT
# Shared helper of the ig2 cad pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""Small numerical helpers: B-spline basis with derivatives, Greville points,
Gauss-Legendre points and a dense linear solver.

Every function works with float, and the spline and solver functions also work
with fractions.Fraction, so that a test can check an exact identity.
"""

from __future__ import annotations

import math
from typing import List, Sequence, Tuple


def open_uniform_knots(p: int, ne: int, a=0, b=1) -> List:
    """Open knot vector of degree p with ne equal elements on [a, b].

    The ends have multiplicity p + 1 and the interior knots are simple.
    With Fraction inputs the knots are Fractions.
    """
    inner = [a + (b - a) * k / ne for k in range(1, ne)]
    return [a] * (p + 1) + inner + [b] * (p + 1)


def find_span(knots: Sequence, p: int, x) -> int:
    """Index s with knots[s] <= x < knots[s + 1], and the last non-empty span for x = knots[-1]."""
    n = len(knots) - p - 1  # number of basis functions
    if x >= knots[n]:
        s = n - 1
        while knots[s] == knots[s + 1]:
            s -= 1
        return s
    lo, hi = p, n
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if x < knots[mid]:
            hi = mid
        else:
            lo = mid
    return lo


def basis_ders(knots: Sequence, p: int, s: int, x, nd: int) -> List[List]:
    """Values and derivatives of the p + 1 B-splines that are non-zero on span s.

    Returns d with d[k][j] = the k-th derivative of N_{s - p + j} at x, for
    k = 0..nd. This is algorithm A2.3 of Piegl and Tiller.
    """
    one = x - x + 1
    zero = x - x
    ndu = [[zero] * (p + 1) for _ in range(p + 1)]
    ndu[0][0] = one
    left = [zero] * (p + 1)
    right = [zero] * (p + 1)
    for j in range(1, p + 1):
        left[j] = x - knots[s + 1 - j]
        right[j] = knots[s + j] - x
        saved = zero
        for r in range(j):
            ndu[j][r] = right[r + 1] + left[j - r]
            temp = ndu[r][j - 1] / ndu[j][r]
            ndu[r][j] = saved + right[r + 1] * temp
            saved = left[j - r] * temp
        ndu[j][j] = saved
    ders = [[zero] * (p + 1) for _ in range(nd + 1)]
    for j in range(p + 1):
        ders[0][j] = ndu[j][p]
    for r in range(p + 1):
        s1, s2 = 0, 1
        a = [[zero] * (p + 1) for _ in range(2)]
        a[0][0] = one
        for k in range(1, nd + 1):
            dval = zero
            rk, pk = r - k, p - k
            if r >= k:
                a[s2][0] = a[s1][0] / ndu[pk + 1][rk]
                dval = a[s2][0] * ndu[rk][pk]
            j1 = 1 if rk >= -1 else -rk
            j2 = k - 1 if r - 1 <= pk else p - r
            for j in range(j1, j2 + 1):
                a[s2][j] = (a[s1][j] - a[s1][j - 1]) / ndu[pk + 1][rk + j]
                dval += a[s2][j] * ndu[rk + j][pk]
            if r <= pk:
                a[s2][k] = -a[s1][k - 1] / ndu[pk + 1][r]
                dval += a[s2][k] * ndu[r][pk]
            ders[k][r] = dval
            s1, s2 = s2, s1
    fac = p
    for k in range(1, nd + 1):
        for j in range(p + 1):
            ders[k][j] = ders[k][j] * fac
        fac *= p - k
    return ders


def all_basis(knots: Sequence, p: int, x, nd: int = 0) -> List[List]:
    """Full rows: out[k][i] = k-th derivative of N_i at x, for all n basis functions."""
    n = len(knots) - p - 1
    s = find_span(knots, p, x)
    d = basis_ders(knots, p, s, x, nd)
    zero = x - x
    out = [[zero] * n for _ in range(nd + 1)]
    for k in range(nd + 1):
        for j in range(p + 1):
            out[k][s - p + j] = d[k][j]
    return out


def greville(knots: Sequence, p: int) -> List:
    """Greville abscissae tau_i = (knots[i+1] + ... + knots[i+p]) / p."""
    n = len(knots) - p - 1
    return [sum(knots[i + 1 : i + p + 1]) / p for i in range(n)]


def solve_dense(a: List[List], b: List) -> List:
    """Solve a x = b by Gaussian elimination with partial pivoting.

    Works with float and with Fraction (then the result is exact).
    Raises ValueError if the matrix is singular (an exact zero pivot).
    Cost O(n^3) operations.
    """
    n = len(a)
    m = [list(row) + [bi] for row, bi in zip(a, b)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(m[r][c]))
        if m[piv][c] == 0:
            raise ValueError("singular matrix")
        m[c], m[piv] = m[piv], m[c]
        for r in range(c + 1, n):
            f = m[r][c] / m[c][c]
            if f != 0:
                row_r, row_c = m[r], m[c]
                for k in range(c, n + 1):
                    row_r[k] -= f * row_c[k]
    x = [0] * n
    for r in range(n - 1, -1, -1):
        acc = m[r][n]
        for k in range(r + 1, n):
            acc -= m[r][k] * x[k]
        x[r] = acc / m[r][r]
    return x


def gauss_legendre(n: int) -> Tuple[List[float], List[float]]:
    """Nodes and weights of the n-point Gauss-Legendre rule on [-1, 1]."""
    xs, ws = [], []
    for i in range(1, n + 1):
        x = math.cos(math.pi * (i - 0.25) / (n + 0.5))
        for _ in range(100):
            p0, p1 = 1.0, x
            for k in range(2, n + 1):
                p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
            dp = n * (x * p1 - p0) / (x * x - 1)
            dx = p1 / dp
            x -= dx
            if abs(dx) < 1e-16:
                break
        p0, p1 = 1.0, x
        for k in range(2, n + 1):
            p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
        dp = n * (x * p1 - p0) / (x * x - 1)
        xs.append(x)
        ws.append(2.0 / ((1 - x * x) * dp * dp))
    return xs, ws
