# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/goldberg-part-orienting-algorithm/. The authors are listed in prov/8BG41W.jsonl.

# Angles are floats. Checks of angles use the tolerance 1e-7 unless a test
# states another one. The grid check of the squeeze function uses 4000 grid
# points on [0, pi) and allows 3 grid steps of error.

import math
import random

from goldberg_part_orienting_algorithm import (Squeeze, convex_hull, diameter,
                                               plan, run_plan, same_mod)

RECT = [(-1, -0.5), (1, -0.5), (1, 0.5), (-1, 0.5)]
GOLDBERG_4GON = [(-42, -41), (48, -41), (39, 25), (-34, 59)]


def regular(k):
    return [(math.cos(2 * math.pi * i / k), math.sin(2 * math.pi * i / k))
            for i in range(k)]


def random_part(rng, n):
    while True:
        pts = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)]
        try:
            S = Squeeze(pts)
        except ValueError:
            continue
        return pts, S


# Reference: breadth-first search over sets of stable orientations. After the
# first squeeze the part is at one of the r minima of a period. The outcome of
# a squeeze at alpha changes only where some m_j - alpha crosses a maximum,
# so the midpoints between the sorted critical values cover every outcome.
def brute_force_length(S):
    r, T = S.r, S.T
    start = frozenset(range(r))
    if len(start) == 1:
        return 1
    seen = {start}
    frontier = [start]
    depth = 1
    while frontier:
        depth += 1
        nxt = []
        for J in frontier:
            crit = sorted(set(round((S.m(j) - S.e(i)) % T, 12)
                              for j in J for i in range(r)))
            cands = [(crit[i] + crit[(i + 1) % len(crit)] +
                      (T if i + 1 == len(crit) else 0)) / 2
                     for i in range(len(crit))]
            for alpha in cands:
                J2 = frozenset(S.step_of(S.m(j) - alpha) % r for j in J)
                if len(J2) == 1:
                    return depth
                if J2 not in seen:
                    seen.add(J2)
                    nxt.append(J2)
        frontier = nxt
    raise AssertionError("no plan found")


def grid_squeeze(hull, theta, N=4000):
    # Walk downhill on a grid of the diameter function.
    h = math.pi / N
    i = round(theta / h)
    d = lambda k: diameter(hull, k * h)
    while True:
        if d(i - 1) < d(i) and d(i - 1) <= d(i + 1):
            i -= 1
        elif d(i + 1) < d(i):
            i += 1
        else:
            return i * h


def test_rectangle_check_values():
    alphas, final, S, levels = plan(RECT)
    a = math.atan(2.0)
    assert abs(S.T - math.pi) < 1e-12 and S.r == 2
    widths = sorted(S.e(j + 1) - S.e(j) for j in range(2))
    assert abs(widths[0] - (math.pi - 2 * a)) < 1e-9
    assert abs(widths[1] - 2 * a) < 1e-9
    assert len(alphas) == 2
    assert abs(alphas[0]) < 1e-12 and abs(alphas[1] + math.pi / 4) < 1e-9
    assert same_mod(final, 3 * math.pi / 4, math.pi)
    assert abs(diameter(S.hull, 0.0) - 1.0) < 1e-12
    assert abs(diameter(S.hull, math.pi / 2) - 2.0) < 1e-12


def test_regular_polygons_need_one_squeeze():
    # Goldberg: a part with k-fold symmetry has T = 2 pi / (k (1 + k mod 2)).
    for k in range(3, 9):
        alphas, final, S, levels = plan(regular(k))
        assert abs(S.T - 2 * math.pi / (k * (1 + k % 2))) < 1e-9
        assert len(alphas) == 1


def test_goldberg_quadrilateral_needs_four_squeezes():
    alphas, final, S, levels = plan(GOLDBERG_4GON)
    assert abs(S.T - math.pi) < 1e-12 and S.r == 4
    assert len(alphas) == 4
    assert brute_force_length(S) == 4


def test_squeeze_function_against_grid_descent():
    rng = random.Random(7)
    for _ in range(4):
        pts, S = random_part(rng, 7)
        hull = convex_hull(pts)
        for _ in range(20):
            theta = rng.uniform(0, math.pi)
            if any(abs((theta - S.e(j)) % math.pi) < 0.01 or
                   abs((S.e(j) - theta) % math.pi) < 0.01
                   for j in range(-S.r, 2 * S.r)):
                continue
            g = grid_squeeze(hull, theta)
            assert same_mod(g, S.s(theta), math.pi, tol=3 * math.pi / 4000)


def test_period_identity():
    rng = random.Random(3)
    for _ in range(10):
        pts, S = random_part(rng, 6)
        for _ in range(50):
            t = rng.uniform(-5, 5)
            assert abs(S.s(t + S.T) - S.s(t) - S.T) < 1e-9
            assert S.e(S.step_of(t)) <= t + 1e-12 < S.e(S.step_of(t) + 1)


def test_plan_orients_every_start():
    rng = random.Random(11)
    for _ in range(25):
        pts, S = random_part(rng, rng.randint(3, 9))
        alphas, final, S, levels = plan(pts)
        starts = [rng.uniform(-4, 4) for _ in range(300)]
        # Also start exactly at and next to each discontinuity.
        starts += [S.e(j) + d for j in range(-S.r, S.r)
                   for d in (0.0, 1e-9, -1e-9)]
        for phi in starts:
            assert same_mod(run_plan(S, alphas, phi), final, S.T)


def test_margin_of_later_squeezes():
    # The rotation of the gripper between squeezes t - 1 and t may err by
    # less than half the slack of level k - t + 1.
    rng = random.Random(5)
    for _ in range(10):
        pts, S = random_part(rng, 8)
        alphas, final, S, levels = plan(pts)
        k = len(alphas)
        for _ in range(100):
            noisy = [alphas[0]]
            for t in range(2, k + 1):
                p, q = levels[k - t + 1]
                a = S.e(levels[k - t][0])
                b = S.e(levels[k - t][1] + 1)
                half = ((b - a) - (S.m(q) - S.m(p))) / 2
                turn = alphas[t - 1] - alphas[t - 2]
                noisy.append(noisy[-1] + turn +
                             rng.uniform(-0.99, 0.99) * half)
            phi = rng.uniform(0, 7)
            # The part ends at the planned stable orientation relative to
            # the last gripper angle.
            out = run_plan(S, noisy, phi)
            assert same_mod(out - noisy[-1], final - alphas[-1], S.T)


def test_optimal_against_brute_force():
    rng = random.Random(2024)
    lengths = []
    for _ in range(30):
        pts, S = random_part(rng, rng.randint(4, 9))
        alphas, final, S, levels = plan(pts)
        assert len(alphas) == brute_force_length(S)
        lengths.append(len(alphas))
    assert max(lengths) >= 3
