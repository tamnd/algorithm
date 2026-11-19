# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cross-lingual-embedding-mapping/. The authors are listed in prov/CP9A01.jsonl.

"""Linear and orthogonal maps between two embedding spaces.

X and Y are lists of n rows of length d. Row i of Y is the vector of the
translation of the word of row i of X (the seed dictionary). A map W is a
d x d matrix that sends a source vector x to W x.

procrustes_map solves min ||W X^T - Y^T||_F over orthogonal W. The answer is
W = U V^T, where U S V^T is the singular value decomposition of M = Y^T X
(Schönemann 1966). The SVD is a one-sided Jacobi method in pure Python.
polar_newton is an independent check: the Newton iteration for the
orthogonal polar factor of a nonsingular M gives the same W.

least_squares_map is the unconstrained map of Mikolov, Le and Sutskever 2013.
"""

import math
from typing import Sequence

Matrix = list[list[float]]


def transpose(a: Sequence[Sequence[float]]) -> Matrix:
    return [list(col) for col in zip(*a)]


def matmul(a: Sequence[Sequence[float]], b: Sequence[Sequence[float]]) -> Matrix:
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def identity(d: int) -> Matrix:
    return [[1.0 if i == j else 0.0 for j in range(d)] for i in range(d)]


def apply(w: Sequence[Sequence[float]], x: Sequence[float]) -> list[float]:
    return [sum(a * b for a, b in zip(row, x)) for row in w]


def normalize_rows(x: Sequence[Sequence[float]], center: bool = False) -> Matrix:
    """Optionally subtract the mean row, then scale each row to unit length."""
    rows = [list(map(float, r)) for r in x]
    if center and rows:
        mean = [sum(c) / len(rows) for c in zip(*rows)]
        rows = [[a - m for a, m in zip(r, mean)] for r in rows]
    out = []
    for r in rows:
        nrm = math.sqrt(sum(a * a for a in r))
        out.append([a / nrm for a in r] if nrm > 0 else r)
    return out


def svd(m: Sequence[Sequence[float]], tol: float = 1e-15, max_sweeps: int = 100):
    """Return U, s, V with M = U diag(s) V^T for a square matrix M.

    One-sided Jacobi (Hestenes): rotate pairs of columns of A = M until they
    are orthogonal, and apply the same rotations to V. Then the column norms
    are the singular values and the normalized columns are the columns of U.
    Columns of U for zero singular values are completed to an orthonormal basis.
    """
    d = len(m)
    a = [list(map(float, r)) for r in m]
    v = identity(d)
    for _ in range(max_sweeps):
        rotated = False
        for p in range(d - 1):
            for q in range(p + 1, d):
                alpha = sum(a[i][p] ** 2 for i in range(d))
                beta = sum(a[i][q] ** 2 for i in range(d))
                gamma = sum(a[i][p] * a[i][q] for i in range(d))
                if abs(gamma) <= tol * math.sqrt(alpha * beta) or gamma == 0.0:
                    continue
                rotated = True
                zeta = (beta - alpha) / (2.0 * gamma)
                t = (1.0 if zeta >= 0 else -1.0) / (abs(zeta) + math.sqrt(1.0 + zeta * zeta))
                c = 1.0 / math.sqrt(1.0 + t * t)
                s = c * t
                for mat in (a, v):
                    for i in range(d):
                        x, y = mat[i][p], mat[i][q]
                        mat[i][p] = c * x - s * y
                        mat[i][q] = s * x + c * y
        if not rotated:
            break
    sv = [math.sqrt(sum(a[i][j] ** 2 for i in range(d))) for j in range(d)]
    order = sorted(range(d), key=lambda j: -sv[j])
    s = [sv[j] for j in order]
    v = [[v[i][j] for j in order] for i in range(d)]
    cols: list[list[float]] = []
    scale = s[0] if s and s[0] > 0 else 1.0
    for k, j in enumerate(order):
        if s[k] > 1e-12 * scale:
            cols.append([a[i][j] / s[k] for i in range(d)])
        else:
            cols.append(None)  # type: ignore[arg-type]
    basis = iter(identity(d))
    for k in range(d):
        if cols[k] is not None:
            continue
        while True:  # Gram-Schmidt on the unit vectors until one is independent
            e = next(basis)
            for c in cols:
                if c is not None:
                    dot = sum(x * y for x, y in zip(e, c))
                    e = [x - dot * y for x, y in zip(e, c)]
            nrm = math.sqrt(sum(x * x for x in e))
            if nrm > 1e-6:
                cols[k] = [x / nrm for x in e]
                break
    u = transpose(cols)
    return u, s, v


