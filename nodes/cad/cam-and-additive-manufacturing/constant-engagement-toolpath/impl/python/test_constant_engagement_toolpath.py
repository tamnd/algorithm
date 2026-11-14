# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/constant-engagement-toolpath/. The authors are listed in prov/X9MBE5.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from constant_engagement_toolpath import (
    Stock,
    circle_engagement,
    constant_engagement_path,
    engagement,
    follow_path,
    front_points,
    straight_engagement,
)

R = 5.0
D = 0.2
N = 60
STEP = 180.0 / N  # the angle of one sample


def square_stock(L, material):
    return Stock(-L, -L, D, int(2 * L / D), int(2 * L / D), material)


@pytest.mark.parametrize("a", [0.5, 1.0, 2.0, 2.5, 4.0, 5.0, 7.5, 9.5])
def test_straight_cut_matches_closed_form(a):
    # material above y = 0; the tool center is at y = a - R, moving along +x
    stock = square_stock(20.0, lambda x, y: y >= 0)
    e = engagement(stock, (0.3, a - R), 0.0, R, N)
    assert abs(e - straight_engagement(a, R)) <= STEP + 2.0


@pytest.mark.parametrize("rho,s", [(8.0, 1.0), (10.0, 2.0), (15.0, 2.0), (25.0, 3.0), (10.0, 4.0)])
def test_circular_cut_matches_closed_form(rho, s):
    Rb = rho - s + R
    stock = square_stock(40.0, lambda x, y: x * x + y * y > Rb * Rb)
    e = engagement(stock, (rho, 0.0), math.pi / 2, R, N)
    assert abs(e - circle_engagement(rho, Rb, R)) <= STEP + 2.0


def test_closed_form_numbers():
    assert math.isclose(straight_engagement(2.0, 5.0), 53.13010235415598)
    assert math.isclose(circle_engagement(10.0, 13.0, 5.0), math.degrees(math.acos(0.44)))
    assert abs(circle_engagement(10.0, 13.0, 5.0) - 63.90) < 0.005
    # the stepover that gives 53.13 degrees on a circle of radius 10
    s = 10 + 5 - math.sqrt(100 + 25 + 2 * 10 * 5 * 0.6)
    assert math.isclose(s, 1.3985, abs_tol=1e-4)
    assert math.isclose(circle_engagement(10.0, 10.0 - s + 5.0, 5.0), 53.13010235415598)


HOLE = 8.0
L = 26.0


def spiral_run(n_steps):
    stock = square_stock(L, lambda x, y: x * x + y * y > HOLE * HOLE)
    start = (HOLE - R, 0.0)
    path = constant_engagement_path(stock, start, math.pi / 2, R, 60.0, 0.5, math.radians(15), n_steps, side=-1, n=N)
    return start, path


def exact_engagement(start, path, k):
    """Engagement at path[k] from the exact stock: the square minus the hole minus
    the capsules cut before step k, tested with Fractions on the same sample points."""
    centers = [start] + [c for c, _, _ in path]
    caps = [(centers[i], centers[i + 1]) for i in range(k)]  # cut before reaching path[k]
    c, psi, _ = path[k]
    rr = F(R) ** 2
    hole2 = F(HOLE) ** 2
    count = 0
    for x, y in front_points(c, psi, R, N):
        fx, fy = F(x), F(y)
        if not (-L <= fx <= L and -L <= fy <= L and fx * fx + fy * fy > hole2):
            continue
        cut = False
        for a, b in caps:
            # a float prefilter with a wide margin, then the exact test
            ex, ey = b[0] - a[0], b[1] - a[1]
            t = max(0.0, min(1.0, ((x - a[0]) * ex + (y - a[1]) * ey) / (ex * ex + ey * ey)))
            if math.hypot(x - a[0] - t * ex, y - a[1] - t * ey) > R + 1e-6:
                continue
            ax, ay, bx, by = F(a[0]), F(a[1]), F(b[0]), F(b[1])
            ex, ey = bx - ax, by - ay
            t = ((fx - ax) * ex + (fy - ay) * ey) / (ex * ex + ey * ey)
            t = min(F(1), max(F(0), t))
            qx, qy = fx - ax - t * ex, fy - ay - t * ey
            if qx * qx + qy * qy <= rr:
                cut = True
                break
        if not cut:
            count += 1
    return 180.0 * count / N


def test_pixel_engagement_matches_exact_stock():
    start, path = spiral_run(300)
    rng = random.Random(5)
    for k in [40, 120] + rng.sample(range(150, 300), 3):
        exact = exact_engagement(start, path, k)
        assert abs(path[k][2] - exact) <= 2 * STEP


def test_generator_holds_the_target_and_beats_constant_stepover():
    _, path = spiral_run(600)
    dev_gen = max(abs(e - 60.0) for _, _, e in path[100:])
    assert dev_gen <= STEP + 1.0
    # the path really spirals out
    r_end = math.hypot(*path[-1][0])
    assert r_end > HOLE + 3
    # an Archimedean spiral with the straight-cut stepover for 60 degrees
    stock = square_stock(L, lambda x, y: x * x + y * y > HOLE * HOLE)
    s0 = R * (1 - math.cos(math.radians(60)))
    centers, phi, r = [], 0.0, HOLE - R
    while r < r_end:
        centers.append((r * math.cos(phi), r * math.sin(phi)))
        phi += 0.5 / r
        r += s0 * (0.5 / r) / (2 * math.pi)
    es = follow_path(stock, centers, R, N)
    dev_spiral = max(abs(e - 60.0) for e in es[100:])
    assert dev_spiral >= 9.0
    assert dev_spiral > 2 * dev_gen


def test_generator_settles_on_a_straight_wall():
    # Material above y = 0; the tool starts with depth 1 and must find the
    # depth R (1 - cos 60) = 2.5, where the straight engagement is 60 degrees.
    stock = Stock(-5.0, -10.0, D, 400, 100, lambda x, y: y >= 0)
    path = constant_engagement_path(stock, (0.0, 1.0 - R), 0.0, R, 60.0, 0.5, math.radians(10), 120, side=1, n=N)
    ys = [c[1] for c, _, _ in path[60:]]
    depth = sum(ys) / len(ys) + R
    assert abs(depth - 2.5) <= 0.3
    assert all(abs(e - 60.0) <= STEP + 1.0 for _, _, e in path[60:])
