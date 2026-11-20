# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ensemble-square-root-filter/. The authors are listed in prov/W0YQYW.jsonl.

import math
import random

import scimat
from ensemble_square_root_filter import ensemble_moments, ensrf_analysis


def kalman_moments(ens, yo, H, r):
    """Oracle: the batch Kalman analysis mean and covariance for the sample covariance."""
    n = len(ens[0])
    xbar, P = ensemble_moments(ens)
    R = [[r[a] if a == b else 0.0 for b in range(len(r))] for a in range(len(r))]
    PHt = scimat.matmul(P, scimat.transpose(H))
    S = scimat.add(scimat.matmul(H, PHt), R)
    K = scimat.transpose(scimat.solve(S, scimat.transpose(PHt)))
    xa = scimat.add(xbar, scimat.matvec(K, scimat.sub(yo, scimat.matvec(H, xbar))))
    Pa = scimat.matmul(scimat.sub(scimat.eye(n), scimat.matmul(K, H)), P)
    return xa, Pa


def close_moments(ens, xa, Pa, tol=1e-9):
    ma, Pe = ensemble_moments(ens)
    n = len(xa)
    for a in range(n):
        assert abs(ma[a] - xa[a]) < tol * (1 + abs(xa[a]))
        for b in range(n):
            assert abs(Pe[a][b] - Pa[a][b]) < tol * (1 + abs(Pa[a][b]))


def test_scalar_check_value():
    s = 1 / math.sqrt(2.0)
    out = ensrf_analysis([[-s], [s]], [1.0], lambda x: [x[0]], [1.0])
    mean, P = ensemble_moments(out)
    assert abs(mean[0] - 0.5) < 1e-12
    assert abs(P[0][0] - 0.5) < 1e-12


def test_two_member_scalar():
    out = ensrf_analysis([[-1.0], [1.0]], [1.0], lambda x: [x[0]], [1.0])
    assert abs(out[0][0] - (2 / 3 - 1 / math.sqrt(3))) < 1e-12
    assert abs(out[1][0] - (2 / 3 + 1 / math.sqrt(3))) < 1e-12


def test_page_example_two_observations():
    out = ensrf_analysis([[-1.0, 0.0], [1.0, 2.0]], [1.0, 2.0], lambda x: list(x), [1.0, 1.0])
    mean, P = ensemble_moments(out)
    assert abs(mean[0] - 0.8) < 1e-12 and abs(mean[1] - 1.8) < 1e-12
    for a in range(2):
        for b in range(2):
            assert abs(P[a][b] - 0.4) < 1e-12
    assert abs(out[1][0] - (0.8 + 1 / math.sqrt(5))) < 1e-12


def test_serial_equals_batch_kalman_moments():
    rng = random.Random(31)
    for _ in range(80):
        n, p, N = rng.randint(1, 5), rng.randint(1, 5), rng.randint(2, 8)
        ens = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(N)]
        H = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(p)]
        r = [rng.uniform(0.1, 2.0) for _ in range(p)]
        yo = [rng.gauss(0, 2) for _ in range(p)]
        out = ensrf_analysis(ens, yo, lambda x: scimat.matvec(H, x), r)
        xa, Pa = kalman_moments(ens, yo, H, r)
        close_moments(out, xa, Pa)


def test_order_of_observations_does_not_change_moments():
    rng = random.Random(32)
    n, p, N = 4, 4, 6
    ens = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(N)]
    H = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(p)]
    r = [0.5, 1.0, 1.5, 2.0]
    yo = [1.0, -1.0, 0.5, 2.0]
    m1, P1 = ensemble_moments(ensrf_analysis(ens, yo, lambda x: scimat.matvec(H, x), r))
    perm = [2, 0, 3, 1]
    Hp = [H[k] for k in perm]
    m2, P2 = ensemble_moments(ensrf_analysis(ens, [yo[k] for k in perm], lambda x: scimat.matvec(Hp, x),
                                             [r[k] for k in perm]))
    for a in range(n):
        assert abs(m1[a] - m2[a]) < 1e-10
        for b in range(n):
            assert abs(P1[a][b] - P2[a][b]) < 1e-10


def test_perturbed_reduction_factor():
    # One scalar observation: the perturbations of the observed value shrink by sqrt(r / (s + r)).
    rng = random.Random(33)
    for _ in range(20):
        N = rng.randint(2, 9)
        ens = [[rng.gauss(0, 2), rng.gauss(0, 1)] for _ in range(N)]
        r = rng.uniform(0.2, 3.0)
        out = ensrf_analysis(ens, [0.7], lambda x: [x[0]], [r])
        xb, _ = ensemble_moments(ens)
        xa, _ = ensemble_moments(out)
        s = sum((x[0] - xb[0]) ** 2 for x in ens) / (N - 1)
        f = math.sqrt(r / (s + r))
        for x, z in zip(ens, out):
            assert abs((z[0] - xa[0]) - f * (x[0] - xb[0])) < 1e-12


def test_localization_weight_zero_freezes_value():
    rng = random.Random(34)
    N = 5
    ens = [[rng.gauss(0, 1) for _ in range(3)] for _ in range(N)]
    loc = [[1.0, 0.5, 0.0]]
    out = ensrf_analysis(ens, [2.0], lambda x: [x[0]], [0.5], loc_state=loc)
    for x, z in zip(ens, out):
        assert abs(z[2] - x[2]) < 1e-14
        assert abs(z[0] - x[0]) > 0
    # Weight 1 everywhere is the same as no localization.
    a = ensrf_analysis(ens, [2.0], lambda x: [x[0]], [0.5], loc_state=[[1.0, 1.0, 1.0]], loc_obs=[[1.0]])
    b = ensrf_analysis(ens, [2.0], lambda x: [x[0]], [0.5])
    assert a == b
