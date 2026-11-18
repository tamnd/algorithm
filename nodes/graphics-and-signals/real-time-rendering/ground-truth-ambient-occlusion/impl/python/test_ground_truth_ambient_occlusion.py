# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ground-truth-ambient-occlusion/. The authors are listed in prov/2H8H92.jsonl.

"""GTAO: the closed form, planes, the wall, and the limit of one depth layer."""

import math
import random

from ground_truth_ambient_occlusion import (
    gtao,
    gtao_pixel,
    inner_integral,
    wall_reference,
)

FLOOR = 200.0


def simpson(f, a, b, n=2000):
    h = (b - a) / n
    s = f(a) + f(b)
    for k in range(1, n):
        s += (4 if k % 2 else 2) * f(a + k * h)
    return s * h / 3


def test_closed_form_matches_quadrature() -> None:
    rng = random.Random(81)
    for _ in range(40):
        gamma = rng.uniform(-1.5, 1.5)
        h1 = rng.uniform(gamma - math.pi / 2, 0.0) if gamma < math.pi / 2 else 0.0
        h2 = rng.uniform(0.0, gamma + math.pi / 2)
        ref = simpson(lambda h: math.cos(h - gamma) * abs(math.sin(h)), h1, 0.0) + simpson(
            lambda h: math.cos(h - gamma) * abs(math.sin(h)), 0.0, h2
        )
        assert abs(inner_integral(h1, h2, gamma) - ref) < 1e-10
    assert abs(inner_integral(-math.pi / 2, math.pi / 2, 0.0) - 1.0) < 1e-15


def test_open_slice_integrates_to_one_over_the_hemisphere() -> None:
    # For a normal tilted by beta, (1/pi) * integral of |n_p| (cos g + g sin g) is 1.
    for beta in (0.2, 0.7, 1.2):
        def f(phi):
            nd, nv = math.sin(beta) * math.cos(phi), math.cos(beta)
            g = math.atan2(nd, nv)
            return math.hypot(nd, nv) * inner_integral(g - math.pi / 2, g + math.pi / 2, g)
        assert abs(simpson(f, 0.0, math.pi) / math.pi - 1.0) < 1e-10


def test_planes_are_open() -> None:
    for gx, gy in [(0.0, 0.0), (0.4, 0.0), (-0.3, 0.6), (1.2, 0.5)]:
        D = [[100.0 + gx * (i + 0.5) + gy * (j + 0.5) for i in range(60)] for j in range(60)]
        A = gtao_pixel(D, 30, 30, 16, 20, 1.0, 1e9, jitter=0.5, mode="bilinear")
        assert abs(A - 1.0) < 1e-9


def test_wall_matches_the_cosine_weighted_formula() -> None:
    D = [[FLOOR if i < 100 else FLOOR - 8.0 for i in range(200)] for _ in range(200)]
    for i, delta in ((97, 2.5), (95, 4.5), (91, 8.5)):
        A = gtao_pixel(D, i, 100, 32, 360, 0.25, 1e9, jitter=0.5)
        assert abs(A - wall_reference(delta, 8.0)) < 0.01
    assert wall_reference(0.0, 8.0) == 0.5


def test_wall_formula_by_cosine_weighted_rays() -> None:
    rng = random.Random(82)
    delta, H, count, hit = 3.0, 5.0, 40000, 0
    for _ in range(count):
        u1, u2 = rng.random(), rng.random()
        ox = math.sqrt(u1) * math.cos(2 * math.pi * u2)
        oz = math.sqrt(1.0 - u1)
        if ox > 0 and oz * (delta / ox) < H:
            hit += 1
    assert abs((1 - hit / count) - wall_reference(delta, H)) < 0.01


def test_one_layer_over_occludes_a_floating_plate() -> None:
    # A plate of thickness 1 over x in [20, 26), its bottom 4 units above the
    # floor. The depth buffer shows only its top, as if it were a solid block.
    D = [[FLOOR - 5.0 if 20 <= i < 26 else FLOOR for i in range(60)] for _ in range(40)]
    A = gtao_pixel(D, 16, 20, 32, 200, 0.25, 1e9, jitter=0.5)
    rng = random.Random(83)
    delta, L, H, tau, count, hit = 3.5, 6.0, 4.0, 1.0, 40000, 0
    for _ in range(count):
        u1, u2 = rng.random(), rng.random()
        ox = math.sqrt(u1) * math.cos(2 * math.pi * u2)
        oz = math.sqrt(1.0 - u1)
        if ox <= 0:
            continue
        t0 = max(delta / ox, H / oz)
        t1 = min((delta + L) / ox, (H + tau) / oz)
        if t0 <= t1:
            hit += 1
    traced = 1 - hit / count
    assert A < traced - 0.02


def test_whole_image_in_range() -> None:
    rng = random.Random(84)
    D = [[50.0 + rng.uniform(-4, 4) for _ in range(14)] for _ in range(12)]
    A = gtao(D, 4, 4, 1.0, 6.0)
    assert all(-1e-12 <= a <= 1.0 + 1e-12 for row in A for a in row)
