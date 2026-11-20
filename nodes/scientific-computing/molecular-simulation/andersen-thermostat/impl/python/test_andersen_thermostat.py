# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/andersen-thermostat/. The authors are listed in prov/8Z4JVW.jsonl.
import math
import random

import pytest

from andersen_thermostat import andersen_thermostat, free, harmonic, kinetic


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
    # 20 oscillators in 1D, N_f = 20, kT = 1: K is Gamma(10, 1),
    # with mean 10 and variance 10.
    n = 20
    rng = random.Random(11)
    x = [[1.0] for _ in range(n)]
    v = [[0.0] for _ in range(n)]
    _, _, ks = andersen_thermostat(x, v, [1.0] * n, harmonic(1.0), 0.05, 6000, 1.0, 1.0, rng)
    (mean, se_mean), (var, se_var) = batch_stats(ks[1000:])
    assert abs(mean - 10.0) < 4 * se_mean + 0.05
    assert abs(var - 10.0) < 4 * se_var + 0.3
    assert se_mean < 0.4 and se_var < 1.5


def test_free_particle_velocity_correlation_decays_as_exp_minus_nu_t():
    # For free particles a velocity survives n steps with probability
    # exp(-nu n h), and a new velocity is independent of the old one.
    n, h, nu = 400, 0.1, 1.0
    rng = random.Random(5)
    x = [[0.0] for _ in range(n)]
    v = [[rng.gauss(0.0, 1.0)] for _ in range(n)]
    history = []
    for _ in range(120):
        x, v, _ = andersen_thermostat(x, v, [1.0] * n, free(), h, 1, 1.0, nu, rng)
        history.append([p[0] for p in v])
    lag = 10
    num = den = 0.0
    for t in range(0, len(history) - lag):
        num += sum(a * b for a, b in zip(history[t], history[t + lag]))
        den += sum(a * a for a in history[t])
    assert abs(num / den - math.exp(-nu * lag * h)) < 0.06


def test_collision_rate_is_one_minus_exp_minus_nu_h():
    # With no forces a velocity changes only at a collision.
    n, h, nu = 500, 0.2, 0.5
    rng = random.Random(9)
    x = [[0.0] for _ in range(n)]
    v = [[1.0] for _ in range(n)]
    changed = 0
    trials = 20
    for _ in range(trials):
        _, v1, _ = andersen_thermostat(x, v, [1.0] * n, free(), h, 1, 1.0, nu, rng)
        changed += sum(1 for a, b in zip(v, v1) if a[0] != b[0])
    p = 1.0 - math.exp(-nu * h)
    se = math.sqrt(p * (1 - p) / (n * trials))
    assert abs(changed / (n * trials) - p) < 4 * se


def test_new_velocities_have_maxwell_boltzmann_variance():
    # One step with nu h large resets almost every velocity; the variance
    # of a component is kT / m.
    n = 500
    rng = random.Random(2)
    m = [4.0] * n
    x = [[0.0, 0.0] for _ in range(n)]
    v = [[0.0, 0.0] for _ in range(n)]
    _, v1, _ = andersen_thermostat(x, v, m, free(), 1.0, 1, 2.0, 50.0, rng)
    comps = [c for p in v1 for c in p]
    var = sum(c * c for c in comps) / len(comps)
    assert abs(var - 0.5) < 4 * 0.5 * math.sqrt(2.0 / len(comps))


def test_zero_collision_rate_is_velocity_verlet():
    rng = random.Random(0)
    x, v, ks = andersen_thermostat([[1.0]], [[0.0]], [1.0], harmonic(1.0), 0.05, 2000, 1.0, 0.0, rng)
    energy = kinetic(v, [1.0]) + 0.5 * x[0][0] ** 2
    assert abs(energy - 0.5) < 0.001


def test_inputs_are_not_changed_and_bad_arguments_raise():
    x, v = [[1.0]], [[0.5]]
    andersen_thermostat(x, v, [1.0], harmonic(1.0), 0.1, 10, 1.0, 1.0, random.Random(1))
    assert x == [[1.0]] and v == [[0.5]]
    with pytest.raises(ValueError):
        andersen_thermostat(x, v, [1.0], harmonic(1.0), 0.1, 10, 1.0, -1.0, random.Random(1))
