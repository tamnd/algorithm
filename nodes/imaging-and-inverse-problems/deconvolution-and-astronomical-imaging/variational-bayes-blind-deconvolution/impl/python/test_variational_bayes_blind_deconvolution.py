# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/variational-bayes-blind-deconvolution/. The authors are listed in prov/JZ0W9B.jsonl.

import math
import random

from imgla import cholesky, cho_solve, matmul, transpose
from variational_bayes_blind_deconvolution import (
    conv,
    embed,
    free_energy,
    gradient,
    kernel_matrix,
    kernel_quadratic,
    second_moments,
    simplex_qp,
    update_q_g,
    update_q_z,
    vb_blind,
)

SUPPORT = [-2, -1, 0, 1, 2]
K_TRUE = [0.1, 0.3, 0.35, 0.15, 0.1]
PI, V, SIGMA2 = (0.9, 0.1), (1e-3, 1.0), 2e-4


def problem(seed, n=24, jumps=4, noise=0.01):
    """A piecewise constant periodic signal with `jumps` steps, blurred by K_TRUE, plus noise."""
    rng = random.Random(seed)
    x = [0.0] * n
    pos = sorted(rng.sample(range(n), jumps))
    levels = [rng.uniform(0, 2) for _ in pos]
    for idx, p in enumerate(pos):
        q = pos[(idx + 1) % jumps]
        i = p
        while True:
            x[(i + 1) % n] = levels[idx]
            i = (i + 1) % n
            if i == q:
                break
    k = embed(K_TRUE, SUPPORT, n)
    y = [v + rng.gauss(0, noise) for v in conv(k, x)]
    return x, k, y


def rel_err(a, b):
    return math.sqrt(sum((p - q) ** 2 for p, q in zip(a, b)) / sum(q * q for q in b))


def random_state(seed, n=10):
    rng = random.Random(seed)
    d = [rng.gauss(0, 1) for _ in range(n)]
    k = embed([rng.random() for _ in SUPPORT], SUPPORT, n)
    s = sum(k)
    k = [v / s for v in k]
    w = [rng.uniform(0.5, 50.0) for _ in range(n)]
    return d, k, w


def test_blur_commutes_with_the_gradient_and_matches_the_matrix():
    rng = random.Random(1)
    n = 12
    x = [rng.random() for _ in range(n)]
    k = embed([rng.random() for _ in SUPPORT], SUPPORT, n)
    a, b = gradient(conv(k, x)), conv(k, gradient(x))
    assert max(abs(p - q) for p, q in zip(a, b)) < 1e-13
    km = kernel_matrix(k)
    assert max(abs(sum(km[r][c] * x[c] for c in range(n)) - v) for r, v in enumerate(conv(k, x))) < 1e-13


def test_q_g_is_the_gaussian_with_the_right_mean_and_covariance():
    d, k, w = random_state(2)
    n = len(d)
    mu, cov, logdet = update_q_g(d, k, w, SIGMA2)
    km = kernel_matrix(k)
    prec = matmul(transpose(km), km)
    prec = [[prec[i][j] / SIGMA2 + (w[i] if i == j else 0.0) for j in range(n)] for i in range(n)]
    eye = matmul(prec, cov)
    assert max(abs(eye[i][j] - (1.0 if i == j else 0.0)) for i in range(n) for j in range(n)) < 1e-9
    # mu minimizes ||d - K g||^2 / (2 sigma2) + sum w_i g_i^2 / 2: the gradient is zero.
    res = [di - v for di, v in zip(d, conv(k, mu))]
    grad = [-sum(km[r][a] * res[r] for r in range(n)) / SIGMA2 + w[a] * mu[a] for a in range(n)]
    assert max(abs(t) for t in grad) < 1e-6 * max(abs(t) for t in d) / SIGMA2
    low = cholesky(prec)
    assert abs(logdet - 2 * sum(math.log(low[i][i]) for i in range(n))) < 1e-9


def test_label_probabilities_are_normalized_and_follow_bayes_rule():
    m2 = [0.0, 1e-4, 0.01, 0.5, 3.0]
    r, w = update_q_z(m2, PI, V)
    for e, ri, wi in zip(m2, r, w):
        dens = [p / math.sqrt(2 * math.pi * v) * math.exp(-e / (2 * v)) for p, v in zip(PI, V)]
        assert abs(sum(ri) - 1.0) < 1e-12
        assert all(abs(a - b / sum(dens)) < 1e-12 for a, b in zip(ri, dens))
        assert abs(wi - sum(a / v for a, v in zip(ri, V))) < 1e-9 * wi


