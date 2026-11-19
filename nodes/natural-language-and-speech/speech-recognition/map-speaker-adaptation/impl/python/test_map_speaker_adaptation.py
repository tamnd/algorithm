# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/map-speaker-adaptation/. The authors are listed in prov/TAZK46.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from map_speaker_adaptation import (
    log_gauss_diag,
    log_prior,
    map_adapt,
    map_means,
    posteriors,
    reynolds_adapt,
    statistics,
)


def mixture(rng, weights, means, variances, T):
    out = []
    for _ in range(T):
        u, m, acc = rng.random(), 0, weights[0]
        while u > acc and m < len(weights) - 1:
            m += 1
            acc += weights[m]
        out.append([rng.gauss(mu, math.sqrt(v)) for mu, v in zip(means[m], variances[m])])
    return out


def test_one_gaussian_exact_values():
    # Prior mean 0, data mean 2, tau = 16: n = 4, 16, 64 give alpha = 1/5, 1/2, 4/5.
    for n, want in ((4, F(2, 5)), (16, F(1)), (64, F(8, 5))):
        (mu,) = map_means([[F(0)]], [F(n)], [[F(2 * n)]], F(16))
        assert mu[0] == want


def test_one_gaussian_is_the_conjugate_posterior_mean():
    rng = random.Random(1)
    var, mu0, tau = 2.5, 1.0, 7.0
    xs = [rng.gauss(3.0, math.sqrt(var)) for _ in range(20)]
    means, _ = map_adapt([[x] for x in xs], [1.0], [[mu0]], [[var]], tau, iterations=1)
    # Posterior of a normal mean with known variance: precisions add.
    prior_prec, data_prec = tau / var, len(xs) / var
    want = (prior_prec * mu0 + data_prec * (sum(xs) / len(xs))) / (prior_prec + data_prec)
    assert means[0][0] == pytest.approx(want, abs=1e-12)


def test_page_example_two_components():
    frames = [[0.5], [1.5], [2.5], [3.0]]
    w, mu0, var = [0.5, 0.5], [[-1.0], [1.0]], [[1.0], [1.0]]
    n, s, _, _ = statistics(frames, w, mu0, var)
    assert n[0] == pytest.approx(0.325533, abs=1e-6)
    assert n[1] == pytest.approx(3.674467, abs=1e-6)
    m16 = map_means(mu0, n, s, 16.0)
    m2 = map_means(mu0, n, s, 2.0)
    assert [m16[0][0], m16[1][0]] == pytest.approx([-0.965986, 1.182763], abs=1e-6)
    assert [m2[0][0], m2[1][0]] == pytest.approx([-0.761219, 1.633676], abs=1e-6)


def test_limits_of_tau():
    rng = random.Random(2)
    w = [0.3, 0.7]
    mu0 = [[0.0, 0.0], [3.0, 1.0]]
    var = [[1.0, 0.5], [0.7, 1.2]]
    frames = mixture(rng, w, [[0.5, 0.2], [2.5, 1.5]], var, 60)
    n, s, _, _ = statistics(frames, w, mu0, var)
    ml = [[x / n[m] for x in s[m]] for m in range(2)]
    assert map_means(mu0, n, s, 0.0) == [pytest.approx(row, abs=1e-12) for row in ml]
    big = map_means(mu0, n, s, 1e12)
    for a, b in zip(big, mu0):
        assert a == pytest.approx(b, abs=1e-9)


def test_map_em_never_decreases_the_log_posterior():
    rng = random.Random(3)
    w = [0.25, 0.25, 0.25, 0.25]
    mu0 = [[-2.0, 0.0], [2.0, 0.0], [0.0, 2.0], [0.0, -2.0]]
    var = [[1.0, 1.0], [0.8, 1.0], [1.0, 0.6], [1.2, 1.0]]
    frames = mixture(rng, w, [[-1.0, 1.0], [3.0, 0.5], [0.5, 3.0], [0.0, -1.0]], var, 150)
    _, hist = map_adapt(frames, w, mu0, var, tau=4.0, iterations=12)
    for a, b in zip(hist, hist[1:]):
        assert b >= a - 1e-9
    assert hist[-1] > hist[0]


