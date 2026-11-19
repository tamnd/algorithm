# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/front-tracking-method/. The authors are listed in prov/7VRC33.jsonl.
"""The front part of the front tracking method of Unverdi and Tryggvason in 2D.

The front is a closed polygon of marker points X[k] = (x, y), in counterclockwise
order, inside the periodic unit square. The flow lives on an n x n grid of cell
centers ((i + 1/2) h, (j + 1/2) h), h = 1/n; grid arrays are indexed g[i][j] with i
along x. Front and grid are linked by the 4-point delta function of Peskin. The flow
solver itself is a parameter of `front_track`: it receives the grid force density and
returns the new grid velocity. The tests use a prescribed velocity.
"""
from __future__ import annotations

import math
from typing import Callable, List, Sequence, Tuple

Grid = List[List[float]]
Point = Tuple[float, float]
FlowStep = Callable[[Grid, Grid, Grid, Grid, float], Tuple[Grid, Grid]]


def peskin_phi(r: float) -> float:
    """Peskin's 4-point kernel: sum_j phi(r - j) = 1, sum_j (r - j) phi(r - j) = 0. O(1)."""
    a = abs(r)
    if a <= 1.0:
        return (3.0 - 2.0 * a + math.sqrt(1.0 + 4.0 * a - 4.0 * a * a)) / 8.0
    if a < 2.0:
        return (5.0 - 2.0 * a - math.sqrt(max(0.0, -7.0 + 12.0 * a - 4.0 * a * a))) / 8.0
    return 0.0


def _stencil(p: float, n: int) -> List[Tuple[int, float]]:
    """Grid indices (mod n) and 1D weights of the 4 cell centers nearest to p (a coordinate)."""
    s = p * n - 0.5  # position in units of h, relative to the first cell center
    base = math.floor(s) - 1
    return [((base + t) % n, peskin_phi(s - (base + t))) for t in range(4)]


def tension_forces(X: Sequence[Point], sigma: float) -> List[Point]:
    """Surface tension force on each front point: sigma (t_{k+1/2} - t_{k-1/2}).

    t_{k+1/2} is the unit tangent of the element from point k to point k + 1. For a
    closed front the forces add up to zero and have zero total torque. Cost O(M).
    """
    m = len(X)
    if m < 3:
        raise ValueError("a closed front needs at least 3 points")
    t = []
    for k in range(m):
        dx = X[(k + 1) % m][0] - X[k][0]
        dy = X[(k + 1) % m][1] - X[k][1]
        ln = math.hypot(dx, dy)
        if ln == 0.0:
            raise ValueError("two front points coincide")
        t.append((dx / ln, dy / ln))
    return [(sigma * (t[k][0] - t[k - 1][0]), sigma * (t[k][1] - t[k - 1][1])) for k in range(m)]  # @line L2


def spread(X: Sequence[Point], F: Sequence[Point], n: int) -> Tuple[Grid, Grid]:
    """Force density on the grid: f(x) = sum_k F_k delta_h(x - X_k). Keeps sum f h^2 = sum F."""
    fx = [[0.0] * n for _ in range(n)]
    fy = [[0.0] * n for _ in range(n)]
    inv = float(n * n)  # 1 / h^2
    for (px, py), (gx, gy) in zip(X, F):
        sx, sy = _stencil(px, n), _stencil(py, n)
        for i, wi in sx:
            for j, wj in sy:
                w = wi * wj * inv
                fx[i][j] += w * gx  # @line L3
                fy[i][j] += w * gy
    return fx, fy


def interpolate(u: Grid, v: Grid, X: Sequence[Point]) -> List[Point]:
    """Front velocities U_k = sum_ij u_ij delta_h(x_ij - X_k) h^2. Exact for linear u."""
    n = len(u)
    out = []
    for px, py in X:
        sx, sy = _stencil(px, n), _stencil(py, n)
        a = b = 0.0
        for i, wi in sx:
            for j, wj in sy:
                a += wi * wj * u[i][j]  # @line L5
                b += wi * wj * v[i][j]
        out.append((a, b))
    return out


def regrid(X: Sequence[Point], lmin: float, lmax: float) -> List[Point]:
    """Split elements longer than lmax at their midpoints, then drop points whose
    element to the next kept point is shorter than lmin. Needs 0 < lmin < lmax / 2."""
    if not 0.0 < lmin < 0.5 * lmax:
        raise ValueError("need 0 < lmin < lmax / 2")
    out: List[Point] = []
    m = len(X)
    for k in range(m):
        p, q = X[k], X[(k + 1) % m]
        ln = math.hypot(q[0] - p[0], q[1] - p[1])
        parts = max(1, math.ceil(ln / lmax))
        for s in range(parts):  # @line L7
            out.append((p[0] + (q[0] - p[0]) * s / parts, p[1] + (q[1] - p[1]) * s / parts))
    kept = [out[0]]
    for p in out[1:]:
        if math.hypot(p[0] - kept[-1][0], p[1] - kept[-1][1]) >= lmin:
            kept.append(p)
    while len(kept) > 3 and math.hypot(kept[0][0] - kept[-1][0], kept[0][1] - kept[-1][1]) < lmin:
        kept.pop()
    return kept


def front_track(X0: Sequence[Point], u: Grid, v: Grid, dt: float, steps: int, sigma: float,
                flow_step: FlowStep, lmin: float, lmax: float) -> Tuple[List[Point], Grid, Grid]:
    """Run `steps` steps of front tracking. Precondition: X0 is a closed front inside the
    unit square, dt > 0, the flow step keeps the front points away from the boundary.

    Each step costs O(M) for the front plus the cost of the flow step, with M front points.
    The front moves by the midpoint rule with the new grid velocity.
    """
    if dt <= 0 or steps < 0:
        raise ValueError("need dt > 0 and steps >= 0")
    X = list(X0)
    n = len(u)
    for _ in range(steps):  # @line L1
        F = tension_forces(X, sigma)
        fx, fy = spread(X, F, n)
        u, v = flow_step(u, v, fx, fy, dt)  # @line L4
        U = interpolate(u, v, X)
        mid = [(x + 0.5 * dt * a, y + 0.5 * dt * b) for (x, y), (a, b) in zip(X, U)]
        Um = interpolate(u, v, mid)
        X = [(x + dt * a, y + dt * b) for (x, y), (a, b) in zip(X, Um)]  # @line L6
        X = regrid(X, lmin, lmax)
    return X, u, v  # @line L8


def circle_front(cx: float, cy: float, r: float, m: int) -> List[Point]:
    """m points on a circle, counterclockwise."""
    return [(cx + r * math.cos(2 * math.pi * k / m), cy + r * math.sin(2 * math.pi * k / m)) for k in range(m)]


def enclosed_area(X: Sequence[Point]) -> float:
    """Signed area of the front polygon (positive for counterclockwise)."""
    m = len(X)
    return 0.5 * sum(X[k][0] * X[(k + 1) % m][1] - X[(k + 1) % m][0] * X[k][1] for k in range(m))


def grid_field(n: int, fu: Callable[[float, float], float]) -> Grid:
    """Sample a function at the cell centers."""
    h = 1.0 / n
    return [[fu((i + 0.5) * h, (j + 0.5) * h) for j in range(n)] for i in range(n)]
