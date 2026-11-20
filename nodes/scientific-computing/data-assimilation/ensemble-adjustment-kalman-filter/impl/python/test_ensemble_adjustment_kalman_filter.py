# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ensemble-adjustment-kalman-filter/. The authors are listed in prov/NP9ZCK.jsonl.

import math
import random

import scimat
from ensemble_adjustment_kalman_filter import adjustment_matrix, eakf_joint, eakf_serial, ensemble_moments


def kalman_moments(ens, yo, H, R):
    n = len(ens[0])
    xbar, P = ensemble_moments(ens)
    PHt = scimat.matmul(P, scimat.transpose(H))
    S = scimat.add(scimat.matmul(H, PHt), R)
    K = scimat.transpose(scimat.solve(S, scimat.transpose(PHt)))
    xa = scimat.add(xbar, scimat.matvec(K, scimat.sub(yo, scimat.matvec(H, xbar))))
    Pa = scimat.matmul(scimat.sub(scimat.eye(n), scimat.matmul(K, H)), P)
    return xa, Pa


def close_moments(ens, xa, Pa, tol=1e-9):
    ma, Pe = ensemble_moments(ens)
    for a in range(len(xa)):
        assert abs(ma[a] - xa[a]) < tol * (1 + abs(xa[a]))
        for b in range(len(xa)):
            assert abs(Pe[a][b] - Pa[a][b]) < tol * (1 + abs(Pa[a][b]))


def diag(r):
    return [[r[a] if a == b else 0.0 for b in range(len(r))] for a in range(len(r))]


def test_scalar_check_value():
    s = 1 / math.sqrt(2.0)
    for out in (eakf_serial([[-s], [s]], [1.0], lambda x: [x[0]], [1.0]),
                eakf_joint([[-s], [s]], [1.0], [[1.0]], [[1.0]])):
        mean, P = ensemble_moments(out)
        assert abs(mean[0] - 0.5) < 1e-12
        assert abs(P[0][0] - 0.5) < 1e-12


def test_page_example():
    ens = [[0.0, 1.0], [1.0, 3.0], [2.0, 2.0]]
    out = eakf_serial(ens, [2.0], lambda x: [x[0]], [1 / 3])
    expect = [[5 / 4, 13 / 8], [7 / 4, 27 / 8], [9 / 4, 17 / 8]]
    for a, b in zip(out, expect):
        assert abs(a[0] - b[0]) < 1e-12 and abs(a[1] - b[1]) < 1e-12
    mean, P = ensemble_moments(out)
    assert abs(mean[1] - 19 / 8) < 1e-12
    assert abs(P[1][1] - 13 / 16) < 1e-12


def test_serial_matches_kalman_moments():
    rng = random.Random(41)
    for _ in range(80):
        n, p, N = rng.randint(1, 5), rng.randint(1, 5), rng.randint(2, 8)
        ens = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(N)]
        H = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(p)]
        r = [rng.uniform(0.1, 2.0) for _ in range(p)]
        yo = [rng.gauss(0, 2) for _ in range(p)]
        out = eakf_serial(ens, yo, lambda x: scimat.matvec(H, x), r)
        xa, Pa = kalman_moments(ens, yo, H, diag(r))
        close_moments(out, xa, Pa)


def test_joint_matches_kalman_moments_with_correlated_R():
    rng = random.Random(42)
    for _ in range(40):
        n, p, N = rng.randint(1, 4), rng.randint(1, 4), rng.randint(2, 8)
        ens = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(N)]
        H = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(p)]
        L = [[rng.uniform(-1, 1) for _ in range(p)] for _ in range(p)]
        R = scimat.add(scimat.matmul(L, scimat.transpose(L)), scimat.scale(0.3, scimat.eye(p)))
        yo = [rng.gauss(0, 2) for _ in range(p)]
        out = eakf_joint(ens, yo, H, R)
        xa, Pa = kalman_moments(ens, yo, H, R)
        close_moments(out, xa, Pa)


def test_adjustment_matrix_identity():
    # A P A^T equals the Kalman analysis covariance, also when P is singular (N < n + 1).
    rng = random.Random(43)
    n, N, p = 5, 3, 2
    ens = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(N)]
    _, P = ensemble_moments(ens)
    H = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(p)]
    R = diag([0.5, 2.0])
    A = adjustment_matrix(P, H, R)
    APAt = scimat.matmul(scimat.matmul(A, P), scimat.transpose(A))
    _, Pa = kalman_moments(ens, [0.0, 0.0], H, R)
    for a in range(n):
        for b in range(n):
            assert abs(APAt[a][b] - Pa[a][b]) < 1e-9


def test_one_observation_serial_equals_joint_and_square_root_filter():
    # For one scalar observation the serial EAKF, the joint EAKF and the reduced gain
    # update x' - alpha K h x' of the serial EnSRF give the same members.
    rng = random.Random(44)
    for _ in range(20):
        n, N = rng.randint(1, 4), rng.randint(2, 7)
        ens = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(N)]
        h = [rng.uniform(-1, 1) for _ in range(n)]
        r = rng.uniform(0.2, 2.0)
        a = eakf_serial(ens, [0.3], lambda x: [scimat.dot(h, x)], [r])
        b = eakf_joint(ens, [0.3], [h], [[r]])
        xbar, P = ensemble_moments(ens)
        Ph = scimat.matvec(P, h)
        s = scimat.dot(h, Ph)
        K = [v / (s + r) for v in Ph]
        alpha = 1 / (1 + math.sqrt(r / (s + r)))
        d = 0.3 - scimat.dot(h, xbar)
        for i in range(N):
            xp = scimat.sub(ens[i], xbar)
            hxp = scimat.dot(h, xp)
            c = [xbar[j] + K[j] * d + xp[j] - alpha * K[j] * hxp for j in range(n)]
            for j in range(n):
                assert abs(a[i][j] - c[j]) < 1e-9
                assert abs(b[i][j] - c[j]) < 1e-9


def test_observation_with_no_spread_is_skipped():
    ens = [[1.0, 0.0], [1.0, 2.0]]
    out = eakf_serial(ens, [5.0], lambda x: [x[0]], [1.0])
    assert out == ens


def test_localization_weight_zero_freezes_value():
    rng = random.Random(45)
    ens = [[rng.gauss(0, 1) for _ in range(3)] for _ in range(5)]
    out = eakf_serial(ens, [1.0], lambda x: [x[0]], [0.5], loc_state=[[1.0, 0.3, 0.0]])
    for x, z in zip(ens, out):
        assert z[2] == x[2]
