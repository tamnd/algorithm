# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ambient-occlusion/. The authors are listed in prov/HNQCM9.jsonl.

"""Ambient occlusion against closed forms.

Cosine-weighted directions project to uniform points of the unit disk
(Malley's method), so the accessibility of a point is the area of the open
part of the disk divided by pi. This gives exact answers for a sphere above
the point, for one or two walls next to it, and for the inside of a closed
sphere. Each estimate must be within 4 standard errors of the exact value,
where the standard error of a fraction of N rays is sqrt(A (1 - A) / N).
"""

import math
import random

from ambient_occlusion import (Plane, Sphere, ambient_occlusion, ambient_occlusion_uniform, cosine_direction, dot,
                               frame, normalize, obscurance)

Z = 4.0
ORIGIN, UP = (0.0, 0.0, 0.0), (0.0, 0.0, 1.0)


def segment(c: float) -> float:
    """The area of the part x >= c of the unit disk."""
    if c >= 1:
        return 0.0
    return math.acos(c) - c * math.sqrt(1 - c * c)


def close(estimate: float, exact: float, n: int) -> bool:
    se = math.sqrt(exact * (1 - exact) / n)
    return abs(estimate - exact) <= Z * se + 1e-12


def test_cosine_directions() -> None:
    rng = random.Random(1)
    for _ in range(200):
        n = normalize((rng.gauss(0, 1), rng.gauss(0, 1), rng.gauss(0, 1)))
        t, b = frame(n)
        for a, c in ((t, t), (b, b), (n, n)):
            assert abs(dot(a, c) - 1) < 1e-12
        assert abs(dot(t, b)) < 1e-12 and abs(dot(t, n)) < 1e-12 and abs(dot(b, n)) < 1e-12
        u1, u2 = rng.random(), rng.random()
        w = cosine_direction(n, u1, u2)
        assert abs(dot(w, w) - 1) < 1e-12
        # sin^2(theta) = u1 exactly, so P(theta <= alpha) = sin^2(alpha): the cosine-weighted measure of a cone.
        assert abs((1 - dot(w, n) ** 2) - u1) < 1e-12


def test_open_point_and_infinite_wall() -> None:
    rng = random.Random(2)
    assert ambient_occlusion([], ORIGIN, UP, 1000, rng) == 1.0
    wall = [Plane((0.5, 0.0, 0.0), (1.0, 0.0, 0.0))]
    n = 20000
    assert close(ambient_occlusion(wall, ORIGIN, UP, n, rng), 0.5, n)


def test_wall_with_a_distance_limit() -> None:
    # A ray with the disk coordinate w_x meets the wall x = a at the distance a / w_x, so it is blocked when w_x >= a / d_max.
    rng = random.Random(3)
    a, n = 0.5, 20000
    wall = [Plane((a, 0.0, 0.0), (1.0, 0.0, 0.0))]
    for d_max in (0.6, 1.0, 2.0, 5.0):
        exact = 1 - segment(a / d_max) / math.pi
        assert close(ambient_occlusion(wall, ORIGIN, UP, n, rng, d_max), exact, n)
    canyon = wall + [Plane((-a, 0.0, 0.0), (-1.0, 0.0, 0.0))]
    for d_max in (1.0, 2.0):
        exact = 1 - 2 * segment(a / d_max) / math.pi
        assert close(ambient_occlusion(canyon, ORIGIN, UP, n, rng, d_max), exact, n)


def test_sphere_above_the_point() -> None:
    # A sphere of radius r at the distance d, at the angle theta_c from the normal and fully above the
    # horizon, covers the cosine-weighted share (r / d)^2 cos(theta_c) of the hemisphere.
    rng = random.Random(4)
    n = 20000
    for r, d, theta in ((0.5, 1.0, 0.0), (0.3, 1.0, 0.6), (1.0, 3.0, 1.0)):
        assert theta + math.asin(r / d) <= math.pi / 2
        ball = [Sphere((d * math.sin(theta), 0.0, d * math.cos(theta)), r)]
        exact = 1 - (r / d) ** 2 * math.cos(theta)
        assert close(ambient_occlusion(ball, ORIGIN, UP, n, rng), exact, n)


def test_inside_a_closed_sphere() -> None:
    # From a point on the inside of a sphere of radius R, the ray at the angle theta has the length 2 R cos(theta).
    rng = random.Random(5)
    radius, n = 1.0, 20000
    shell = [Sphere((0.0, 0.0, 0.0), radius)]
    x = (0.0, 0.0, -radius)
    assert ambient_occlusion(shell, x, UP, 2000, rng) == 0.0
    for d_max in (0.5, 1.0, 1.5):
        exact = 1 - (d_max / (2 * radius)) ** 2
        assert close(ambient_occlusion(shell, x, UP, n, rng, d_max), exact, n)


def test_obscurance_with_a_linear_falloff() -> None:
    # rho(s) = s next to the wall x = a: with c = a / d_max and s_c = sqrt(1 - c^2),
    # W = 1 - seg(c) / pi + (2 c / pi) (ln((1 + s_c) / c) - s_c).
    rng = random.Random(6)
    a, n = 0.5, 20000
    wall = [Plane((a, 0.0, 0.0), (1.0, 0.0, 0.0))]
    for d_max in (1.0, 2.0):
        c = a / d_max
        s = math.sqrt(1 - c * c)
        exact = 1 - segment(c) / math.pi + 2 * c / math.pi * (math.log((1 + s) / c) - s)
        values = []
        for _ in range(n):
            values.append(obscurance(wall, ORIGIN, UP, 1, rng, d_max, lambda u: u))
        mean = sum(values) / n
        var = sum((v - mean) ** 2 for v in values) / (n - 1)
        assert abs(mean - exact) <= Z * math.sqrt(var / n)
    step = obscurance(wall, ORIGIN, UP, 2000, random.Random(7), 1.0, lambda u: 1.0 if u >= 1 else 0.0)
    assert step == ambient_occlusion(wall, ORIGIN, UP, 2000, random.Random(7), 1.0)


def test_uniform_estimator_is_unbiased_with_more_variance() -> None:
    # Sphere straight above with sin(alpha) = r / d = 1/2: A = cos^2(alpha) = 3/4.
    # The cosine estimator is a Bernoulli variable with the variance A (1 - A) = 3/16.
    # The uniform estimator 2 cos(theta) V has the variance 4 cos^3(alpha) / 3 - cos^4(alpha).
    rng = random.Random(8)
    n = 20000
    ball = [Sphere((0.0, 0.0, 1.0), 0.5)]
    cos_a = math.sqrt(3) / 2
    exact, var_uniform = cos_a ** 2, 4 * cos_a ** 3 / 3 - cos_a ** 4
    values = ambient_occlusion_uniform(ball, ORIGIN, UP, n, rng)
    mean = sum(values) / n
    var = sum((v - mean) ** 2 for v in values) / (n - 1)
    m4 = sum((v - mean) ** 4 for v in values) / n
    assert abs(mean - exact) <= Z * math.sqrt(var / n)
    assert abs(var - var_uniform) <= Z * math.sqrt(m4 / n)
    assert var > exact * (1 - exact) + Z * math.sqrt(m4 / n)
