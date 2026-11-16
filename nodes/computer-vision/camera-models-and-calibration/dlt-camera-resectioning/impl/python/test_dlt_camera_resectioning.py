# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dlt-camera-resectioning/. The authors are listed in prov/WCKDXR.jsonl.
"""Tests of the normalized DLT and of the shared helpers cvla and cvgeom."""

import math
import random
from fractions import Fraction

import cvgeom
import cvla
from cvgeom import (add_noise, axis_angle_to_R, camera_center, camera_matrix,
                    from_h, make_K, project, quat_to_R, random_rotation,
                    random_scene, rot_x, rot_y, rot_z, to_h)
from cvla import (add, cholesky, cross, det, dot, eye, inv, matvec, mul, norm,
                  nullvec, polyroots_real, qr, rq, scale, skew, solve, sub,
                  svd, sym_eig, transpose, zeros)
from dlt_camera_resectioning import (dlt_matrix, dlt_resection, normalize_2d,
                                     normalize_3d, normalize_P, reprojection_errors,
                                     rms, singular_values_of_dlt)


def close(a, b, tol):
    return norm(sub(a, b)) <= tol


def diag(s, m, n):
    return [[s[i] if i == j else 0.0 for j in range(n)] for i in range(m)]


# ------------------------------------------------------------ cvla

def test_cvla_self_test():
    cvla.self_test()


def test_basic_ops():
    a = [[1.0, 2.0], [3.0, 4.0]]
    assert mul(a, eye(2)) == a
    assert transpose(a) == [[1.0, 3.0], [2.0, 4.0]]
    assert add(a, a) == scale(a, 2.0)
    assert sub(a, a) == zeros(2, 2)
    assert matvec(a, [1.0, 1.0]) == [3.0, 7.0]
    assert dot([1, 2, 3], [4, 5, 6]) == 32
    assert norm([3.0, 4.0]) == 5.0
    assert abs(norm(a) - math.sqrt(30.0)) < 1e-15
    u, v = [1.0, 2.0, 3.0], [-2.0, 0.5, 4.0]
    assert matvec(skew(u), v) == cross(u, v)
    assert dot(cross(u, v), u) == 0.0


def test_solve_inv_det_exact_with_fractions():
    rng = random.Random(3)
    for _ in range(20):
        n = rng.randint(1, 5)
        a = [[Fraction(rng.randint(-9, 9)) for _ in range(n)] for _ in range(n)]
        if det(a) == 0:
            continue
        x = [Fraction(rng.randint(-9, 9), rng.randint(1, 5)) for _ in range(n)]
        b = matvec(a, x)
        assert solve(a, b) == x
        ident = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
        assert mul(a, inv(a)) == ident
    a = [[Fraction(2), Fraction(1), Fraction(0)], [Fraction(1), Fraction(3), Fraction(1)],
         [Fraction(0), Fraction(1), Fraction(4)]]
    assert det(a) == 18
    assert det([[1.0, 2.0], [2.0, 4.0]]) == 0


def test_det_matches_permutation_expansion():
    import itertools
    rng = random.Random(4)
    a = [[rng.uniform(-1, 1) for _ in range(4)] for _ in range(4)]
    total = 0.0
    for perm in itertools.permutations(range(4)):
        inversions = sum(1 for i in range(4) for j in range(i + 1, 4) if perm[i] > perm[j])
        term = -1.0 if inversions % 2 else 1.0
        for i in range(4):
            term *= a[i][perm[i]]
        total += term
    assert abs(det(a) - total) < 1e-12


def test_solve_singular_raises():
    try:
        solve([[1.0, 2.0], [2.0, 4.0]], [1.0, 1.0])
    except ValueError:
        return
    raise AssertionError("expected ValueError")


def test_svd_shapes_and_orthogonality():
    rng = random.Random(5)
    for m, n in [(7, 4), (4, 7), (3, 3), (12, 12), (5, 1), (1, 5)]:
        a = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(m)]
        u, s, v = svd(a)
        k = min(m, n)
        assert len(u) == m and len(u[0]) == k and len(s) == k and len(v) == n
        assert close(mul(mul(u, diag(s, k, k)), transpose(v)), a, 1e-12)
        assert close(mul(transpose(u), u), eye(k), 1e-12)
        assert close(mul(transpose(v), v), eye(len(v[0])), 1e-12)
        assert all(s[i] >= s[i + 1] >= 0 for i in range(k - 1))


