# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parameter-correction/. The authors are listed in prov/RY3SVA.jsonl.

"""Parameter correction for least-squares B-spline curve fitting.

The fit alternates two steps on the error E(P, t) = sum_k |Q_k - C_P(t_k)|^2:
for fixed parameters t it solves the linear least-squares problem for the
control points P, and for fixed control points it moves every parameter t_k
to the foot point of Q_k on the current curve, the point where the error
vector Q_k - C(t_k) is normal to the curve. Neither step can raise E.

The curve is a clamped B-spline of degree p on the knot vector U, with
control points in any dimension. The foot point search takes the best of the
current parameter and a set of samples of the curve, refines it by Newton
steps on (C(t) - q) . C'(t) = 0, and keeps the new parameter only when the
distance does not grow.
"""

from typing import List, Optional, Sequence, Tuple

from re1lin import dot, solve, sub

Point = Tuple[float, ...]


# ---- B-spline evaluation ----


def find_span(U: Sequence[float], p: int, t: float) -> int:
    """The index s with U[s] <= t < U[s + 1], and the last span at the right end."""
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
    """All n + 1 B-spline values N_{i,p}(t), by the Cox-de Boor recursion on the span of t."""
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


def derivative_curve(P: Sequence[Point], U: Sequence[float], p: int) -> Tuple[List[Point], List[float], int]:
    """Control points, knots and degree of C'(t)."""
    Q = []
    for i in range(len(P) - 1):
        h = U[i + p + 1] - U[i + 1]
        Q.append(tuple(p * (a - b) / h if h > 0 else 0.0 for a, b in zip(P[i + 1], P[i])))
    return Q, list(U[1:-1]), p - 1


def evaluate(P: Sequence[Point], U: Sequence[float], p: int, t: float) -> Point:
    row = basis_row(U, p, t)
    return tuple(sum(r * c[j] for r, c in zip(row, P)) for j in range(len(P[0])))


class Curve:
    """A clamped B-spline curve with its first and second derivative curves."""

    def __init__(self, P: Sequence[Point], U: Sequence[float], p: int):
        self.P, self.U, self.p = [tuple(map(float, x)) for x in P], list(map(float, U)), p
        self.d1 = derivative_curve(self.P, self.U, p) if p >= 1 else None
        self.d2 = derivative_curve(*self.d1) if p >= 2 else None
        self.a, self.b = self.U[p], self.U[len(self.U) - p - 1]

    def point(self, t: float) -> Point:
        return evaluate(self.P, self.U, self.p, t)

    def first(self, t: float) -> Point:
        if self.d1 is None:
            return tuple(0.0 for _ in self.P[0])
        return evaluate(*self.d1, t)

    def second(self, t: float) -> Point:
        if self.d2 is None or self.d2[2] < 0:
            return tuple(0.0 for _ in self.P[0])
        return evaluate(*self.d2, t)


# ---- the two steps ----


def fit_control_points(Q: Sequence[Point], t: Sequence[float], U: Sequence[float], p: int) -> List[Point]:
    """Least-squares control points for fixed parameters, by the normal equations N^T N P = N^T Q.

    Precondition: N^T N is nonsingular (Schoenberg-Whitney), else ValueError.
    Cost: Theta(m p n + n^3) with the dense solver used here.
    """
    rows = [basis_row(U, p, tk) for tk in t]
    n1 = len(rows[0])
    A = [[0.0] * n1 for _ in range(n1)]
    for row in rows:
        nz = [i for i in range(n1) if row[i] != 0.0]
        for i in nz:
            for j in nz:
                A[i][j] += row[i] * row[j]
    big = max(A[i][i] for i in range(n1))
    cols = []
    for c in range(len(Q[0])):
        rhs = [sum(row[i] * q[c] for row, q in zip(rows, Q)) for i in range(n1)]
        x = solve(A, rhs, 1e-13 * big)
        if x is None:
            raise ValueError("the collocation matrix does not have full rank")
        cols.append(x)
    return [tuple(cols[c][i] for c in range(len(Q[0]))) for i in range(n1)]


