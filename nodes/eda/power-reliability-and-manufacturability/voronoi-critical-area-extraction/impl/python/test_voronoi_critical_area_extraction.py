# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/voronoi-critical-area-extraction/. The authors are listed in prov/VXSKTK.jsonl.

import math
import random
from fractions import Fraction

from voronoi_critical_area_extraction import (
    area,
    average_critical_area,
    build_faces,
    critical_area,
    critical_radius,
    evaluate,
    face_of,
    split,
    survival,
    voronoi_critical_area,
)


def union_area(rects):
    """Exact area of a union of closed rectangles (x1, y1, x2, y2), by coordinate compression."""
    xs = sorted(set(v for r in rects for v in (r[0], r[2])))
    total = Fraction(0)
    for xa, xb in zip(xs, xs[1:]):
        spans = sorted((r[1], r[3]) for r in rects if r[0] <= xa and r[2] >= xb)
        length = Fraction(0)
        cur_lo = cur_hi = None
        for lo, hi in spans:
            if cur_hi is None or lo > cur_hi:
                if cur_hi is not None:
                    length += cur_hi - cur_lo
                cur_lo, cur_hi = lo, hi
            else:
                cur_hi = max(cur_hi, hi)
        if cur_hi is not None:
            length += cur_hi - cur_lo
        total += (xb - xa) * length
    return total


def union_critical_area(rects, window, r):
    """A(r) from the definition: the union over pairs of different nets of the
    intersections of the rectangles expanded by r, clipped to the window."""
    r = Fraction(r)
    X1, Y1, X2, Y2 = window
    grown = [(a - r, b - r, c + r, d + r, n) for a, b, c, d, n in rects]
    boxes = []
    for i in range(len(grown)):
        for j in range(i + 1, len(grown)):
            p, q = grown[i], grown[j]
            if p[4] == q[4]:
                continue
            box = (max(p[0], q[0], X1), max(p[1], q[1], Y1), min(p[2], q[2], X2), min(p[3], q[3], Y2))
            if box[0] < box[2] and box[1] < box[3]:
                boxes.append(box)
    return union_area(boxes)


def random_layout(rng, n, nets, size):
    rects = []
    for i in range(n):
        x1 = rng.randint(0, size - 2)
        y1 = rng.randint(0, size - 2)
        rects.append((x1, y1, x1 + rng.randint(1, 4), y1 + rng.randint(1, 4), "n%d" % (i % nets)))
    return rects


WIRES = [(0, -1, 20, 0, "A"), (0, 1, 20, 2, "B")]
WIRE_WINDOW = (-10, -10, 30, 12)


def test_two_wires_closed_form():
    faces = build_faces(WIRES, WIRE_WINDOW)
    L, s = 20, 1
    for r in [Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(1), Fraction(3), Fraction(15, 2)]:
        expected = (L + 2 * r) * max(2 * r - s, 0)
        assert critical_area(faces, r) == expected


def test_matches_union_of_expanded_rectangles():
    rng = random.Random(1)
    for trial in range(6):
        rects = random_layout(rng, 7, 3, 14)
        window = (0, 0, 14, 14)
        faces = build_faces(rects, window)
        radii = [Fraction(k, 4) for k in range(0, 33, 3)] + [Fraction(rng.randint(1, 600), 97) for _ in range(4)]
        for r in radii:
            assert critical_area(faces, r) == union_critical_area(rects, window, r), (trial, r)


def test_faces_partition_window_and_h2_is_critical_radius():
    rng = random.Random(2)
    rects = random_layout(rng, 8, 3, 12)
    window = (0, 0, 12, 12)
    faces = build_faces(rects, window)
    assert sum(area(f[0]) for f in faces) == 144
    for _ in range(300):
        p = (Fraction(rng.randint(0, 1200), 100), Fraction(rng.randint(0, 1200), 100))
        poly, nu, h1, h2 = face_of(faces, p)
        assert evaluate(h2, p) == critical_radius(p, rects)


