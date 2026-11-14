# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cox-partial-likelihood/. The authors are listed in prov/9HJDFT.jsonl.

import itertools
import math
import random
from fractions import Fraction

from cox_partial_likelihood import (
    TIES, fit, schoenfeld_residuals, score_information, score_test,
)

# Remission times in weeks of the leukemia trial of Freireich et al. (1963), as listed by Gehan (1965).
MP_T = [6, 6, 6, 6, 7, 9, 10, 10, 11, 13, 16, 17, 19, 20, 22, 23, 25, 32, 32, 34, 35]
MP_D = [1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0]
PL_T = [1, 1, 2, 2, 3, 4, 4, 5, 5, 8, 8, 8, 8, 11, 11, 12, 12, 15, 17, 22, 23]
GEHAN_T = MP_T + PL_T
GEHAN_D = MP_D + [1] * 21
GEHAN_X = [[0]] * 21 + [[1]] * 21  # x = 1 for placebo


def random_data(rng, n, p, tmax=6, censor=0.3):
    """Integer times (so ties occur), random censoring and covariates."""
    T = [rng.randint(1, tmax) for _ in range(n)]
    D = [0 if rng.random() < censor else 1 for _ in range(n)]
    X = [[round(rng.gauss(0, 1), 2) for _ in range(p)] for _ in range(n)]
    return T, D, X


def direct_loglik(T, D, X, beta, ties):
    """The log partial likelihood by direct summation over each risk set."""
    eta = [sum(a * b for a, b in zip(x, beta)) for x in X]
    ll = 0.0
    for t in sorted({y for y, e in zip(T, D) if e}):
        R = [i for i in range(len(T)) if T[i] >= t]
        Dset = [i for i in R if T[i] == t and D[i]]
        d = len(Dset)
        ll += sum(eta[i] for i in Dset)
        if ties == "breslow":
            ll -= d * math.log(sum(math.exp(eta[i]) for i in R))
        elif ties == "efron":
            sR = sum(math.exp(eta[i]) for i in R)
            sD = sum(math.exp(eta[i]) for i in Dset)
            ll -= sum(math.log(sR - r / d * sD) for r in range(d))
        else:  # exact: every subset of size d of the risk set could have been the d failures
            ll -= math.log(sum(math.exp(sum(eta[i] for i in s)) for s in itertools.combinations(R, d)))
    return ll


def test_loglik_matches_direct_summation():
    rng = random.Random(1)
    for _ in range(20):
        T, D, X = random_data(rng, 12, 2)
        beta = [rng.uniform(-1, 1), rng.uniform(-1, 1)]
        for ties in TIES:
            got = score_information(T, D, X, beta, ties).loglik
            assert abs(got - direct_loglik(T, D, X, beta, ties)) < 1e-9


def test_score_and_information_match_numerical_derivatives():
    rng = random.Random(2)
    h = 1e-5
    for _ in range(10):
        T, D, X = random_data(rng, 14, 2)
        beta = [rng.uniform(-1, 1), rng.uniform(-1, 1)]
        for ties in TIES:
            f = score_information(T, D, X, beta, ties)
            for a in range(2):
                up = list(beta); up[a] += h
                dn = list(beta); dn[a] -= h
                num = (direct_loglik(T, D, X, up, ties) - direct_loglik(T, D, X, dn, ties)) / (2 * h)
                assert abs(f.score[a] - num) < 1e-6
                su = score_information(T, D, X, up, ties).score
                sd = score_information(T, D, X, dn, ties).score
                for b in range(2):
                    # The information is minus the Hessian: minus the derivative of the score.
                    assert abs(f.information[b][a] + (su[b] - sd[b]) / (2 * h)) < 1e-6


def test_log_partial_likelihood_is_concave():
    rng = random.Random(3)
    for _ in range(10):
        T, D, X = random_data(rng, 15, 3)
        for ties in TIES:
            for _ in range(5):
                b = [rng.uniform(-2, 2) for _ in range(3)]
                v = [rng.gauss(0, 1) for _ in range(3)]
                f = score_information(T, D, X, b, ties)
                quad = sum(v[i] * f.information[i][j] * v[j] for i in range(3) for j in range(3))
                assert quad >= -1e-12  # the information is positive semidefinite
                g = lambda s: score_information(T, D, X, [bi + s * vi for bi, vi in zip(b, v)], ties).loglik
                assert g(0.3) + g(-0.3) - 2 * g(0.0) <= 1e-9