def sample_table(curve: Curve, samples: int) -> List[Tuple[float, Point]]:
    """The pairs (s, C(s)) for samples + 1 equally spaced parameters s of [a, b]."""
    grid = [curve.a + (curve.b - curve.a) * i / samples for i in range(samples + 1)]
    return [(s, curve.point(s)) for s in grid]


def foot_point(curve: Curve, q: Point, t0: float, table: Sequence[Tuple[float, Point]],
               newton_steps: int = 30) -> float:
    """A parameter t whose distance |q - C(t)| is at most that of t0, refined to a foot point.

    Starts from the best of t0 and the sampled curve points of the table, and
    runs Newton steps on g(t) = (C(t) - q) . C'(t), clamped to [a, b].
    Cost: Theta(S d + k p^2) for S samples and k Newton steps.
    """
    def dist2(t):
        e = sub(curve.point(t), q)
        return dot(e, e)

    best_t, best = t0, dist2(t0)
    for s, c in table:
        e = sub(c, q)
        v = dot(e, e)
        if v < best:
            best_t, best = s, v
    t = best_t
    for _ in range(newton_steps):
        e = sub(curve.point(t), q)
        c1, c2 = curve.first(t), curve.second(t)
        g = dot(e, c1)
        h = dot(c1, c1) + dot(e, c2)
        if h <= 0.0:
            break
        tn = min(curve.b, max(curve.a, t - g / h))
        if abs(tn - t) <= 1e-15 * max(1.0, abs(t)):
            t = tn
            break
        t = tn
    return t if dist2(t) <= best else best_t


def chord_length_parameters(Q: Sequence[Point], a: float = 0.0, b: float = 1.0) -> List[float]:
    """Parameters proportional to the cumulative chord length, from a to b."""
    acc = [0.0]
    for x, y in zip(Q, Q[1:]):
        acc.append(acc[-1] + sum((u - v) ** 2 for u, v in zip(x, y)) ** 0.5)
    total = acc[-1] or 1.0
    return [a + (b - a) * s / total for s in acc]


def error(Q: Sequence[Point], curve: Curve, t: Sequence[float]) -> float:
    return sum(dot(sub(q, curve.point(tk)), sub(q, curve.point(tk))) for q, tk in zip(Q, t))


def parameter_correction(Q: Sequence[Point], U: Sequence[float], p: int, t: Optional[Sequence[float]] = None,
                         iterations: int = 100, tol: float = 0.0, samples: int = 64, fix_ends: bool = True
                         ) -> Tuple[List[Point], List[float], List[float]]:
    """Fit a B-spline curve to the points Q with parameter correction.

    With fix_ends the first and the last parameter stay at a and b, so the
    curve does not grow past the end points of the data.

    Precondition: the collocation matrix has full rank at every parameter set
    reached (for example, the parameters stay spread over all spans).
    Returns (control points, parameters, history of E after each fit); the
    history never increases, up to rounding. Cost: Theta(S p n + m (S d + k p n)
    + m p n + n^3) per iteration with S samples and k Newton steps per foot
    point (the dense rows of length n + 1 used here cost Theta(n) each).
    """
    Q = [tuple(map(float, q)) for q in Q]
    U = [float(u) for u in U]
    a, b = U[p], U[len(U) - p - 1]
    t = list(map(float, t)) if t is not None else chord_length_parameters(Q, a, b)    # @line L1
    P = fit_control_points(Q, t, U, p)                                                 # @line L2
    curve = Curve(P, U, p)
    history = [error(Q, curve, t)]
    for _ in range(iterations):                                                        # @line L3
        table = sample_table(curve, samples)
        t = [tk if fix_ends and k in (0, len(Q) - 1) else foot_point(curve, q, tk, table)
             for k, (q, tk) in enumerate(zip(Q, t))]                                   # @line L4
        P = fit_control_points(Q, t, U, p)                                             # @line L5
        curve = Curve(P, U, p)
        e = error(Q, curve, t)                                                         # @line L6
        history.append(e)
        if history[-2] - history[-1] <= tol * history[-2] or e < 1e-30:                # @line L7
            break
    return P, t, history                                                               # @line L8
