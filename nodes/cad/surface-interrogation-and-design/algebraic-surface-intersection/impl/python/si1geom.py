# SPDX-License-Identifier: MIT
# Shared helper of the si1 cad pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""Small geometric and algebraic tools for the si1 pages.

Vectors are tuples of three numbers. A tensor product Bezier patch of bidegree
(m, n) is a list of m + 1 rows of n + 1 control points. Univariate polynomials
are lists of coefficients from the constant term up. Entries may be int,
Fraction or float; exact inputs give exact results where no square root or
division by a float is involved. No function here is the algorithm of a page.
"""

from fractions import Fraction
from math import comb, sqrt
from typing import Sequence

Vec = tuple
Num = float


# ---- vectors ---------------------------------------------------------------

def add(a: Vec, b: Vec) -> Vec:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def sub(a: Vec, b: Vec) -> Vec:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def scale(t, a: Vec) -> Vec:
    return (t * a[0], t * a[1], t * a[2])


def dot(a: Vec, b: Vec):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a: Vec, b: Vec) -> Vec:
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def norm(a: Vec) -> float:
    return sqrt(float(dot(a, a)))


def lincomb(ws: Sequence, ps: Sequence[Vec]) -> Vec:
    """Return sum of ws[i] * ps[i]."""
    x = y = z = 0
    for w, p in zip(ws, ps):
        x += w * p[0]
        y += w * p[1]
        z += w * p[2]
    return (x, y, z)


# ---- Bernstein basis -------------------------------------------------------

def bernstein(n: int, t) -> list:
    """Values B_{i,n}(t) for i = 0..n, by the explicit formula."""
    s = 1 - t
    return [comb(n, i) * t ** i * s ** (n - i) for i in range(n + 1)]


def bernstein_d(n: int, t, k: int) -> list:
    """k-th derivatives of B_{i,n} at t, for k = 0, 1, 2, from the difference formula."""
    if k == 0 or n == 0:
        return bernstein(n, t) if k == 0 else [0] * (n + 1)
    low = bernstein_d(n - 1, t, k - 1)
    out = []
    for i in range(n + 1):
        a = low[i - 1] if i >= 1 else 0
        b = low[i] if i <= n - 1 else 0
        out.append(n * (a - b))
    return out


def patch_point(P: Sequence[Sequence[Vec]], u, v) -> Vec:
    m, n = len(P) - 1, len(P[0]) - 1
    bu, bv = bernstein(m, u), bernstein(n, v)
    x = y = z = 0
    for i in range(m + 1):
        for j in range(n + 1):
            w = bu[i] * bv[j]
            q = P[i][j]
            x += w * q[0]
            y += w * q[1]
            z += w * q[2]
    return (x, y, z)


def patch_derivs(P: Sequence[Sequence[Vec]], u, v) -> tuple:
    """Return (r, r_u, r_v, r_uu, r_uv, r_vv) of a Bezier patch at (u, v)."""
    m, n = len(P) - 1, len(P[0]) - 1
    U = [bernstein_d(m, u, k) for k in range(3)]
    V = [bernstein_d(n, v, k) for k in range(3)]
    out = []
    for a, b in ((0, 0), (1, 0), (0, 1), (2, 0), (1, 1), (0, 2)):
        x = y = z = 0
        for i in range(m + 1):
            ui = U[a][i]
            for j in range(n + 1):
                w = ui * V[b][j]
                q = P[i][j]
                x += w * q[0]
                y += w * q[1]
                z += w * q[2]
        out.append((x, y, z))
    return tuple(out)


def curve_point(C: Sequence[Vec], t) -> Vec:
    return lincomb(bernstein(len(C) - 1, t), C)


# ---- univariate polynomials, coefficient lists from the constant term ------

def ptrim(a: list) -> list:
    a = list(a)
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def padd(a: list, b: list) -> list:
    n = max(len(a), len(b))
    return ptrim([(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)])


def pscale(c, a: list) -> list:
    return ptrim([c * x for x in a])


def pmul(a: list, b: list) -> list:
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x == 0:
            continue
        for j, y in enumerate(b):
            out[i + j] += x * y
    return ptrim(out)


def ppow(a: list, k: int) -> list:
    out = [1]
    for _ in range(k):
        out = pmul(out, a)
    return out


def peval(a: list, t):
    s = 0
    for c in reversed(a):
        s = s * t + c
    return s


def pderiv(a: list) -> list:
    return ptrim([i * a[i] for i in range(1, len(a))]) if len(a) > 1 else [0]


def real_roots(a: list, lo: float, hi: float, tol: float = 1e-13) -> list:
    """Real roots of a polynomial in [lo, hi], each once, in increasing order.

    The roots of the derivative split [lo, hi] into pieces on which the
    polynomial is monotone; each piece holds at most one root, found by
    bisection. A root of even multiplicity is found when the polynomial is
    zero (to within the rounding of a float) at a critical point.
    """
    a = ptrim([float(c) for c in a])
    if len(a) == 1:
        return []
    crit = real_roots(pderiv(a), lo, hi, tol) if len(a) > 2 else []
    knots = [lo] + [c for c in crit if lo < c < hi] + [hi]
    scale_ = max(abs(c) for c in a)
    roots = []
    for x0, x1 in zip(knots, knots[1:]):
        f0, f1 = peval(a, x0), peval(a, x1)
        if f0 == 0 or abs(f0) <= 1e-14 * scale_:
            if not roots or abs(roots[-1] - x0) > 1e-9:
                roots.append(x0)
            continue
        if f0 * f1 > 0:
            continue
        if f1 == 0 or abs(f1) <= 1e-14 * scale_:
            continue
        a0, a1 = x0, x1
        while a1 - a0 > tol:
            mid = 0.5 * (a0 + a1)
            fm = peval(a, mid)
            if (fm < 0) == (f0 < 0):
                a0, f0 = mid, fm
            else:
                a1 = mid
        roots.append(0.5 * (a0 + a1))
    f_hi = peval(a, hi)
    if abs(f_hi) <= 1e-14 * scale_ and (not roots or abs(roots[-1] - hi) > 1e-9):
        roots.append(hi)
    return roots


# ---- dense linear algebra --------------------------------------------------

def solve(A: list, b: list) -> list:
    """Solve A x = b by Gaussian elimination with partial pivoting.

    Works for Fraction entries (exact, pivot = first nonzero) and for floats.
    Raises ZeroDivisionError when A is singular (exactly, or to the pivot test
    1e-300 for floats).
    """
    n = len(A)
    M = [list(A[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(M[r][c]))
        if M[piv][c] == 0 or (isinstance(M[piv][c], float) and abs(M[piv][c]) < 1e-300):
            raise ZeroDivisionError("singular matrix")
        M[c], M[piv] = M[piv], M[c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]
            if f != 0:
                for k in range(c, n + 1):
                    M[r][k] -= f * M[c][k]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        s = M[i][n] - sum(M[i][k] * x[k] for k in range(i + 1, n))
        x[i] = s / M[i][i]
    return x


def det(A: list):
    """Determinant by fraction free Bareiss elimination for int and Fraction
    entries, and by Gaussian elimination for floats."""
    n = len(A)
    if n == 0:
        return 1
    if any(isinstance(x, float) for row in A for x in row):
        M = [list(map(float, row)) for row in A]
        d = 1.0
        for c in range(n):
            piv = max(range(c, n), key=lambda r: abs(M[r][c]))
            if M[piv][c] == 0:
                return 0.0
            if piv != c:
                M[c], M[piv] = M[piv], M[c]
                d = -d
            d *= M[c][c]
            for r in range(c + 1, n):
                f = M[r][c] / M[c][c]
                for k in range(c, n):
                    M[r][k] -= f * M[c][k]
        return d
    M = [[Fraction(x) for x in row] for row in A]
    sign = 1
    prev = Fraction(1)
    for c in range(n - 1):
        if M[c][c] == 0:
            piv = next((r for r in range(c + 1, n) if M[r][c] != 0), None)
            if piv is None:
                return Fraction(0)
            M[c], M[piv] = M[piv], M[c]
            sign = -sign
        for r in range(c + 1, n):
            for k in range(c + 1, n):
                M[r][k] = (M[r][k] * M[c][c] - M[r][c] * M[c][k]) / prev
            M[r][c] = Fraction(0)
        prev = M[c][c]
    return sign * M[n - 1][n - 1]


def jacobi_eigen(A: list, sweeps: int = 60) -> tuple:
    """Eigenvalues and eigenvectors of a small symmetric float matrix by the
    cyclic Jacobi method. Returns (values, vectors) with vectors[k] the unit
    eigenvector of values[k], sorted by increasing value."""
    n = len(A)
    M = [[float(x) for x in row] for row in A]
    V = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(sweeps):
        off = sum(M[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off < 1e-30:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if abs(M[p][q]) < 1e-300:
                    continue
                theta = (M[q][q] - M[p][p]) / (2 * M[p][q])
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + sqrt(theta * theta + 1))
                c = 1 / sqrt(t * t + 1)
                s = t * c
                for k in range(n):
                    mkp, mkq = M[k][p], M[k][q]
                    M[k][p], M[k][q] = c * mkp - s * mkq, s * mkp + c * mkq
                for k in range(n):
                    mpk, mqk = M[p][k], M[q][k]
                    M[p][k], M[q][k] = c * mpk - s * mqk, s * mpk + c * mqk
                for k in range(n):
                    vkp, vkq = V[k][p], V[k][q]
                    V[k][p], V[k][q] = c * vkp - s * vkq, s * vkp + c * vkq
    order = sorted(range(n), key=lambda i: M[i][i])
    return [M[i][i] for i in order], [[V[k][i] for k in range(n)] for i in order]
