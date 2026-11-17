# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conservative-advancement/. The authors are listed in prov/C2728X.jsonl.

import math
import random

from conservative_advancement import Body, conservative_advancement, polygon_distance

SQ = [(-1.0, -1.0), (1.0, -1.0), (1.0, 1.0), (-1.0, 1.0)]


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def hull(points):
    pts = sorted(set(points))
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def random_body(rng, cx, cy):
    while True:
        h = hull([(rng.uniform(-1.5, 1.5), rng.uniform(-1.5, 1.5)) for _ in range(rng.randint(3, 7))])
        if len(h) >= 3 and abs(sum(cross((0, 0), h[i], h[(i + 1) % len(h)]) for i in range(len(h)))) > 0.5:
            break
    v = (rng.uniform(-8, 8), rng.uniform(-8, 8))
    return Body(h, (cx, cy), rng.uniform(0, 2 * math.pi), v, rng.uniform(-6, 6))


def dist(A, B, t):
    return polygon_distance(A.at(t), B.at(t))[0]


def first_contact(A, B, T=1.0, samples=400):
    """The first contact time by dense sampling and bisection, or None if no sample touches."""
    prev = 0.0
    if dist(A, B, 0.0) == 0:
        return 0.0
    for i in range(1, samples + 1):
        s = T * i / samples
        if dist(A, B, s) == 0:
            lo, hi = prev, s
            for _ in range(50):
                mid = (lo + hi) / 2
                if dist(A, B, mid) == 0:
                    hi = mid
                else:
                    lo = mid
            return hi
        prev = s
    return None


def test_polygon_distance():
    P = [(0.0, 0.0), (2.0, 0.0), (2.0, 2.0), (0.0, 2.0)]
    d, pa, pb = polygon_distance(P, [(5.0, 1.0), (7.0, 0.0), (7.0, 2.0)])
    assert (d, pa, pb) == (3.0, (2.0, 1.0), (5.0, 1.0))
    d, pa, pb = polygon_distance([(5.0, 1.0), (7.0, 0.0), (7.0, 2.0)], P)
    assert (d, pa, pb) == (3.0, (5.0, 1.0), (2.0, 1.0))
    assert polygon_distance(P, [(1.0, 1.0), (3.0, 1.0), (3.0, 3.0)])[0] == 0
    assert polygon_distance(P, [(0.5, 0.5), (1.5, 0.5), (1.0, 1.5)])[0] == 0
    assert polygon_distance(P, [(2.0, 2.0), (4.0, 2.0), (4.0, 4.0)])[0] == 0


def test_page_example():
    A = Body(SQ, (0.0, 0.0), 0.0, (0.0, 0.0), 0.0)
    B = Body(SQ, (6.0, 0.0), 0.0, (-6.0, 0.0), math.pi)
    t, steps = conservative_advancement(A, B, tol=1e-3)
    assert steps == 7 and abs(t - 0.6176228740) < 1e-9
    t_star = first_contact(A, B, samples=2000)
    assert abs(t_star - 0.61769886) < 1e-7
    assert t <= t_star and dist(A, B, t) <= 1e-3
    previous = -1.0
    for tol in (1e-2, 1e-4, 1e-6, 1e-8):
        t, _ = conservative_advancement(A, B, tol=tol)
        assert previous < t <= t_star
        previous = t


def test_random_motions_never_pass_the_first_contact():
    rng = random.Random(1996)
    hits = misses = 0
    for _ in range(120):
        A = random_body(rng, 0.0, 0.0)
        B = random_body(rng, rng.uniform(-9, 9), rng.uniform(-9, 9))
        s = rng.uniform(0.3, 1.5)  # aim B roughly at A, so that about half of the motions hit
        B = Body(B.local, B.c0, B.theta0, (-s * B.c0[0] + B.v[0] / 4, -s * B.c0[1] + B.v[1] / 4), B.omega)
        if dist(A, B, 0.0) == 0:
            continue
        t_star = first_contact(A, B)
        t, _ = conservative_advancement(A, B, tol=1e-7)
        if t_star is not None:
            hits += 1
            assert t is not None and t <= t_star
        if t is None:
            misses += 1
            assert t_star is None
        else:
            assert dist(A, B, t) <= 1e-7
    assert hits >= 20 and misses >= 20


def test_the_step_bound_is_a_true_bound():
    rng = random.Random(5)
    for _ in range(300):
        A = random_body(rng, 0.0, 0.0)
        B = random_body(rng, rng.uniform(-9, 9), rng.uniform(-9, 9))
        t0 = rng.uniform(0, 1)
        d0, pa, pb = polygon_distance(A.at(t0), B.at(t0))
        if d0 == 0:
            continue
        n = ((pa[0] - pb[0]) / d0, (pa[1] - pb[1]) / d0)
        dv = (A.v[0] - B.v[0], A.v[1] - B.v[1])
        mu = -(n[0] * dv[0] + n[1] * dv[1]) + abs(A.omega) * A.radius() + abs(B.omega) * B.radius()
        for _ in range(5):
            t1 = t0 + rng.uniform(0, 0.5)
            gap = min(n[0] * x[0] + n[1] * x[1] for x in A.at(t1)) - max(n[0] * y[0] + n[1] * y[1] for y in B.at(t1))
            assert gap >= d0 - (t1 - t0) * mu - 1e-9
            assert dist(A, B, t1) >= gap - 1e-9 or gap < 0


def test_simple_cases():
    A = Body(SQ, (0.0, 0.0), 0.0, (0.0, 0.0), 0.0)
    # moving apart without spin: the bound is negative at once
    assert conservative_advancement(A, Body(SQ, (4.0, 0.0), 0.0, (3.0, 0.0), 0.0)) == (None, 0)
    # head on without spin: the bound is exact, and one step reaches the contact
    t, steps = conservative_advancement(A, Body(SQ, (6.0, 0.0), 0.0, (-8.0, 0.0), 0.0))
    assert steps == 1 and abs(t - 0.5) < 1e-12
    # too slow to arrive before T
    assert conservative_advancement(A, Body(SQ, (6.0, 0.0), 0.0, (-2.0, 0.0), 0.0))[0] is None


def test_grazing_motion_needs_many_steps():
    A = Body(SQ, (0.0, 0.0), 0.0, (0.0, 0.0), 0.0)
    counts = []
    for g in (1.0, 0.1, 0.01, 0.001):
        B = Body(SQ, (-6.0, 1.0 + math.sqrt(2) + g), -math.pi / 4, (12.0, 0.0), math.pi)
        assert abs(dist(A, B, 0.5) - g) < 1e-9
        t, steps = conservative_advancement(A, B, tol=1e-6)
        assert t is None
        counts.append(steps)
    assert counts == [3, 9, 39, 152]
