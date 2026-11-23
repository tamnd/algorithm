# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/objective-perturbation/. The authors are listed in prov/HFPG7H.jsonl.

import math
import random

import pytest

import dpkit
from objective_perturbation import (
    C_LOGISTIC,
    jacobian_matrix,
    log_det,
    minimize_perturbed,
    noise_of,
    norm,
    objective_perturbation,
    output_log_density,
    perturbed_gradient,
    perturbed_objective,
    privacy_parameters,
    sample_noise,
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
    eps_prime, extra = privacy_parameters(4, 0.5, 1.0)
    assert eps_prime == pytest.approx(1 - 2 * math.log(1.125)) and extra == 0.0
    assert eps_prime == pytest.approx(0.764434, abs=1e-6)
    eps_prime, extra = privacy_parameters(4, 0.05, 0.5)
    assert eps_prime == 0.25 and extra == pytest.approx(0.419401, abs=1e-6)
    f = minimize_perturbed(EXAMPLE, 0.5, [0.0, 0.0], 0.0)
    assert abs(f[0] - 0.4368) < 1e-4 and abs(f[1] - 0.3532) < 1e-4
    g = objective_perturbation(EXAMPLE, 0.5, 1.0, random.Random(9))
    assert abs(g[0] + 0.2786) < 1e-4 and abs(g[1] + 0.5192) < 1e-4


def test_bad_input():
    with pytest.raises(ValueError):
        objective_perturbation(EXAMPLE, 0.5, 0.0, random.Random(0))
    with pytest.raises(ValueError):
        objective_perturbation([((0.0, 1.5), 1)], 0.5, 1.0, random.Random(0))


def test_extra_regularizer_is_nonnegative_and_balances_the_budget():
    rng = random.Random(1)
    for _ in range(500):
        n = rng.randint(1, 50)
        lam = rng.uniform(0.001, 1.0)
        eps = rng.uniform(0.05, 3.0)
        eps_prime, extra = privacy_parameters(n, lam, eps)
        assert eps_prime > 0 and extra >= 0
        # The two parts of the privacy loss add up to at most epsilon.
        assert eps_prime + 2 * math.log(1 + C_LOGISTIC / (n * (lam + extra))) <= eps + 1e-12


def bisect_1d(data, lam, b, extra):
    """Independent oracle in one dimension: the zero of the increasing derivative, by bisection."""
    lo, hi = -100.0, 100.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if perturbed_gradient([mid], data, lam, [b], extra)[0] > 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def test_minimizer_against_bisection():
    rng = random.Random(2)
    for _ in range(500):
        n = rng.randint(1, 8)
        lam = rng.uniform(0.2, 1.0)
        extra = rng.choice((0.0, rng.uniform(0.0, 0.5)))
        data = random_data(n, 1, rng)
        b = rng.uniform(-5, 5)
        f = minimize_perturbed(data, lam, [b], extra)
        assert abs(f[0] - bisect_1d(data, lam, b, extra)) < 1e-9


def test_noise_is_recovered_from_the_output():
    rng = random.Random(3)
    for _ in range(100):
        n = rng.randint(1, 6)
        d = rng.randint(1, 3)
        lam = rng.uniform(0.2, 1.0)
        extra = rng.choice((0.0, 0.3))
        data = random_data(n, d, rng)
        b = sample_noise(d, rng.uniform(0.3, 2.0), rng)
        f = minimize_perturbed(data, lam, b, extra)
        back = noise_of(f, data, lam, extra)
        assert norm([u - v for u, v in zip(back, b)]) < 1e-8
        for _ in range(5):
            g = [fi + rng.uniform(-0.1, 0.1) for fi in f]
            assert perturbed_objective(g, data, lam, b, extra) >= perturbed_objective(f, data, lam, b, extra)


def test_log_det_against_closed_form():
    rng = random.Random(4)
    for _ in range(100):
        a, c = rng.uniform(1, 3), rng.uniform(1, 3)
        b = rng.uniform(-0.9, 0.9)
        assert log_det([[a, b], [b, c]]) == pytest.approx(math.log(a * c - b * b))


@pytest.mark.parametrize("lam, eps", [(0.5, 1.0), (0.05, 0.5)])
def test_output_density_ratio_is_at_most_epsilon(lam, eps):
    """Both branches: Delta = 0 for (0.5, 1.0) and Delta > 0 for (0.05, 0.5), with n = 4."""
    rng = random.Random(5)
    grid = [(i / 4, j / 4) for i in range(-12, 13) for j in range(-12, 13)]
    worst = 0.0
    for _ in range(10):
        data = random_data(4, 2, rng)
        other = list(data)
        other[rng.randrange(4)] = (random_point(2, rng), rng.choice((-1, 1)))
        loss = dpkit.log_ratio_grid(
            lambda f: output_log_density(f, data, lam, eps),
            lambda f: output_log_density(f, other, lam, eps),
            grid,
        )
        assert loss <= eps + 1e-9
        worst = max(worst, loss)
    assert worst > 0.1 * eps


def test_density_matches_the_exact_law_in_one_dimension():
    """In one dimension, f_priv <= t exactly when b >= noise_of(t), and b is Laplace."""
    rng = random.Random(6)
    data = random_data(5, 1, rng)
    lam, eps = 0.3, 1.0
    eps_prime, extra = privacy_parameters(5, lam, eps)
    beta = eps_prime / 2

    def exact_cdf(t):
        u = noise_of([t], data, lam, extra)[0]
        return 0.5 * math.exp(-beta * u) if u >= 0 else 1 - 0.5 * math.exp(beta * u)

    # The integral of the density, by the trapezoid rule, matches the exact law.
    lo, h = -60.0, 0.005
    total, prev, t = 0.0, math.exp(output_log_density([lo], data, lam, eps)), lo
    checks = {-2.0: None, -0.5: None, 0.0: None, 0.5: None, 2.0: None}
    while t < 2.0 - 1e-12:
        t += h
        cur = math.exp(output_log_density([t], data, lam, eps))
        total += (prev + cur) * h / 2
        prev = cur
        for key in checks:
            if abs(t - key) < h / 2:
                checks[key] = total
    for key, value in checks.items():
        assert value == pytest.approx(exact_cdf(key), abs=1e-3)
    # The sampler matches the exact law.
    m = 2000
    samples = [objective_perturbation(data, lam, eps, rng)[0] for _ in range(m)]
    margin = dpkit.hoeffding_margin(m, 1e-6)
    for key in checks:
        emp = sum(1 for s in samples if s <= key) / m
        assert abs(emp - exact_cdf(key)) <= margin


def test_jacobian_matches_finite_differences():
    rng = random.Random(7)
    data = random_data(4, 2, rng)
    f = [0.3, -0.2]
    a = jacobian_matrix(f, data, 0.4, 0.1)
    h = 1e-6
    for j in range(2):
        fp = list(f)
        fp[j] += h
        fm = list(f)
        fm[j] -= h
        col = [(u - v) / (2 * h) for u, v in zip(noise_of(fp, data, 0.4, 0.1), noise_of(fm, data, 0.4, 0.1))]
        for i in range(2):
            assert -col[i] == pytest.approx(a[i][j], abs=1e-5)