def test_svd_against_sym_eig():
    rng = random.Random(6)
    a = [[rng.uniform(-1, 1) for _ in range(4)] for _ in range(6)]
    _, s, _ = svd(a)
    w, _ = sym_eig(mul(transpose(a), a))
    assert all(abs(si * si - wi) < 1e-12 for si, wi in zip(s, reversed(w)))


def test_svd_rank_deficient():
    a = [[1.0, 2.0, 3.0], [2.0, 4.0, 6.0], [1.0, 1.0, 1.0], [0.0, 0.0, 0.0]]
    u, s, v = svd(a)
    assert s[2] < 1e-14
    assert close(mul(transpose(u), u), eye(3), 1e-12)
    assert close(mul(mul(u, diag(s, 3, 3)), transpose(v)), a, 1e-12)


def test_nullvec():
    a = [[1.0, 2.0, 3.0], [2.0, 4.0, 6.0], [1.0, 1.0, 1.0]]
    x = nullvec(a)
    assert abs(norm(x) - 1.0) < 1e-14 and norm(matvec(a, x)) < 1e-14
    b = [[1.0, 2.0, 3.0, 4.0], [2.0, 4.0, 6.0, 8.5]]
    y = nullvec(b)
    assert abs(norm(y) - 1.0) < 1e-14 and norm(matvec(b, y)) < 1e-14


def test_qr_rq_cholesky():
    rng = random.Random(8)
    for m, n in [(3, 3), (5, 3), (3, 5), (4, 4)]:
        a = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(m)]
        q, r = qr(a)
        assert close(mul(q, r), a, 1e-13)
        assert close(mul(transpose(q), q), eye(m), 1e-13)
        assert all(r[i][j] == 0.0 for i in range(m) for j in range(min(i, n)))
        assert all(r[i][i] >= 0.0 for i in range(min(m, n)))
    for _ in range(5):
        a = [[rng.uniform(-1, 1) for _ in range(3)] for _ in range(3)]
        r, q = rq(a)
        assert close(mul(r, q), a, 1e-13)
        assert close(mul(q, transpose(q)), eye(3), 1e-13)
        assert r[1][0] == r[2][0] == r[2][1] == 0.0
        assert all(r[i][i] >= 0.0 for i in range(3))
        spd = add(mul(a, transpose(a)), eye(3))
        low = cholesky(spd)
        assert close(mul(low, transpose(low)), spd, 1e-13)
        assert low[0][1] == low[0][2] == low[1][2] == 0.0
    try:
        cholesky([[1.0, 2.0], [2.0, 1.0]])
    except ValueError:
        return
    raise AssertionError("expected ValueError")


def test_polyroots_real():
    assert all(abs(x - y) < 1e-10 for x, y in zip(polyroots_real([1, -6, 11, -6]), [1, 2, 3]))
    assert polyroots_real([1.0, 0.0, 1.0]) == []
    assert polyroots_real([0.0, 2.0, -4.0]) == [2.0]
    assert polyroots_real([5.0]) == []
    assert polyroots_real([1.0, 0.0, -1.0, 0.0]) == [-1.0, 0.0, 1.0]
    double = polyroots_real([1.0, -2.0, 1.0])
    assert len(double) == 2 and all(abs(x - 1.0) < 1e-6 for x in double)
    rng = random.Random(9)
    for _ in range(10):
        true = sorted(rng.uniform(-5, 5) for _ in range(6))
        c = [1.0]
        for r in true:
            c = [a - r * b for a, b in zip(c + [0.0], [0.0] + c)]
        # x^2 + 1 adds two complex roots that must be dropped
        c = [a + b for a, b in zip(c + [0.0, 0.0], [0.0, 0.0] + c)]
        got = polyroots_real(c)
        assert len(got) == 6
        assert all(abs(x - y) < 1e-8 for x, y in zip(got, true))


# ------------------------------------------------------------ cvgeom

