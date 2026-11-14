# SPDX-License-Identifier: MIT
# Shared helper of the re1 cad pages of https://algorithm.tamnd.com/. The authors are listed in prov/.

"""Small dense linear algebra for the re1 fitting pages.

Vectors are tuples or lists of numbers, matrices are lists of rows. The
elimination routines work with int, Fraction or float entries: with Fraction
they are exact. The Jacobi routine is float only. The helper holds no
fitting algorithm of any page.
"""

from fractions import Fraction
from math import atan2, cos, sin, sqrt
from typing import List, Optional, Sequence, Tuple

Vec = Sequence
Mat = List[List]


# ---- vectors ----


def dot(a: Vec, b: Vec):
    return sum(x * y for x, y in zip(a, b))


def add(a: Vec, b: Vec) -> tuple:
    return tuple(x + y for x, y in zip(a, b))


def sub(a: Vec, b: Vec) -> tuple:
    return tuple(x - y for x, y in zip(a, b))


def scale(s, a: Vec) -> tuple:
    return tuple(s * x for x in a)


def norm(a: Vec) -> float:
    return sqrt(float(dot(a, a)))


def cross(a: Vec, b: Vec) -> tuple:
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


# ---- matrices ----


def zeros(n: int, m: int, z=0) -> Mat:
    return [[z] * m for _ in range(n)]


def transpose(a: Mat) -> Mat:
    return [list(r) for r in zip(*a)]


def mat_vec(a: Mat, x: Vec) -> list:
    return [dot(r, x) for r in a]


def mat_mul(a: Mat, b: Mat) -> Mat:
    bt = transpose(b)
    return [[dot(r, c) for c in bt] for r in a]


def gram(rows: Sequence[Vec]) -> Mat:
    """The matrix sum over the rows u of u u^T."""
    n = len(rows[0])
    g = zeros(n, n)
    for u in rows:
        for i in range(n):
            if u[i] == 0:
                continue
            for j in range(n):
                g[i][j] += u[i] * u[j]
    return g


# ---- elimination (exact with Fraction) ----


def solve(a: Mat, b: Vec, tol: float = 0.0) -> Optional[list]:
    """Solve a x = b for a square a by Gaussian elimination with partial pivoting.

    Returns None when a pivot has absolute value at most tol (singular
    matrix). With Fraction entries and tol = 0 the answer is exact.
    """
    n = len(a)
    m = [list(a[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        if abs(m[p][c]) <= tol:
            return None
        m[c], m[p] = m[p], m[c]
        for r in range(c + 1, n):
            f = m[r][c] / m[c][c]
            if f != 0:
                for k in range(c, n + 1):
                    m[r][k] -= f * m[c][k]
    x = [0] * n
    for r in range(n - 1, -1, -1):
        s = m[r][n] - sum(m[r][k] * x[k] for k in range(r + 1, n))
        x[r] = s / m[r][r]
    return x


def lstsq(a: Mat, b: Vec, tol: float = 0.0) -> Optional[list]:
    """Least squares solution of a x = b by the normal equations (a^T a) x = a^T b."""
    at = transpose(a)
    return solve(mat_mul(at, a), mat_vec(at, b), tol)


def nullspace(a: Mat) -> List[list]:
    """A basis of the null space of a, by reduced row echelon form. Exact for Fraction entries."""
    m = [[Fraction(x) for x in r] for r in a]
    rows, cols = len(m), len(m[0])
    piv = []
    r = 0
    for c in range(cols):
        p = next((i for i in range(r, rows) if m[i][c] != 0), None)
        if p is None:
            continue
        m[r], m[p] = m[p], m[r]
        inv = 1 / m[r][c]
        m[r] = [x * inv for x in m[r]]
        for i in range(rows):
            if i != r and m[i][c] != 0:
                f = m[i][c]
                m[i] = [x - f * y for x, y in zip(m[i], m[r])]
        piv.append(c)
        r += 1
        if r == rows:
            break
    free = [c for c in range(cols) if c not in piv]
    basis = []
    for f in free:
        v = [Fraction(0)] * cols
        v[f] = Fraction(1)
        for i, c in enumerate(piv):
            v[c] = -m[i][f]
        basis.append(v)
    return basis


def rank(a: Mat) -> int:
    return len(a[0]) - len(nullspace(a))


# ---- symmetric matrices (float) ----


def cholesky(a: Mat, rtol: float = 0.0) -> Mat:
    """Lower triangular l with l l^T = a, for a symmetric positive definite a.

    Raises ValueError when a pivot is at most rtol times the largest diagonal entry.
    """
    n = len(a)
    l = zeros(n, n, 0.0)
    big = max(abs(float(a[i][i])) for i in range(n))
    for i in range(n):
        for j in range(i + 1):
            s = a[i][j] - sum(l[i][k] * l[j][k] for k in range(j))
            if i == j:
                if s <= rtol * big:
                    raise ValueError("matrix is not positive definite")
                l[i][i] = sqrt(s)
            else:
                l[i][j] = s / l[j][j]
    return l


def lower_solve(l: Mat, b: Vec) -> list:
    x = []
    for i in range(len(l)):
        x.append((b[i] - sum(l[i][k] * x[k] for k in range(i))) / l[i][i])
    return x


def upper_solve_t(l: Mat, b: Vec) -> list:
    """Solve l^T x = b for a lower triangular l."""
    n = len(l)
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(l[k][i] * x[k] for k in range(i + 1, n))) / l[i][i]
    return x


def jacobi_eigen(a: Mat, sweeps: int = 100, eps: float = 1e-15) -> Tuple[list, Mat]:
    """Eigenvalues and eigenvectors of a symmetric matrix by cyclic Jacobi rotations.

    Returns (values, vectors) with the values in ascending order and
    vectors[k] the unit eigenvector of values[k].
    """
    n = len(a)
    s = [[float(x) for x in r] for r in a]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(sweeps):
        off = sum(s[i][j] ** 2 for i in range(n) for j in range(n) if i != j)
        if off <= eps * eps * max(1.0, sum(s[i][i] ** 2 for i in range(n))):
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if s[p][q] == 0.0:
                    continue
                th = 0.5 * atan2(2 * s[p][q], s[q][q] - s[p][p])
                c, sn = cos(th), sin(th)
                for k in range(n):
                    skp, skq = s[k][p], s[k][q]
                    s[k][p] = c * skp - sn * skq
                    s[k][q] = sn * skp + c * skq
                for k in range(n):
                    spk, sqk = s[p][k], s[q][k]
                    s[p][k] = c * spk - sn * sqk
                    s[q][k] = sn * spk + c * sqk
                for k in range(n):
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p] = c * vkp - sn * vkq
                    v[k][q] = sn * vkp + c * vkq
    order = sorted(range(n), key=lambda i: s[i][i])
    return [s[i][i] for i in order], [[v[k][i] for k in range(n)] for i in order]
