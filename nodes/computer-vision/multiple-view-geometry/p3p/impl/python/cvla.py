# SPDX-License-Identifier: MIT
# Shared helper of the computer vision pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""Small dense linear algebra for the computer vision pages.

A matrix is a list of rows. A vector is a flat list. The functions do not
change their arguments. Entries are floats, but zeros, eye, transpose, add,
sub, scale, mul, matvec, dot, cross, skew, solve, inv and det also work with
fractions.Fraction entries and then give exact results.

Tolerances:
- solve, inv and det raise ValueError only on an exact zero pivot. A matrix
  that is close to singular gives large entries; check the condition yourself.
- sym_eig and svd stop a Jacobi sweep when every off-diagonal term is below
  1e-15 times the size of its pair (at most 100 sweeps).
- polyroots_real keeps a root z when |Im z| <= imag_tol * max(1, |z|), with
  imag_tol = 1e-6 by default. Roots of multiplicity k are found with an error
  of about 1e-16^(1/k) relative, so a double root keeps an imaginary part near
  1e-8.

This module holds no algorithm of a computer vision page.
"""

from __future__ import annotations

import cmath
import math
from typing import List, Sequence, Tuple

Matrix = List[List[float]]
Vector = List[float]

_JACOBI_EPS = 1e-15
_MAX_SWEEPS = 100


# ---------------------------------------------------------------- basics

def zeros(m: int, n: int) -> Matrix:
    """The m x n zero matrix."""
    return [[0.0] * n for _ in range(m)]


def eye(n: int) -> Matrix:
    """The n x n identity matrix."""
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def _is_matrix(a) -> bool:
    return len(a) > 0 and isinstance(a[0], (list, tuple))


def transpose(a: Sequence[Sequence[float]]) -> Matrix:
    """The transpose of a matrix."""
    return [list(col) for col in zip(*a)]


def add(a, b):
    """a + b for two vectors or two matrices of the same shape."""
    if _is_matrix(a):
        return [[x + y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]
    return [x + y for x, y in zip(a, b)]


def sub(a, b):
    """a - b for two vectors or two matrices of the same shape."""
    if _is_matrix(a):
        return [[x - y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]
    return [x - y for x, y in zip(a, b)]


def scale(a, c):
    """c times a, for a vector or a matrix a and a number c."""
    if _is_matrix(a):
        return [[c * x for x in row] for row in a]
    return [c * x for x in a]


def mul(a: Sequence[Sequence[float]], b: Sequence[Sequence[float]]) -> Matrix:
    """The matrix product a b."""
    if len(a[0]) != len(b):
        raise ValueError("mul: shapes do not match")
    bt = list(zip(*b))
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def matvec(a: Sequence[Sequence[float]], x: Sequence[float]) -> Vector:
    """The product a x of a matrix and a vector."""
    if len(a[0]) != len(x):
        raise ValueError("matvec: shapes do not match")
    return [sum(p * q for p, q in zip(row, x)) for row in a]


def dot(x: Sequence[float], y: Sequence[float]) -> float:
    """The inner product of two vectors."""
    return sum(p * q for p, q in zip(x, y))


def norm(a) -> float:
    """The Euclidean norm of a vector, or the Frobenius norm of a matrix."""
    if _is_matrix(a):
        return math.sqrt(sum(float(x) * float(x) for row in a for x in row))
    return math.sqrt(sum(float(x) * float(x) for x in a))


def cross(a: Sequence[float], b: Sequence[float]) -> Vector:
    """The cross product a x b of two 3-vectors."""
    return [a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0]]


def skew(a: Sequence[float]) -> Matrix:
    """The skew matrix [a]_x, with skew(a) b = cross(a, b)."""
    z = a[0] - a[0]
    return [[z, -a[2], a[1]],
            [a[2], z, -a[0]],
            [-a[1], a[0], z]]


# ---------------------------------------------------- Gaussian elimination

def _eliminate(a: Matrix, b: Matrix) -> Tuple[Matrix, Matrix, int]:
    """Reduce [a | b] to upper triangular form with partial pivoting.

    Works in place on copies made by the caller. Returns a, b and the sign
    of the row permutation.
    """
    n = len(a)
    sign = 1
    for k in range(n):
        p = max(range(k, n), key=lambda i: abs(a[i][k]))
        if a[p][k] == 0:
            raise ValueError("singular matrix")
        if p != k:
            a[k], a[p] = a[p], a[k]
            b[k], b[p] = b[p], b[k]
            sign = -sign
        piv = a[k][k]
        for i in range(k + 1, n):
            f = a[i][k] / piv
            if f == 0:
                continue
            ai, ak = a[i], a[k]
            for j in range(k, n):
                ai[j] = ai[j] - f * ak[j]
            bi, bk = b[i], b[k]
            for j in range(len(bi)):
                bi[j] = bi[j] - f * bk[j]
    return a, b, sign


def solve(a: Sequence[Sequence[float]], b):
    """Solve a x = b for a square a, by Gaussian elimination with partial
    pivoting. b is a vector or a matrix (several right-hand sides); the
    result has the same form. Raises ValueError on an exact zero pivot."""
    n = len(a)
    if any(len(row) != n for row in a):
        raise ValueError("solve: matrix is not square")
    vec = not _is_matrix(b)
    rhs = [[x] for x in b] if vec else [list(row) for row in b]
    if len(rhs) != n:
        raise ValueError("solve: shapes do not match")
    u, c, _ = _eliminate([list(row) for row in a], rhs)
    m = len(c[0]) if n else 0
    x = [[0.0] * m for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(m):
            s = c[i][j]
            for k in range(i + 1, n):
                s = s - u[i][k] * x[k][j]
            x[i][j] = s / u[i][i]
    return [row[0] for row in x] if vec else x


def inv(a: Sequence[Sequence[float]]) -> Matrix:
    """The inverse of a square matrix. Raises ValueError if it is singular."""
    n = len(a)
    one = a[0][0] - a[0][0] + 1 if n else 1.0
    ident = [[one if i == j else one - one for j in range(n)] for i in range(n)]
    return solve(a, ident)


def det(a: Sequence[Sequence[float]]) -> float:
    """The determinant of a square matrix, by Gaussian elimination."""
    n = len(a)
    if any(len(row) != n for row in a):
        raise ValueError("det: matrix is not square")
    if n == 0:
        return 1.0
    try:
        u, _, sign = _eliminate([list(row) for row in a], [[] for _ in range(n)])
    except ValueError:
        return a[0][0] - a[0][0]
    d = u[0][0] - u[0][0] + sign
    for i in range(n):
        d = d * u[i][i]
    return d


# ------------------------------------------------------- Jacobi methods

def sym_eig(a: Sequence[Sequence[float]]) -> Tuple[Vector, Matrix]:
    """Eigenvalues and eigenvectors of a real symmetric matrix by the cyclic
    Jacobi method. Returns (w, V): w ascending, and column j of V is a unit
    eigenvector for w[j], so a = V diag(w) V^T. Only the upper triangle of
    a is read (the lower triangle is taken as its mirror)."""
    n = len(a)
    s = [[float(a[min(i, j)][max(i, j)]) for j in range(n)] for i in range(n)]
    v = eye(n)
    for _ in range(_MAX_SWEEPS):
        rotated = False
        for p in range(n - 1):
            for q in range(p + 1, n):
                apq = s[p][q]
                if apq == 0.0:
                    continue
                app, aqq = s[p][p], s[q][q]
                if abs(apq) <= _JACOBI_EPS * math.sqrt(abs(app * aqq)) or \
                        abs(apq) < 1e-300:
                    s[p][q] = s[q][p] = 0.0
                    continue
                rotated = True
                theta = (aqq - app) / (2.0 * apq)
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                sn = t * c
                for k in range(n):
                    skp, skq = s[k][p], s[k][q]
                    s[k][p] = c * skp - sn * skq
                    s[k][q] = sn * skp + c * skq
                for k in range(n):
                    spk, sqk = s[p][k], s[q][k]
                    s[p][k] = c * spk - sn * sqk
                    s[q][k] = sn * spk + c * sqk
                s[p][q] = s[q][p] = 0.0
                for k in range(n):
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p] = c * vkp - sn * vkq
                    v[k][q] = sn * vkp + c * vkq
        if not rotated:
            break
    order = sorted(range(n), key=lambda i: s[i][i])
    w = [s[i][i] for i in order]
    vs = [[v[k][i] for i in order] for k in range(n)]
    return w, vs


def _complete_basis(cols: List[Vector], m: int, need: List[int]) -> None:
    """Replace the columns with index in need by unit vectors orthogonal to
    all other columns (Gram-Schmidt on the standard basis)."""
    keep = [c for i, c in enumerate(cols) if i not in need]
    for i in need:
        best, best_norm = None, -1.0
        for e in range(m):
            x = [0.0] * m
            x[e] = 1.0
            for _ in range(2):
                for c in keep:
                    d = dot(c, x)
                    x = [xi - d * ci for xi, ci in zip(x, c)]
            nx = norm(x)
            if nx > best_norm:
                best, best_norm = x, nx
        u = [xi / best_norm for xi in best]
        cols[i] = u
        keep.append(u)


def _svd_tall(a: Sequence[Sequence[float]]) -> Tuple[Matrix, Vector, Matrix]:
    m, n = len(a), len(a[0])
    cols = [[float(a[i][j]) for i in range(m)] for j in range(n)]
    vcols = [[1.0 if i == j else 0.0 for i in range(n)] for j in range(n)]
    for _ in range(_MAX_SWEEPS):
        rotated = False
        for p in range(n - 1):
            for q in range(p + 1, n):
                cp, cq = cols[p], cols[q]
                alpha = sum(x * x for x in cp)
                beta = sum(x * x for x in cq)
                gamma = sum(x * y for x, y in zip(cp, cq))
                if gamma == 0.0 or abs(gamma) <= _JACOBI_EPS * math.sqrt(alpha * beta):
                    continue
                rotated = True
                zeta = (beta - alpha) / (2.0 * gamma)
                t = (1.0 if zeta >= 0 else -1.0) / (abs(zeta) + math.sqrt(1.0 + zeta * zeta))
                c = 1.0 / math.sqrt(1.0 + t * t)
                s = c * t
                cols[p] = [c * x - s * y for x, y in zip(cp, cq)]
                cols[q] = [s * x + c * y for x, y in zip(cp, cq)]
                vp, vq = vcols[p], vcols[q]
                vcols[p] = [c * x - s * y for x, y in zip(vp, vq)]
                vcols[q] = [s * x + c * y for x, y in zip(vp, vq)]
        if not rotated:
            break
    sv = [norm(c) for c in cols]
    order = sorted(range(n), key=lambda i: -sv[i])
    sv = [sv[i] for i in order]
    cols = [cols[i] for i in order]
    vcols = [vcols[i] for i in order]
    smax = sv[0] if sv else 0.0
    ucols: List[Vector] = []
    need: List[int] = []
    for i, c in enumerate(cols):
        if sv[i] > 1e-13 * smax and sv[i] > 1e-300:
            ucols.append([x / sv[i] for x in c])
        else:
            ucols.append([0.0] * m)
            need.append(i)
    if need:
        _complete_basis(ucols, m, need)
    return transpose(ucols), sv, transpose(vcols)


def svd(a: Sequence[Sequence[float]]) -> Tuple[Matrix, Vector, Matrix]:
    """Thin singular value decomposition by the one-sided Jacobi method.

    For an m x n matrix a with k = min(m, n), returns (U, S, V) with U of
    size m x k, S a list of k values in descending order and V of size
    n x k, such that a = U diag(S) V^T. U and V have orthonormal columns.
    For m >= n, V is square (n x n)."""
    m, n = len(a), len(a[0])
    if m >= n:
        return _svd_tall(a)
    u, s, v = _svd_tall(transpose(a))
    return v, s, u


def nullvec(a: Sequence[Sequence[float]]) -> Vector:
    """A unit vector x that minimizes ||a x||: the right singular vector of
    the smallest singular value. If a has fewer rows than columns, zero rows
    are added first, so the result is in the null space. The sign is not
    fixed."""
    m, n = len(a), len(a[0])
    rows = [list(map(float, r)) for r in a] + [[0.0] * n for _ in range(n - m)]
    _, _, v = _svd_tall(rows)
    return [v[i][n - 1] for i in range(n)]


# ---------------------------------------------- orthogonal factorizations

def qr(a: Sequence[Sequence[float]]) -> Tuple[Matrix, Matrix]:
    """QR factorization by Householder reflections. For an m x n matrix a,
    returns Q (m x m, orthogonal) and R (m x n, upper triangular) with
    a = Q R. The signs are chosen so that the diagonal of R is >= 0."""
    m, n = len(a), len(a[0])
    r = [[float(x) for x in row] for row in a]
    q = eye(m)
    for k in range(min(m - 1, n)):
        x = [r[i][k] for i in range(k, m)]
        nx = norm(x)
        if nx == 0.0:
            continue
        alpha = -nx if x[0] >= 0 else nx
        v = list(x)
        v[0] -= alpha
        nv = norm(v)
        if nv == 0.0:
            continue
        v = [vi / nv for vi in v]
        for j in range(n):
            d = sum(v[i - k] * r[i][j] for i in range(k, m))
            if d != 0.0:
                for i in range(k, m):
                    r[i][j] -= 2.0 * v[i - k] * d
        for i in range(m):
            d = sum(q[i][l] * v[l - k] for l in range(k, m))
            if d != 0.0:
                for l in range(k, m):
                    q[i][l] -= 2.0 * d * v[l - k]
    for k in range(min(m, n)):
        if r[k][k] < 0:
            r[k] = [-x for x in r[k]]
            for i in range(m):
                q[i][k] = -q[i][k]
    for i in range(m):
        for j in range(min(i, n)):
            r[i][j] = 0.0
    return q, r


def rq(a: Sequence[Sequence[float]]) -> Tuple[Matrix, Matrix]:
    """RQ factorization of a square matrix: returns R (upper triangular,
    with a diagonal >= 0) and Q (orthogonal) with a = R Q. It is computed
    from the QR factorization of the transpose of the row-reversed matrix."""
    n = len(a)
    if any(len(row) != n for row in a):
        raise ValueError("rq: matrix is not square")
    flipped = transpose([list(row) for row in reversed(a)])
    q1, r1 = qr(flipped)
    rt = transpose(r1)
    r = [list(reversed(row)) for row in reversed(rt)]
    q = [list(row) for row in reversed(transpose(q1))]
    return r, q


def cholesky(a: Sequence[Sequence[float]]) -> Matrix:
    """The lower triangular L with a = L L^T, for a symmetric positive
    definite a. Raises ValueError if a pivot is not positive."""
    n = len(a)
    low = zeros(n, n)
    for j in range(n):
        d = a[j][j] - sum(low[j][k] * low[j][k] for k in range(j))
        if d <= 0:
            raise ValueError("cholesky: matrix is not positive definite")
        low[j][j] = math.sqrt(d)
        for i in range(j + 1, n):
            low[i][j] = (a[i][j] - sum(low[i][k] * low[j][k] for k in range(j))) / low[j][j]
    return low


# ---------------------------------------------------------- polynomials

def _horner(c: Sequence[complex], x):
    p = 0.0
    for ci in c:
        p = p * x + ci
    return p


def polyroots_real(coeffs: Sequence[float], imag_tol: float = 1e-6) -> Vector:
    """Real roots of the polynomial with the given coefficients, highest
    power first. All complex roots are found by the Durand-Kerner method.
    A root z is kept as real when |Im z| <= imag_tol * max(1, |z|); its real
    part is then polished by Newton steps on the real polynomial. Returns
    the real roots in ascending order, with repeats for multiple roots."""
    c = [float(x) for x in coeffs]
    while c and c[0] == 0.0:
        c.pop(0)
    n = len(c) - 1
    if n < 1:
        return []
    c = [x / c[0] for x in c]
    rho = max([abs(c[i]) ** (1.0 / i) for i in range(1, n + 1)] + [0.0])
    if rho == 0.0:
        return [0.0] * n
    z = [rho * cmath.exp(1j * (2.0 * math.pi * k / n + 0.4)) for k in range(n)]
    for _ in range(2000):
        moved = 0.0
        for k in range(n):
            den = 1.0 + 0j
            for j in range(n):
                if j != k:
                    den *= z[k] - z[j]
            if den == 0:
                den = 1e-12 * rho
            step = _horner(c, z[k]) / den
            z[k] -= step
            moved = max(moved, abs(step) / max(1.0, abs(z[k])))
        if moved <= 1e-15:
            break
    deriv = [c[i] * (n - i) for i in range(n)]
    roots = []
    for zk in z:
        if abs(zk.imag) > imag_tol * max(1.0, abs(zk)):
            continue
        x = zk.real
        px = _horner(c, x)
        for _ in range(8):
            dp = _horner(deriv, x)
            if dp == 0.0 or px == 0.0:
                break
            xn = x - px / dp
            pn = _horner(c, xn)
            if abs(pn) >= abs(px):
                break
            x, px = xn, pn
        roots.append(x)
    return sorted(roots)


# ------------------------------------------------------------ self-test

def self_test() -> None:
    """Check svd, sym_eig and polyroots_real. Raises AssertionError."""
    import random
    rng = random.Random(7)
    for _ in range(3):
        a = [[rng.uniform(-1, 1) for _ in range(5)] for _ in range(5)]
        u, s, v = svd(a)
        rec = mul(mul(u, [[s[i] if i == j else 0.0 for j in range(5)] for i in range(5)]), transpose(v))
        assert norm(sub(rec, a)) <= 1e-10
        assert all(s[i] >= s[i + 1] for i in range(4))
        sym = add(a, transpose(a))
        w, vv = sym_eig(sym)
        rec = mul(mul(vv, [[w[i] if i == j else 0.0 for j in range(5)] for i in range(5)]), transpose(vv))
        assert norm(sub(rec, sym)) <= 1e-10
        assert all(w[i] <= w[i + 1] for i in range(4))
    r = polyroots_real([1.0, -6.0, 11.0, -6.0])
    assert len(r) == 3
    assert all(abs(x - y) <= 1e-10 for x, y in zip(r, [1.0, 2.0, 3.0]))


if __name__ == "__main__":
    self_test()
