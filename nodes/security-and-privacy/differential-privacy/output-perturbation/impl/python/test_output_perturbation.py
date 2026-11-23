# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/output-perturbation/. The authors are listed in prov/DE6SYB.jsonl.

import math
import random

import pytest

import dpkit
from output_perturbation import (
    minimize_risk,
    norm,
    output_log_density,
    output_perturbation,
    risk,
    risk_gradient,
    sample_noise,
    sensitivity_bound,
)


def random_point(d, rng):
    """A point of the unit ball."""
    while True:
        x = [rng.uniform(-1, 1) for _ in range(d)]
        if norm(x) <= 1:
            return x


def random_data(n, d, rng):
    return [(random_point(d, rng), rng.choice((-1, 1))) for _ in range(n)]


EXAMPLE = [((0.6, 0.8), 1), ((1.0, 0.0), 1), ((-0.6, 0.0), -1), ((0.0, -1.0), -1)]


def test_check_values():
    f = minimize_risk(EXAMPLE, 0.5)
    assert abs(f[0] - 0.4368) < 1e-4 and abs(f[1] - 0.3532) < 1e-4
    other = EXAMPLE[:3] + [((0.0, 1.0), -1)]
    g = minimize_risk(other, 0.5)
    assert abs(g[0] - 0.4568) < 1e-4 and abs(g[1] + 0.0642) < 1e-4
    assert abs(norm([a - b for a, b in zip(f, g)]) - 0.4178) < 1e-4
    assert sensitivity_bound(4, 0.5) == 1.0
    assert sensitivity_bound(100, 0.1) == pytest.approx(0.2)


def test_bad_input():
    with pytest.raises(ValueError):
        output_perturbation(EXAMPLE, 0.0, 1.0, random.Random(0))
    with pytest.raises(ValueError):
        output_perturbation([((2.0, 0.0), 1)], 0.5, 1.0, random.Random(0))


def bisect_1d(data, lam):
    """Independent oracle in one dimension: the zero of the increasing derivative of J, by bisection."""
    lo, hi = -10.0, 10.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if risk_gradient([mid], data, lam)[0] > 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def test_minimizer_against_bisection():
    rng = random.Random(1)
    for _ in range(500):
        n = rng.randint(1, 8)
        lam = rng.uniform(0.2, 1.0)
        data = random_data(n, 1, rng)
        assert abs(minimize_risk(data, lam)[0] - bisect_1d(data, lam)) < 1e-9


def test_sensitivity_bound_on_random_replace_pairs():
    rng = random.Random(2)
    worst = 0.0
    for _ in range(500):
        n = rng.randint(1, 8)
        d = rng.randint(1, 2)
        lam = rng.uniform(0.2, 1.0)
        data = random_data(n, d, rng)
        other = list(data)
        other[rng.randrange(n)] = (random_point(d, rng), rng.choice((-1, 1)))
        f1 = minimize_risk(data, lam)
        f2 = minimize_risk(other, lam)
        gap = norm([a - b for a, b in zip(f1, f2)])
        assert gap <= sensitivity_bound(n, lam) + 1e-9
        worst = max(worst, gap * n * lam / 2)
    assert worst > 0.3


def test_minimizer_is_stationary_and_minimal():
    rng = random.Random(3)
    data = random_data(10, 3, rng)
    f = minimize_risk(data, 0.3)
    assert norm(risk_gradient(f, data, 0.3)) < 1e-10
    for _ in range(50):
        g = [fi + rng.uniform(-0.1, 0.1) for fi in f]
        assert risk(g, data, 0.3) >= risk(f, data, 0.3)


def test_output_density_ratio_is_at_most_epsilon():
    rng = random.Random(4)
    for _ in range(20):
        n = rng.randint(2, 6)
        lam = rng.uniform(0.2, 1.0)
        eps = rng.uniform(0.2, 2.0)
        data = random_data(n, 2, rng)
        other = list(data)
        other[0] = (random_point(2, rng), -other[0][1])
        f1, f2 = minimize_risk(data, lam), minimize_risk(other, lam)
        beta = n * lam * eps / 2
        grid = [(i / 4, j / 4) for i in range(-24, 25) for j in range(-24, 25)]
        loss = dpkit.log_ratio_grid(
            lambda z: output_log_density(z, f1, beta),
            lambda z: output_log_density(z, f2, beta),
            grid,
        )
        assert loss <= eps + 1e-9
        assert loss <= beta * norm([a - b for a, b in zip(f1, f2)]) + 1e-9


def gamma_cdf_integer_shape(t, d, beta):
    s = sum((beta * t) ** k / math.factorial(k) for k in range(d))
    return 1 - math.exp(-beta * t) * s


def test_noise_norm_and_direction():
    rng = random.Random(5)
    n = 2000
    d, beta = 3, 2.0
    samples = [sample_noise(d, beta, rng) for _ in range(n)]
    margin = dpkit.hoeffding_margin(n, 1e-6)
    for t in (0.5, 1.0, 1.5, 2.5):
        emp = sum(1 for b in samples if norm(b) <= t) / n
        assert abs(emp - gamma_cdf_integer_shape(t, d, beta)) <= margin
    for j in range(d):
        emp = sum(1 for b in samples if b[j] > 0) / n
        assert abs(emp - 0.5) <= margin


def test_private_model_runs_and_is_reproducible():
    a = output_perturbation(EXAMPLE, 0.5, 1.0, random.Random(9))
    b = output_perturbation(EXAMPLE, 0.5, 1.0, random.Random(9))
    assert a == b and len(a) == 2