def procrustes_map(x: Sequence[Sequence[float]], y: Sequence[Sequence[float]]) -> Matrix:
    """The orthogonal W that minimizes sum_i |W x_i - y_i|^2."""
    m = matmul(transpose(y), x)  # @line L2
    u, _, v = svd(m)  # @line L3
    return matmul(u, transpose(v))  # @line L4


def fit_orthogonal(x, y, normalize: bool = True, center: bool = False) -> Matrix:
    """The full method: optional unit length (and centering), then Procrustes."""
    if normalize:
        x, y = normalize_rows(x, center), normalize_rows(y, center)  # @line L1
    return procrustes_map(x, y)  # @line L5


def inverse(m: Sequence[Sequence[float]]) -> Matrix:
    """Gauss-Jordan inverse with partial pivoting."""
    d = len(m)
    a = [list(map(float, r)) + [1.0 if i == j else 0.0 for j in range(d)] for i, r in enumerate(m)]
    for c in range(d):
        p = max(range(c, d), key=lambda r: abs(a[r][c]))
        if abs(a[p][c]) < 1e-300:
            raise ValueError("singular matrix")
        a[c], a[p] = a[p], a[c]
        piv = a[c][c]
        a[c] = [t / piv for t in a[c]]
        for r in range(d):
            if r != c and a[r][c] != 0.0:
                f = a[r][c]
                a[r] = [s - f * t for s, t in zip(a[r], a[c])]
    return [row[d:] for row in a]


def polar_newton(m: Sequence[Sequence[float]], iters: int = 100, tol: float = 1e-15) -> Matrix:
    """Orthogonal polar factor of a nonsingular M by W <- (W + W^-T) / 2."""
    w = [list(map(float, r)) for r in m]
    for _ in range(iters):
        nxt = [[(a + b) / 2.0 for a, b in zip(r1, r2)] for r1, r2 in zip(w, transpose(inverse(w)))]
        diff = max(abs(a - b) for r1, r2 in zip(nxt, w) for a, b in zip(r1, r2))
        w = nxt
        if diff < tol:
            break
    return w


def least_squares_map(x: Sequence[Sequence[float]], y: Sequence[Sequence[float]]) -> Matrix:
    """The unconstrained W = (Y^T X)(X^T X)^-1; needs n >= d and X of full rank."""
    return matmul(matmul(transpose(y), x), inverse(matmul(transpose(x), x)))


def loss(w: Sequence[Sequence[float]], x, y) -> float:
    return sum(sum((a - b) ** 2 for a, b in zip(apply(w, xi), yi)) for xi, yi in zip(x, y))


def orthogonality_error(w: Sequence[Sequence[float]]) -> float:
    g = matmul(w, transpose(w))
    return max(abs(g[i][j] - (1.0 if i == j else 0.0)) for i in range(len(g)) for j in range(len(g)))


def cosine(u: Sequence[float], v: Sequence[float]) -> float:
    nu = math.sqrt(sum(a * a for a in u))
    nv = math.sqrt(sum(a * a for a in v))
    return sum(a * b for a, b in zip(u, v)) / (nu * nv)


def translate(w, source: dict[str, Sequence[float]], target: dict[str, Sequence[float]]) -> dict[str, str]:
    """Nearest target word by cosine for each mapped source word (ties: the first in sorted order)."""
    out = {}
    for s, vec in source.items():
        z = apply(w, vec)
        best = max(sorted(target), key=lambda t: cosine(z, target[t]))
        out[s] = best
    return out


def precision_at_1(pred: dict[str, str], gold: dict[str, set[str]]) -> float:
    return sum(1 for s in gold if pred.get(s) in gold[s]) / len(gold)
