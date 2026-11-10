# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/p-stable-distribution/. The authors are listed in prov/9QBY0D.jsonl.

import math
import random

import pytest

from p_stable_distribution import (
    char_function,
    cms_transform,
    empirical_char_function,
    sample,
    sample_cauchy,
)

# With N draws, the mean of cos(t X) has standard deviation at most
# 1 / sqrt(2 N), which is 0.011 for N = 4000. The tolerance 0.05 is
# more than 4 standard deviations.
N = 4000
TOL = 0.05


def test_cms_reduces_to_known_formulas() -> None:
    for theta in (-1.5, -0.7, -0.1, 0.0, 0.3, 1.2, 1.55):
        for w in (0.01, 0.5, 1.0, 3.0):
            # p = 2: 2 sin(theta) sqrt(w), a normal law with variance 2.
            assert math.isclose(cms_transform(2, theta, w), 2 * math.sin(theta) * math.sqrt(w), rel_tol=1e-12, abs_tol=1e-12)
            # p = 1 is the limit of the general formula: tan(theta), and w drops out.
            assert cms_transform(1, theta, w) == math.tan(theta)
            near = cms_transform(1 + 1e-9, theta, w)
            assert math.isclose(near, math.tan(theta), rel_tol=1e-6, abs_tol=1e-9)


def test_characteristic_function_matches() -> None:
    rng = random.Random(7)
    for p in (0.5, 1.0, 1.5, 2.0):
        xs = [sample(p, rng) for _ in range(N)]
        for t in (0.5, 1.0, 2.0):
            assert abs(empirical_char_function(xs, t) - char_function(p, t)) <= TOL


def test_stability_of_linear_combinations() -> None:
    rng = random.Random(11)
    a = [3.0, -1.0, 2.0, 0.5]
    for p in (0.7, 1.0, 1.8):
        norm = sum(abs(x) ** p for x in a) ** (1 / p)
        ys = [sum(ai * sample(p, rng) for ai in a) for _ in range(N)]
        for t in (0.5, 1.0, 2.0):
            # sum a_i X_i has the law of ||a||_p X, so its value at t / ||a||_p is exp(-|t|^p).
            assert abs(empirical_char_function(ys, t / norm) - char_function(p, t)) <= TOL


def test_median_of_absolute_cauchy_is_one() -> None:
    # P(|tan theta| <= 1) = P(|theta| <= pi/4) = 1/2 exactly.
    assert math.isclose(math.tan(math.pi / 4), 1.0)
    rng = random.Random(3)
    xs = sorted(abs(sample_cauchy(rng)) for _ in range(4001))
    # The sample median has standard deviation about 1 / (2 sqrt(n) density) = 0.025.
    assert abs(xs[2000] - 1.0) <= 0.1


def test_gaussian_case_has_variance_two() -> None:
    rng = random.Random(5)
    xs = [sample(2, rng) for _ in range(N)]
    # Var(X^2) = 8, so the mean of X^2 has standard deviation 0.045.
    assert abs(sum(x * x for x in xs) / N - 2.0) <= 0.2


def test_rejects_p_outside_range() -> None:
    rng = random.Random(0)
    for p in (0, -1, 2.5):
        with pytest.raises(ValueError):
            sample(p, rng)
