# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/homography-decomposition/. The authors are listed in prov/NHSK5N.jsonl.
"""Tests of the SVD decomposition of a plane-induced homography."""

import math
import random

import pytest

from cvgeom import axis_angle_to_R, camera_matrix, make_K, project
from cvla import cross, det, eye, matvec, mul, norm, scale, sub, transpose
from homography_decomposition import homography_decomposition, plane_homography


def rot_angle(R1, R2):
    """The angle of R1^T R2, from the Frobenius distance (accurate near 0)."""
    return 2.0 * math.asin(min(1.0, norm(sub(R1, R2)) / (2.0 * math.sqrt(2.0))))


def plane_basis(n):
    a = [1.0, 0.0, 0.0] if abs(n[0]) < 0.9 else [0.0, 1.0, 0.0]
    e1 = cross(n, a)
    e1 = scale(e1, 1.0 / norm(e1))
    return e1, cross(n, e1)


def random_case(rng, rotation_only=False):
    K1 = make_K(800, 820, 320, 240)
    K2 = make_K(700, 700, 300, 250, 0.5)
    R = axis_angle_to_R([rng.gauss(0, 1) for _ in range(3)], rng.uniform(0.0, 0.5))
    t = [0.0, 0.0, 0.0] if rotation_only else [rng.gauss(0, 0.5) for _ in range(3)]
    n = [rng.gauss(0, 0.3), rng.gauss(0, 0.3), 1.0]
    n = scale(n, 1.0 / norm(n))
    d = rng.uniform(2.0, 6.0)
    e1, e2 = plane_basis(n)
    X = []
    while len(X) < 12:
        a, b = rng.uniform(-2, 2), rng.uniform(-2, 2)
        p = [d * n[i] + a * e1[i] + b * e2[i] for i in range(3)]
        q = [u + v for u, v in zip(matvec(R, p), t)]
        if p[2] > 0.1 and q[2] > 0.1:
            X.append(p)
    P1 = camera_matrix(K1, eye(3), [0.0, 0.0, 0.0])
    P2 = camera_matrix(K2, R, t)
    x1 = [project(P1, p) for p in X]
    x2 = [project(P2, p) for p in X]
    return K1, K2, R, t, n, d, x1, x2


def euclidean_h(R, t, n, d=1.0):
    return [[R[i][j] + t[i] * n[j] / d for j in range(3)] for i in range(3)]


def test_worked_example():
    R = [[0.8, 0.0, 0.6], [0.0, 1.0, 0.0], [-0.6, 0.0, 0.8]]
    t, n, d = [1.0, 0.0, 0.0], [0.0, 0.0, 1.0], 2.0
    K = eye(3)
    G = plane_homography(K, K, R, t, n, d)
    assert norm(sub(G, [[0.8, 0.0, 1.1], [0.0, 1.0, 0.0], [-0.6, 0.0, 0.8]])) <= 1e-15
    x1 = [[0.0, 0.0], [0.2, 0.1], [-0.2, 0.1]]
    x2 = []
    for p in x1:
        q = [a + b for a, b in zip(matvec(R, [d * p[0], d * p[1], d]), t)]
        x2.append([q[0] / q[2], q[1] / q[2]])
    sols = homography_decomposition(G, K, K, x1, x2)
    assert len(sols) == 2
    true = [s for s in sols if rot_angle(s[0], R) <= 1e-9]
    assert len(true) == 1
    assert norm(sub(true[0][1], [0.5, 0.0, 0.0])) <= 1e-9
    assert norm(sub(true[0][2], n)) <= 1e-9
    other = [s for s in sols if rot_angle(s[0], R) > 1e-9][0]
    assert abs(other[0][0][0] - 0.5505) <= 1e-4 and abs(other[0][0][2] - 0.8349) <= 1e-4
    assert abs(other[2][0] - 0.6854) <= 1e-4 and abs(other[2][2] - 0.7282) <= 1e-4


def test_random_scenes():
    rng = random.Random(1)
    sizes = {1: 0, 2: 0}
    for _ in range(120):
        K1, K2, R, t, n, d, x1, x2 = random_case(rng)
        G = scale(plane_homography(K1, K2, R, t, n, d), rng.choice([-1.0, 1.0]) * rng.uniform(0.1, 10.0))
        sols = homography_decomposition(G, K1, K2, x1, x2)
        assert len(sols) in (1, 2)
        sizes[len(sols)] += 1
        Ht = euclidean_h(R, t, n, d)
        found = 0
        for Rs, ts, ns in sols:
            assert norm(sub(mul(transpose(Rs), Rs), eye(3))) <= 1e-9
            assert abs(det(Rs) - 1.0) <= 1e-9
            assert abs(norm(ns) - 1.0) <= 1e-9
            assert norm(sub(euclidean_h(Rs, ts, ns), Ht)) <= 1e-8 * norm(Ht)
            if rot_angle(Rs, R) <= 1e-8 and norm(sub(ns, n)) <= 1e-8 \
                    and norm(sub(ts, scale(t, 1.0 / d))) <= 1e-8:
                found += 1
        assert found == 1
    assert sizes[2] > sizes[1]


def test_visibility_of_kept_solutions():
    rng = random.Random(2)
    for _ in range(40):
        K1, K2, R, t, n, d, x1, x2 = random_case(rng)
        G = plane_homography(K1, K2, R, t, n, d)
        for _, _, ns in homography_decomposition(G, K1, K2, x1, x2):
            y = [matvec([[1 / 800.0, 0.0, -320 / 800.0], [0.0, 1 / 820.0, -240 / 820.0], [0.0, 0.0, 1.0]],
                        [p[0], p[1], 1.0]) for p in x1]
            assert sum(1 for q in y if sum(a * b for a, b in zip(ns, q)) > 0) * 2 > len(y)


def test_pure_rotation():
    rng = random.Random(3)
    for _ in range(20):
        K1, K2, R, t, n, d, x1, x2 = random_case(rng, rotation_only=True)
        G = plane_homography(K1, K2, R, t, n, d)
        sols = homography_decomposition(G, K1, K2, x1, x2)
        assert len(sols) == 1
        Rs, ts, ns = sols[0]
        assert ns is None and ts == [0.0, 0.0, 0.0]
        assert rot_angle(Rs, R) <= 1e-8


def test_scale_and_sign_do_not_matter():
    rng = random.Random(4)
    K1, K2, R, t, n, d, x1, x2 = random_case(rng)
    G = plane_homography(K1, K2, R, t, n, d)
    a = homography_decomposition(G, K1, K2, x1, x2)
    b = homography_decomposition(scale(G, -3.5), K1, K2, x1, x2)
    assert len(a) == len(b)
    for (Ra, ta, na), (Rb, tb, nb) in zip(a, b):
        assert rot_angle(Ra, Rb) <= 1e-9
        assert norm(sub(ta, tb)) <= 1e-9 and norm(sub(na, nb)) <= 1e-9


def test_noise_keeps_the_true_solution_close():
    rng = random.Random(5)
    for _ in range(20):
        K1, K2, R, t, n, d, x1, x2 = random_case(rng)
        if norm(t) / d < 0.05:
            continue
        G = plane_homography(K1, K2, R, t, n, d)
        G = [[g * (1.0 + rng.gauss(0.0, 1e-7)) for g in row] for row in G]
        sols = homography_decomposition(G, K1, K2, x1, x2)
        assert min(rot_angle(s[0], R) for s in sols) <= 1e-4


def test_bad_input():
    with pytest.raises(ValueError):
        homography_decomposition(eye(3), eye(3), eye(3), [], [])