def test_grid_of_defect_centres():
    # Count the cells of a grid whose centre is critical; the error is at most the
    # area of the grid cells that meet the boundary of the critical region.
    rng = random.Random(3)
    rects = random_layout(rng, 6, 2, 10)
    window = (0, 0, 10, 10)
    faces = build_faces(rects, window)
    m = 160
    h = Fraction(10, m)
    radii = {(i, j): critical_radius(((i + 0.5) * float(h), (j + 0.5) * float(h)), rects) for i in range(m) for j in range(m)}
    for r in [Fraction(1, 2), Fraction(5, 4), Fraction(2)]:
        hits = sum(1 for t in radii.values() if t <= r)
        grid = float(hits * h * h)
        exact = float(critical_area(faces, r))
        perimeter, edges = 0.0, 0
        for poly, _, _, h2 in faces:
            low, _ = split(poly, (h2[0], h2[1], h2[2] - r))
            if low is not None:
                edges += len(low)
                perimeter += sum(math.dist(low[k], low[(k + 1) % len(low)]) for k in range(len(low)))
        bound = float(h) * (math.sqrt(2) * perimeter + 2 * float(h) * edges)
        assert abs(grid - exact) <= bound
        assert abs(grid - exact) <= 0.05 * max(exact, 1.0)


def test_average_critical_area_against_grid_of_centres():
    # The average is the integral over the window of P(R >= t(p)). The function t is
    # 1-Lipschitz in the L-infinity norm and the survival function is (1/r0)-Lipschitz,
    # so the midpoint rule on cells of side h errs by at most |W| h / (2 r0).
    rng = random.Random(4)
    rects = random_layout(rng, 6, 3, 10)
    window = (0, 0, 10, 10)
    faces = build_faces(rects, window)
    r0 = 0.5
    exact = average_critical_area(faces, r0)
    m = 160
    h = 10.0 / m
    fr = [(float(a), float(b), float(c), float(d), n) for a, b, c, d, n in rects]
    total = 0.0
    for i in range(m):
        for j in range(m):
            total += survival(critical_radius(((i + 0.5) * h, (j + 0.5) * h), fr), r0)
    grid = total * h * h
    assert abs(grid - exact) <= 100 * h / (2 * r0) + 1e-9
    assert abs(grid - exact) <= 0.01 * exact


def test_average_matches_direct_integral_of_a():
    # Integrate A(r) f(r) numerically with the exact A of the union method.
    rects = [(0, 0, 6, 1, "A"), (0, 2, 6, 3, "B"), (7, 0, 8, 3, "C")]
    window = (0, 0, 8, 3)
    faces = build_faces(rects, window)
    r0 = 0.25
    exact = average_critical_area(faces, r0)
    tmax = max(evaluate(f[3], p) for f in faces for p in f[0])
    n = 4000
    total = 0.0
    for k in range(n):
        r = (k + 0.5) * float(tmax) / n
        fr = r / r0 ** 2 if r <= r0 else r0 ** 2 / r ** 3
        total += float(union_critical_area(rects, window, Fraction(r))) * fr * float(tmax) / n
    total += 24 * survival(float(tmax), r0)
    assert abs(total - exact) <= 1e-3 * exact


def test_page_example():
    rects = [(0, 0, 6, 1, "A"), (0, 2, 6, 3, "B"), (7, 0, 8, 3, "C")]
    faces, crit, avg = voronoi_critical_area(rects, (0, 0, 8, 3), 0.25)
    for k in range(0, 41):
        r = Fraction(k, 10)
        expected = 0 if r <= Fraction(1, 2) else (24 if r >= 2 else (2 * r - 1) * (10 - r))
        assert crit(r) == expected
    closed = 0.25 ** 2 * (12.75 - 4 * math.log(2) + 3)
    assert abs(avg - closed) <= 1e-12


def test_limits():
    rng = random.Random(5)
    rects = random_layout(rng, 6, 2, 10)
    window = (0, 0, 10, 10)
    faces = build_faces(rects, window)
    prev = Fraction(-1)
    for k in range(0, 41):
        a = critical_area(faces, Fraction(k, 4))
        assert a >= prev
        prev = a
    assert critical_area(faces, 100) == 100
