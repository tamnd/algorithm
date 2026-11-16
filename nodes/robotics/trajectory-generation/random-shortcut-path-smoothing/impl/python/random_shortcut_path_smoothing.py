# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/random-shortcut-path-smoothing/. The authors are listed in prov/N97VRM.jsonl.
"""Random shortcut smoothing of a 2D polyline among axis-aligned rectangles.

shortcut(path, obstacles, iterations, rng) repeats: pick two random points
on the path (by arc length), and if the straight segment between them is
free, replace the part of the path between them with that segment. The
path stays collision-free and its length never grows. This is a heuristic:
the result is usually much shorter, but it is not a shortest path.

An obstacle is (xmin, ymin, xmax, ymax). A segment collides when it meets the
open interior of a rectangle, so a path may touch rectangle borders.
"""

import math


def segment_free(p, q, obstacles):
    """True when the segment pq meets the open interior of no rectangle (slab test)."""
    for x0, y0, x1, y1 in obstacles:
        lo, hi = 0.0, 1.0
        blocked = True
        for a, d, mn, mx in ((p[0], q[0] - p[0], x0, x1), (p[1], q[1] - p[1], y0, y1)):
            if d == 0:
                if not (mn < a < mx):
                    blocked = False
                    break
            else:
                t0, t1 = (mn - a) / d, (mx - a) / d
                if t0 > t1:
                    t0, t1 = t1, t0
                lo, hi = max(lo, t0), min(hi, t1)
        if blocked and lo < hi:
            return False
    return True


def path_free(path, obstacles):
    return all(segment_free(path[i], path[i + 1], obstacles) for i in range(len(path) - 1))


def path_length(path):
    return sum(math.dist(path[i], path[i + 1]) for i in range(len(path) - 1))


def _point_at(path, cum, s):
    """Index i of the segment that holds arc length s, and the point at s."""
    i = 0
    while i < len(path) - 2 and cum[i + 1] < s:
        i += 1
    seg = cum[i + 1] - cum[i]
    u = 0.0 if seg == 0 else (s - cum[i]) / seg
    p, q = path[i], path[i + 1]
    return i, (p[0] + u * (q[0] - p[0]), p[1] + u * (q[1] - p[1]))


def shortcut(path, obstacles, iterations, rng):
    """Return a shorter free path with the same end points. rng is a random.Random."""
    path = [tuple(p) for p in path]
    for _ in range(iterations):  # @line L1
        cum = [0.0]
        for i in range(len(path) - 1):  # @line L2
            cum.append(cum[-1] + math.dist(path[i], path[i + 1]))
        if cum[-1] == 0:
            break
        s1, s2 = sorted((rng.uniform(0, cum[-1]), rng.uniform(0, cum[-1])))  # @line L3
        i, a = _point_at(path, cum, s1)  # @line L4
        j, b = _point_at(path, cum, s2)
        if i == j:
            continue  # both points on one segment: nothing to gain
        if segment_free(a, b, obstacles):  # @line L5
            path = path[: i + 1] + [a, b] + path[j + 1:]  # @line L6
    return path  # @line L7
