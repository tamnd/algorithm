# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/svm-poisoning-attack/. The authors are listed in prov/VZRNHS.jsonl.

"""The poisoning attack of Biggio, Nelson and Laskov (2012) on a linear soft-margin SVM, as an abstract model.

The tests build every training set and validation set from a fixed seed (two Gaussian
blobs in a few dimensions). Nothing here reads a real data set or a deployed model.
Labels are +1 and -1. The SVM is the dual problem

    min_a  1/2 a^T Q a - 1^T a   subject to  0 <= a_i <= C  and  sum_i y_i a_i = 0,

with Q_ij = y_i y_j <x_i, x_j>, solved by SMO and then made exact on its active set.
"""

import math
from dataclasses import dataclass
from typing import Sequence

Vector = list[float]
Matrix = list[list[float]]


def dot(u: Sequence[float], v: Sequence[float]) -> float:
    """Inner product. Cost O(d)."""
    return math.fsum(a * b for a, b in zip(u, v, strict=True))


def solve(a: Matrix, rhs: Vector) -> Vector:
    """Solve a x = rhs by Gaussian elimination with partial pivoting. Raises ValueError if a is singular. Cost O(m^3)."""
    m = len(a)
    aug = [list(a[i]) + [rhs[i]] for i in range(m)]
    scale = max((abs(x) for row in a for x in row), default=0.0)
    for col in range(m):
        piv = max(range(col, m), key=lambda r: abs(aug[r][col]))
        if abs(aug[piv][col]) <= 1e-12 * max(scale, 1.0):
            raise ValueError("singular system")
        aug[col], aug[piv] = aug[piv], aug[col]
        for r in range(m):
            if r != col and aug[r][col] != 0.0:
                f = aug[r][col] / aug[col][col]
                for c in range(col, m + 1):
                    aug[r][c] -= f * aug[col][c]
    return [aug[i][m] / aug[i][i] for i in range(m)]


@dataclass
class Svm:
    """A trained linear SVM: dual variables, weights w, bias b, and the index sets of the solution."""

    alpha: Vector
    w: Vector
    b: float
    margin: list[int]  # S: 0 < alpha < C, so y f(x) = 1
    error: list[int]  # E: alpha = C, so y f(x) <= 1
    rest: list[int]  # R: alpha = 0, so y f(x) >= 1


def _sets(alpha: Sequence[float], c: float, eps: float) -> tuple[list[int], list[int], list[int]]:
    s, e, r = [], [], []
    for i, a in enumerate(alpha):
        (r if a <= eps else e if a >= c - eps else s).append(i)
    return s, e, r


def _finish(xs: Sequence[Sequence[float]], ys: Sequence[int], alpha: Vector, b: float, c: float) -> Svm:
    d = len(xs[0])
    w = [math.fsum(alpha[i] * ys[i] * xs[i][j] for i in range(len(xs))) for j in range(d)]
    s, e, r = _sets(alpha, c, 1e-9 * c)
    return Svm(alpha, w, b, s, e, r)


def kkt_violation(xs: Sequence[Sequence[float]], ys: Sequence[int], m: Svm, c: float) -> float:
    """The largest violation of the KKT conditions of m, in units of the margin. Cost O(n d)."""
    worst = abs(math.fsum(a * y for a, y in zip(m.alpha, ys)))
    for i, (x, y) in enumerate(zip(xs, ys)):
        g = y * (dot(m.w, x) + m.b)
        a = m.alpha[i]
        worst = max(worst, -a, a - c)
        if i in m.margin:
            worst = max(worst, abs(g - 1.0))
        elif i in m.error:
            worst = max(worst, g - 1.0)
        else:
            worst = max(worst, 1.0 - g)
    return worst


