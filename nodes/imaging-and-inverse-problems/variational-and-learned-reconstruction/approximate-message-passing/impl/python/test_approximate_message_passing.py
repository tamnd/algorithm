# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/approximate-message-passing/. The authors are listed in prov/SKJZMH.jsonl.

import math
import random

from approximate_message_passing import amp, mse_soft, soft, state_evolution


def gauss_matrix(rng, m, n):
    return [[rng.gauss(0.0, 1.0) / math.sqrt(m) for _ in range(n)] for _ in range(m)]


def matvec(a, x):
    return [sum(p * q for p, q in zip(row, x)) for row in a]


def lasso_cd(a, y, lam, sweeps=3000):
    """Reference LASSO solver: cyclic coordinate descent on 1/2 ||y - A x||^2 + lam ||x||_1."""
    m, n = len(a), len(a[0])
    cols = [[a[i][j] for i in range(m)] for j in range(n)]
    sq = [sum(v * v for v in c) for c in cols]
    x = [0.0] * n
    r = list(y)
    for _ in range(sweeps):
        change = 0.0
        for j in range(n):
            c = cols[j]
            rho = sum(ci * ri for ci, ri in zip(c, r)) + sq[j] * x[j]
            new = soft(rho, lam) / sq[j]
            d = new - x[j]
            if d != 0.0:
                r = [ri - d * ci for ri, ci in zip(r, c)]
                x[j] = new
                change = max(change, abs(d))
        if change < 1e-14:
            break
    return x


def test_soft_threshold():
    assert soft(3.0, 1.0) == 2.0
    assert soft(-3.0, 1.0) == -2.0
    assert soft(0.5, 1.0) == 0.0


def test_mse_of_soft_threshold_matches_closed_form_at_zero():
    # For X = 0: E[eta(tau Z; theta)^2] = 2 [(tau^2 + theta^2) Q(c) - tau theta phi(c)], c = theta / tau.
    tau, theta = 0.7, 1.1
    c = theta / tau
    q = 0.5 * math.erfc(c / math.sqrt(2.0))
    phi = math.exp(-0.5 * c * c) / math.sqrt(2.0 * math.pi)
    exact = 2.0 * ((tau * tau + theta * theta) * q - tau * theta * phi)
    # Simpson's rule loses accuracy at the two kinks of eta, so the tolerance is 1e-6.
    assert abs(mse_soft([(0.0, 1.0)], tau, theta) - exact) <= 1e-6


def test_fixed_point_solves_the_lasso():
    # At a fixed point with k = ||x||_0 < m, x solves the LASSO with
    # lambda = theta (1 - k/m). Check the KKT conditions and compare with
    # an independent coordinate descent solver.
    for seed in range(3):
        rng = random.Random(seed)
        m, n = 32, 64
        a = gauss_matrix(rng, m, n)
        x0 = [rng.gauss(0.0, 1.0) if rng.random() < 0.15 else 0.0 for _ in range(n)]
        y = [v + rng.gauss(0.0, 0.05) for v in matvec(a, x0)]
        x, z, hist = amp(a, y, alpha=2.0, iters=1000, tol=1e-13)
        assert len(hist) < 1001
        theta = 2.0 * hist[-2][1]
        k = sum(1 for v in x if v != 0.0)
        assert k < m
        lam = theta * (1.0 - k / m)
        r = [yi - v for yi, v in zip(y, matvec(a, x))]
        g = [sum(a[i][j] * r[i] for i in range(m)) for j in range(n)]
        for j in range(n):
            if x[j] != 0.0:
                assert abs(g[j] - lam * math.copysign(1.0, x[j])) <= 1e-9
            else:
                assert abs(g[j]) <= lam + 1e-9
        ref = lasso_cd(a, y, lam)
        assert math.sqrt(sum((p - q) ** 2 for p, q in zip(x, ref))) <= 1e-7


def test_noiseless_recovery_below_the_phase_transition():
    for seed in range(3):
        rng = random.Random(20 + seed)
        m, n, s = 64, 128, 6
        a = gauss_matrix(rng, m, n)
        x0 = [0.0] * n
        for i in rng.sample(range(n), s):
            x0[i] = rng.choice([-1.0, 1.0])
        x, _, _ = amp(a, matvec(a, x0), alpha=1.5, iters=200, tol=1e-13)
        assert math.sqrt(sum((p - q) ** 2 for p, q in zip(x, x0))) <= 1e-8


def test_state_evolution_predicts_the_mse_and_the_onsager_term_matters():
    # Prior: 0 with probability 0.9, +1 or -1 with probability 0.05 each.
    # delta = m/n = 1/2, no noise, alpha = 1.5. The prediction is for the
    # large system limit; at n = 400 the agreement is within about 25 percent.
    eps, alpha, n, m, steps = 0.1, 1.5, 400, 200, 6
    prior = [(0.0, 1.0 - eps), (1.0, eps / 2.0), (-1.0, eps / 2.0)]
    _, se = state_evolution(prior, m / n, 0.0, alpha, steps)
    with_term = [0.0] * steps
    without = [0.0] * steps
    trials = 2
    for tr in range(trials):
        rng = random.Random(10 + tr)
        a = gauss_matrix(rng, m, n)
        x0 = [rng.choice([1.0, -1.0]) if rng.random() < eps else 0.0 for _ in range(n)]
        y = matvec(a, x0)
        for ons, acc in ((True, with_term), (False, without)):
            _, _, hist = amp(a, y, alpha=alpha, iters=steps, onsager=ons)
            for t in range(steps):
                xt = hist[t + 1][0]
                acc[t] += sum((p - q) ** 2 for p, q in zip(xt, x0)) / n / trials
    for t in range(steps):
        assert abs(with_term[t] - se[t]) <= 0.3 * se[t]
    # State evolution decreases; without the Onsager term the error does not follow it.
    assert all(se[t + 1] < se[t] for t in range(steps - 1))
    assert without[-1] > 3.0 * se[-1]
