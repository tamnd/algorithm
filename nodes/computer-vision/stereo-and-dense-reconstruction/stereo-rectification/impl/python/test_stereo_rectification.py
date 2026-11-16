# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stereo-rectification/. The authors are listed in prov/K5RE9X.jsonl.

import math
import random

import pytest

from cvgeom import axis_angle_to_R, camera_matrix, make_K, project, rot_y
from cvla import det, matvec, mul, norm, transpose
from stereo_rectification import (
    apply_homography,
    bilinear,
    rectified_fundamental,
    rectify_calibrated,
    warp_image,
)


def pose(R, C):
    """(R, t) of a camera with rotation R and center C."""
    return R, [-v for v in matvec(R, C)]


def random_rig(rng):
    K1 = make_K(rng.uniform(400, 600), rng.uniform(400, 600), rng.uniform(150, 170), rng.uniform(110, 130))
    K2 = make_K(rng.uniform(400, 600), rng.uniform(400, 600), rng.uniform(150, 170), rng.uniform(110, 130))
    R1 = axis_angle_to_R([rng.gauss(0, 1) for _ in range(3)], rng.uniform(0, 0.2))
    R2 = axis_angle_to_R([rng.gauss(0, 1) for _ in range(3)], rng.uniform(0, 0.2))
    C1 = [rng.uniform(-1, 1) for _ in range(3)]
    C2 = [C1[0] + rng.uniform(0.05, 0.5), C1[1] + rng.uniform(-0.03, 0.03), C1[2] + rng.uniform(-0.03, 0.03)]
    R1, t1 = pose(R1, C1)
    R2, t2 = pose(R2, C2)
    return K1, R1, t1, K2, R2, t2


def points_in_front(rng, R, C, n):
    """n points 2 to 6 units in front of the camera (R, C)."""
    out = []
    Rt = transpose(R)
    for _ in range(n):
        z = rng.uniform(2.0, 6.0)
        xc = [rng.uniform(-0.3, 0.3) * z, rng.uniform(-0.3, 0.3) * z, z]
        out.append([a + c for a, c in zip(matvec(Rt, xc), C)])
    return out


def normalize_f(F):
    s = norm(F)
    G = [[x / s for x in row] for row in F]
    if G[2][1] < 0:
        G = [[-x for x in row] for row in G]
    return G


def test_rows_match_and_disparity_is_f_b_over_z():
    rng = random.Random(1)
    for _ in range(20):
        K1, R1, t1, K2, R2, t2 = random_rig(rng)
        r = rectify_calibrated(K1, R1, t1, K2, R2, t2)
        P1, P2 = camera_matrix(K1, R1, t1), camera_matrix(K2, R2, t2)
        Rn, Kn, b, C1 = r["Rn"], r["Kn"], r["b"], r["C1"]
        for X in points_in_front(rng, R1, C1, 15):
            x1 = apply_homography(r["H1"], project(P1, X))
            x2 = apply_homography(r["H2"], project(P2, X))
            Zn = matvec(Rn, [a - c for a, c in zip(X, C1)])[2]
            assert abs(x1[1] - x2[1]) <= 1e-8
            d = x1[0] - x2[0]
            assert d > 0
            assert abs(d - Kn[0][0] * b / Zn) <= 1e-8 * max(1.0, d)


def test_homography_equals_new_camera():
    rng = random.Random(2)
    K1, R1, t1, K2, R2, t2 = random_rig(rng)
    r = rectify_calibrated(K1, R1, t1, K2, R2, t2)
    P1, P2 = camera_matrix(K1, R1, t1), camera_matrix(K2, R2, t2)
    for X in points_in_front(rng, R1, r["C1"], 10):
        for H, P, Pn in ((r["H1"], P1, r["P1"]), (r["H2"], P2, r["P2"])):
            a = apply_homography(H, project(P, X))
            c = project(Pn, X)
            assert max(abs(p - q) for p, q in zip(a, c)) <= 1e-8


def test_new_rotation_is_a_rotation_with_x_along_the_baseline():
    rng = random.Random(3)
    for _ in range(10):
        K1, R1, t1, K2, R2, t2 = random_rig(rng)
        r = rectify_calibrated(K1, R1, t1, K2, R2, t2)
        Rn = r["Rn"]
        RtR = mul(transpose(Rn), Rn)
        assert all(abs(RtR[i][j] - (1.0 if i == j else 0.0)) <= 1e-12 for i in range(3) for j in range(3))
        assert abs(det(Rn) - 1.0) <= 1e-12
        base = [a - c for a, c in zip(r["C2"], r["C1"])]
        assert matvec(Rn, base)[0] == pytest.approx(r["b"], rel=1e-12)
        assert abs(matvec(Rn, base)[1]) <= 1e-12 and abs(matvec(Rn, base)[2]) <= 1e-12
        # the new optical axis keeps a positive component along the old one
        assert sum(p * q for p, q in zip(Rn[2], R1[2])) > 0


def test_rectified_fundamental_matrix():
    rng = random.Random(4)
    K1, R1, t1, K2, R2, t2 = random_rig(rng)
    r = rectify_calibrated(K1, R1, t1, K2, R2, t2)
    F = normalize_f(rectified_fundamental(r["Kn"], r["b"]))
    s = 1.0 / math.sqrt(2.0)
    target = [[0.0, 0.0, 0.0], [0.0, 0.0, -s], [0.0, s, 0.0]]
    assert max(abs(F[i][j] - target[i][j]) for i in range(3) for j in range(3)) <= 1e-12
    P1, P2 = camera_matrix(K1, R1, t1), camera_matrix(K2, R2, t2)
    for X in points_in_front(rng, R1, r["C1"], 10):
        x1 = apply_homography(r["H1"], project(P1, X)) + [1.0]
        x2 = apply_homography(r["H2"], project(P2, X)) + [1.0]
        assert abs(sum(x2[i] * sum(F[i][j] * x1[j] for j in range(3)) for i in range(3))) <= 1e-9


