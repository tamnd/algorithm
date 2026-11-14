# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-method-of-moments/. The authors are listed in prov/A39F7K.jsonl.

from collections.abc import Callable, Sequence
from typing import Any, NamedTuple

from stdist import chi2_sf

Vector = list
Matrix = list
MomentFn = Callable[[Any, Vector], Vector]
JacobianFn = Callable[[Any, Vector], Matrix]


def solve(a: Matrix, b: Vector) -> Vector:
    """Solve a x = b by Gaussian elimination with partial pivoting.

    Works for float and Fraction entries. Precondition: a is square and
    nonsingular. Cost: O(k^3) for a k x k matrix.
    """
    k = len(a)
    m = [list(row) + [b[i]] for i, row in enumerate(a)]
    for c in range(k):
        p = max(range(c, k), key=lambda r: abs(m[r][c]))
        if m[p][c] == 0:
            raise ZeroDivisionError("singular matrix")
        m[c], m[p] = m[p], m[c]
        for r in range(c + 1, k):
            f = m[r][c] / m[c][c]
            if f != 0:
                for j in range(c, k + 1):
                    m[r][j] = m[r][j] - f * m[c][j]
    x = [0] * k
    for r in range(k - 1, -1, -1):
        s = m[r][k]
        for j in range(r + 1, k):
            s = s - m[r][j] * x[j]
        x[r] = s / m[r][r]
    return x


def inverse(a: Matrix) -> Matrix:
    """Return the inverse of a nonsingular square matrix, column by column."""
    k = len(a)
    cols = [solve(a, [1 if i == j else 0 for i in range(k)]) for j in range(k)]
    return [[cols[j][i] for j in range(k)] for i in range(k)]