def test_newton_matches_a_fine_grid():
    rng = random.Random(4)
    for ties in TIES:
        T, D, X = random_data(rng, 20, 1)
        res = fit(T, D, X, ties)
        assert res.converged
        ll = lambda b: score_information(T, D, X, [b], ties).loglik
        grid = [k / 100 for k in range(-400, 401)]
        best = max(grid, key=ll)
        for step in (1e-4, 1e-6):  # refine around the best point twice
            best = max([best + k * step for k in range(-100, 101)], key=ll)
        assert abs(best - res.beta[0]) <= 2e-5
        assert ll(res.beta[0]) >= ll(best) - 1e-12


def log_rank(T, D, G):
    """Log-rank O - E for group 1 and the hypergeometric variance, in Fractions."""
    U = V = Fraction(0)
    for t in sorted({y for y, e in zip(T, D) if e}):
        n = sum(1 for y in T if y >= t)
        n1 = sum(1 for y, g in zip(T, G) if y >= t and g)
        d = sum(1 for y, e in zip(T, D) if y == t and e)
        d1 = sum(1 for y, e, g in zip(T, D, G) if y == t and e and g)
        U += d1 - Fraction(d * n1, n)
        if n > 1:
            V += Fraction(d * n1 * (n - n1) * (n - d), n * n * (n - 1))
    return U, V


def test_score_test_at_zero_is_the_log_rank_statistic_without_ties():
    rng = random.Random(5)
    for _ in range(30):
        n = rng.randint(4, 12)
        T = rng.sample(range(1, 40), n)  # distinct times, so no ties
        D = [rng.randint(0, 1) for _ in range(n)]
        if not any(D):
            D[0] = 1
        G = [rng.randint(0, 1) for _ in range(n)]
        if len(set(G)) < 2:
            G[0], G[1] = 0, 1
        U, V = log_rank(T, D, G)
        for ties in TIES:  # with no ties the three rules are the same function
            f = score_information(T, D, [[g] for g in G], [0], ties)
            assert f.score[0] == U and f.information[0][0] == V
            if V > 0:
                stat, df, _ = score_test(T, D, [[g] for g in G], [0], ties)
                assert stat == U * U / V and df == 1


def test_exact_ties_score_test_is_the_log_rank_with_hypergeometric_variance():
    rng = random.Random(6)
    for _ in range(30):
        T, D, _ = random_data(rng, 10, 1, tmax=4)
        if not any(D):
            D[0] = 1
        G = [rng.randint(0, 1) for _ in range(10)]
        U, V = log_rank(T, D, G)
        f = score_information(T, D, [[g] for g in G], [0], "exact")
        assert f.score[0] == U and f.information[0][0] == V
        # Breslow keeps the score but uses the binomial variance d n1 n0 / n^2.
        fb = score_information(T, D, [[g] for g in G], [0], "breslow")
        VB = Fraction(0)
        for t in sorted({y for y, e in zip(T, D) if e}):
            n = sum(1 for y in T if y >= t)
            n1 = sum(1 for y, g in zip(T, G) if y >= t and g)
            d = sum(1 for y, e in zip(T, D) if y == t and e)
            VB += Fraction(d * n1 * (n - n1), n * n)
        assert fb.score[0] == U and fb.information[0][0] == VB and VB >= V


def test_efron_score_and_information_at_zero_match_the_formula():
    rng = random.Random(7)
    for _ in range(20):
        T, D, _ = random_data(rng, 10, 1, tmax=4)
        X = [[rng.randint(-2, 2)] for _ in range(10)]
        f = score_information(T, D, X, [0], "efron")
        U = I = Fraction(0)
        for t in sorted({y for y, e in zip(T, D) if e}):
            R = [i for i in range(10) if T[i] >= t]
            Ds = [i for i in R if T[i] == t and D[i]]
            d = len(Ds)
            U += sum(X[i][0] for i in Ds)
            for r in range(d):
                c = Fraction(r, d)
                A0 = len(R) - c * len(Ds)
                A1 = sum(X[i][0] for i in R) - c * sum(X[i][0] for i in Ds)
                A2 = sum(X[i][0] ** 2 for i in R) - c * sum(X[i][0] ** 2 for i in Ds)
                U -= A1 / A0
                I += A2 / A0 - (A1 / A0) ** 2
        assert f.score[0] == U and f.information[0][0] == I


