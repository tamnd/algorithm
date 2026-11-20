# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-likelihood-localization/. The authors are listed in prov/XKDP82.jsonl.

import math
import random

from maximum_likelihood_localization import (
    crb,
    derivatives,
    fisher_information,
    localize,
    model,
    nll,
    poisson_image,
)

THETA = [4.3, 3.8, 500.0, 2.0]
SHAPE = (9, 9)
S = 1.3


def test_gradient_and_hessian_match_finite_differences():
    rng = random.Random(1)
    counts = poisson_image(rng, model(THETA, SHAPE, S))
    theta = [4.1, 4.0, 450.0, 2.5]
    _, g, h, _ = derivatives(theta, counts, S)
    steps = [1e-5, 1e-5, 1e-3, 1e-5]
    for i in range(4):
        up = list(theta)
        dn = list(theta)
        up[i] += steps[i]
        dn[i] -= steps[i]
        fd = (nll(up, counts, S) - nll(dn, counts, S)) / (2 * steps[i])
        assert abs(fd - g[i]) < 1e-5 * (1 + abs(g[i]))
        _, gu, _, _ = derivatives(up, counts, S)
        _, gd, _, _ = derivatives(dn, counts, S)
        for j in range(4):
            fd2 = (gu[j] - gd[j]) / (2 * steps[i])
            assert abs(fd2 - h[i][j]) < 1e-4 * (1 + abs(h[i][j]))


def test_fisher_information_is_the_mean_hessian():
    # E[c] = mu makes the second term of the Hessian vanish.
    mu = model(THETA, SHAPE, S)
    _, _, h, fi = derivatives(THETA, mu, S)
    ref = fisher_information(THETA, SHAPE, S)
    for i in range(4):
        for j in range(4):
            assert abs(h[i][j] - fi[i][j]) < 1e-9 * (1 + abs(fi[i][j]))
            assert abs(fi[i][j] - ref[i][j]) < 1e-12 * (1 + abs(ref[i][j]))


def test_noise_free_data_gives_the_true_parameters():
    mu = model(THETA, SHAPE, S)
    for start in (None, [1.0, 7.0, 50.0, 10.0], [2.0, 6.0, 100.0, 5.0], [7.5, 0.5, 2000.0, 0.1]):
        theta, _ = localize(mu, S, theta0=start)
        for a, b in zip(theta, THETA):
            assert abs(a - b) < 1e-6 * (1 + abs(b))


def test_negative_log_likelihood_never_increases():
    rng = random.Random(2)
    counts = poisson_image(rng, model(THETA, SHAPE, S))
    values = []
    localize(counts, S, theta0=[2.0, 6.0, 100.0, 5.0], callback=lambda t, v: values.append(v))
    assert len(values) > 3
    for a, b in zip(values, values[1:]):
        assert b <= a + 1e-9


def test_variance_is_close_to_the_cramer_rao_bound():
    # A measurement: 200 Poisson images, sample variance against I^{-1}.
    rng = random.Random(11)
    mu = model(THETA, SHAPE, S)
    bound = crb(THETA, SHAPE, S)
    fits = [localize(poisson_image(rng, mu), S)[0] for _ in range(200)]
    for k in (0, 1):
        vals = [f[k] for f in fits]
        mean = sum(vals) / len(vals)
        var = sum((v - mean) ** 2 for v in vals) / (len(vals) - 1)
        assert abs(var / bound[k][k] - 1) < 0.3
        assert abs(mean - THETA[k]) < 3 * math.sqrt(bound[k][k] / len(vals))


def test_bound_for_100_nm_pixels_and_1000_photons():
    # s = a = 100 nm, N = 1000, almost no background: about 3.29 nm,
    # which is sqrt((s^2 + a^2 / 12) / N).
    n = 15
    bound = crb([(n - 1) / 2, (n - 1) / 2, 1000.0, 1e-6], (n, n), 1.0)
    nm = 100 * math.sqrt(bound[0][0])
    assert abs(nm - 3.2914) < 1e-3
    assert abs(nm - 100 * math.sqrt((1 + 1 / 12) / 1000)) < 1e-3
