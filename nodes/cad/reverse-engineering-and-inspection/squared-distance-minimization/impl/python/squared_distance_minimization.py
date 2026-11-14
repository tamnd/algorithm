# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/squared-distance-minimization/. The authors are listed in prov/YVZM72.jsonl.

"""Squared distance minimization (SDM) for fitting a planar B-spline curve.

Each iteration computes the foot point K_k of every data point X_k on the
current curve, with the unit tangent T_k, the unit normal N_k (T turned by
90 degrees to the left), the signed curvature kappa_k and the signed distance
d_k = (X_k - K_k) . N_k. Near X_k the squared distance to the curve is, to
second order, w ((y - K) . T)^2 + ((y - K) . N)^2 with

    w = d / (d - rho) = kappa d / (kappa d - 1),   rho = 1 / kappa.

SDM puts the curve displacement into this model: it minimizes

    sum_k [ w_k ((C_Q(t_k) - X_k) . T_k)^2 + ((C_Q(t_k) - X_k) . N_k)^2 ] + mu R(Q)

over the new control points Q (plus a tiny damping term |Q - P|^2), a linear
least-squares problem, with w_k set
to 0 when 0 <= kappa d < 1 (the model is then the tangent distance) and to 1
when the foot point is an end of the curve (the model is then the distance to
that end point). R is the sum of the squared second differences of the control
points. A step is shortened by halving until the true energy

    f(P) = sum_k dist(X_k, C_P)^2 + mu R(P)

does not grow, so the energy never increases.
"""

from math import sqrt
from typing import List, Optional, Sequence, Tuple

from re1lin import dot, solve, sub

Point = Tuple[float, float]


# ---- B-spline evaluation ----


def find_span(U: Sequence[float], p: int, t: float) -> int:
    n = len(U) - p - 2
    if t >= U[n + 1]:
        return n
    if t <= U[p]:
        return p
    lo, hi = p, n + 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if t < U[mid]:
            hi = mid
        else:
            lo = mid
    return lo


def basis_row(U: Sequence[float], p: int, t: float) -> List[float]:
    """All B-spline values N_{i,p}(t), by the Cox-de Boor recursion on the span of t."""
    n = len(U) - p - 2
    s = find_span(U, p, t)
    b = [0.0] * (p + 1)
    b[0] = 1.0
    left, right = [0.0] * (p + 1), [0.0] * (p + 1)
    for j in range(1, p + 1):
        left[j] = t - U[s + 1 - j]
        right[j] = U[s + j] - t
        saved = 0.0
        for r in range(j):
            tmp = b[r] / (right[r + 1] + left[j - r])
            b[r] = saved + right[r + 1] * tmp
            saved = left[j - r] * tmp
        b[j] = saved
    row = [0.0] * (n + 1)
    for a in range(p + 1):
        row[s - p + a] = b[a]
    return row


def _derivative(P, U, p):
    Q = []
    for i in range(len(P) - 1):
        h = U[i + p + 1] - U[i + 1]
        Q.append(tuple(p * (a - b) / h if h > 0 else 0.0 for a, b in zip(P[i + 1], P[i])))
    return Q, list(U[1:-1]), p - 1


def _evaluate(P, U, p, t):
    row = basis_row(U, p, t)
    return tuple(sum(r * c[j] for r, c in zip(row, P)) for j in range(len(P[0])))


class Curve:
    """A clamped planar B-spline curve with its first two derivatives."""

    def __init__(self, P: Sequence[Point], U: Sequence[float], p: int):
        if p < 2:
            raise ValueError("SDM needs curvature, so the degree must be at least 2")
        self.P, self.U, self.p = [tuple(map(float, x)) for x in P], list(map(float, U)), p
        self.d1 = _derivative(self.P, self.U, p)
        self.d2 = _derivative(*self.d1)
        self.a, self.b = self.U[p], self.U[len(self.U) - p - 1]

    def point(self, t: float) -> Point:
        return _evaluate(self.P, self.U, self.p, t)

    def first(self, t: float) -> Point:
        return _evaluate(*self.d1, t)

    def second(self, t: float) -> Point:
        return _evaluate(*self.d2, t)


def foot_point(curve: Curve, x: Point, table: Sequence[Tuple[float, Point]], newton_steps: int = 30) -> float:
    """The parameter of a nearest curve point to x: best sample, then Newton steps, never farther."""
    def dist2(t):
        e = sub(curve.point(t), x)
        return dot(e, e)

    best_t, best = min(((s, dot(sub(c, x), sub(c, x))) for s, c in table), key=lambda v: v[1])
    t = best_t
    for _ in range(newton_steps):
        e = sub(curve.point(t), x)
        c1, c2 = curve.first(t), curve.second(t)
        g, h = dot(e, c1), dot(c1, c1) + dot(e, c2)
        if h <= 0.0:
            break
        tn = min(curve.b, max(curve.a, t - g / h))
        done = abs(tn - t) <= 1e-15 * max(1.0, abs(t))
        t = tn
        if done:
            break
    return t if dist2(t) <= best else best_t


def sample_table(curve: Curve, samples: int) -> List[Tuple[float, Point]]:
    return [(s, curve.point(s)) for s in (curve.a + (curve.b - curve.a) * i / samples for i in range(samples + 1))]


# ---- the local model ----


def frame(curve: Curve, t: float) -> Tuple[Point, Point, float]:
    """Unit tangent T, unit normal N (T turned left) and signed curvature kappa at C(t)."""
    c1, c2 = curve.first(t), curve.second(t)
    speed = sqrt(dot(c1, c1))
    T = (c1[0] / speed, c1[1] / speed)
    N = (-T[1], T[0])
    kappa = (c1[0] * c2[1] - c1[1] * c2[0]) / speed ** 3
    return T, N, kappa


