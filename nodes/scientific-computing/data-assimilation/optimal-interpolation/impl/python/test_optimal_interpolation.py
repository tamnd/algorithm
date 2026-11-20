# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optimal-interpolation/. The authors are listed in prov/BG2VYK.jsonl.

import math
import random
from fractions import Fraction as Fr

import scimat
from optimal_interpolation import (
    ar1_covariance,
    gaussian_covariance,
    interpolation_operator,
    oi_analysis,
    radius_selector,
)


def information_form(xb, B, yo, H, R):
    """Oracle: x^a = (B^-1 + H^T R^-1 H)^-1 (B^-1 x^b + H^T R^-1 y^o) and P^a."""
    Bi = scimat.inv(B)
    Ri = scimat.inv(R)
    Ht = scimat.transpose(H)
    A = scimat.add(Bi, scimat.matmul(scimat.matmul(Ht, Ri), H))
    rhs = scimat.add(scimat.matvec(Bi, xb), scimat.matvec(scimat.matmul(Ht, Ri), yo))
    return scimat.solve(A, rhs), scimat.inv(A)


def random_spd(rng, n, exact):
    L = [[Fr(rng.randint(-3, 3), rng.randint(1, 3)) for _ in range(n)] for _ in range(n)]
    S = scimat.add(scimat.matmul(L, scimat.transpose(L)), scimat.eye(n))
    if exact:
        return S
    return [[float(v) for v in row] for row in S]


def test_scalar_check_value():
    xa, va = oi_analysis([Fr(0)], [[Fr(1)]], [Fr(1)], [[Fr(1)]], [[Fr(1)]])
    assert xa == [Fr(1, 2)]
    assert va == [Fr(1, 2)]


def test_two_point_spreading():
    B = [[Fr(1), Fr(1, 2)], [Fr(1, 2), Fr(1)]]
    xa, va = oi_analysis([Fr(10), Fr(12)], B, [Fr(11)], [[1, 0]], [[Fr(1)]])
    assert xa == [Fr(21, 2), Fr(49, 4)]
    assert va == [Fr(1, 2), Fr(7, 8)]


def page_problem():
    n = 6
    B = ar1_covariance(n, Fr(1), Fr(1, 2))
    H = [[1 if j == q else 0 for j in range(n)] for q in (1, 4)]
    R = [[Fr(1, 4), 0], [0, Fr(1, 4)]]
    xb = [Fr(v) for v in (2, 3, 4, 4, 3, 2)]
    yo = [Fr(4), Fr(2)]
    return xb, B, yo, H, R


def test_page_example_global_and_local():
    xb, B, yo, H, R = page_problem()
    xa, va = oi_analysis(xb, B, yo, H, R)
    assert xa == [Fr(43, 18), Fr(34, 9), Fr(38, 9), Fr(34, 9), Fr(20, 9), Fr(29, 18)]
    assert va == [Fr(1267, 1584), Fr(79, 396), Fr(76, 99), Fr(76, 99), Fr(79, 396), Fr(1267, 1584)]
    sel = radius_selector(list(range(6)), [1, 4], Fr(3, 2))
    xl, vl = oi_analysis(xb, B, yo, H, R, sel)
    assert xl == [Fr(12, 5), Fr(19, 5), Fr(22, 5), Fr(18, 5), Fr(11, 5), Fr(8, 5)]
    assert vl == [Fr(4, 5), Fr(1, 5), Fr(4, 5), Fr(4, 5), Fr(1, 5), Fr(4, 5)]
    for i in range(6):
        assert vl[i] >= va[i]


def test_global_equals_information_form_exact():
    rng = random.Random(11)
    for _ in range(40):
        n, p = rng.randint(1, 4), rng.randint(1, 3)
        B = random_spd(rng, n, True)
        R = random_spd(rng, p, True)
        H = [[Fr(rng.randint(-2, 2)) for _ in range(n)] for _ in range(p)]
        xb = [Fr(rng.randint(-5, 5)) for _ in range(n)]
        yo = [Fr(rng.randint(-5, 5)) for _ in range(p)]
        xa, va = oi_analysis(xb, B, yo, H, R)
        xo, Po = information_form(xb, B, yo, H, R)
        assert xa == xo
        assert va == [Po[i][i] for i in range(n)]


def test_global_equals_information_form_float_many():
    rng = random.Random(12)
    for _ in range(500):
        n, p = rng.randint(1, 5), rng.randint(1, 4)
        B = random_spd(rng, n, False)
        R = random_spd(rng, p, False)
        H = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(p)]
        xb = [rng.uniform(-3, 3) for _ in range(n)]
        yo = [rng.uniform(-3, 3) for _ in range(p)]
        xa, va = oi_analysis(xb, B, yo, H, R)
        xo, Po = information_form(xb, B, yo, H, R)
        for i in range(n):
            assert abs(xa[i] - xo[i]) <= 1e-10 * (1 + abs(xo[i]))
            assert abs(va[i] - Po[i][i]) <= 1e-10 * (1 + abs(Po[i][i]))
            assert -1e-12 <= va[i] <= B[i][i] + 1e-12