def test_cvgeom_self_test():
    cvgeom.self_test()


def test_homogeneous_and_projection():
    assert to_h([2, 3]) == [2.0, 3.0, 1.0]
    assert from_h([4.0, 6.0, 2.0]) == [2.0, 3.0]
    try:
        from_h([1.0, 0.0])
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
    K = make_K(500, 500, 320, 240)
    P = camera_matrix(K, eye(3), [0.0, 0.0, 0.0])
    assert project(P, [0.1, -0.2, 2.0]) == [345.0, 190.0]
    assert project(P, [0.2, -0.4, 4.0, 2.0]) == [345.0, 190.0]
    assert project(P, [[0.0, 0.0, 1.0], [0.1, -0.2, 2.0]]) == [[320.0, 240.0], [345.0, 190.0]]
    assert make_K(1, 2, 3, 4, 0.5) == [[1.0, 0.5, 3.0], [0.0, 2.0, 4.0], [0.0, 0.0, 1.0]]


def test_camera_center():
    rng = random.Random(10)
    for _ in range(5):
        R = random_rotation(rng)
        C = [rng.uniform(-3, 3) for _ in range(3)]
        t = [-v for v in matvec(R, C)]
        P = camera_matrix(make_K(700, 650, 300, 200, 1.5), R, t)
        assert close(camera_center(P), C, 1e-12)
        assert norm(matvec(P, to_h(C))) < 1e-9


def test_rotations():
    a = 0.7
    assert close(axis_angle_to_R([1, 0, 0], a), rot_x(a), 1e-15)
    assert close(axis_angle_to_R([0, 2, 0], a), rot_y(a), 1e-15)
    assert close(axis_angle_to_R([0, 0, 0.5], a), rot_z(a), 1e-15)
    assert close(axis_angle_to_R([0, 0, a]), rot_z(a), 1e-15)
    # right-hand rule: a quarter turn about Z maps X to Y
    assert close([matvec(rot_z(math.pi / 2), [1.0, 0.0, 0.0])], [[0.0, 1.0, 0.0]], 1e-15)
    h = math.sqrt(0.5)
    assert close(quat_to_R([h, 0.0, 0.0, h]), rot_z(math.pi / 2), 1e-15)
    assert close(quat_to_R([-h, 0.0, 0.0, -h]), rot_z(math.pi / 2), 1e-15)
    rng = random.Random(12)
    for _ in range(10):
        R = random_rotation(rng)
        assert close(mul(transpose(R), R), eye(3), 1e-12)
        assert abs(det(R) - 1.0) < 1e-12
        axis = [rng.gauss(0, 1) for _ in range(3)]
        Ra = axis_angle_to_R(axis, 1.1)
        assert close(matvec(Ra, axis), axis, 1e-12)


def test_random_rotation_mean_trace():
    # For the uniform distribution on SO(3), E[trace R] = 0.
    rng = random.Random(13)
    m = 3000
    s = sum(sum(random_rotation(rng)[i][i] for i in range(3)) for _ in range(m)) / m
    assert abs(s) < 0.1


def test_random_scene():
    rng = random.Random(14)
    sc = random_scene(rng, n=25, n_cams=3, size=(640, 480))
    for P, R, t, xs in zip(sc["P"], sc["R"], sc["t"], sc["x"]):
        for X, x in zip(sc["X"], xs):
            assert matvec(R, X)[2] + t[2] > 0.0
            assert 0.0 <= x[0] <= 640.0 and 0.0 <= x[1] <= 480.0
            assert close(project(P, X), x, 1e-9)
    sc = random_scene(rng, n=10, n_cams=3, planar=True, first_identity=True)
    assert sc["R"][0] == eye(3) and sc["t"][0] == [0.0, 0.0, 0.0]
    for P, xs in zip(sc["P"], sc["x"]):
        for X, x in zip(sc["X"], xs):
            assert close(project(P, X), x, 1e-9)
    cams = [(make_K(500, 500, 0, 0), eye(3), [0.0, 0.0, 10.0])]
    sc = random_scene(rng, n=5, cams=cams)
    assert sc["t"] == [[0.0, 0.0, 10.0]]


