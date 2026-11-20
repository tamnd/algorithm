# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wirtinger-flow/. The authors are listed in prov/E17F69.jsonl.

import cmath
import math
import random

from wirtinger_flow import (dist, gaussian_design, inner, loss, measure, norm, spectral_start, step_size,
                            wirtinger_flow, wirtinger_gradient)


def unit_signal(rng, n):
    x = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(n)]
    s = norm(x)
    return [v / s for v in x]


def test_gradient_gives_the_directional_derivative() -> None:
    # d/dt f(z + t d) at t = 0 equals 2 Re <g(z), d>; check with a central difference.
    rng = random.Random(1)
    n = 5
    a = gaussian_design(rng, 30, n)
    y = measure(a, unit_signal(rng, n))
    for _ in range(5):
        z = unit_signal(rng, n)
        d = unit_signal(rng, n)
        h = 1e-5
        plus = loss(a, y, [u + h * v for u, v in zip(z, d)])
        minus = loss(a, y, [u - h * v for u, v in zip(z, d)])
        numeric = (plus - minus) / (2 * h)
        exact = 2.0 * inner(wirtinger_gradient(a, y, z), d).real
        assert abs(numeric - exact) < 1e-7 * max(1.0, abs(exact))


def test_signal_is_a_zero_and_a_stationary_point() -> None:
    rng = random.Random(2)
    x = unit_signal(rng, 6)
    a = gaussian_design(rng, 40, 6)
    y = measure(a, x)
    assert loss(a, y, x) < 1e-28
    assert norm(wirtinger_gradient(a, y, x)) < 1e-14


def test_loss_ignores_a_global_phase() -> None:
    rng = random.Random(3)
    x = unit_signal(rng, 4)
    a = gaussian_design(rng, 20, 4)
    y = measure(a, x)
    z = unit_signal(rng, 4)
    turned = [cmath.exp(1.1j) * v for v in z]
    assert abs(loss(a, y, z) - loss(a, y, turned)) < 1e-12
    assert abs(dist(z, x) - dist(turned, x)) < 1e-12


def test_step_size_schedule() -> None:
    assert abs(step_size(1) - (1.0 - math.exp(-1.0 / 330.0))) < 1e-15
    assert step_size(1) < 0.0031
    assert step_size(10000) == 0.4
    assert step_size(10000, mu_max=0.3) == 0.3
    increasing = [step_size(t) for t in range(1, 400)]
    assert all(u <= v for u, v in zip(increasing, increasing[1:]))


def test_small_step_decreases_the_loss() -> None:
    rng = random.Random(4)
    n = 6
    a = gaussian_design(rng, 48, n)
    y = measure(a, unit_signal(rng, n))
    z = spectral_start(a, y)
    rec = []
    wirtinger_flow(a, y, 30, z0=z, record=rec)
    values = [loss(a, y, w) for w in rec]
    assert all(v <= u for u, v in zip(values, values[1:]))


def test_recovery_measurement() -> None:
    # Measurement, not a theorem: n = 8, m = 8 n, complex Gaussian design, mu_max = 0.3.
    n, m = 8, 64
    for seed in range(1, 4):
        rng = random.Random(seed)
        x = unit_signal(rng, n)
        a = gaussian_design(rng, m, n)
        y = measure(a, x)
        z0 = spectral_start(a, y)
        z = wirtinger_flow(a, y, 500, z0=z0, mu_max=0.3)
        assert dist(z0, x) > 0.3
        assert dist(z, x) < 1e-8
