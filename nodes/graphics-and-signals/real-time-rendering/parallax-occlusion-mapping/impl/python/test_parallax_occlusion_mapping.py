# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallax-occlusion-mapping/. The authors are listed in prov/2N7VM7.jsonl.

"""Tests of parallax occlusion mapping.

The secant step is exact for a planar depth map (checked with Fractions).
On smooth depth maps the result is within one step of the first hit found by
a dense march with bisection, whenever the ray stays under the surface for at
least one step. The tests also check the bracket of the returned hit, the
view along the normal, and the thin feature that a coarse march misses.
"""

import random
from fractions import Fraction
from math import cos, pi, sin, sqrt

from parallax_occlusion_mapping import depth_texture, first_hit_dense, pom


def f_of(depth, uv0, view, scale):
    vx, vy, vz = view
    du, dv = -scale * vx / vz, -scale * vy / vz
    return lambda r: r - depth(uv0[0] + r * du, uv0[1] + r * dv)


def test_planar_depth_is_exact():
    rng = random.Random(1)
    for _ in range(300):
        a = Fraction(rng.randint(35, 60), 100)
        b, c = Fraction(rng.randint(-20, 20), 100), Fraction(rng.randint(-20, 20), 100)

        def depth(u, v):
            return a + b * u + c * v

        uv0 = (Fraction(rng.randint(40, 60), 100), Fraction(rng.randint(40, 60), 100))
        view = (Fraction(rng.randint(-100, 100), 100), Fraction(rng.randint(-100, 100), 100),
                Fraction(rng.randint(50, 100), 100))
        scale = Fraction(1, 10)
        du, dv = -scale * view[0] / view[2], -scale * view[1] / view[2]
        want = (a + b * uv0[0] + c * uv0[1]) / (1 - b * du - c * dv)
        (u, v), r = pom(depth, uv0, view, scale, rng.randint(1, 40), exact=True)
        assert r == want
        assert (u, v) == (uv0[0] + want * du, uv0[1] + want * dv)
        assert r == depth(u, v)


def smooth_depth(u, v):
    return 0.5 + 0.25 * sin(2 * pi * 2 * u) * cos(2 * pi * 3 * v)


def test_within_one_step_of_first_hit():
    rng = random.Random(2)
    checked = 0
    for _ in range(150):
        uv0 = (rng.random(), rng.random())
        theta, phi = rng.uniform(0, 1.3), rng.uniform(0, 2 * pi)
        view = (sin(theta) * cos(phi), sin(theta) * sin(phi), cos(theta))
        scale, k = 0.08, rng.choice((8, 16, 32))
        (_, _), r = pom(smooth_depth, uv0, view, scale, k)
        f = f_of(smooth_depth, uv0, view, scale)
        rstar = first_hit_dense(smooth_depth, uv0, view, scale, samples=2000)
        # The condition of the theorem: f >= 0 on [r*, r* + 1/k].
        if all(f(rstar + j / (200 * k)) >= -1e-12 for j in range(201) if rstar + j / (200 * k) <= 1):
            assert abs(r - rstar) <= 1 / k + 1e-9
            checked += 1
    assert checked > 100


def test_result_brackets_a_root():
    rng = random.Random(3)
    tex = depth_texture([[rng.random() for _ in range(16)] for _ in range(16)])
    for _ in range(300):
        uv0 = (rng.random(), rng.random())
        view = (rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(0.2, 1))
        k = rng.randint(1, 30)
        (_, _), r = pom(tex, uv0, view, 0.1, k)
        assert 0 <= r <= 1
        f = f_of(tex, uv0, view, 0.1)
        if r > 0:
            i = -(-r * k // 1)  # the sample that stopped the march
            lo, hi = (i - 1) / k, i / k
            assert lo - 1e-12 <= r <= hi + 1e-12
            assert f(lo) < 0 <= f(hi) + 1e-12


def test_view_along_normal_returns_same_texel():
    tex = depth_texture([[0.1, 0.7], [0.4, 0.9]])
    for uv0 in ((0.1, 0.2), (0.6, 0.6), (0.9, 0.3)):
        (u, v), r = pom(tex, uv0, (0.0, 0.0, 1.0), 0.1, 10)
        assert (u, v) == uv0
        assert abs(r - tex(*uv0)) < 1e-12


def test_thin_wall_is_missed_by_a_coarse_march():
    n = 256
    row = [1.0] * n
    row[n // 2] = 0.0  # a wall one texel wide, at u = 0.5
    tex = depth_texture([row] * 4)
    uv0, scale = (0.31, 0.5), 0.1
    view = (-4 / sqrt(17), 0.0, 1 / sqrt(17))  # the ray moves +0.4 in u per unit depth
    (_, _), coarse = pom(tex, uv0, view, scale, 8)
    (_, _), fine = pom(tex, uv0, view, scale, 512)
    rstar = first_hit_dense(tex, uv0, view, scale)
    assert abs(fine - rstar) <= 1 / 512
    assert rstar < 0.5
    assert coarse > 0.9  # the coarse march passes the wall and hits the floor