def test_add_noise():
    rng = random.Random(15)
    pts = [[0.0, 0.0] for _ in range(2000)]
    noisy = add_noise(rng, pts, 0.5)
    assert pts[0] == [0.0, 0.0]
    var = sum(p[0] ** 2 + p[1] ** 2 for p in noisy) / (2 * len(noisy))
    assert abs(math.sqrt(var) - 0.5) < 0.03


# ------------------------------------------------------------ DLT

def scene(seed, n, planar=False):
    rng = random.Random(seed)
    K = make_K(800, 780, 320, 240, 2.0)
    sc = random_scene(rng, n=n, n_cams=1, K=K, size=(640, 480), planar=planar)
    return rng, sc["X"], sc["x"][0], sc["P"][0]


def test_normalizations():
    _, X, x, _ = scene(20, 12)
    T, U = normalize_2d(x), normalize_3d(X)
    xs = [from_h(matvec(T, to_h(p))) for p in x]
    Xs = [from_h(matvec(U, to_h(p))) for p in X]
    assert all(abs(sum(p[k] for p in xs)) < 1e-12 for k in range(2))
    assert abs(sum(norm(p) for p in xs) / len(xs) - math.sqrt(2)) < 1e-12
    assert all(abs(sum(p[k] for p in Xs)) < 1e-12 for k in range(3))
    assert abs(sum(norm(p) for p in Xs) / len(Xs) - math.sqrt(3)) < 1e-12


def test_dlt_rows_vanish_on_true_P():
    _, X, x, P = scene(21, 8)
    a = dlt_matrix([to_h(p) for p in X], [to_h(p) for p in x])
    p = P[0] + P[1] + P[2]
    assert norm(matvec(a, p)) < 1e-9 * norm(p)


def test_exact_recovery_without_noise():
    for seed, n in [(22, 6), (23, 7), (24, 20), (25, 60)]:
        _, X, x, P = scene(seed, n)
        for flag in (True, False):
            est = dlt_resection(X, x, normalize=flag)
            assert close(est, normalize_P(P), 1e-8)
            assert max(reprojection_errors(est, X, x)) < 1e-8


def test_against_inhomogeneous_reference():
    # Reference: fix p34 = 1 and solve 11 of the 12 equations of 6 points.
    _, X, x, P = scene(26, 6)
    a = dlt_matrix([to_h(p) for p in X], [to_h(p) for p in x])[:11]
    m = [row[:11] for row in a]
    rhs = [-row[11] for row in a]
    p = solve(m, rhs) + [1.0]
    ref = normalize_P([p[0:4], p[4:8], p[8:12]])
    assert close(dlt_resection(X, x), ref, 1e-8)


def test_scale_and_sign_rule():
    _, X, x, P = scene(27, 10)
    est = dlt_resection(X, x)
    assert abs(norm(est) - 1.0) < 1e-12
    assert det([row[:3] for row in est]) > 0
    # positive third coordinate: the points are in front of the camera
    assert all(matvec(est, to_h(p))[2] > 0 for p in X)


def test_noise():
    # sigma = 0.5 pixels on 50 points: the residual is near sigma sqrt(2)
    # and the center is within 0.1 (the scene is 5 units away).
    rng, X, x, P = scene(28, 50)
    C = camera_center(P)
    for _ in range(3):
        xn = add_noise(rng, x, 0.5)
        est = dlt_resection(X, xn)
        assert rms(reprojection_errors(est, X, xn)) < 0.9
        assert rms(reprojection_errors(est, X, x)) < 0.5
        assert norm(sub(camera_center(est), C)) < 0.1


def test_coplanar_points_are_degenerate():
    _, X, x, _ = scene(29, 20, planar=True)
    s = singular_values_of_dlt(X, x)
    assert s[-3] < 1e-12 * s[0]
    _, X, x, _ = scene(30, 20)
    s = singular_values_of_dlt(X, x)
    assert s[-1] < 1e-12 * s[0] and s[-2] > 1e-3 * s[0]


def test_too_few_points():
    _, X, x, _ = scene(31, 6)
    try:
        dlt_resection(X[:5], x[:5])
    except ValueError:
        return
    raise AssertionError("expected ValueError")
