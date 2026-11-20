# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stochastic-velocity-rescaling/. The authors are listed in prov/BYYCSC.jsonl.
import math
import random

import pytest

from stochastic_velocity_rescaling import free, harmonic, rescale_factor, stochastic_velocity_rescaling


def batch_stats(xs, nb=10):
    """Mean and variance of xs, each with a batch-means standard error."""
    size = len(xs) // nb
    total = sum(xs) / len(xs)
    means, variances = [], []
    for b in range(nb):
        part = xs[b * size:(b + 1) * size]
        means.append(sum(part) / size)
        variances.append(sum((z - total) ** 2 for z in part) / size)

    def summary(vals):
        mu = sum(vals) / nb
        sd = math.sqrt(sum((z - mu) ** 2 for z in vals) / (nb - 1))
        return mu, sd / math.sqrt(nb)
    return summary(means), summary(variances)


def test_kinetic_energy_has_canonical_mean_and_variance():
    # 20 oscillators in 1D, N_f = 20, kT = 1: K is Gamma(10, 1). The start
    # values differ: the thermostat scales all velocities by one factor, so
    # equal oscillators would stay equal.
    n = 20
    rng = random.Random(4)
    x = [[rng.gauss(0.0, 1.0)] for _ in range(n)]
    v = [[rng.gauss(0.0, 1.0)] for _ in range(n)]
    _, _, ks, eff = stochastic_velocity_rescaling(x, v, [1.0] * n, harmonic(1.0), 0.05, 6000, 1.0, 0.1, n, rng)
    (mean, se_mean), (var, se_var) = batch_stats(ks[500:])
    assert abs(mean - 10.0) < 4 * se_mean + 0.05
    assert abs(var - 10.0) < 4 * se_var + 0.3
    assert se_mean < 0.3 and se_var < 1.5
    # the effective energy drifts only by the Verlet error
    assert max(eff) - min(eff) < 0.05


def test_free_particles_sample_the_gamma_law_for_any_step():
    # With no forces the rescaling is the whole dynamics, and it is exact.
    nf = 5
    rng = random.Random(8)
    x = [[0.0] for _ in range(nf)]
    v = [[1.0] for _ in range(nf)]
    _, _, ks, _ = stochastic_velocity_rescaling(x, v, [1.0] * nf, free(), 1.0, 8000, 1.0, 0.2, nf, rng)
    (mean, se_mean), (var, se_var) = batch_stats(ks)
    assert abs(mean - 2.5) < 4 * se_mean
    assert abs(var - 2.5) < 4 * se_var


def test_one_draw_has_the_exact_conditional_mean_and_variance():
    # The SDE dK = (K0 - K) dt / tau + 2 sqrt(K K0 / N_f) dW / sqrt(tau) gives
    # E[K'] = K0 + (K - K0) c and
    # Var[K'] = 2 (1 - c) (K0 / N_f) (2 c K + (1 - c) K0) for c = exp(-h / tau).
    nf, k0, k = 6, 3.0, 4.0
    c = math.exp(-0.5)
    rng = random.Random(3)
    draws = [rescale_factor(k, k0, nf, c, rng) ** 2 * k for _ in range(20000)]
    mean = sum(draws) / len(draws)
    var = sum((d - mean) ** 2 for d in draws) / len(draws)
    exact_var = 2 * (1 - c) * (k0 / nf) * (2 * c * k + (1 - c) * k0)
    assert mean == pytest.approx(k0 + (k - k0) * c, abs=4 * math.sqrt(exact_var / len(draws)))
    assert var == pytest.approx(exact_var, rel=0.05)


def test_canonical_law_is_invariant_under_one_draw():
    # Start K from Gamma(N_f / 2, kT); after one rescaling K is still
    # Gamma(N_f / 2, kT), with mean and variance N_f kT / 2.
    nf, kT = 4, 1.0
    rng = random.Random(6)
    c = math.exp(-1.0)
    out = []
    for _ in range(20000):
        k = rng.gammavariate(nf / 2, kT)
        out.append(rescale_factor(k, nf * kT / 2, nf, c, rng) ** 2 * k)
    mean = sum(out) / len(out)
    var = sum((d - mean) ** 2 for d in out) / len(out)
    assert mean == pytest.approx(2.0, abs=4 * math.sqrt(2.0 / len(out)))
    assert var == pytest.approx(2.0, rel=0.08)


def test_bad_arguments_raise():
    with pytest.raises(ValueError):
        stochastic_velocity_rescaling([[0.0]], [[1.0]], [1.0], free(), 0.1, 1, 1.0, 0.0, 1, random.Random(1))