def _matmul(a: Matrix, b: Matrix) -> Matrix:
    return [[sum(a[i][t] * b[t][j] for t in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def _t(a: Matrix) -> Matrix:
    return [list(col) for col in zip(*a)]


def _matvec(a: Matrix, v: Vector) -> Vector:
    return [sum(r[j] * v[j] for j in range(len(v))) for r in a]


def sample_moments(g: MomentFn, data: Sequence, theta: Vector) -> tuple[Vector, list]:
    """Return g-bar(theta) = (1/n) sum g(x_i, theta) and the rows g(x_i, theta). Cost O(n q)."""
    rows = [g(x, theta) for x in data]
    n = len(rows)
    q = len(rows[0])
    return [sum(r[j] for r in rows) / n for j in range(q)], rows  # @line L2


def mean_jacobian(dg: JacobianFn | None, g: MomentFn, data: Sequence, theta: Vector, h: float = 1e-6) -> Matrix:
    """Return G = d g-bar / d theta (q x k). Central differences when dg is None."""
    n = len(data)
    if dg is not None:
        mats = [dg(x, theta) for x in data]
        q, k = len(mats[0]), len(mats[0][0])
        return [[sum(m[i][j] for m in mats) / n for j in range(k)] for i in range(q)]
    k = len(theta)
    cols = []
    for j in range(k):
        up = list(theta)
        dn = list(theta)
        up[j] += h
        dn[j] -= h
        gu, _ = sample_moments(g, data, up)
        gd, _ = sample_moments(g, data, dn)
        cols.append([(a - b) / (2 * h) for a, b in zip(gu, gd)])
    return _t(cols)


def moment_covariance(rows: list, gbar: Vector) -> Matrix:
    """Centered S = (1/n) sum (g_i - g-bar)(g_i - g-bar)'. Divisor n. Cost O(n q^2)."""
    n = len(rows)
    q = len(gbar)
    return [[sum((r[i] - gbar[i]) * (r[j] - gbar[j]) for r in rows) / n for j in range(q)] for i in range(q)]


def objective(g: MomentFn, data: Sequence, theta: Vector, w: Matrix) -> float:
    """Q(theta) = g-bar' W g-bar."""
    gb, _ = sample_moments(g, data, theta)
    return sum(gb[i] * w[i][j] * gb[j] for i in range(len(gb)) for j in range(len(gb)))


def minimize_gmm(
    g: MomentFn,
    data: Sequence,
    theta0: Sequence,
    w: Matrix,
    dg: JacobianFn | None = None,
    tol: float = 1e-14,
    max_iter: int = 100,
    min_step: float = 2.0 ** -30,
) -> tuple[Vector, int, bool]:
    """Minimize g-bar' W g-bar by Gauss-Newton steps with step halving.

    W must be symmetric positive definite and G'WG nonsingular. The step is
    delta = -(G'WG)^-1 G'W g-bar. Stops when the decrement -b'delta <= tol.
    For moments linear in theta one exact step reaches the minimum.
    Cost per step: O(n q k) for G plus O(k^3).
    """
    theta = list(theta0)
    for t in range(max_iter):
        gb, _ = sample_moments(g, data, theta)
        big_g = mean_jacobian(dg, g, data, theta)
        gtw = _matmul(_t(big_g), w)
        a = _matmul(gtw, big_g)
        b = _matvec(gtw, gb)
        delta = [-v for v in solve(a, b)]
        dec = -sum(bi * di for bi, di in zip(b, delta))
        if dec <= tol:
            return theta, t, True
        q_old = sum(gb[i] * w[i][j] * gb[j] for i in range(len(gb)) for j in range(len(gb)))
        s = 1
        new = [ti + di for ti, di in zip(theta, delta)]
        q_new = objective(g, data, new, w)
        while q_new > q_old and s > min_step:
            s = s / 2
            new = [ti + s * di for ti, di in zip(theta, delta)]
            q_new = objective(g, data, new, w)
        if q_new > q_old:
            return theta, t, False
        theta = new
    return theta, max_iter, False


def efficient_cov(big_g: Matrix, s: Matrix, n: int) -> Matrix:
    """(G' S^-1 G)^-1 / n, the covariance of efficient GMM."""
    gts = _matmul(_t(big_g), inverse(s))
    v = inverse(_matmul(gts, big_g))
    return [[e / n for e in row] for row in v]


def sandwich_cov(big_g: Matrix, w: Matrix, s: Matrix, n: int) -> Matrix:
    """(G'WG)^-1 G'W S W G (G'WG)^-1 / n, the covariance for a fixed weight W."""
    gtw = _matmul(_t(big_g), w)
    bread = inverse(_matmul(gtw, big_g))
    meat = _matmul(_matmul(gtw, s), _t(gtw))
    v = _matmul(_matmul(bread, meat), bread)
    return [[e / n for e in row] for row in v]


class GMMResult(NamedTuple):
    theta: list        # two-step estimate
    cov: list          # (G' S^-1 G)^-1 / n at theta, S from the first step
    j_stat: float      # n g-bar' S^-1 g-bar at theta
    df: int            # q - k
    p_value: float     # chi-squared(q - k) upper tail of j_stat; 1.0 when df = 0
    first_step: list   # estimate with the first weight
    weight: list       # S^-1, the second-step weight
    converged: bool


def gmm(
    g: MomentFn,
    data: Sequence,
    theta0: Sequence,
    dg: JacobianFn | None = None,
    w1: Matrix | None = None,
    tol: float = 1e-14,
    max_iter: int = 100,
) -> GMMResult:
    """Two-step efficient GMM with Hansen's J test of the overidentifying conditions.

    g(x, theta) returns the q moment functions of one observation, with
    E g(X, theta_0) = 0 at the true theta_0 and q >= k = len(theta0). The data
    are iid. dg(x, theta) is the q x k derivative; None uses central
    differences. w1 is the first-step weight (identity when None).
    S is centered with divisor n. Cost: O(n q (q + k)) per Gauss-Newton step.
    """
    data = list(data)  # @line L1
    n = len(data)
    q = len(g(data[0], list(theta0)))
    k = len(theta0)
    if q < k:
        raise ValueError("need at least as many moment conditions as parameters")
    w = w1 if w1 is not None else [[1 if i == j else 0 for j in range(q)] for i in range(q)]  # @line L3
    th1, _, ok1 = minimize_gmm(g, data, theta0, w, dg, tol, max_iter)  # @line L4
    gb1, rows1 = sample_moments(g, data, th1)
    s = moment_covariance(rows1, gb1)  # @line L5
    w2 = inverse(s)
    th, _, ok2 = minimize_gmm(g, data, th1, w2, dg, tol, max_iter)  # @line L6
    big_g = mean_jacobian(dg, g, data, th)  # @line L7
    cov = efficient_cov(big_g, s, n)  # @line L8
    gb, _ = sample_moments(g, data, th)
    j = n * sum(gb[a] * w2[a][b] * gb[b] for a in range(q) for b in range(q))  # @line L9
    df = q - k
    p = chi2_sf(float(j), df) if df > 0 else 1.0
    return GMMResult(th, cov, j, df, p, th1, w2, ok1 and ok2)  # @line L10