def _polish(xs: Sequence[Sequence[float]], ys: Sequence[int], alpha: Vector, c: float) -> tuple[Vector, float] | None:
    """Solve the KKT equations exactly on the active sets that alpha suggests; None if they do not hold."""
    n = len(xs)
    s, e, _ = _sets(alpha, c, 1e-6 * c)
    if not s:
        return None
    fixed = [c if i in e else 0.0 for i in range(n)]
    k = len(s)
    a = [[ys[p] * ys[q] * dot(xs[p], xs[q]) for q in s] + [float(ys[p])] for p in s]
    a.append([float(ys[q]) for q in s] + [0.0])
    rhs = [1.0 - math.fsum(ys[p] * ys[j] * dot(xs[p], xs[j]) * fixed[j] for j in e) for p in s]
    rhs.append(-math.fsum(ys[j] * fixed[j] for j in e))
    try:
        sol = solve(a, rhs)
    except ValueError:
        return None
    new = fixed[:]
    for t, p in enumerate(s):
        new[p] = sol[t]
    b = sol[k]
    m = _finish(xs, ys, new, b, c)
    m.margin, m.error = s, e
    m.rest = [i for i in range(n) if i not in s and i not in e]
    if kkt_violation(xs, ys, m, c) > 1e-9:
        return None
    return new, b


def train_svm(xs: Sequence[Sequence[float]], ys: Sequence[int], c: float, tol: float = 1e-10, max_iter: int = 200000) -> Svm:
    """Train a linear soft-margin SVM by SMO with the maximal violating pair, then solve its active set exactly.

    Precondition: both labels occur and c > 0. Cost O(max_iter n + n^2 d) for SMO, and O(n^3) for the exact solve.
    """
    n = len(xs)
    q = [[ys[i] * ys[j] * dot(xs[i], xs[j]) for j in range(n)] for i in range(n)]
    alpha = [0.0] * n
    grad = [-1.0] * n  # Q alpha - 1
    for _ in range(max_iter):
        up = [t for t in range(n) if (ys[t] > 0 and alpha[t] < c) or (ys[t] < 0 and alpha[t] > 0)]
        low = [t for t in range(n) if (ys[t] > 0 and alpha[t] > 0) or (ys[t] < 0 and alpha[t] < c)]
        i = max(up, key=lambda t: -ys[t] * grad[t])
        j = min(low, key=lambda t: -ys[t] * grad[t])
        if -ys[i] * grad[i] + ys[j] * grad[j] < tol:
            break
        ai, aj = alpha[i], alpha[j]
        if ys[i] != ys[j]:
            quad = max(q[i][i] + q[j][j] + 2 * q[i][j], 1e-12)
            delta = (-grad[i] - grad[j]) / quad
            diff = ai - aj
            ni, nj = ai + delta, aj + delta
            if diff > 0:
                if nj < 0:
                    nj, ni = 0.0, diff
            elif ni < 0:
                ni, nj = 0.0, -diff
            if diff > 0:
                if ni > c:
                    ni, nj = c, c - diff
            elif nj > c:
                nj, ni = c, c + diff
        else:
            quad = max(q[i][i] + q[j][j] - 2 * q[i][j], 1e-12)
            delta = (grad[i] - grad[j]) / quad
            total = ai + aj
            ni, nj = ai - delta, aj + delta
            if total > c:
                if ni > c:
                    ni, nj = c, total - c
            elif nj < 0:
                nj, ni = 0.0, total
            if total > c:
                if nj > c:
                    nj, ni = c, total - c
            elif ni < 0:
                ni, nj = 0.0, total
        di, dj = ni - ai, nj - aj
        alpha[i], alpha[j] = ni, nj
        for t in range(n):
            grad[t] += q[t][i] * di + q[t][j] * dj
    polished = _polish(xs, ys, alpha, c)
    if polished is not None:
        new, b = polished
        m = _finish(xs, ys, new, b, c)
        s, e, _ = _sets(alpha, c, 1e-6 * c)
        m.margin, m.error = s, e
        m.rest = [i for i in range(n) if i not in s and i not in e]
        return m
    free = [t for t in range(n) if 0 < alpha[t] < c]
    if free:
        b = -math.fsum(ys[t] * grad[t] for t in free) / len(free)
    else:
        up = [t for t in range(n) if (ys[t] > 0 and alpha[t] < c) or (ys[t] < 0 and alpha[t] > 0)]
        low = [t for t in range(n) if (ys[t] > 0 and alpha[t] > 0) or (ys[t] < 0 and alpha[t] < c)]
        b = (max(-ys[t] * grad[t] for t in up) + min(-ys[t] * grad[t] for t in low)) / 2
    return _finish(xs, ys, alpha, b, c)