def test_check_value_depth():
    K = make_K(500, 500, 320, 240)
    I = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    R1, t1 = pose(I, [0.0, 0.0, 0.0])
    R2, t2 = pose(I, [0.1, 0.0, 0.0])
    r = rectify_calibrated(K, R1, t1, K, R2, t2)
    for H in (r["H1"], r["H2"]):
        assert all(abs(H[i][j] - I[i][j]) <= 1e-12 for i in range(3) for j in range(3))
    X = [0.3, -0.2, 2.5]
    x1 = project(r["P1"], X)
    x2 = project(r["P2"], X)
    assert x1[0] - x2[0] == pytest.approx(20.0, abs=1e-12)
    assert 500 * 0.1 / (x1[0] - x2[0]) == pytest.approx(2.5, abs=1e-12)


def test_worked_example():
    K = make_K(500, 500, 320, 240)
    R1, t1 = pose(rot_y(0.05), [0.0, 0.0, 0.0])
    R2, t2 = pose(rot_y(-0.05), [0.1, 0.0, 0.0])
    r = rectify_calibrated(K, R1, t1, K, R2, t2)
    X = [0.2, 0.1, 2.0]
    x1 = project(camera_matrix(K, R1, t1), X)
    x2 = project(camera_matrix(K, R2, t2), X)
    y1 = apply_homography(r["H1"], x1)
    y2 = apply_homography(r["H2"], x2)
    assert abs(y1[1] - y2[1]) <= 1e-9
    assert y1[0] - y2[0] == pytest.approx(25.0, abs=1e-9)


def test_degenerate_rigs():
    K = make_K(500, 500, 320, 240)
    I = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    R1, t1 = pose(I, [0.0, 0.0, 0.0])
    R2, t2 = pose(I, [0.0, 0.0, 0.0])
    with pytest.raises(ValueError):
        rectify_calibrated(K, R1, t1, K, R2, t2)
    R2, t2 = pose(I, [0.0, 0.0, 0.5])
    with pytest.raises(ValueError):
        rectify_calibrated(K, R1, t1, K, R2, t2)


def test_baseline_to_the_left_still_gives_positive_disparity():
    # camera 2 to the left of camera 1: the new X axis points left, and the
    # new frame is the old one turned by pi about the optical axis.
    K = make_K(500, 500, 320, 240)
    I = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    R1, t1 = pose(I, [0.0, 0.0, 0.0])
    R2, t2 = pose(I, [-0.1, 0.0, 0.0])
    r = rectify_calibrated(K, R1, t1, K, R2, t2)
    # Rn rotates by pi about the optical axis: the image turns upside down
    assert r["Rn"][2] == pytest.approx([0.0, 0.0, 1.0], abs=1e-12)
    assert r["Rn"][0] == pytest.approx([-1.0, 0.0, 0.0], abs=1e-12)
    X = [0.1, 0.2, 2.5]
    d = project(r["P1"], X)[0] - project(r["P2"], X)[0]
    assert d == pytest.approx(20.0, abs=1e-9)


def test_bilinear_and_warp():
    rng = random.Random(5)
    img = [[rng.randint(0, 255) for _ in range(9)] for _ in range(7)]
    I = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    out = warp_image(img, I, 9, 7)
    assert all(abs(out[v][u] - img[v][u]) <= 1e-12 for v in range(7) for u in range(9))
    T = [[1.0, 0.0, 2.0], [0.0, 1.0, 1.0], [0.0, 0.0, 1.0]]
    out = warp_image(img, T, 9, 7, fill=-1.0)
    for v in range(7):
        for u in range(9):
            if u >= 2 and v >= 1:
                assert abs(out[v][u] - img[v - 1][u - 2]) <= 1e-12
            else:
                assert out[v][u] == -1.0
    assert bilinear([[0, 10], [20, 30]], 0.5, 0.5) == pytest.approx(15.0)
    assert bilinear([[0, 10], [20, 30]], 1.0, 1.0) == pytest.approx(30.0)
    assert bilinear([[0, 10], [20, 30]], 1.5, 0.0, fill=7.0) == 7.0


def test_warp_rectifies_a_synthetic_dot():
    # a bright dot at a 3D point lands on the same row in both rectified images
    K = make_K(40, 40, 16, 12)
    R1, t1 = pose(rot_y(0.04), [0.0, 0.0, 0.0])
    R2, t2 = pose(rot_y(-0.04), [0.2, 0.02, 0.0])
    r = rectify_calibrated(K, R1, t1, K, R2, t2)
    X = [0.1, 0.05, 2.0]
    rows = []
    for (R, t), H in (((R1, t1), r["H1"]), ((R2, t2), r["H2"])):
        u, v = project(camera_matrix(K, R, t), X)
        img = [[math.exp(-((x - u) ** 2 + (y - v) ** 2) / 2.0) for x in range(32)] for y in range(24)]
        out = warp_image(img, H, 32, 24)
        best = max((out[y][x], y, x) for y in range(24) for x in range(32))
        rows.append(best[1])
        assert best[0] > 0.5
    assert rows[0] == rows[1]