def test_kernel_quadratic_equals_the_expected_misfit():
    d, k0, w = random_state(3)
    n = len(d)
    mu, cov, _ = update_q_g(d, k0, w, SIGMA2)
    a, b = kernel_quadratic(d, mu, cov, SUPPORT)
    rng = random.Random(4)
    kv = [rng.random() for _ in SUPPORT]
    k = embed(kv, SUPPORT, n)
    km = kernel_matrix(k)
    res = [di - v for di, v in zip(d, conv(k, mu))]
    trace = sum(km[i][p] * cov[p][q] * km[i][q] for i in range(n) for p in range(n) for q in range(n))
    expected = sum(t * t for t in res) + trace
    quad = sum(kv[p] * a[p][q] * kv[q] for p in range(5) for q in range(5)) - 2 * sum(bp * kp for bp, kp in zip(b, kv))
    assert abs(quad + sum(t * t for t in d) - expected) < 1e-9 * expected


def test_simplex_qp_beats_random_points_of_the_simplex():
    rng = random.Random(5)
    for _ in range(5):
        m = rng.choice([2, 3, 5])
        g = [[rng.gauss(0, 1) for _ in range(m + 1)] for _ in range(m)]
        a = [[sum(g[i][t] * g[j][t] for t in range(m + 1)) for j in range(m)] for i in range(m)]
        b = [rng.gauss(0, 1) for _ in range(m)]
        k = simplex_qp(a, b)
        assert min(k) >= 0 and abs(sum(k) - 1) < 1e-12

        def f(z):
            return sum(z[i] * a[i][j] * z[j] for i in range(m) for j in range(m)) - 2 * sum(p * q for p, q in zip(b, z))

        best = f(k)
        for _ in range(2000):
            z = [rng.expovariate(1.0) for _ in range(m)]
            if rng.random() < 0.5:
                z[rng.randrange(m)] = 0.0
            s = sum(z)
            if s == 0:
                continue
            assert f([t / s for t in z]) >= best - 1e-10


def test_free_energy_equals_the_log_evidence_for_a_gaussian_prior():
    # One mixture component: the model is linear and Gaussian, and the optimal
    # q(g) makes the bound tight: F = log N(d; 0, v K K^T + sigma2 I).
    d, k, _ = random_state(6, n=8)
    n = len(d)
    v = 0.7
    mu, cov, logdet = update_q_g(d, k, [1.0 / v] * n, SIGMA2)
    r, _ = update_q_z(second_moments(mu, cov), (1.0,), (v,))
    f = free_energy(d, k, mu, cov, logdet, r, (1.0,), (v,), SIGMA2)
    km = kernel_matrix(k)
    c = matmul(km, transpose(km))
    c = [[v * c[i][j] + (SIGMA2 if i == j else 0.0) for j in range(n)] for i in range(n)]
    low = cholesky(c)
    z = cho_solve(low, d)
    log_ev = -0.5 * n * math.log(2 * math.pi) - sum(math.log(low[i][i]) for i in range(n)) - 0.5 * sum(p * q for p, q in zip(d, z))
    assert abs(f - log_ev) < 1e-7 * abs(log_ev)


def test_free_energy_never_decreases():
    _, _, y = problem(2)
    hist = []
    vb_blind(gradient(y), [0.2] * 5, SUPPORT, PI, V, SIGMA2, iters=10, history=hist)
    assert len(hist) == 29
    assert all(hist[i + 1] >= hist[i] - 1e-9 * abs(hist[i]) for i in range(len(hist) - 1))


def test_joint_map_with_a_laplace_prior_prefers_no_blur():
    # ||k * g||_1 <= ||g||_1 for k >= 0 with sum 1, so with noise-free data the
    # pair (d, delta) costs no more than the true pair under lam ||g||_1.
    rng = random.Random(7)
    for _ in range(200):
        n = rng.randint(4, 16)
        g = [rng.gauss(0, 1) if rng.random() < 0.4 else 0.0 for _ in range(n)]
        kv = [rng.random() for _ in SUPPORT]
        s = sum(kv)
        k = embed([t / s for t in kv], SUPPORT, n)
        d = conv(k, g)
        assert sum(abs(t) for t in d) <= sum(abs(t) for t in g) + 1e-12


def test_measured_marginal_estimate_beats_the_naive_one_on_seed_5():
    # A measurement: with the covariance term the kernel is close to the truth;
    # without it the estimate collapses to the delta kernel.
    _, kt, y = problem(5)
    d = gradient(y)
    k, _, _ = vb_blind(d, [0.2] * 5, SUPPORT, PI, V, SIGMA2, iters=50)
    k_naive, _, _ = vb_blind(d, [0.2] * 5, SUPPORT, PI, V, SIGMA2, iters=50, use_cov=False)
    assert rel_err(k, kt) < 0.15
    assert k_naive[0] > 0.99