def test_schoenfeld_residuals_sum_to_the_score():
    rng = random.Random(8)
    for _ in range(10):
        T, D, _ = random_data(rng, 12, 1)
        X = [[rng.randint(0, 3), rng.randint(-1, 1)] for _ in range(12)]
        for ties in ("breslow", "efron"):
            res = schoenfeld_residuals(T, D, X, [0, 0], ties)
            f = score_information(T, D, X, [0, 0], ties)
            assert [sum(r[2][a] for r in res) for a in range(2)] == f.score  # exact at beta = 0
            bhat = fit(T, D, [[float(v) for v in x] for x in X], ties)
            if bhat.converged:
                res = schoenfeld_residuals(T, D, X, bhat.beta, ties)
                assert all(abs(sum(r[2][a] for r in res)) < 1e-8 for a in range(2))


def test_gehan_leukemia_data():
    want = {"breslow": (1.5092, 0.4096), "efron": (1.5721, 0.4124), "exact": (1.6282, 0.4331)}
    for ties, (b, se) in want.items():
        r = fit(GEHAN_T, GEHAN_D, GEHAN_X, ties)
        assert r.converged
        assert abs(r.beta[0] - b) < 1e-4 and abs(math.sqrt(r.covariance[0][0]) - se) < 1e-4
    stat, _, p = score_test(GEHAN_T, GEHAN_D, GEHAN_X, [0], "exact")
    U, V = log_rank(GEHAN_T, GEHAN_D, [x[0] for x in GEHAN_X])
    assert stat == U * U / V and abs(float(stat) - 16.793) < 1e-3 and p < 1e-4


def test_invariance_to_shift_and_scale_of_a_covariate():
    rng = random.Random(9)
    T, D, X = random_data(rng, 25, 2)
    r = fit(T, D, X, "efron")
    shifted = [[x[0] + 7.0, x[1] - 3.0] for x in X]
    scaled = [[2.0 * x[0], x[1]] for x in X]
    r1 = fit(T, D, shifted, "efron")
    r2 = fit(T, D, scaled, "efron")
    assert max(abs(a - b) for a, b in zip(r.beta, r1.beta)) < 1e-8
    assert abs(r2.beta[0] - r.beta[0] / 2) < 1e-8 and abs(r2.beta[1] - r.beta[1]) < 1e-8


def test_monotone_likelihood_does_not_converge():
    # Every event is in group 1 and group 1 is always in the risk set: the
    # partial likelihood increases in beta without bound.
    T = [1, 2, 3, 4, 5, 6, 7, 8]
    D = [1, 1, 1, 1, 0, 0, 0, 0]
    X = [[1], [1], [1], [1], [0], [0], [0], [0]]
    r = fit(T, D, X, "breslow", max_iter=30)
    assert not r.converged and r.beta[0] > 10


def test_score_test_size_by_simulation():
    # Under beta = 0 the score statistic is asymptotically chi-square(1).
    rng = random.Random(10)
    reps, rejections = 2000, 0
    for _ in range(reps):
        n = 40
        X = [[rng.randint(0, 1)] for _ in range(n)]
        T = [rng.expovariate(1.0) for _ in range(n)]
        C = [rng.expovariate(0.5) for _ in range(n)]
        Y = [min(a, b) for a, b in zip(T, C)]
        D = [1 if a <= b else 0 for a, b in zip(T, C)]
        if not any(D) or len({x[0] for x in X}) < 2:
            continue
        rejections += score_test(Y, D, X, [0], "breslow")[2] < 0.05
    rate = rejections / reps
    assert abs(rate - 0.05) < 4 * math.sqrt(0.05 * 0.95 / reps) + 0.01
