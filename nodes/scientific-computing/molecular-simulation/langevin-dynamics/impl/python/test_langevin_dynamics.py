# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/langevin-dynamics/. The authors are listed in prov/YHB5S5.jsonl.
import math
import random

import pytest

from langevin_dynamics import free, harmonic, langevin_dynamics


def stationary_covariance(h, gamma, omega2=1.0, kT=1.0):
    """Exact stationary covariance of (x, v) for one OBABO step on U = omega2 x^2 / 2.

    Iterates S <- A S A^T + Q over the five linear parts of the step.
    """
    c = math.exp(-0.5 * gamma * h)
    o = ([[1, 0], [0, c]], [[0, 0], [0, (1 - c * c) * kT]])
    b = ([[1, 0], [-0.5 * h * omega2, 1]], [[0, 0], [0, 0]])
    a = ([[1, h], [0, 1]], [[0, 0], [0, 0]])
    s = [[0.0, 0.0], [0.0, 0.0]]
    for _ in range(3000):
        for mat, q in (o, b, a, b, o):
            ms = [[sum(mat[i][k] * s[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
            s = [[sum(ms[i][k] * mat[j][k] for k in range(2)) + q[i][j] for j in range(2)] for i in range(2)]
    return s


def moments(samples, n):
    xx = sum(p[0] ** 2 for s in samples for p in s[0]) / (len(samples) * n)
    vv = sum(p[0] ** 2 for s in samples for p in s[1]) / (len(samples) * n)
    return xx, vv


def test_harmonic_oscillator_matches_exact_discrete_stationary_law():
    # OBABO keeps <v^2> = kT / m exactly and gives <x^2> = (kT / k) / (1 - h^2 omega^2 / 4).
    h = 1.0
    s = stationary_covariance(h, 1.0)
    assert s[1][1] == pytest.approx(1.0, abs=1e-12)
    assert s[0][0] == pytest.approx(1.0 / (1.0 - h * h / 4.0), abs=1e-12)
    n = 50
    rng = random.Random(1)
    _, _, samples = langevin_dynamics([[0.0]] * n, [[0.0]] * n, [1.0] * n, harmonic(1.0), h, 1200, 1.0, 1.0, rng, every=5)
    xx, vv = moments(samples[20:], n)
    assert xx == pytest.approx(s[0][0], rel=0.05)
    assert vv == pytest.approx(s[1][1], rel=0.05)


def test_small_step_approaches_canonical_values():
    h = 0.1
    s = stationary_covariance(h, 2.0)
    assert s[0][0] == pytest.approx(1.0, abs=0.003)
    n = 50
    rng = random.Random(2)
    _, _, samples = langevin_dynamics([[0.0]] * n, [[0.0]] * n, [1.0] * n, harmonic(1.0), h, 1500, 1.0, 2.0, rng, every=10)
    xx, vv = moments(samples[10:], n)
    assert xx == pytest.approx(1.0, rel=0.1)
    assert vv == pytest.approx(1.0, rel=0.1)


def test_free_particle_velocities_are_an_ornstein_uhlenbeck_process():
    # With no forces one step maps v to exp(-gamma h) v + noise, exactly.
    n, h, gamma = 500, 0.5, 1.0
    rng = random.Random(3)
    v0 = [[rng.gauss(0.0, 1.0)] for _ in range(n)]
    _, v1, _ = langevin_dynamics([[0.0]] * n, v0, [1.0] * n, free(), h, 1, 1.0, gamma, rng)
    cov = sum(a[0] * b[0] for a, b in zip(v0, v1)) / n
    var1 = sum(b[0] ** 2 for b in v1) / n
    assert cov == pytest.approx(math.exp(-gamma * h), abs=0.15)
    assert var1 == pytest.approx(1.0, abs=0.25)


def test_zero_friction_is_velocity_verlet():
    x, v, _ = langevin_dynamics([[1.0]], [[0.0]], [1.0], harmonic(1.0), 0.05, 200, 1.0, 0.0, random.Random(0))
    assert 0.5 * v[0][0] ** 2 + 0.5 * x[0][0] ** 2 == pytest.approx(0.5, abs=1e-3)
    assert x[0][0] == pytest.approx(math.cos(10.0), abs=0.01)


def test_bad_arguments_raise():
    with pytest.raises(ValueError):
        langevin_dynamics([[1.0]], [[0.0]], [1.0], harmonic(1.0), 0.05, 1, 1.0, -1.0, random.Random(0))
