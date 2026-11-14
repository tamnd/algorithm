# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/knockoff-filter/. The authors are listed in prov/WNY22A.jsonl.
"""The fixed-X knockoff filter of Barber and Candes (2015), in pure Python.

knockoffs(X) normalizes the columns of the n x p design X (n >= 2p) and builds
equicorrelated knockoffs Xk with
  Xk^T Xk = Sigma,  X^T Xk = Sigma - s I,  Sigma = X^T X,
where s = min(2 lambda_min(Sigma), 1), as
  Xk = X (I - s Sigma^{-1}) + U C,  C^T C = 2 s I - s^2 Sigma^{-1},
with U an n x p orthonormal matrix orthogonal to the columns of X.

A statistic W_j is large and positive when X_j beats its knockoff. Two choices are
given: the marginal one |X_j^T y| - |Xk_j^T y|, and the OLS one on [X Xk].
The filter selects {j : W_j >= T}, with
  T = min{t in {|W_j| : W_j != 0} : (offset + #{W_j <= -t}) / max(#{W_j >= t}, 1) <= q},
offset = 1 for knockoff+ (FDR <= q) and 0 for the plain knockoff (modified FDR <= q).
"""

import math
import random
from bisect import bisect_left
from collections.abc import Callable, Sequence


def _dot(a: Sequence[float], b: Sequence[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def _transpose(a: Sequence[Sequence[float]]) -> list[list[float]]:
    return [list(r) for r in zip(*a)]


def _matmul(a: Sequence[Sequence[float]], b: Sequence[Sequence[float]]) -> list[list[float]]:
    bt = _transpose(b)
    return [[_dot(row, col) for col in bt] for row in a]


def jacobi_eigen(a: Sequence[Sequence[float]], tol: float = 1e-13, max_sweeps: int = 100):
    """Eigenvalues and eigenvectors of a symmetric matrix by cyclic Jacobi rotations: a = V diag(w) V^T."""
    n = len(a)
    a = [list(map(float, row)) for row in a]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    scale = max(1.0, max((abs(x) for row in a for x in row), default=0.0))
    for _ in range(max_sweeps):
        off = math.sqrt(sum(a[i][j] ** 2 for i in range(n) for j in range(i + 1, n)))
        if off <= tol * scale:
            break
        for p in range(n):
            for q in range(p + 1, n):
                if a[p][q] == 0.0:
                    continue
                theta = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1.0))
                c = 1.0 / math.sqrt(t * t + 1.0)
                s = t * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p], a[k][q] = c * akp - s * akq, s * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k], a[q][k] = c * apk - s * aqk, s * apk + c * aqk
                for k in range(n):
                    vkp, vkq = v[k][p], v[k][q]
                    v[k][p], v[k][q] = c * vkp - s * vkq, s * vkp + c * vkq
    return [a[i][i] for i in range(n)], v


def _orthonormal_complement(x: Sequence[Sequence[float]], k: int, rng: random.Random) -> list[list[float]]:
    """An n x k matrix with orthonormal columns, orthogonal to the columns of x (Gram-Schmidt, twice)."""
    n, p = len(x), len(x[0])
    basis: list[list[float]] = []
    candidates = [[x[i][j] for i in range(n)] for j in range(p)]
    candidates += [[rng.gauss(0.0, 1.0) for _ in range(n)] for _ in range(k)]
    for v in candidates:
        norm0 = math.sqrt(_dot(v, v))
        for _ in range(2):
            for b in basis:
                c = _dot(b, v)
                v = [vi - c * bi for vi, bi in zip(v, b)]
        norm = math.sqrt(_dot(v, v))
        if norm <= 1e-10 * max(norm0, 1.0):
            raise ValueError("the design does not have full column rank, or n < 2p")
        basis.append([vi / norm for vi in v])
    return _transpose(basis[p:])


