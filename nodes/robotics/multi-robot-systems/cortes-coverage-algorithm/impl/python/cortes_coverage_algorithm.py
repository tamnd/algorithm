# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cortes-coverage-algorithm/. The authors are listed in prov/CV7WDC.jsonl.

"""Distributed Lloyd coverage algorithm (Cortes, Martinez, Karatas and Bullo).

Robots p_1..p_r lie in a convex polygon Q with uniform density. Each robot
computes its Voronoi cell inside Q, the centroid C_i of the cell, and moves
by p_i <- p_i + k (C_i - p_i) with a gain 0 < k <= 1 (k = 1 is Lloyd's step).
The coverage cost H(P) = sum_i integral over V_i of |q - p_i|^2 dq never
increases.
"""

from typing import Sequence

Point = tuple[float, float]
Polygon = list[Point]


def clip(poly: Sequence[Point], a: Point, b: float, eps: float = 1e-14) -> Polygon:
    """Part of a convex polygon where a . x <= b (Sutherland-Hodgman, one half-plane)."""
    out: Polygon = []
    n = len(poly)
    for idx in range(n):
        p, q = poly[idx], poly[(idx + 1) % n]
        fp = a[0] * p[0] + a[1] * p[1] - b
        fq = a[0] * q[0] + a[1] * q[1] - b
        if fp <= eps:
            out.append(p)
        if (fp < -eps and fq > eps) or (fp > eps and fq < -eps):
            s = fp / (fp - fq)
            out.append((p[0] + s * (q[0] - p[0]), p[1] + s * (q[1] - p[1])))
    return out


def voronoi_cell(i: int, pts: Sequence[Point], region: Sequence[Point]) -> Polygon:
    """Voronoi cell of robot i inside the convex polygon region."""
    pi = pts[i]
    cell: Polygon = list(region)  # @line L3
    for j, pj in enumerate(pts):  # @line L4
        if j != i and cell:
            a = (pj[0] - pi[0], pj[1] - pi[1])
            b = (pj[0] ** 2 + pj[1] ** 2 - pi[0] ** 2 - pi[1] ** 2) / 2
            cell = clip(cell, a, b)  # @line L5
    return cell


def moments(poly: Sequence[Point]) -> tuple[float, float, float, float]:
    """Area M, centroid (cx, cy) and polar moment J = integral |q|^2 dq of a polygon."""
    a = sx = sy = jj = 0.0
    n = len(poly)
    for idx in range(n):
        x0, y0 = poly[idx]
        x1, y1 = poly[(idx + 1) % n]
        cr = x0 * y1 - x1 * y0
        a += cr
        sx += (x0 + x1) * cr
        sy += (y0 + y1) * cr
        jj += (x0 * x0 + x0 * x1 + x1 * x1 + y0 * y0 + y0 * y1 + y1 * y1) * cr
    a /= 2
    if a <= 0:
        return 0.0, 0.0, 0.0, 0.0
    return a, sx / (6 * a), sy / (6 * a), jj / 12


def cell_data(pts: Sequence[Point], region: Sequence[Point]):
    """For each robot: (mass M_i, centroid C_i, cost of the cell around p_i)."""
    res = []
    for i, p in enumerate(pts):
        m, cx, cy, j = moments(voronoi_cell(i, pts, region))  # @line L6
        cost = j - 2 * m * (p[0] * cx + p[1] * cy) + m * (p[0] ** 2 + p[1] ** 2)
        res.append((m, (cx, cy) if m > 0 else p, cost))
    return res


def coverage_cost(pts: Sequence[Point], region: Sequence[Point]) -> float:
    """H(P) = sum_i integral over V_i of |q - p_i|^2 dq (uniform density)."""
    return sum(c for _, _, c in cell_data(pts, region))


def coverage_step(pts: Sequence[Point], region: Sequence[Point], k: float = 1.0) -> list[Point]:
    """One synchronous step: every robot moves the fraction k toward its centroid."""
    new = []
    for p, (_, (cx, cy), _) in zip(pts, cell_data(pts, region)):  # @line L2
        new.append((p[0] + k * (cx - p[0]), p[1] + k * (cy - p[1])))  # @line L7
    return new


def run(pts: Sequence[Point], region: Sequence[Point], k: float = 1.0, steps: int = 100) -> list[Point]:
    cur = [tuple(map(float, p)) for p in pts]
    for _ in range(steps):  # @line L1
        cur = coverage_step(cur, region, k)
    return cur  # @line L8


def centroid_gap(pts: Sequence[Point], region: Sequence[Point]) -> float:
    """max_i |p_i - C_i|, zero exactly at a centroidal Voronoi configuration."""
    return max(((p[0] - c[0]) ** 2 + (p[1] - c[1]) ** 2) ** 0.5
               for p, (_, c, _) in zip(pts, cell_data(pts, region)))
