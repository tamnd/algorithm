# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/baoab-langevin-integrator/. The authors are listed in prov/V8MPCG.jsonl.
import math
import random

import pytest

from baoab_langevin_integrator import baoab, harmonic, quartic


def stationary_covariance(h, gamma, omega2=1.0, kT=1.0):
    """Exact stationary covariance of (x, v) for one BAOAB step on U = omega2 x^2 / 2.

    Iterates S <- A S A^T + Q over the five linear parts of the step.
    """
    c = math.exp(-gamma * h)
    b = ([[1, 0], [-0.5 * h * omega2, 1]], [[0, 0], [0, 0]])
    a = ([[1, 0.5 * h], [0, 1]], [[0, 0], [0, 0]])
    o = ([[1, 0], [0, c]], [[0, 0], [0, (1 - c * c) * kT]])
    s = [[0.0, 0.0], [0.0, 0.0]]
    for _ in range(3000):
        for mat, q in (b, a, o, a, b):
            ms = [[sum(mat[i][k] * s[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
            s = [[sum(ms[i][k] * mat[j][k] for k in range(2)) + q[i][j] for j in range(2)] for i in range(2)]
    return s


def moments(samples, n):
    xx = sum(p[0] ** 2 for s in samples for p in s[0]) / (len(samples) * n)
    vv = sum(p[0] ** 2 for s in samples for p in s[1]) / (len(samples) * n)
    return xx, vv


@pytest.mark.parametrize("h", [0.5, 1.0, 1.5])
def test_harmonic_positions_are_exact_for_every_stable_step(h):
    # BAOAB gives <x^2> = kT / k exactly for h omega < 2, and
    # <v^2> = (kT / m)(1 - h^2 omega^2 / 4).
    s = stationary_covariance(h, 1.0)
    assert s[0][0] == pytest.approx(1.0, abs=1e-10)
    assert s[1][1] == pytest.approx(1.0 - h * h / 4.0, abs=1e-10)
    assert s[0][1] == pytest.approx(0.0, abs=1e-10)


def test_harmonic_samples_match_the_exact_law():
    n, h = 50, 1.0
    rng = random.Random(1)
    _, _, samples = baoab([[0.0]] * n, [[0.0]] * n, [1.0] * n, harmonic(1.0), h, 1200, 1.0, 1.0, rng, every=5)
    xx, vv = moments(samples[20:], n)
    assert xx == pytest.approx(1.0, rel=0.06)
    assert vv == pytest.approx(0.75, rel=0.06)


def test_quartic_well_position_moment_is_close_to_canonical():
    # Canonical <x^2> for U = x^4 / 4 at kT = 1 is 2 Gamma(3/4) / Gamma(1/4).
    exact = 2 * math.gamma(0.75) / math.gamma(0.25)
    assert exact == pytest.approx(0.67598, abs=1e-5)
    n = 50
    rng = random.Random(1)
    _, _, samples = baoab([[0.0]] * n, [[0.0]] * n, [1.0] * n, quartic(), 0.3, 1500, 1.0, 1.0, rng, every=5)
    xx, _ = moments(samples[20:], n)
    assert xx == pytest.approx(exact, rel=0.04)


def test_zero_friction_is_velocity_verlet_and_conserves_energy():
    x, v, _ = baoab([[1.0]], [[0.0]], [1.0], harmonic(1.0), 0.05, 200, 1.0, 0.0, random.Random(0))
    assert 0.5 * v[0][0] ** 2 + 0.5 * x[0][0] ** 2 == pytest.approx(0.5, abs=1e-3)
    assert x[0][0] == pytest.approx(math.cos(10.0), abs=0.01)


def test_bad_arguments_raise():
    with pytest.raises(ValueError):
        baoab([[1.0]], [[0.0]], [1.0], harmonic(1.0), 0.0, 1, 1.0, 1.0, random.Random(0))
