# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ando-circumcenter-algorithm/. The authors are listed in prov/TK3VSR.jsonl.

import itertools
import math
import random

from ando_circumcenter_algorithm import (
    ando_round,
    ando_target,
    diameter,
    run,
    smallest_enclosing_circle,
    visibility_edges,
)


def brute_force_circle(pts):
    """Smallest circle through 2 or 3 of the points that contains all points."""
    best = None
    cands = []
    for a, b in itertools.combinations(pts, 2):
        cands.append(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, math.dist(a, b) / 2))
    for a, b, c in itertools.combinations(pts, 3):
        bx, by, cx, cy = b[0] - a[0], b[1] - a[1], c[0] - a[0], c[1] - a[1]
        den = 2 * (bx * cy - by * cx)
        if abs(den) > 1e-12:
            b2, c2 = bx * bx + by * by, cx * cx + cy * cy
            ux, uy = (cy * b2 - by * c2) / den, (bx * c2 - cx * b2) / den
            cands.append((a[0] + ux, a[1] + uy, math.hypot(ux, uy)))
    for cx, cy, rad in cands:
        if all(math.dist((cx, cy), p) <= rad + 1e-9 for p in pts):
            if best is None or rad < best[2]:
                best = (cx, cy, rad)
    return best if best is not None else (pts[0][0], pts[0][1], 0.0)


def connected(pos, vis):
    edges = visibility_edges(pos, vis)
    seen, stack = {0}, [0]
    while stack:
        i = stack.pop()
        for a, b in edges:
            for x, y in ((a, b), (b, a)):
                if x == i and y not in seen:
                    seen.add(y)
                    stack.append(y)
    return len(seen) == len(pos)


def random_connected(rng, n, vis, box):
    while True:
        pos = [(rng.uniform(0, box), rng.uniform(0, box)) for _ in range(n)]
        if connected(pos, vis):
            return pos


def test_circle_against_brute_force() -> None:
    rng = random.Random(1)
    for _ in range(300):
        n = rng.randrange(1, 9)
        pts = [(rng.uniform(-3, 3), rng.uniform(-3, 3)) for _ in range(n)]
        if rng.random() < 0.2 and n >= 3:
            pts[2] = ((pts[0][0] + pts[1][0]) / 2, (pts[0][1] + pts[1][1]) / 2)
        c = smallest_enclosing_circle(pts, random.Random(rng.randrange(1000)))
        b = brute_force_circle(pts)
        assert abs(c[2] - b[2]) < 1e-9
        assert all(math.dist(c[:2], p) <= c[2] + 1e-9 for p in pts)


def test_line_of_four_by_hand() -> None:
    pos = [(float(i), 0.0) for i in range(4)]
    want = [[0.5, 1.0, 2.0, 2.5], [0.75, 1.25, 1.75, 2.25], [1.25, 1.5, 1.5, 1.75], [1.5] * 4]
    for w in want:
        pos = ando_round(pos, 1.0)
        assert max(abs(p[0] - x) for p, x in zip(pos, w)) < 1e-12
        assert all(p[1] == 0.0 for p in pos)


def test_binding_constraint() -> None:
    pos = [(0.0, 0.0), (-0.97, 0.21), (0.17, -0.71), (0.94, 0.32)]
    cx, cy, _ = smallest_enclosing_circle(pos)
    x, y = ando_target(0, pos, 1.0)
    t = math.hypot(x, y) / math.hypot(cx, cy)
    assert 0.59 < t < 0.6
    assert abs(math.dist((x, y), (0.085, -0.355)) - 0.5) < 1e-12


def test_visibility_is_kept_and_diameter_shrinks() -> None:
    rng = random.Random(2)
    for _ in range(40):
        n = rng.randrange(2, 9)
        pos = random_connected(rng, n, 1.0, 2.5)
        for _ in range(15):
            act = None if rng.random() < 0.5 else [i for i in range(n) if rng.random() < 0.6]
            new = ando_round(pos, 1.0, act)
            for i, j in visibility_edges(pos, 1.0):
                assert math.dist(new[i], new[j]) <= 1.0 + 1e-9
            assert diameter(new) <= diameter(pos) + 1e-12
            pos = new


def test_new_points_stay_in_bounding_box() -> None:
    rng = random.Random(3)
    for _ in range(40):
        pos = random_connected(rng, 6, 1.0, 2.0)
        new = ando_round(pos, 1.0)
        for c in range(2):
            lo, hi = min(p[c] for p in pos), max(p[c] for p in pos)
            assert all(lo - 1e-12 <= p[c] <= hi + 1e-12 for p in new)


def test_synchronous_exact_rendezvous() -> None:
    rng = random.Random(4)
    for _ in range(30):
        n = rng.randrange(2, 9)
        pos = random_connected(rng, n, 1.0, 2.5)
        k = 0
        while diameter(pos) > 0 and k < 200:
            pos = ando_round(pos, 1.0)
            k += 1
        assert diameter(pos) == 0.0


def test_complete_visibility_meets_in_one_round() -> None:
    rng = random.Random(5)
    for _ in range(30):
        pos = [(rng.uniform(0, 1), rng.uniform(0, 1)) for _ in range(rng.randrange(2, 8))]
        new = ando_round(pos, 10.0)
        c = smallest_enclosing_circle(pos)
        assert all(math.dist(p, c[:2]) < 1e-12 for p in new)


def test_semi_synchronous_convergence() -> None:
    rng = random.Random(6)
    for _ in range(10):
        pos = random_connected(rng, 6, 1.0, 2.5)
        out = run(pos, 1.0, 400, rng, p_active=0.5)
        assert diameter(out) < 1e-6


def test_disconnected_groups_stay_apart() -> None:
    pos = [(0.0, 0.0), (0.5, 0.0), (5.0, 0.0), (5.4, 0.3)]
    out = run(pos, 1.0, 50)
    assert diameter(out[:2]) == 0.0 and diameter(out[2:]) == 0.0
    assert math.dist(out[0], out[2]) > 4.0
