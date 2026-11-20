# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lmmse-channel-estimation/. The authors are listed in prov/5PBE09.jsonl.

import random

import pytest

import cbb
from lmmse_channel_estimation import error_covariance, lmmse_estimate, lmmse_matrix, lmmse_mse, training_matrix


def close(a, b, tol=1e-9):
    if a and isinstance(a[0], list):
        return len(a) == len(b) and all(close(r, s, tol) for r, s in zip(a, b))
    return len(a) == len(b) and all(abs(p - q) <= tol for p, q in zip(a, b))


def trace(a):
    return sum(a[i][i] for i in range(len(a))).real


def random_covariance(rng, n, rank=None):
    """R = C C^H for a random n by rank matrix C, so R is Hermitian, positive semidefinite."""
    c = [[cbb.cn(rng, 1.0) for _ in range(rank or n)] for _ in range(n)]
    return cbb.matmul(c, cbb.herm(c))


def textbook_matrix(xm, r_h, n0):
    """The other form W = R_h X^H (X R_h X^H + N0 I)^(-1), with an m by m inverse."""
    xh = cbb.herm(xm)
    k = cbb.add(cbb.matmul(cbb.matmul(xm, r_h), xh), cbb.scale(n0, cbb.eye(len(xm))))
    return cbb.matmul(cbb.matmul(r_h, xh), cbb.inv(k))


def linear_mse(w, xm, r_h, n0):
    """E||W v - h||^2 for v = X h + w: tr(W K W^H) - 2 Re tr(W X R_h) + tr(R_h), K = X R_h X^H + N0 I."""
    k = cbb.add(cbb.matmul(cbb.matmul(xm, r_h), cbb.herm(xm)), cbb.scale(n0, cbb.eye(len(xm))))
    t1 = trace(cbb.matmul(cbb.matmul(w, k), cbb.herm(w)))
    t2 = trace(cbb.matmul(cbb.matmul(w, xm), r_h))
    return t1 - 2 * t2 + trace(r_h)


def test_example_on_the_page() -> None:
    x = [1, 1, -1, 1, 1]
    r_h = [[0.8, 0], [0, 0.2]]
    y = [1.3, 1.6, -0.7, 0.55, 1.6]  # the LS page example; y[0] is not used
    assert close(lmmse_estimate(x, y, 2, r_h, 0.5), [3.2 / 3.7 * 1.1125, 0.8 / 1.3 * 0.4875])
    assert close(lmmse_estimate(x, y, 2, r_h, 0.5), [0.9621621621621622, 0.3])
    c = error_covariance(x, 2, r_h, 0.5)
    assert close(c, [[0.4 / 3.7, 0], [0, 0.1 / 1.3]])
    assert abs(lmmse_mse(x, 2, r_h, 0.5) - 0.18503118503118504) < 1e-12
    assert lmmse_mse(x, 2, r_h, 0.5) < 0.5 / 2  # the LS error N0 tr((X^H X)^(-1)) = 0.25


def test_the_two_forms_agree() -> None:
    rng = random.Random(5201)
    for _ in range(60):
        taps = rng.randint(1, 4)
        x = [cbb.cn(rng, 1.0) for _ in range(taps + rng.randint(0, 6))]
        r_h = random_covariance(rng, taps, rng.randint(1, taps))  # may be singular
        n0 = rng.uniform(0.05, 2.0)
        xm = training_matrix(x, taps)
        assert close(lmmse_matrix(x, taps, r_h, n0), textbook_matrix(xm, r_h, n0), 1e-8)
        y = [cbb.cn(rng, 1.0) for _ in x]
        assert close(lmmse_estimate(x, y, taps, r_h, n0), cbb.matvec(lmmse_matrix(x, taps, r_h, n0), y[taps - 1 :]), 1e-9)