def hinge_total(m: Svm, val: Sequence[tuple[Sequence[float], int]]) -> float:
    """The attacker objective L = sum over the validation set of max(0, 1 - y f(x)). Cost O(v d)."""
    return math.fsum(max(0.0, 1.0 - y * (dot(m.w, x) + m.b)) for x, y in val)


def error_rate(m: Svm, val: Sequence[tuple[Sequence[float], int]]) -> float:
    """Fraction of validation points with y f(x) <= 0. Cost O(v d)."""
    return sum(1 for x, y in val if y * (dot(m.w, x) + m.b) <= 0) / len(val)


def poison_gradient(xs: Sequence[Sequence[float]], ys: Sequence[int], m: Svm, c: float, val: Sequence[tuple[Sequence[float], int]]) -> Vector:
    """Gradient of hinge_total in the last training point x_c, with the sets S, E, R of m held fixed.

    The last point (xs[-1], ys[-1]) is the attack point. Precondition: it is not in S
    (its alpha is 0 or C), S is not empty, and the KKT matrix on S is nonsingular; the
    gradient then exists wherever no point changes set and no validation point sits on
    its margin. Cost O(s^3 + s d^2 + v d) for s = |S| and v validation points.
    """
    cidx = len(xs) - 1
    d = len(xs[0])
    if cidx in m.margin:
        raise ValueError("the attack point is a margin support vector")
    s = m.margin
    if not s:
        raise ValueError("no margin support vector")
    yc, ac = ys[cidx], m.alpha[cidx]
    k = len(s)
    a = [[ys[p] * ys[q] * dot(xs[p], xs[q]) for q in s] + [float(ys[p])] for p in s]
    a.append([float(ys[q]) for q in s] + [0.0])
    # Columns j = 1..d: d(alpha_S, b) / d(x_c)_j = -K^{-1} [a_c y_c y_s (x_s)_j ; 0]
    dalpha = [[0.0] * d for _ in range(k)]
    db = [0.0] * d
    for j in range(d):
        rhs = [-ac * yc * ys[p] * xs[p][j] for p in s] + [0.0]
        sol = solve(a, rhs)
        for t in range(k):
            dalpha[t][j] = sol[t]
        db[j] = sol[k]
    # dw / d(x_c) = sum_s y_s x_s (d alpha_s)^T + a_c y_c I
    dw = [[math.fsum(ys[p] * xs[p][r] * dalpha[t][j] for t, p in enumerate(s)) + (ac * yc if r == j else 0.0) for j in range(d)] for r in range(d)]
    g = [0.0] * d
    for x, y in val:
        if 1.0 - y * (dot(m.w, x) + m.b) > 0.0:
            for j in range(d):
                g[j] -= y * (math.fsum(x[r] * dw[r][j] for r in range(d)) + db[j])
    return g


def poison(
    xs: Sequence[Sequence[float]],
    ys: Sequence[int],
    val: Sequence[tuple[Sequence[float], int]],
    c: float,
    x0: Sequence[float],
    yc: int,
    step: float,
    lo: float,
    hi: float,
    iters: int,
    eps: float,
) -> tuple[Vector, list[float]]:
    """Gradient ascent on the validation hinge loss over one attack point (x_c, yc) in the box [lo, hi]^d.

    Stops when the loss rises by less than eps, after iters steps, or where the gradient
    does not exist or is zero. Returns the final x_c and the loss after each training.
    Precondition: the conditions of poison_gradient at each step. Cost O(iters) SVM trainings.
    """
    xc = list(x0)  # @line L1
    losses: list[float] = []
    for _ in range(iters):  # @line L2
        m = train_svm(list(xs) + [xc], list(ys) + [yc], c)  # @line L3
        losses.append(hinge_total(m, val))
        if len(losses) >= 2 and losses[-1] - losses[-2] < eps:  # @line L6
            break
        try:
            u = poison_gradient(list(xs) + [xc], list(ys) + [yc], m, c, val)  # @line L4
        except ValueError:
            break
        norm = math.sqrt(math.fsum(a * a for a in u))
        if norm <= 1e-9 * max(len(val), 1):  # a flat region, for example |S| = d + 1
            break
        xc = [min(max(a + step * g / norm, lo), hi) for a, g in zip(xc, u)]  # @line L5
    return xc, losses  # @line L7
