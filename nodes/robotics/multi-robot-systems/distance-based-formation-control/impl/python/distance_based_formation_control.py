# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distance-based-formation-control/. The authors are listed in prov/W2E44J.jsonl.

"""Gradient control of inter-robot distances for single integrator robots.

Robot i has position p_i in R^dim and the model p_i' = u_i. The target is a
set of distances d_ij on the edges of an undirected graph. The potential is

    V(p) = 1/4 * sum over edges of (|p_i - p_j|^2 - d_ij^2)^2

and the control is u = -grad V, that is

    u_i = - sum over neighbors j of (|p_i - p_j|^2 - d_ij^2) (p_i - p_j).

Positions are lists of tuples or lists of floats. Edges are pairs (i, j).
"""

from typing import Sequence

Point = Sequence[float]


def _sub(a: Point, b: Point) -> list[float]:
    return [x - y for x, y in zip(a, b)]


def _dot(a: Point, b: Point) -> float:
    return sum(x * y for x, y in zip(a, b))


def potential(p: Sequence[Point], edges: Sequence[tuple], dist: Sequence[float]) -> float:
    """V(p) = 1/4 sum (|p_i - p_j|^2 - d_ij^2)^2."""
    total = 0.0
    for (i, j), d in zip(edges, dist):
        z = _sub(p[i], p[j])
        e = _dot(z, z) - d * d
        total += e * e
    return total / 4


def control(p: Sequence[Point], edges: Sequence[tuple], dist: Sequence[float]) -> list[list[float]]:
    """Return u_i = -sum_j e_ij (p_i - p_j) for all robots, where e_ij is the squared distance error."""
    nbrs: list[list[tuple]] = [[] for _ in p]
    for (i, j), d in zip(edges, dist):  # @line L1
        nbrs[i].append((j, d))
        nbrs[j].append((i, d))
    u = []
    for i in range(len(p)):  # @line L3
        ui = [0.0] * len(p[i])  # @line L4
        for j, d in nbrs[i]:  # @line L5
            z = _sub(p[i], p[j])  # @line L6
            e = _dot(z, z) - d * d  # @line L7
            ui = [a - e * b for a, b in zip(ui, z)]  # @line L8
        u.append(ui)
    return u


def rk4_step(p: Sequence[Point], edges, dist, h: float) -> list[list[float]]:
    """One step of the classic RK4 method for p' = u(p)."""

    def add(q, k, s):
        return [[a + s * b for a, b in zip(qi, ki)] for qi, ki in zip(q, k)]

    k1 = control(p, edges, dist)
    k2 = control(add(p, k1, h / 2), edges, dist)
    k3 = control(add(p, k2, h / 2), edges, dist)
    k4 = control(add(p, k3, h), edges, dist)
    return [[a + h / 6 * (b1 + 2 * b2 + 2 * b3 + b4) for a, b1, b2, b3, b4 in zip(pi, c1, c2, c3, c4)]
            for pi, c1, c2, c3, c4 in zip(p, k1, k2, k3, k4)]


def run_formation(p0: Sequence[Point], edges, dist, t: float, h: float) -> list[list[float]]:
    """Integrate the closed loop from 0 to t with fixed step h."""
    p = [list(map(float, q)) for q in p0]
    steps = max(1, round(t / h))  # @line L2
    for _ in range(steps):
        p = rk4_step(p, edges, dist, t / steps)  # @line L9
    return p  # @line L10


def rigidity_matrix(p: Sequence[Point], edges) -> list[list[float]]:
    """Row for edge (i, j): p_i - p_j in the columns of i, p_j - p_i in the columns of j."""
    dim = len(p[0])
    rows = []
    for i, j in edges:
        row = [0.0] * (dim * len(p))
        z = _sub(p[i], p[j])
        for c in range(dim):
            row[dim * i + c] = z[c]
            row[dim * j + c] = -z[c]
        rows.append(row)
    return rows


def rank(m: list[list[float]], tol: float = 1e-9) -> int:
    """Rank by Gaussian elimination with partial pivoting."""
    a = [list(r) for r in m]
    rk = 0
    cols = len(a[0]) if a else 0
    for c in range(cols):
        piv = max(range(rk, len(a)), key=lambda k: abs(a[k][c]), default=None)
        if piv is None or abs(a[piv][c]) <= tol:
            continue
        a[rk], a[piv] = a[piv], a[rk]
        for k in range(rk + 1, len(a)):
            f = a[k][c] / a[rk][c]
            a[k] = [x - f * y for x, y in zip(a[k], a[rk])]
        rk += 1
        if rk == len(a):
            break
    return rk


def is_infinitesimally_rigid_2d(p: Sequence[Point], edges) -> bool:
    """A planar framework with n >= 2 points is infinitesimally rigid when rank R = 2n - 3."""
    n = len(p)
    return rank(rigidity_matrix(p, edges)) == 2 * n - 3