def test_orthogonality_and_minimum_over_all_linear_estimators() -> None:
    rng = random.Random(5202)
    for _ in range(60):
        taps = rng.randint(1, 4)
        x = [cbb.cn(rng, 1.0) for _ in range(taps + rng.randint(0, 5))]
        r_h = random_covariance(rng, taps)
        n0 = rng.uniform(0.05, 2.0)
        xm = training_matrix(x, taps)
        w = lmmse_matrix(x, taps, r_h, n0)
        # orthogonality: E[(W v - h) v^H] = W K - R_h X^H = 0
        k = cbb.add(cbb.matmul(cbb.matmul(xm, r_h), cbb.herm(xm)), cbb.scale(n0, cbb.eye(len(xm))))
        assert close(cbb.matmul(w, k), cbb.matmul(r_h, cbb.herm(xm)), 1e-8)
        best = linear_mse(w, xm, r_h, n0)
        assert abs(best - lmmse_mse(x, taps, r_h, n0)) < 1e-9
        for _ in range(5):
            other = [[a + cbb.cn(rng, 0.05) for a in row] for row in w]
            assert linear_mse(other, xm, r_h, n0) >= best - 1e-12
        rand_w = [[cbb.cn(rng, 1.0) for _ in range(len(xm))] for _ in range(taps)]
        assert linear_mse(rand_w, xm, r_h, n0) >= best


def test_monte_carlo_mse_matches_the_closed_form() -> None:
    rng = random.Random(5203)
    taps, n0, runs = 3, 0.3, 4000
    x = [complex(rng.choice((-1, 1)), rng.choice((-1, 1))) / 2**0.5 for _ in range(8)]
    pdp = [0.6, 0.3, 0.1]  # exponential-like power delay profile with correlated taps
    r_h = [[0.5 ** abs(i - k) * (pdp[i] * pdp[k]) ** 0.5 for k in range(taps)] for i in range(taps)]
    chol = cbb.cholesky(r_h)
    xm = training_matrix(x, taps)
    w = lmmse_matrix(x, taps, r_h, n0)
    sq, mean = 0.0, [0j] * taps
    for _ in range(runs):
        h = cbb.matvec(chol, [cbb.cn(rng, 1.0) for _ in range(taps)])
        v = cbb.awgn(rng, cbb.matvec(xm, h), n0)
        e = cbb.sub(cbb.matvec(w, v), h)
        sq += cbb.norm2(e) / runs
        mean = [a + b / runs for a, b in zip(mean, e)]
    want = lmmse_mse(x, taps, r_h, n0)
    assert abs(sq - want) < 0.08 * want  # 4000 runs, seed 5203
    assert max(abs(a) for a in mean) < 0.03


def test_lmmse_beats_ls_and_tends_to_ls() -> None:
    rng = random.Random(5204)
    for _ in range(60):
        taps = rng.randint(1, 4)
        x = [cbb.cn(rng, 1.0) for _ in range(2 * taps - 1 + rng.randint(1, 5))]
        r_h = random_covariance(rng, taps)
        n0 = rng.uniform(0.05, 2.0)
        xm = training_matrix(x, taps)
        g = cbb.matmul(cbb.herm(xm), xm)
        ls_mse = n0 * trace(cbb.inv(g))
        assert lmmse_mse(x, taps, r_h, n0) <= ls_mse + 1e-12
        y = [cbb.cn(rng, 1.0) for _ in x]
        ls = cbb.solve(g, cbb.matvec(cbb.herm(xm), y[taps - 1 :]))
        assert close(lmmse_estimate(x, y, taps, r_h, 1e-10), ls, 1e-6)


def test_noiseless_data_and_a_known_zero_tap() -> None:
    x = [1, 1, -1, 1, 1, -1, -1]
    h = [0.9 - 0.2j, 0, 0.3j]
    y = cbb.conv(x, h)[: len(x)]
    r_h = [[1, 0, 0], [0, 0, 0], [0, 0, 0.5]]  # singular: the middle tap is known to be zero
    got = lmmse_estimate(x, y, 3, r_h, 1e-12)
    assert close(got, h, 1e-9)
    assert got[1] == 0


def test_errors() -> None:
    with pytest.raises(ValueError):
        lmmse_estimate([1, 1], [1, 1], 2, [[1, 0], [0, 1]], 0.0)
    with pytest.raises(ValueError):
        lmmse_estimate([1, 1], [1, 1], 2, [[1]], 0.1)
    with pytest.raises(ValueError):
        lmmse_estimate([1], [1], 2, [[1, 0], [0, 1]], 0.1)
