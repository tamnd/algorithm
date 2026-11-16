# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optimal-triangulation/. The authors are listed in prov/FJGF9W.jsonl.
"""Tests of Hartley-Sturm optimal triangulation."""

import math
import random

import pytest

from cvgeom import add_noise, camera_matrix, random_scene, rot_y
from cvla import inv, matvec, mul, norm, sub, transpose
from optimal_triangulation import (cost_s, fundamental_from_cameras,
                                   optimal_correction, optimal_triangulation,
                                   reprojection_cost, triangulate_dlt)

I3 = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
P1 = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0]]
P2 = [[1.0, 0.0, 0.0, -1.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0]]
P2B = camera_matrix(I3, rot_y(-0.3), [-1.0, 0.0, 0.2])
Y1 = [0.25, 0.5]
Y2N = [-0.2741747441668867, 0.48329905176727356]


def rel(a, b):
    return norm(sub(a, b)) / max(1.0, norm(b))


def epipolar(F, x1, x2):
    return sum((x2 + [1.0])[i] * F[i][j] * (x1 + [1.0])[j] for i in range(3) for j in range(3))


def noisy_cases(seed, count, sigma=2.0):
    rng = random.Random(seed)
    out = []
    for _ in range(count):
        sc = random_scene(rng, n=1, n_cams=2, max_angle=0.5)
        xa, xb = add_noise(rng, [sc["x"][0][0], sc["x"][1][0]], sigma)
        out.append((sc["P"][0], sc["P"][1], xa, xb, sc["X"][0]))
    return out


def test_worked_example_pure_translation():
    X, x1h, x2h, cost = optimal_triangulation(P1, P2, [0.25, 0.5], [0.0, 0.52])
    assert rel(x1h, [0.25, 0.51]) <= 1e-12 and rel(x2h, [0.0, 0.51]) <= 1e-12
    assert rel(X, [1.0, 2.04, 4.0]) <= 1e-12
    assert abs(cost - 2e-4) <= 1e-15


def test_worked_example_general():
    F = fundamental_from_cameras(P1, P2B)
    x1h, x2h, cost, info = optimal_correction(F, Y1, Y2N, details=True)
    assert abs(abs(info["f"]) - 0.464944) <= 1e-6
    assert abs(abs(info["f2"]) - 0.210505) <= 1e-6
    assert len(info["roots"]) == 2
    assert abs(info["roots"][0] - 0.0094559) <= 1e-6
    assert abs(info["roots"][1] - 11.419014) <= 1e-5
    assert abs(cost - 1.880302e-4) <= 1e-9
    assert rel(x1h, [0.247761, 0.509187]) <= 1e-6
    assert rel(x2h, [-0.273185, 0.473418]) <= 1e-6
    X = triangulate_dlt(P1, P2B, x1h, x2h)
    assert rel(X, [1.054300, 2.166745, 4.255303]) <= 1e-6
    Xl = triangulate_dlt(P1, P2B, Y1, Y2N)
    assert reprojection_cost(P1, P2B, Xl, Y1, Y2N) > cost
    a, b, c, d = info["abcd"]
    for t in info["roots"]:
        h = 1e-6 * max(1.0, abs(t))
        ds = (cost_s(t + h, a, b, c, d, info["f"], info["f2"])
              - cost_s(t - h, a, b, c, d, info["f"], info["f2"])) / (2 * h)
        assert abs(ds) <= 1e-6


def test_exact_data():
    rng = random.Random(1)
    for _ in range(6):
        sc = random_scene(rng, n=1, n_cams=2, max_angle=0.5)
        xa, xb = sc["x"][0][0], sc["x"][1][0]
        X, x1h, x2h, cost = optimal_triangulation(sc["P"][0], sc["P"][1], xa, xb)
        assert rel(X, sc["X"][0]) <= 1e-8
        assert norm(sub(x1h, xa)) <= 1e-8 * norm(xa)
        assert cost <= 1e-12 * norm(xa) ** 2


def test_corrected_points_satisfy_the_epipolar_constraint():
    for Pa, Pb, xa, xb, _ in noisy_cases(2, 6):
        F = fundamental_from_cameras(Pa, Pb)
        x1h, x2h, _ = optimal_correction(F, xa, xb)
        scale = norm(F) * (norm(x1h) + 1.0) * (norm(x2h) + 1.0)
        assert abs(epipolar(F, x1h, x2h)) <= 1e-12 * scale


def test_cost_is_reprojection_error_and_beats_linear():
    for Pa, Pb, xa, xb, Xt in noisy_cases(3, 6):
        X, _, _, cost = optimal_triangulation(Pa, Pb, xa, xb)
        assert abs(reprojection_cost(Pa, Pb, X, xa, xb) - cost) <= 1e-8 * max(1.0, cost)
        Xl = triangulate_dlt(Pa, Pb, xa, xb)
        assert cost <= reprojection_cost(Pa, Pb, Xl, xa, xb) + 1e-9
        assert cost <= reprojection_cost(Pa, Pb, Xt, xa, xb) + 1e-9


def test_global_minimum_over_the_pencil():
    for Pa, Pb, xa, xb, _ in noisy_cases(4, 4, sigma=5.0):
        F = fundamental_from_cameras(Pa, Pb)
        _, _, _, info = optimal_correction(F, xa, xb, details=True)
        a, b, c, d = info["abcd"]
        best = min(cost_s(math.tan(math.pi * (k + 0.5) / 4000 - math.pi / 2),
                          a, b, c, d, info["f"], info["f2"]) for k in range(4000))
        assert info["s"] <= best + 1e-12


def test_local_perturbations_do_not_help():
    rng = random.Random(5)
    for Pa, Pb, xa, xb, _ in noisy_cases(5, 3):
        X, _, _, cost = optimal_triangulation(Pa, Pb, xa, xb)
        for _ in range(30):
            Z = [x + rng.gauss(0, 1e-3) for x in X]
            assert reprojection_cost(Pa, Pb, Z, xa, xb) >= cost - 1e-9


def test_projective_invariance():
    rng = random.Random(6)
    H = [[rng.uniform(-1, 1) + (2.0 if i == j else 0.0) for j in range(4)] for i in range(4)]
    Hi = inv(H)
    for Pa, Pb, xa, xb, _ in noisy_cases(7, 3):
        X, x1h, x2h, cost = optimal_triangulation(Pa, Pb, xa, xb)
        X2, y1h, y2h, cost2 = optimal_triangulation(mul(Pa, Hi), mul(Pb, Hi), xa, xb)
        assert rel(y1h, x1h) <= 1e-8 and rel(y2h, x2h) <= 1e-8
        assert abs(cost2 - cost) <= 1e-8 * max(1.0, cost)
        Xh = matvec(H, X + [1.0])
        assert rel([v / Xh[3] for v in Xh[:3]], X2) <= 1e-7


def test_point_at_the_epipole_raises():
    C2 = [-v for v in matvec(transpose(rot_y(-0.3)), [-1.0, 0.0, 0.2])]
    e1 = [C2[0] / C2[2], C2[1] / C2[2]]
    F = fundamental_from_cameras(P1, P2B)
    with pytest.raises(ValueError):
        optimal_correction(F, e1, Y2N)
