# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ensemble-transform-kalman-filter/. The authors are listed in prov/5GQ96N.jsonl.

import math
import random

import scimat
from ensemble_transform_kalman_filter import ensemble_moments, etkf_analysis, etkf_transform, sym_eig


def kalman_moments(ens, yo, H, R, rho=1.0):
    """Oracle: the Kalman analysis mean and covariance for the inflated sample covariance."""
    n = len(ens[0])
    xbar, Pf = ensemble_moments(ens)
    P = scimat.scale(rho, Pf)
    PHt = scimat.matmul(P, scimat.transpose(H))
    S = scimat.add(scimat.matmul(H, PHt), R)
    K = scimat.transpose(scimat.solve(S, scimat.transpose(PHt)))
    xa = scimat.add(xbar, scimat.matvec(K, scimat.sub(yo, scimat.matvec(H, xbar))))
    Pa = scimat.matmul(scimat.sub(scimat.eye(n), scimat.matmul(K, H)), P)
    return xa, Pa


def random_spd(rng, n):
    L = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
    return scimat.add(scimat.matmul(L, scimat.transpose(L)), scimat.scale(0.5, scimat.eye(n)))


def test_scalar_check_value():
    s = 1 / math.sqrt(2.0)
    out = etkf_analysis([[-s], [s]], [1.0], lambda x: [x[0]], [[1.0]])
    mean, P = ensemble_moments(out)
    assert abs(mean[0] - 0.5) < 1e-12
    assert abs(P[0][0] - 0.5) < 1e-12


def test_page_example():
    out = etkf_analysis([[-1.0], [1.0]], [1.0], lambda x: [x[0]], [[1.0]])
    assert abs(out[0][0] - (2 / 3 - 1 / math.sqrt(3))) < 1e-12
    assert abs(out[1][0] - (2 / 3 + 1 / math.sqrt(3))) < 1e-12
    wbar, W = etkf_transform([[-1.0, 1.0]], [[1.0]], [1.0])
    assert abs(wbar[0] + 1 / 3) < 1e-12 and abs(wbar[1] - 1 / 3) < 1e-12
    a, b = (1 + 1 / math.sqrt(3)) / 2, (1 - 1 / math.sqrt(3)) / 2
    for i, j, v in ((0, 0, a), (0, 1, b), (1, 0, b), (1, 1, a)):
        assert abs(W[i][j] - v) < 1e-12


def test_cholesky_square_root_moves_the_mean():
    # The pitfall of the page: a triangular square root of P~ does not keep the mean.
    Pt = [[2 / 3, 1 / 3], [1 / 3, 2 / 3]]
    L = scimat.cholesky(Pt)
    X = [-1.0, 1.0]
    members = [2 / 3 + sum(X[k] * L[k][i] for k in range(2)) for i in range(2)]
    mean = sum(members) / 2
    assert abs(mean - (2 / 3 + (1 / math.sqrt(2) - 1 / math.sqrt(6)) / 2)) < 1e-12
    assert mean - 2 / 3 > 0.14


def test_matches_kalman_moments():
    rng = random.Random(21)
    for _ in range(60):
        n, p, N = rng.randint(1, 5), rng.randint(1, 4), rng.randint(2, 7)
        ens = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(N)]
        H = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(p)]
        R = random_spd(rng, p)
        yo = [rng.gauss(0, 2) for _ in range(p)]
        rho = rng.choice([1.0, 1.1, 1.5])
        out = etkf_analysis(ens, yo, lambda x: scimat.matvec(H, x), R, rho)
        ma, Pe = ensemble_moments(out)
        xa, Pa = kalman_moments(ens, yo, H, R, rho)
        for a in range(n):
            assert abs(ma[a] - xa[a]) < 1e-9 * (1 + abs(xa[a]))
            for b in range(n):
                assert abs(Pe[a][b] - Pa[a][b]) < 1e-9 * (1 + abs(Pa[a][b]))


def test_transform_is_symmetric_and_keeps_ones():
    rng = random.Random(22)
    for _ in range(30):
        p, N = rng.randint(1, 5), rng.randint(2, 8)
        Y = [[rng.gauss(0, 1) for _ in range(N)] for _ in range(p)]
        Y = [[v - sum(row) / N for v in row] for row in Y]
        rho = rng.choice([1.0, 1.21])
        wbar, W = etkf_transform(Y, random_spd(rng, p), [rng.gauss(0, 1) for _ in range(p)], rho)
        for a in range(N):
            assert abs(sum(W[a]) - math.sqrt(rho)) < 1e-10
            for b in range(N):
                assert abs(W[a][b] - W[b][a]) < 1e-12
        assert abs(sum(wbar)) < 1e-10  # wbar is orthogonal to the ones vector


def test_analysis_stays_in_ensemble_span():
    # n = 6 and N = 3: the analysis members lie in xbar + span of the forecast perturbations.
    rng = random.Random(23)
    n, N = 6, 3
    ens = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(N)]
    H = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(4)]
    out = etkf_analysis(ens, [1.0, 0.0, -1.0, 2.0], lambda x: scimat.matvec(H, x), scimat.eye(4))
    xbar, _ = ensemble_moments(ens)
    D = [[ens[i][j] - xbar[j] for j in range(n)] for i in range(2)]  # two perturbations span the space
    G = scimat.matmul(D, scimat.transpose(D))
    for x in out:
        z = scimat.sub(x, xbar)
        c = scimat.solve(G, scimat.matvec(D, z))
        resid = scimat.sub(z, scimat.matvec(scimat.transpose(D), c))
        assert scimat.norm2(resid) < 1e-10


def test_nonlinear_operator_runs_and_reduces_spread():
    rng = random.Random(24)
    n, N = 3, 10
    ens = [[1.0 + rng.gauss(0, 1) for _ in range(n)] for _ in range(N)]
    h = lambda x: [x[0] ** 2, x[1] + x[2] ** 3 / 10]
    out = etkf_analysis(ens, [1.5, 1.0], h, [[0.1, 0.0], [0.0, 0.1]])
    _, Pf = ensemble_moments(ens)
    _, Pa = ensemble_moments(out)
    assert sum(Pa[j][j] for j in range(n)) < sum(Pf[j][j] for j in range(n))


def test_sym_eig_reconstructs():
    rng = random.Random(25)
    for n in (1, 3, 7):
        A = random_spd(rng, n)
        vals, V = sym_eig(A)
        for i in range(n):
            for j in range(n):
                assert abs(sum(V[i][m] * vals[m] * V[j][m] for m in range(n)) - A[i][j]) < 1e-12
