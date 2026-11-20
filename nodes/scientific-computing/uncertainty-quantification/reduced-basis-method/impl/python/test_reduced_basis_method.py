# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reduced-basis-method/. The authors are listed in prov/YM1D2Z.jsonl.
import math
import random

import pytest

from reduced_basis_method import alpha_lb, assemble, fe_model, offline, online, truth_solve, x_dot
from scimat import matvec, solve

N = 99
MU_BAR = 10.0
AQ, F = fe_model(N)
X = [[AQ[0][i][j] + MU_BAR * AQ[1][i][j] for j in range(N)] for i in range(N)]


def x_norm(v):
    return math.sqrt(x_dot(X, v, v))


def test_truth_matches_the_exact_solution():
    mu = 10.0
    u = truth_solve(AQ, F, mu)
    exact_mid = (1.0 - 1.0 / math.cosh(math.sqrt(mu) / 2.0)) / mu
    assert u[N // 2] == pytest.approx(exact_mid, abs=1e-5)


def test_min_theta_bound_by_hand():
    assert alpha_lb(3.0, 10.0) == pytest.approx(0.3)
    assert alpha_lb(30.0, 10.0) == 1.0
    rng = random.Random(3)
    for _ in range(20):  # a(v, v; mu) >= alpha_lb ||v||_X^2 for random v
        mu = rng.uniform(1.0, 100.0)
        v = [rng.gauss(0, 1) for _ in range(N)]
        a = assemble(AQ, mu)
        assert sum(vi * avi for vi, avi in zip(v, matvec(a, v))) >= alpha_lb(mu, MU_BAR) * x_dot(X, v, v) * (1 - 1e-12)


def test_reproduces_the_snapshots():
    rb = offline(AQ, F, X, [1.0, 10.0, 100.0])
    for mu in (1.0, 10.0, 100.0):
        ur, delta, s_r, ds = online(rb, mu, MU_BAR)
        u = truth_solve(AQ, F, mu)
        assert x_norm([a - b for a, b in zip(u, ur)]) < 1e-12
        assert delta < 1e-6  # rounding in the offline-online sum sets a floor near sqrt(eps)


def test_example_values():
    rb = offline(AQ, F, X, [1.0, 10.0, 100.0])
    ur, delta, s_r, ds = online(rb, 3.0, MU_BAR)
    u = truth_solve(AQ, F, 3.0)
    err = x_norm([a - b for a, b in zip(u, ur)])
    assert err == pytest.approx(1.1838e-05, rel=1e-3)
    assert delta == pytest.approx(3.8780e-05, rel=1e-3)
    assert delta / err <= 1.0 / 0.3


def test_bound_and_effectivity_on_random_parameters():
    rng = random.Random(11)
    for samples in ([1.0, 100.0], [1.0, 10.0, 100.0], [1.0, 4.0, 20.0, 100.0]):
        rb = offline(AQ, F, X, samples)
        for _ in range(6):
            mu = math.exp(rng.uniform(0.0, math.log(100.0)))
            ur, delta, s_r, ds = online(rb, mu, MU_BAR)
            u = truth_solve(AQ, F, mu)
            e = [a - b for a, b in zip(u, ur)]
            err = x_norm(e)
            assert err <= delta * (1 + 1e-9) + 1e-12
            gamma = max(1.0, mu / MU_BAR)
            if err > 1e-7:
                assert delta <= gamma / alpha_lb(mu, MU_BAR) * err * (1 + 1e-6)
            # the online residual norm equals the direct one, sqrt(R^T X^-1 R)
            a = assemble(AQ, mu)
            res = [fi - ai for fi, ai in zip(F, matvec(a, ur))]
            direct = math.sqrt(max(sum(ri * yi for ri, yi in zip(res, solve(X, res))), 0.0))
            assert delta * alpha_lb(mu, MU_BAR) == pytest.approx(direct, rel=1e-5, abs=1e-8)
            # compliance output: 0 <= s - s_r <= Delta_s
            s = sum(fi * ui for fi, ui in zip(F, u))
            assert -1e-14 <= s - s_r <= ds * (1 + 1e-6) + 1e-14


def test_error_falls_as_the_basis_grows():
    errs = []
    for samples in ([1.0, 100.0], [1.0, 10.0, 100.0], [1.0, 4.0, 20.0, 100.0]):
        rb = offline(AQ, F, X, samples)
        ur, delta, s_r, ds = online(rb, 30.0, MU_BAR)
        errs.append(x_norm([a - b for a, b in zip(truth_solve(AQ, F, 30.0), ur)]))
    assert errs[0] > 10 * errs[1] > 100 * errs[2]


def test_repeated_parameter_is_rejected():
    with pytest.raises(ValueError):
        offline(AQ, F, X, [2.0, 2.0])
