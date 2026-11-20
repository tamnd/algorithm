# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hybrid-ensemble-variational/. The authors are listed in prov/GBD29Q.jsonl.

import math
import random

import scimat
from hybrid_ensemble_variational import gaspari_cohn, hybrid_covariance, hybrid_envar, localization_matrix


def random_spd(rng, n, shift=0.5):
    L = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
    S = scimat.matmul(L, scimat.transpose(L))
    for i in range(n):
        S[i][i] += shift
    return S


def three_d_var(xb, B, y, H, R):
    """Reference: the 3D-Var minimizer x^b + B H^T (H B H^T + R)^-1 (y - H x^b), by elimination."""
    HB = scimat.matmul(H, B)
    S = scimat.add(scimat.matmul(HB, scimat.transpose(H)), R)
    w = scimat.solve(S, scimat.sub(y, scimat.matvec(H, xb)))
    return scimat.add(xb, scimat.matvec(scimat.transpose(HB), w))


def close(a, b, tol):
    return all(abs(u - v) <= tol * (1 + abs(v)) for u, v in zip(a, b))


def draw(rng, LB):
    return scimat.matvec(LB, [rng.gauss(0, 1) for _ in range(len(LB))])


def test_scalar_check_value():
    # B_c = 1, members -1 and 1 (variance 2), weights 1/2 each: B = 1.5 and x^a = 1.5 / 2.5.
    xa = hybrid_envar([0.0], [[-1.0], [1.0]], [[1.0]], [[1.0]], 0.5, 0.5, [1.0], [[1.0]], [[1.0]])
    assert abs(xa[0] - 0.6) < 1e-14


def test_gaspari_cohn_values():
    assert gaspari_cohn(0.0, 2.0) == 1.0
    assert abs(gaspari_cohn(2.0, 2.0) - 5.0 / 24.0) < 1e-15  # z = 1 from both pieces
    assert abs(gaspari_cohn(2.0 + 1e-9, 2.0) - 5.0 / 24.0) < 1e-8
    assert abs(gaspari_cohn(4.0, 2.0)) < 1e-14 and gaspari_cohn(5.0, 2.0) == 0.0


def test_equals_3dvar_with_hybrid_covariance():
    rng = random.Random(91)
    for _ in range(25):
        n = rng.randint(1, 6)
        N = rng.randint(2, 5)
        p = rng.randint(1, n + 1)
        Bc = random_spd(rng, n)
        ens = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(N)]
        L = localization_matrix([float(j) for j in range(n)], rng.uniform(0.5, 3.0))
        bc2 = rng.uniform(0.0, 1.0)
        be2 = rng.uniform(0.0, 1.0)
        H = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(p)]
        R = random_spd(rng, p)
        xb = [rng.uniform(-1, 1) for _ in range(n)]
        y = [rng.uniform(-2, 2) for _ in range(p)]
        xa = hybrid_envar(xb, ens, Bc, L, bc2, be2, y, H, R)
        ref = three_d_var(xb, hybrid_covariance(ens, Bc, L, bc2, be2), y, H, R)
        assert close(xa, ref, 1e-8)


def test_limits_static_and_pure_ensemble():
    rng = random.Random(92)
    n, N = 5, 3
    Bc = random_spd(rng, n)
    ens = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(N)]
    ones = [[1.0] * n for _ in range(n)]
    H = [[1.0 if j == 2 * i else 0.0 for j in range(n)] for i in range(3)]
    R = [[0.5 if i == j else 0.0 for j in range(3)] for i in range(3)]
    xb = [0.0] * n
    y = [1.0, -1.0, 0.5]
    assert close(hybrid_envar(xb, ens, Bc, ones, 1.0, 0.0, y, H, R), three_d_var(xb, Bc, y, H, R), 1e-10)
    xp = hybrid_covariance(ens, Bc, ones, 0.0, 1.0)  # the sample covariance X' X'^T
    xa = hybrid_envar(xb, ens, Bc, ones, 0.0, 1.0, y, H, R)
    assert close(xa, three_d_var(xb, xp, y, H, R), 1e-9)
    # Without localization the increment lies in the span of the N perturbations.
    mean = [sum(x[j] for x in ens) / N for j in range(n)]
    P = [[x[j] - mean[j] for j in range(n)] for x in ens[:2]]
    G = [[scimat.dot(a, b) for b in P] for a in P]
    c = scimat.solve(G, [scimat.dot(a, xa) for a in P])
    resid = scimat.sub(xa, [c[0] * P[0][j] + c[1] * P[1][j] for j in range(n)])
    assert scimat.norm2(resid) < 1e-9


def test_hybrid_beats_static_and_localized_ensemble_in_a_twin():
    # Each case has its own error variance profile (a bump at a random place), which the
    # ensemble of 5 members sees and the static B_c, with the mean variance, does not.
    n, N = 16, 5
    pos = [float(j) for j in range(n)]
    C = localization_matrix(pos, 3.0)
    Lloc = localization_matrix(pos, 4.0)
    ones = [[1.0] * n for _ in range(n)]
    H = [[1.0 if j == 2 * i else 0.0 for j in range(n)] for i in range(8)]
    R = [[0.25 if i == j else 0.0 for j in range(8)] for i in range(8)]
    err = {"static": 0.0, "ensemble": 0.0, "hybrid": 0.0}
    for seed in range(93, 133):
        rng = random.Random(seed)
        xb = [0.0] * n
        c0 = rng.uniform(0, n - 1)
        s = [0.05 + 4.0 * math.exp(-(((j - c0) / 2.0) ** 2)) for j in range(n)]
        Btrue = [[math.sqrt(s[a] * s[b]) * C[a][b] for b in range(n)] for a in range(n)]
        LB = scimat.cholesky(Btrue)
        Bc = scimat.scale(sum(s) / n, C)
        truth = draw(rng, LB)
        y = [v + rng.gauss(0, 0.5) for v in scimat.matvec(H, truth)]
        ens = [draw(rng, LB) for _ in range(N)]
        cases = {
            "static": hybrid_envar(xb, ens, Bc, ones, 1.0, 0.0, y, H, R),
            "ensemble": hybrid_envar(xb, ens, Bc, Lloc, 0.0, 1.0, y, H, R),
            "hybrid": hybrid_envar(xb, ens, Bc, Lloc, 0.25, 0.75, y, H, R),
        }
        for key, xa in cases.items():
            err[key] += sum((a - t) ** 2 for a, t in zip(xa, truth)) / n
    assert err["hybrid"] < err["ensemble"] < err["static"]