def test_unselected_observations_have_no_effect():
    rng = random.Random(13)
    n = 12
    pos = list(range(n))
    obs = [0.5, 2.25, 4.0, 6.75, 9.5, 11.0]
    B = gaussian_covariance(pos, 1.0, 1.5)
    H = interpolation_operator(obs, n, 1.0, period=False)
    R = [[0.25 if i == j else 0.0 for j in range(len(obs))] for i in range(len(obs))]
    xb = [rng.uniform(-1, 1) for _ in range(n)]
    yo = [rng.uniform(-1, 1) for _ in range(len(obs))]
    sel = radius_selector(pos, obs, 2.0)
    xa, _ = oi_analysis(xb, B, yo, H, R, sel)
    for k in range(len(obs)):
        y2 = list(yo)
        y2[k] += 10.0
        xa2, _ = oi_analysis(xb, B, y2, H, R, sel)
        for i in range(n):
            if k in sel(i):
                assert abs(xa2[i] - xa[i]) > 1e-6
            else:
                assert xa2[i] == xa[i]


def test_local_equals_global_when_influence_is_local():
    # Diagonal B and observations at grid points: each point only feels its own observation.
    n = 5
    B = [[Fr(i + 1) if i == j else Fr(0) for j in range(n)] for i in range(n)]
    obs = [0, 2, 3]
    H = [[1 if j == q else 0 for j in range(n)] for q in obs]
    R = [[Fr(1, 2) if i == j else 0 for j in range(3)] for i in range(3)]
    xb = [Fr(1)] * n
    yo = [Fr(3), Fr(-1), Fr(2)]
    g = oi_analysis(xb, B, yo, H, R)
    loc = oi_analysis(xb, B, yo, H, R, radius_selector(list(range(n)), obs, 0))
    assert g == loc


def test_max_obs_limits_selection():
    sel = radius_selector([0.0, 5.0], [0.1, 0.2, 0.9, 4.0, 9.0], 10.0, max_obs=2)
    assert sel(0) == [0, 1]
    assert sel(1) == [3, 4]  # distances 1.0 and 4.0 beat 4.1
    per = radius_selector([0.0], [9.5, 3.0], 1.0, period=10.0)
    assert per(0) == [0]


def test_analysis_variance_by_sampling():
    # The error of the analysis has variance var_a when B and R are the true covariances.
    rng = random.Random(14)
    B = [[1.0, 0.6, 0.2], [0.6, 1.0, 0.6], [0.2, 0.6, 1.0]]
    H = [[0.5, 0.5, 0.0], [0.0, 0.0, 1.0]]
    R = [[0.5, 0.0], [0.0, 0.25]]
    LB = scimat.cholesky(B)
    xt = [0.0, 0.0, 0.0]
    N = 6000
    sq = [0.0, 0.0, 0.0]
    va = None
    for _ in range(N):
        z = [rng.gauss(0, 1) for _ in range(3)]
        xb = [sum(LB[i][k] * z[k] for k in range(3)) for i in range(3)]
        yo = [0.0 + math.sqrt(R[0][0]) * rng.gauss(0, 1), 0.0 + math.sqrt(R[1][1]) * rng.gauss(0, 1)]
        xa, va = oi_analysis(xb, B, yo, H, R)
        for i in range(3):
            sq[i] += (xa[i] - xt[i]) ** 2
    for i in range(3):
        est = sq[i] / N
        se = va[i] * math.sqrt(2.0 / N)
        assert abs(est - va[i]) < 4 * se


def test_interpolation_operator_reproduces_linear_functions():
    n, dx = 8, 0.5
    obs = [0.0, 0.3, 1.25, 3.5]
    H = interpolation_operator(obs, n, dx, period=False)
    grid = [2.0 + 3.0 * j * dx for j in range(n)]
    vals = scimat.matvec(H, grid)
    for q, v in zip(obs, vals):
        assert abs(v - (2.0 + 3.0 * q)) < 1e-12
    for row in interpolation_operator([3.9, 0.2], n, dx):
        assert abs(sum(row) - 1.0) < 1e-12


def test_no_observations_keeps_background():
    xb, B, yo, H, R = page_problem()
    xa, va = oi_analysis(xb, B, yo, H, R, lambda i: [])
    assert xa == xb
    assert va == [B[i][i] for i in range(6)]
