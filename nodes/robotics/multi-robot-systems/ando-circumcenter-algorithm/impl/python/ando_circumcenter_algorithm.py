# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ando-circumcenter-algorithm/. The authors are listed in prov/TK3VSR.jsonl.

"""Ando's circumcenter algorithm for point robots in the plane with a visibility radius V.

In each round every active robot i looks at the robots within distance V
(itself included), computes the center c of their smallest enclosing circle,
and moves on the segment toward c as far as it can while it stays in the disk
of radius V/2 around the midpoint (p_i + p_j)/2 of every visible robot j.
Two robots that see each other then still see each other after the round.

Robots are oblivious: the step depends only on the current positions.
"""

import math
import random
from typing import Iterable, Sequence

Point = tuple[float, float]


def _circle2(a: Point, b: Point) -> tuple[float, float, float]:
    cx, cy = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    return cx, cy, math.dist(a, b) / 2


def _circle3(a: Point, b: Point, c: Point):
    """Circumscribed circle of three points, or None if they are collinear."""
    bx, by = b[0] - a[0], b[1] - a[1]
    cx, cy = c[0] - a[0], c[1] - a[1]
    den = 2 * (bx * cy - by * cx)
    if abs(den) < 1e-18:
        return None
    b2, c2 = bx * bx + by * by, cx * cx + cy * cy
    ux = (cy * b2 - by * c2) / den
    uy = (bx * c2 - cx * b2) / den
    return a[0] + ux, a[1] + uy, math.hypot(ux, uy)


def _inside(circ, p: Point, tol: float = 1e-12) -> bool:
    return math.dist((circ[0], circ[1]), p) <= circ[2] * (1 + tol) + tol


def smallest_enclosing_circle(points: Iterable[Point], rng: random.Random | None = None):
    """Return (cx, cy, radius) of the smallest circle that contains all points.

    Randomized incremental algorithm (Welzl's method written as three nested
    loops), expected O(n) time after a random shuffle.
    """
    pts = list(points)
    if not pts:
        raise ValueError("no points")
    (rng or random.Random(0)).shuffle(pts)
    circ = (pts[0][0], pts[0][1], 0.0)
    for i in range(1, len(pts)):
        if _inside(circ, pts[i]):
            continue
        circ = (pts[i][0], pts[i][1], 0.0)
        for j in range(i):
            if _inside(circ, pts[j]):
                continue
            circ = _circle2(pts[i], pts[j])
            for k in range(j):
                if _inside(circ, pts[k]):
                    continue
                c3 = _circle3(pts[i], pts[j], pts[k])
                if c3 is None:
                    # collinear: the circle on the two farthest points
                    trio = [pts[i], pts[j], pts[k]]
                    a, b = max(((u, v) for u in trio for v in trio), key=lambda uv: math.dist(*uv))
                    c3 = _circle2(a, b)
                circ = c3
    return circ


def _max_step(p: Point, c: Point, m: Point, half: float) -> float:
    """Largest t in [0, 1] with |p + t (c - p) - m| <= half, given |p - m| <= half."""
    dx, dy = c[0] - p[0], c[1] - p[1]
    fx, fy = p[0] - m[0], p[1] - m[1]
    a = dx * dx + dy * dy
    if a == 0:
        return 1.0
    b = 2 * (dx * fx + dy * fy)
    cc = fx * fx + fy * fy - half * half  # <= 0 up to rounding
    disc = max(0.0, b * b - 4 * a * cc)
    t = (-b + math.sqrt(disc)) / (2 * a)
    return max(0.0, min(1.0, t))


def ando_target(i: int, pos: Sequence[Point], vis: float) -> Point:
    """New position of robot i after one activation."""
    p = pos[i]
    seen = [q for q in pos if math.dist(p, q) <= vis]  # @line L3
    cx, cy, _ = smallest_enclosing_circle(seen)  # @line L4
    t = 1.0  # @line L5
    for q in seen:  # @line L6
        if q is not p:
            m = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)  # @line L7
            t = min(t, _max_step(p, (cx, cy), m, vis / 2))  # @line L8
    return p[0] + t * (cx - p[0]), p[1] + t * (cy - p[1])  # @line L9


def ando_round(pos: Sequence[Point], vis: float, active: Iterable[int] | None = None) -> list[Point]:
    """One round: the active robots (all if None) compute from the same snapshot and move."""
    pos = [tuple(map(float, q)) for q in pos]
    act = range(len(pos)) if active is None else active  # @line L2
    new = list(pos)
    for i in act:
        new[i] = ando_target(i, pos, vis)
    return new  # @line L10


def run(pos: Sequence[Point], vis: float, rounds: int, rng: random.Random | None = None,
        p_active: float = 1.0) -> list[Point]:
    """Run several rounds. With p_active < 1 each robot is active with that probability (SSYNC)."""
    cur = [tuple(map(float, q)) for q in pos]
    for _ in range(rounds):  # @line L1
        if p_active >= 1.0:
            cur = ando_round(cur, vis)
        else:
            act = [i for i in range(len(cur)) if rng.random() < p_active]
            cur = ando_round(cur, vis, act)
    return cur


def diameter(pos: Sequence[Point]) -> float:
    return max((math.dist(a, b) for a in pos for b in pos), default=0.0)


def visibility_edges(pos: Sequence[Point], vis: float) -> set[tuple[int, int]]:
    n = len(pos)
    return {(i, j) for i in range(n) for j in range(i + 1, n) if math.dist(pos[i], pos[j]) <= vis}
