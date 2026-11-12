# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/variational-autoencoder/. The authors are listed in prov/GZ4VWM.jsonl.

import math
import random

from variational_autoencoder import (
    LOG2PI,
    elbo_estimate,
    elbo_exact,
    elbo_gradient,
    encode,
    init_params,
    kl_diag_gaussian,
    log_marginal,
    log_normal_diag,
    train,
)


def mean_and_se(values):
    n = len(values)
    m = sum(values) / n
    var = sum((v - m) ** 2 for v in values) / (n - 1)
    return m, math.sqrt(var / n)


def ppca_data(seed=4, n=300):
    r = random.Random(seed)
    out = []
    for _ in range(n):
        z = r.gauss(0.0, 1.0)
        out.append([2.0 * z + r.gauss(0.0, 0.5) + 1.0, 1.0 * z + r.gauss(0.0, 0.5) - 0.5])
    return out


def test_closed_form_kl_matches_monte_carlo():
    mu, lv = [0.7, -1.2], [math.log(0.3), math.log(2.0)]
    rng = random.Random(0)
    samples = []
    for _ in range(100000):
        z = [m + math.exp(l / 2) * rng.gauss(0.0, 1.0) for m, l in zip(mu, lv)]
        log_p = -0.5 * sum(LOG2PI + v * v for v in z)
        samples.append(log_normal_diag(z, mu, lv) - log_p)
    est, se = mean_and_se(samples)
    assert abs(est - kl_diag_gaussian(mu, lv)) < 4 * se


def test_reparameterized_gradient_of_simple_expectation_is_unbiased():
    # E[z^2] for z = mu + sigma eps equals mu^2 + sigma^2; its gradient is (2 mu, 2 sigma).
    mu, sigma = 0.8, 1.5
    rng = random.Random(1)
    eps = [rng.gauss(0.0, 1.0) for _ in range(50000)]
    g_mu, se_mu = mean_and_se([2 * (mu + sigma * e) for e in eps])
    g_sig, se_sig = mean_and_se([2 * (mu + sigma * e) * e for e in eps])
    assert abs(g_mu - 2 * mu) < 4 * se_mu
    assert abs(g_sig - 2 * sigma) < 4 * se_sig


def _flat(p):
    out = []
    for key in sorted(p):
        for i, v in enumerate(p[key]):
            if isinstance(v, list):
                out += [(key, i, j) for j in range(len(v))]
            else:
                out.append((key, i, None))
    return out


def _get(p, idx):
    key, i, j = idx
    return p[key][i] if j is None else p[key][i][j]


def _add(p, idx, h):
    key, i, j = idx
    if j is None:
        p[key][i] += h
    else:
        p[key][i][j] += h


def test_gradient_matches_finite_differences():
    p = init_params(3, 2, random.Random(2), scale=0.5)
    r = random.Random(3)
    for key in ("a", "b", "c"):
        p[key] = [r.gauss(0.0, 0.3) for _ in p[key]]
    p["B"] = [[r.gauss(0.0, 0.3) for _ in row] for row in p["B"]]
    p["tau"] = [0.4]
    x, eps = [0.5, -1.0, 2.0], [0.3, -1.1]
    g = elbo_gradient(p, x, eps)
    h = 1e-6
    for idx in _flat(p):
        _add(p, idx, h)
        up = elbo_estimate(p, x, eps)
        _add(p, idx, -2 * h)
        down = elbo_estimate(p, x, eps)
        _add(p, idx, h)
        assert abs((up - down) / (2 * h) - _get(g, idx)) < 1e-5


def test_reparameterized_elbo_gradient_is_unbiased():
    p = init_params(2, 1, random.Random(5), scale=0.7)
    p["b"] = [math.log(0.5)]
    p["tau"] = [0.2]
    x = [1.0, -0.5]
    rng = random.Random(6)
    grads = [elbo_gradient(p, x, [rng.gauss(0.0, 1.0)]) for _ in range(10000)]
    h = 1e-6
    for idx in _flat(p):
        _add(p, idx, h)
        up = elbo_exact(p, x)
        _add(p, idx, -2 * h)
        down = elbo_exact(p, x)
        _add(p, idx, h)
        exact = (up - down) / (2 * h)
        est, se = mean_and_se([_get(g, idx) for g in grads])
        assert abs(est - exact) < 5 * se + 1e-6


def test_elbo_is_a_lower_bound_and_tight_at_the_true_posterior():
    rng = random.Random(7)
    for _ in range(20):
        p = init_params(3, 2, rng, scale=1.0)
        p["B"] = [[rng.gauss(0.0, 0.3) for _ in range(3)] for _ in range(2)]
        p["tau"] = [rng.uniform(-1.0, 1.0)]
        x = [rng.gauss(0.0, 2.0) for _ in range(3)]
        assert elbo_exact(p, x) <= log_marginal(p, x) + 1e-12
    # C with orthogonal columns: the true posterior N(S C^T (x - c) / s2, S), S = (I + C^T C / s2)^-1, is diagonal
    p = init_params(3, 2, rng)
    p["C"] = [[2.0, 0.0], [0.0, 1.0], [0.0, 0.0]]
    p["c"] = [0.1, -0.2, 0.3]
    p["tau"] = [math.log(0.5)]
    s2 = 0.5
    post_var = [1.0 / (1.0 + 4.0 / s2), 1.0 / (1.0 + 1.0 / s2)]
    p["A"] = [[post_var[j] * p["C"][i][j] / s2 for i in range(3)] for j in range(2)]
    p["a"] = [-sum(p["A"][j][i] * p["c"][i] for i in range(3)) for j in range(2)]
    p["B"] = [[0.0] * 3 for _ in range(2)]
    p["b"] = [math.log(v) for v in post_var]
    x = [1.5, -0.7, 0.9]
    assert abs(elbo_exact(p, x) - log_marginal(p, x)) < 1e-12


def test_training_closes_the_gap():
    data = ppca_data()
    p = train(data, 1, random.Random(1))
    elbo = sum(elbo_exact(p, x) for x in data) / len(data)
    logp = sum(log_marginal(p, x) for x in data) / len(data)
    assert elbo > -3.1 and 0.0 <= logp - elbo < 0.05


def test_large_fixed_noise_gives_posterior_collapse():
    data = ppca_data()
    p = train(data, 1, random.Random(1), steps=1000, fixed_tau=math.log(10.0))
    kl = sum(kl_diag_gaussian(*encode(p, x)) for x in data) / len(data)
    assert kl < 1e-3