def test_m_step_is_a_stationary_point_of_the_auxiliary_function():
    rng = random.Random(4)
    w = [0.5, 0.5]
    mu0 = [[0.0, 1.0], [2.0, -1.0]]
    var = [[1.0, 2.0], [0.5, 1.0]]
    tau = 3.0
    frames = mixture(rng, w, mu0, var, 40)
    gam = [posteriors(o, w, mu0, var)[0] for o in frames]
    n, s, _, _ = statistics(frames, w, mu0, var)
    new = map_means(mu0, n, s, tau)

    def objective(means):
        q = math.fsum(g[m] * log_gauss_diag(o, means[m], var[m]) for o, g in zip(frames, gam) for m in range(2))
        return q + log_prior(means, mu0, var, tau)

    h = 1e-6
    best = objective(new)
    for m in range(2):
        for i in range(2):
            up = [row[:] for row in new]
            dn = [row[:] for row in new]
            up[m][i] += h
            dn[m][i] -= h
            assert abs((objective(up) - objective(dn)) / (2 * h)) < 1e-5
            up[m][i] += 0.1
            assert objective(up) < best


def test_reynolds_adapt():
    rng = random.Random(5)
    w = [0.2, 0.5, 0.3]
    mu = [[-2.0], [0.0], [3.0]]
    var = [[1.0], [0.5], [2.0]]
    frames = mixture(rng, w, [[-1.5], [0.5], [3.0]], [[1.2], [0.4], [1.5]], 80)
    n, s, q, _ = statistics(frames, w, mu, var)
    # Weights sum to 1 and the means agree with one MAP step with tau = r.
    nw, nm, nv = reynolds_adapt(frames, w, mu, var, r=16.0)
    assert math.fsum(nw) == pytest.approx(1.0, abs=1e-12)
    assert nm == [pytest.approx(row, abs=1e-12) for row in map_means(mu, n, s, 16.0)]
    assert all(v[0] > 0 for v in nv)
    # r = 0 gives the maximum likelihood re-estimate of one EM step.
    w0, m0, v0 = reynolds_adapt(frames, w, mu, var, r=0.0)
    T = len(frames)
    for m in range(3):
        assert w0[m] == pytest.approx(n[m] / T, abs=1e-12)
        E = s[m][0] / n[m]
        assert m0[m][0] == pytest.approx(E, abs=1e-12)
        assert v0[m][0] == pytest.approx(q[m][0] / n[m] - E * E, abs=1e-9)
    # A huge r leaves the model unchanged.
    wb, mb, vb = reynolds_adapt(frames, w, mu, var, r=1e12)
    assert wb == pytest.approx(w, abs=1e-9)
    assert [x[0] for x in mb] == pytest.approx([x[0] for x in mu], abs=1e-9)
    assert [x[0] for x in vb] == pytest.approx([x[0] for x in var], abs=1e-6)
    # Only the named parts change.
    ww, wm, wv = reynolds_adapt(frames, w, mu, var, r=16.0, adapt="m")
    assert ww == w and wv == var


def test_component_without_data_keeps_its_prior_mean():
    frames = [[0.0], [0.1], [-0.1]]
    w = [0.5, 0.5]
    mu0 = [[0.0], [1000.0]]
    var = [[1.0], [1.0]]
    means, _ = map_adapt(frames, w, mu0, var, tau=16.0)
    assert means[1][0] == pytest.approx(1000.0, abs=1e-9)


def test_log_space_where_plain_densities_underflow():
    w = [0.5, 0.5]
    mu0 = [[0.0], [10.0]]
    var = [[1.0], [1.0]]
    x = [-900.0]
    assert [wi * math.exp(-0.5 * (x[0] - m[0]) ** 2) for wi, m in zip(w, mu0)] == [0.0, 0.0]
    g, z = posteriors(x, w, mu0, var)
    assert g[0] == pytest.approx(1.0) and g[1] < 1e-300
    assert math.isfinite(z)
    means, _ = map_adapt([x], w, mu0, var, tau=1.0)
    assert means[0][0] == pytest.approx(-450.0, abs=1e-9)
    assert means[1][0] == pytest.approx(10.0, abs=1e-9)