def knockoffs(x: Sequence[Sequence[float]], s: float | None = None, rng: random.Random | None = None):
    """Return (Xn, Xk, s): the column-normalized design, its equicorrelated fixed-X knockoffs, and s."""
    n, p = len(x), len(x[0])
    if n < 2 * p:
        raise ValueError("fixed-X knockoffs need n >= 2p")
    rng = rng or random.Random(0)
    norms = [math.sqrt(sum(x[i][j] ** 2 for i in range(n))) for j in range(p)]
    xn = [[x[i][j] / norms[j] for j in range(p)] for i in range(n)]  # @line L1
    sigma = _matmul(_transpose(xn), xn)
    w, v = jacobi_eigen(sigma)
    if min(w) <= 1e-12:
        raise ValueError("the design does not have full column rank")
    if s is None:
        s = min(2.0 * min(w), 1.0)  # @line L2
    if not 0 < s <= 2.0 * min(w) + 1e-12:
        raise ValueError("need 0 < s <= 2 lambda_min(Sigma)")
    sigma_inv = [[sum(v[i][k] * v[j][k] / w[k] for k in range(p)) for j in range(p)] for i in range(p)]
    a = [[(2.0 * s if i == j else 0.0) - s * s * sigma_inv[i][j] for j in range(p)] for i in range(p)]
    mu, vv = jacobi_eigen(a)
    c = [[math.sqrt(max(mu[k], 0.0)) * vv[j][k] for j in range(p)] for k in range(p)]  # @line L3
    u = _orthonormal_complement(xn, p, rng)  # @line L4
    shrink = [[(1.0 if i == j else 0.0) - s * sigma_inv[i][j] for j in range(p)] for i in range(p)]
    left, right = _matmul(xn, shrink), _matmul(u, c)
    xk = [[left[i][j] + right[i][j] for j in range(p)] for i in range(n)]  # @line L5
    return xn, xk, s


def marginal_statistic(xn: Sequence[Sequence[float]], xk: Sequence[Sequence[float]]) -> Callable:
    """y -> W with W_j = |X_j^T y| - |Xk_j^T y|."""
    xt, xkt = _transpose(xn), _transpose(xk)
    return lambda y: [abs(_dot(a, y)) - abs(_dot(b, y)) for a, b in zip(xt, xkt)]


def ols_statistic(xn: Sequence[Sequence[float]], xk: Sequence[Sequence[float]]) -> Callable:
    """y -> W with W_j = |b_j| - |b_{j+p}|, b the least-squares fit of y on [X Xk]. Needs s < 2 lambda_min."""
    p = len(xn[0])
    aug = [list(r1) + list(r2) for r1, r2 in zip(xn, xk)]
    w, v = jacobi_eigen(_matmul(_transpose(aug), aug))
    if min(w) <= 1e-9 * max(w):
        raise ValueError("[X Xk] is singular; choose s below 2 lambda_min(Sigma)")
    gram_inv = [[sum(v[i][k] * v[j][k] / w[k] for k in range(2 * p)) for j in range(2 * p)] for i in range(2 * p)]
    m = _matmul(gram_inv, _transpose(aug))

    def stat(y: Sequence[float]) -> list[float]:
        b = [_dot(row, y) for row in m]
        return [abs(b[j]) - abs(b[j + p]) for j in range(p)]

    return stat


def knockoff_threshold(w: Sequence, q, plus: bool = True):
    """The smallest t in {|W_j| : W_j != 0} with (offset + #{W <= -t}) <= q max(#{W >= t}, 1); inf if none."""
    offset = 1 if plus else 0
    ts = sorted({abs(x) for x in w if x != 0})  # @line L6
    neg = sorted(-x for x in w if x < 0)
    pos = sorted(x for x in w if x > 0)
    for t in ts:
        n_neg = len(neg) - bisect_left(neg, t)
        n_pos = len(pos) - bisect_left(pos, t)
        if offset + n_neg <= q * max(n_pos, 1):  # @line L7
            return t
    return math.inf


def knockoff_select(w: Sequence, q, plus: bool = True) -> list[bool]:
    t = knockoff_threshold(w, q, plus)
    return [x >= t for x in w]  # @line L8