def sdm_weight(kappa: float, d: float) -> float:
    """w = d / (d - rho) = kappa d / (kappa d - 1), set to 0 when 0 <= kappa d < 1."""
    kd = kappa * d
    if kd >= 0.0:
        return 0.0
    return kd / (kd - 1.0)


def squared_distance_model(K: Point, T: Point, N: Point, kappa: float, y: Point) -> float:
    """The second-order model of the squared distance to the curve at y, for a point whose foot is K."""
    v = sub(y, K)
    d = dot(v, N)
    kd = kappa * d
    w = kd / (kd - 1.0)
    return w * dot(v, T) ** 2 + d * d


# ---- energy ----


def roughness(P: Sequence[Point]) -> float:
    return sum((P[i + 1][j] - 2 * P[i][j] + P[i - 1][j]) ** 2 for i in range(1, len(P) - 1) for j in range(2))


def energy(X: Sequence[Point], P: Sequence[Point], U: Sequence[float], p: int, mu: float = 0.0,
           samples: int = 64) -> float:
    """f(P) = sum of squared distances from the points to C_P, plus mu times the roughness."""
    curve = Curve(P, U, p)
    table = sample_table(curve, samples)
    total = 0.0
    for x in X:
        e = sub(curve.point(foot_point(curve, x, table)), x)
        total += dot(e, e)
    return total + mu * roughness(P)


# ---- SDM ----


def sdm_step(X: Sequence[Point], P: Sequence[Point], U: Sequence[float], p: int, mu: float,
             samples: int, damping: float = 0.0) -> List[Point]:
    """The minimizer of the SDM model: one linear least-squares problem in 2n unknowns.

    damping adds damping * (largest diagonal entry) * |Q - P|^2, which keeps the
    system nonsingular when tangential moves cost nothing, as on straight data.
    """
    curve = Curve(P, U, p)
    table = sample_table(curve, samples)
    n1 = len(P)
    m2 = 2 * n1
    A = [[0.0] * m2 for _ in range(m2)]
    rhs = [0.0] * m2

    def add_row(coef, target, weight):
        nz = [i for i in range(m2) if coef[i] != 0.0]
        for i in nz:
            rhs[i] += weight * coef[i] * target
            for j in nz:
                A[i][j] += weight * coef[i] * coef[j]

    for x in X:
        t = foot_point(curve, x, table)                                         # @line L3
        K = curve.point(t)
        T, N, kappa = frame(curve, t)
        d = dot(sub(x, K), N)
        end = t <= curve.a or t >= curve.b
        w = 1.0 if end else sdm_weight(kappa, d)                                 # @line L4
        row = basis_row(U, p, t)
        for direction, weight in ((T, w), (N, 1.0)):
            if weight == 0.0:
                continue
            coef = [0.0] * m2
            for i in range(n1):
                coef[2 * i] = row[i] * direction[0]
                coef[2 * i + 1] = row[i] * direction[1]
            add_row(coef, dot(x, direction), weight)
    if mu > 0.0:
        for i in range(1, n1 - 1):
            for j in range(2):
                coef = [0.0] * m2
                coef[2 * (i - 1) + j], coef[2 * i + j], coef[2 * (i + 1) + j] = 1.0, -2.0, 1.0
                add_row(coef, 0.0, mu)
    big = max(A[i][i] for i in range(m2))
    if damping > 0.0:
        for i in range(n1):
            for j in range(2):
                A[2 * i + j][2 * i + j] += damping * big
                rhs[2 * i + j] += damping * big * P[i][j]
    sol = solve(A, rhs, 1e-14 * big)                                            # @line L5
    if sol is None:
        raise ValueError("the SDM system is singular; use a positive damping")
    return [(sol[2 * i], sol[2 * i + 1]) for i in range(n1)]


def squared_distance_minimization(X: Sequence[Point], P: Sequence[Point], U: Sequence[float], p: int,
                                  mu: float = 1e-6, iterations: int = 50, tol: float = 1e-12,
                                  samples: int = 64, min_step: float = 1e-6, damping: float = 1e-10
                                  ) -> Tuple[List[Point], List[float], List[float]]:
    """Fit a planar clamped B-spline curve of degree p >= 2 to the points X by SDM.

    P is the starting control polygon. Returns (control points, history of the
    energy f, accepted step lengths). The energy history never increases.
    Precondition: the SDM systems are nonsingular (damping > 0 is enough).
    Cost per iteration: Theta(S p^2 + m (S + k p^2) + m n^2 + n^3) with the dense
    system used here, plus the same for each energy evaluation of the step search.
    """
    X = [tuple(map(float, x)) for x in X]
    P = [tuple(map(float, q)) for q in P]                                       # @line L1
    f = energy(X, P, U, p, mu, samples)
    history, steps = [f], []
    for _ in range(iterations):                                                 # @line L2
        target = sdm_step(X, P, U, p, mu, samples, damping)
        alpha = 1.0                                                             # @line L6
        while True:
            trial = [tuple(a + alpha * (b - a) for a, b in zip(q, r)) for q, r in zip(P, target)]
            ft = energy(X, trial, U, p, mu, samples)
            if ft <= f or alpha < min_step:
                break
            alpha /= 2
        if ft > f:
            break
        P, gain, f = trial, f - ft, ft                                          # @line L7
        history.append(f)
        steps.append(alpha)
        if gain <= tol * max(f, 1e-300):                                        # @line L8
            break
    return P, history, steps                                                    # @line L9
