# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fisher-vector/. The authors are listed in prov/WR6YRW.jsonl.

import math
import random

from fisher_vector import fisher_vector, log_likelihood, posteriors, raw_gradients

W = [0.5, 0.5]
MU = [[-1.0], [1.0]]
SIG = [[1.0], [1.0]]
X = [[0.0], [1.0], [2.0]]


def close(a, b, tol):
    return len(a) == len(b) and all(abs(x - y) <= tol for x, y in zip(a, b))


def random_gmm(rng, K, D):
    a = [rng.uniform(-1.0, 1.0) for _ in range(K)]
    s = sum(math.exp(t) for t in a)
    w = [math.exp(t) / s for t in a]
    mu = [[rng.uniform(-2.0, 2.0) for _ in range(D)] for _ in range(K)]
    sigma = [[rng.uniform(0.5, 1.5) for _ in range(D)] for _ in range(K)]
    return w, mu, sigma


def sample(rng, w, mu, sigma):
    u, k = rng.random(), 0
    while k < len(w) - 1 and u > w[k]:
        u -= w[k]
        k += 1
    return [rng.gauss(m, s) for m, s in zip(mu[k], sigma[k])]


def test_example_of_the_page():
    g = posteriors([1.0], W, MU, SIG)
    assert abs(g[1] - 1 / (1 + math.exp(-2))) < 1e-12
    raw = fisher_vector(X, W, MU, SIG, rho=1.0, normalize=False, include_weights=True)
    s0 = 0.5 + 1 / (1 + math.exp(2)) + 1 / (1 + math.exp(4))
    assert abs(raw[0] - (s0 - 1.5) / (3 * math.sqrt(0.5))) < 1e-12
    assert close(raw, [-0.4067, 0.4067, 0.3735, 0.1672, 0.2272, -0.2936], 5e-5)
    assert close(fisher_vector(X, W, MU, SIG), [0.5932, 0.3968, 0.4627, -0.5259], 5e-5)


def test_dimension_and_unit_norm():
    rng = random.Random(1)
    for K, D in [(1, 2), (3, 2), (4, 3)]:
        w, mu, sigma = random_gmm(rng, K, D)
        xs = [sample(rng, w, mu, sigma) for _ in range(20)]
        z = fisher_vector(xs, w, mu, sigma)
        assert len(z) == 2 * K * D
        assert abs(sum(t * t for t in z) - 1.0) < 1e-12
        assert len(fisher_vector(xs, w, mu, sigma, include_weights=True)) == (2 * D + 1) * K


def test_gradients_match_finite_differences():
    rng = random.Random(2)
    K, D, h = 3, 2, 1e-5
    w, mu, sigma = random_gmm(rng, K, D)
    alpha = [math.log(t) for t in w]
    xs = [sample(rng, w, mu, sigma) for _ in range(15)]
    g_alpha, g_mu, g_sigma = raw_gradients(xs, w, mu, sigma)

    def softmax(a):
        s = sum(math.exp(t) for t in a)
        return [math.exp(t) / s for t in a]

    for k in range(K):
        ap, am = list(alpha), list(alpha)
        ap[k] += h
        am[k] -= h
        fd = (log_likelihood(xs, softmax(ap), mu, sigma) - log_likelihood(xs, softmax(am), mu, sigma)) / (2 * h)
        assert abs(fd - g_alpha[k]) < 1e-6
        for i in range(D):
            for par, grad in ((mu, g_mu), (sigma, g_sigma)):
                old = par[k][i]
                par[k][i] = old + h
                fp = log_likelihood(xs, w, mu, sigma)
                par[k][i] = old - h
                fm = log_likelihood(xs, w, mu, sigma)
                par[k][i] = old
                assert abs((fp - fm) / (2 * h) - grad[k][i]) < 1e-6


