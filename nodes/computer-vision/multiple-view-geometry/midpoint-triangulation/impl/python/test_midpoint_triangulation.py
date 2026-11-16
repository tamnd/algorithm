# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/midpoint-triangulation/. The authors are listed in prov/NVV9NG.jsonl.
"""Tests of midpoint triangulation."""

import math
import random

import pytest

from cvgeom import add_noise, make_K, random_rotation, random_scene, rot_y
from cvla import cross, dot, inv, matvec, norm, sub
from midpoint_triangulation import (camera_ray, midpoint,
                                    midpoint_triangulation,
                                    nearest_point_to_rays)

I3 = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]


def rel(a, b):
    return norm(sub(a, b)) / max(1.0, norm(b))


def line_dist2(X, C, d):
    v = sub(X, C)
    c = cross(v, d)
    return dot(c, c) / dot(d, d)


def random_rays(rng):
    C1 = [rng.uniform(-1, 1) for _ in range(3)]
    C2 = [rng.uniform(-1, 1) for _ in range(3)]
    d1 = [rng.gauss(0, 1) for _ in range(3)]
    d2 = [rng.gauss(0, 1) for _ in range(3)]
    return C1, d1, C2, d2


def test_worked_example_exact():
    X = midpoint_triangulation(I3, [0, 0, 0], [0.25, 0.5], I3, [-1, 0, 0], [0.0, 0.5])
    assert rel(X, [1.0, 2.0, 4.0]) <= 1e-12
    C1, d1 = camera_ray(I3, [0, 0, 0], [0.25, 0.5])
    C2, d2 = camera_ray(I3, [-1, 0, 0], [0.0, 0.5])
    assert C2 == [1.0, 0.0, 0.0]
    _, l1, l2 = midpoint(C1, d1, C2, d2)
    assert abs(l1 - 4.0) <= 1e-12 and abs(l2 - 4.0) <= 1e-12


def test_worked_example_noisy():
    C1, d1 = camera_ray(I3, [0, 0, 0], [0.25, 0.5])
    C2, d2 = camera_ray(I3, [-1, 0, 0], [0.0, 0.52])
    X, l1, l2 = midpoint(C1, d1, C2, d2)
    assert rel(X, [0.997494, 2.021303, 3.963659]) <= 1e-6
    assert abs(l1 - 3.979950) <= 1e-6 and abs(l2 - 3.947368) <= 1e-6
    Q1 = [p + l1 * q for p, q in zip(C1, d1)]
    Q2 = [p + l2 * q for p, q in zip(C2, d2)]
    assert abs(norm(sub(Q1, Q2)) - 0.070799) <= 1e-6


def test_gap_is_perpendicular_to_both_rays():
    rng = random.Random(1)
    for _ in range(50):
        C1, d1, C2, d2 = random_rays(rng)
        _, l1, l2 = midpoint(C1, d1, C2, d2)
        g = sub([p + l1 * q for p, q in zip(C1, d1)],
                [p + l2 * q for p, q in zip(C2, d2)])
        scale = max(1.0, norm(g)) * norm(d1) * norm(d2)
        assert abs(dot(g, d1)) <= 1e-10 * scale
        assert abs(dot(g, d2)) <= 1e-10 * scale


def test_exact_recovery_and_depths():
    rng = random.Random(2)
    for _ in range(5):
        sc = random_scene(rng, n=10, n_cams=2, max_angle=0.4)
        Kinv = inv(sc["K"][0])
        (R1, R2), (t1, t2) = sc["R"], sc["t"]
        for j, X in enumerate(sc["X"]):
            y1 = matvec(Kinv, sc["x"][0][j] + [1.0])[:2]
            y2 = matvec(Kinv, sc["x"][1][j] + [1.0])[:2]
            C1, d1 = camera_ray(R1, t1, y1)
            C2, d2 = camera_ray(R2, t2, y2)
            Y, l1, l2 = midpoint(C1, d1, C2, d2)
            assert rel(Y, X) <= 1e-8
            z1 = matvec(R1, X)[2] + t1[2]
            z2 = matvec(R2, X)[2] + t2[2]
            assert abs(l1 - z1) <= 1e-8 * z1 and abs(l2 - z2) <= 1e-8 * z2


def test_direction_length_does_not_matter():
    rng = random.Random(3)
    for _ in range(20):
        C1, d1, C2, d2 = random_rays(rng)
        X = midpoint(C1, d1, C2, d2)[0]
        s1, s2 = rng.uniform(0.1, 10), rng.uniform(-10, -0.1)
        Y = midpoint(C1, [s1 * v for v in d1], C2, [s2 * v for v in d2])[0]
        assert rel(Y, X) <= 1e-10


