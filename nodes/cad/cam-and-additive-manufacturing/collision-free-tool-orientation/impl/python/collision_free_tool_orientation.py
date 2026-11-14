# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/collision-free-tool-orientation/. The authors are listed in prov/E9RNYT.jsonl.

"""Collision-free tool orientation in a two-dimensional C-space of directions.

The tool is a half-line from the tool center p (for a ball end mill, the
center of the ball) in the direction d. Obstacles are closed axis-aligned
boxes (x0, x1, y0, y1, z0, z1): blocks of a terrain, walls, clamps. A tool
of radius r is handled by growing every box by r on each side, which can
only remove free directions.

Directions above the horizon are written in the gnomonic chart
d = (qx, qy, 1), so the C-space at p is the plane of q. A box blocks q at p
when the ray p + t (q, 1), t > 0, meets it. With T0 = max(z0 - pz, 0) and
T1 = z1 - pz, this happens exactly when the segment from T0 q to T1 q in the
plane meets the rectangle [x0 - px, x1 - px] x [y0 - py, y1 - py]. So each box
maps to an exact region of the C-space, the shadow of its rectangle, and
the test uses only rational arithmetic.

The planner takes a grid of candidate directions, keeps the free ones at
each point, and picks one per point by dynamic programming over the layers,
minimizing

    w * sum |g_i - pref_i|^2 + sum |g_i - g_(i-1)|^2

over integer grid points g_i, where the direction of g is q = g * step.
"""

from fractions import Fraction


def segment_meets_rect(a, b, rect):
    """Whether the closed segment from a to b meets the closed rectangle.

    a and b are points (x, y); rect is (x0, x1, y0, y1). Exact with ints or
    Fractions (Liang-Barsky clipping).
    """
    lo, hi = Fraction(0), Fraction(1)
    for k, (m0, m1) in enumerate(((rect[0], rect[1]), (rect[2], rect[3]))):
        s, e = a[k], b[k] - a[k]
        if e == 0:
            if s < m0 or s > m1:
                return False
            continue
        t0, t1 = Fraction(m0 - s) / e, Fraction(m1 - s) / e
        if t0 > t1:
            t0, t1 = t1, t0
        lo, hi = max(lo, t0), min(hi, t1)
        if lo > hi:
            return False
    return True


def box_blocks(p, box, q):
    """Whether the box blocks the direction q = (qx, qy) at the tool center p."""
    x0, x1, y0, y1, z0, z1 = box
    t1 = z1 - p[2]
    if t1 <= 0:
        return False  # the box is below the tool center
    t0 = max(z0 - p[2], 0)
    rect = (x0 - p[0], x1 - p[0], y0 - p[1], y1 - p[1])
    return segment_meets_rect((t0 * q[0], t0 * q[1]), (t1 * q[0], t1 * q[1]), rect)


def grow(box, r):
    """The box grown by r on each side, a conservative stand-in for a tool of radius r."""
    x0, x1, y0, y1, z0, z1 = box
    return (x0 - r, x1 + r, y0 - r, y1 + r, z0 - r, z1 + r)


def free_directions(p, boxes, grid, step):
    """The grid points g whose direction q = g * step no box blocks at p."""
    return [g for g in grid if not any(box_blocks(p, b, (g[0] * step, g[1] * step)) for b in boxes)]


def _d2(g, h):
    return (g[0] - h[0]) ** 2 + (g[1] - h[1]) ** 2


def plan_orientations(points, boxes, grid, step, pref, w=1):
    """One free grid direction per tool center, at least total cost.

    Returns (cost, [g_1, ..., g_m]). Raises ValueError if some point has no
    free direction on the grid.
    """
    free = []
    for i, p in enumerate(points):  # @line L1
        f = free_directions(p, boxes, grid, step)  # @line L2
        if not f:  # @line L3
            raise ValueError("no free direction on the grid at point %d" % i)
        free.append(f)
    cost = {g: w * _d2(g, pref[0]) for g in free[0]}  # @line L4
    back = [None]
    for i in range(1, len(points)):  # @line L5
        new, ptr = {}, {}
        for g in free[i]:  # @line L6
            h = min(cost, key=lambda h: (cost[h] + _d2(g, h), h))
            new[g] = w * _d2(g, pref[i]) + cost[h] + _d2(g, h)
            ptr[g] = h
        cost = new
        back.append(ptr)
    g = min(cost, key=lambda h: (cost[h], h))  # @line L7
    best = cost[g]
    path = [g]
    for i in range(len(points) - 1, 0, -1):
        g = back[i][g]
        path.append(g)
    path.reverse()
    return best, path  # @line L8