def test_normalized_gradient_is_raw_gradient_scaled():
    rng = random.Random(3)
    K, D = 2, 3
    w, mu, sigma = random_gmm(rng, K, D)
    xs = [sample(rng, w, mu, sigma) for _ in range(10)]
    T = len(xs)
    g_alpha, g_mu, g_sigma = raw_gradients(xs, w, mu, sigma)
    z = fisher_vector(xs, w, mu, sigma, rho=1.0, normalize=False, include_weights=True)
    expect = [g_alpha[k] / (T * math.sqrt(w[k])) for k in range(K)]
    for k in range(K):
        expect += [g_mu[k][i] * sigma[k][i] / (T * math.sqrt(w[k])) for i in range(D)]
        expect += [g_sigma[k][i] * sigma[k][i] / (T * math.sqrt(2 * w[k])) for i in range(D)]
    assert close(z, expect, 1e-12)


def test_whitening_for_separated_components():
    # Well separated components: posteriors are almost 0 or 1, the diagonal
    # Fisher information is almost exact, and each normalized per-sample
    # gradient entry of the means and sigmas has mean 0 and variance 1.
    # The weight entries have variance 1 - w_k, not 1.
    rng = random.Random(4)
    w = [0.3, 0.7]
    mu = [[0.0, 0.0], [30.0, -30.0]]
    sigma = [[1.0, 2.0], [0.5, 1.0]]
    n = 3000
    dim = 2 + 2 * 2 * 2
    s1, s2 = [0.0] * dim, [0.0] * dim
    for _ in range(n):
        z = fisher_vector([sample(rng, w, mu, sigma)], w, mu, sigma, rho=1.0, normalize=False, include_weights=True)
        for j in range(dim):
            s1[j] += z[j]
            s2[j] += z[j] * z[j]
    for j in range(dim):
        mean = s1[j] / n
        var = s2[j] / n - mean * mean
        target = 1.0 - w[j] if j < 2 else 1.0
        assert abs(mean) < 0.15
        assert abs(var - target) < 0.3


def test_hard_assignment_gives_scaled_vlad():
    rng = random.Random(5)
    K, D, T = 4, 2, 30
    w = [1.0 / K] * K
    mu = [[rng.uniform(-3, 3) for _ in range(D)] for _ in range(K)]
    sigma = [[1.0] * D for _ in range(K)]
    xs = [[rng.uniform(-4, 4) for _ in range(D)] for _ in range(T)]
    v = [[0.0] * D for _ in range(K)]
    for x in xs:
        k = min(range(K), key=lambda j: (sum((a - b) ** 2 for a, b in zip(x, mu[j])), j))
        for i in range(D):
            v[k][i] += x[i] - mu[k][i]
    z = fisher_vector(xs, w, mu, sigma, rho=1.0, normalize=False, hard=True)
    for k in range(K):
        assert close(z[2 * D * k:2 * D * k + D], [math.sqrt(K) / T * t for t in v[k]], 1e-12)


def test_order_invariance_and_power_sign():
    rng = random.Random(6)
    w, mu, sigma = random_gmm(rng, 3, 2)
    xs = [sample(rng, w, mu, sigma) for _ in range(25)]
    ys = list(xs)
    rng.shuffle(ys)
    a = fisher_vector(xs, w, mu, sigma)
    assert close(a, fisher_vector(ys, w, mu, sigma), 1e-12)
    plain = fisher_vector(xs, w, mu, sigma, rho=1.0)
    assert all((p > 0) == (q > 0) for p, q in zip(plain, a) if p != 0)


def test_posteriors_sum_to_one_far_from_all_components():
    g = posteriors([1e3, -1e3], [0.5, 0.5], [[0.0, 0.0], [1.0, 1.0]], [[1.0, 1.0], [1.0, 1.0]])
    # A naive exp() of log densities near -1e6 underflows to 0/0; log-sum-exp does not.
    assert abs(sum(g) - 1.0) < 1e-9
    assert all(0.0 < t < 1.0 for t in g)