def test_similarity_invariance():
    rng = random.Random(4)
    for _ in range(20):
        C1, d1, C2, d2 = random_rays(rng)
        X = midpoint(C1, d1, C2, d2)[0]
        Q = random_rotation(rng)
        s = rng.uniform(0.2, 5.0)
        T = [rng.uniform(-3, 3) for _ in range(3)]

        def point(p):
            return [s * a + b for a, b in zip(matvec(Q, p), T)]

        Y = midpoint(point(C1), matvec(Q, d1), point(C2), matvec(Q, d2))[0]
        assert rel(Y, point(X)) <= 1e-9


def test_not_affine_invariant():
    C1, d1 = camera_ray(I3, [0, 0, 0], [0.25, 0.5])
    C2, d2 = camera_ray(I3, [-1, 0, 0], [0.0, 0.52])
    X = midpoint(C1, d1, C2, d2)[0]
    A = [[1.0, 0.0, 0.0], [0.0, 1.0, 2.0], [0.0, 0.0, 1.0]]
    Y = midpoint(matvec(A, C1), matvec(A, d1), matvec(A, C2), matvec(A, d2))[0]
    assert norm(sub(Y, matvec(A, X))) > 1e-3
    # On exact data the rays meet, and every affine map keeps the meeting point.
    C2e, d2e = camera_ray(I3, [-1, 0, 0], [0.0, 0.5])
    X = midpoint(C1, d1, C2e, d2e)[0]
    Y = midpoint(matvec(A, C1), matvec(A, d1), matvec(A, C2e), matvec(A, d2e))[0]
    assert rel(Y, matvec(A, X)) <= 1e-12


def test_two_rays_least_squares_point_is_the_midpoint():
    rng = random.Random(5)
    for _ in range(30):
        C1, d1, C2, d2 = random_rays(rng)
        X = midpoint(C1, d1, C2, d2)[0]
        Y = nearest_point_to_rays([C1, C2], [d1, d2])
        assert rel(Y, X) <= 1e-8


def test_midpoint_minimizes_sum_of_squared_distances():
    rng = random.Random(6)
    for _ in range(10):
        C1, d1, C2, d2 = random_rays(rng)
        X = midpoint(C1, d1, C2, d2)[0]
        f0 = line_dist2(X, C1, d1) + line_dist2(X, C2, d2)
        for _ in range(20):
            Z = [x + rng.gauss(0, 0.05) for x in X]
            assert line_dist2(Z, C1, d1) + line_dist2(Z, C2, d2) >= f0 - 1e-12


def test_n_views_exact_and_noisy():
    rng = random.Random(7)
    sc = random_scene(rng, n=8, n_cams=5, max_angle=0.5)
    Kinv = inv(sc["K"][0])
    for j, X in enumerate(sc["X"]):
        Cs, ds = [], []
        for i in range(5):
            y = matvec(Kinv, sc["x"][i][j] + [1.0])[:2]
            C, d = camera_ray(sc["R"][i], sc["t"][i], y)
            Cs.append(C)
            ds.append(d)
        assert rel(nearest_point_to_rays(Cs, ds), X) <= 1e-8


def test_noise_gives_a_small_error():
    rng = random.Random(8)
    # Two cameras 5 units from the origin, 0.6 rad apart: a good baseline.
    R2 = rot_y(-0.6)
    t2 = [-v for v in matvec(R2, [5.0 * math.sin(0.6), 0.0, -5.0 * math.cos(0.6)])]
    K = make_K(800, 800, 320, 240)
    sc = random_scene(rng, n=20, cams=[(K, I3, [0.0, 0.0, 5.0]), (K, R2, t2)])
    Kinv = inv(K)
    xs = [add_noise(rng, sc["x"][i], 0.5) for i in range(2)]
    for j, X in enumerate(sc["X"]):
        ys = [matvec(Kinv, xs[i][j] + [1.0])[:2] for i in range(2)]
        Y = midpoint_triangulation(sc["R"][0], sc["t"][0], ys[0],
                                   sc["R"][1], sc["t"][1], ys[1])
        assert norm(sub(Y, X)) <= 0.05


def test_parallel_rays_raise():
    with pytest.raises(ValueError):
        midpoint([0, 0, 0], [0, 0, 1], [1, 0, 0], [0, 0, 2])
    with pytest.raises(ValueError):
        nearest_point_to_rays([[0, 0, 0], [1, 0, 0]], [[0, 0, 1], [0, 0, -3]])


def test_point_behind_a_camera_gives_negative_depth():
    C1, d1 = [0.0, 0.0, 0.0], [0.0, 0.0, 1.0]
    C2, d2 = [1.0, 0.0, 0.0], [1.0, 0.0, 1.0]
    X, l1, l2 = midpoint(C1, d1, C2, d2)
    assert rel(X, [0.0, 0.0, -1.0]) <= 1e-12
    assert l1 < 0 and l2 < 0
    assert math.isclose(l1, -1.0)
