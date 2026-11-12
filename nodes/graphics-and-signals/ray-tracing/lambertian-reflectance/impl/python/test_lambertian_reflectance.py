# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lambertian-reflectance/. The authors are listed in prov/K8919H.jsonl.

import math
import random

from lambertian_reflectance import (
    albedo_monte_carlo,
    albedo_quadrature,
    lambert,
    radiance_point_light,
    sample_cosine,
    sample_uniform,
)


def random_dir(rng):
    while True:
        v = (rng.gauss(0, 1), rng.gauss(0, 1), abs(rng.gauss(0, 1)))
        s = math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)
        if s > 1e-9:
            return (v[0] / s, v[1] / s, v[2] / s)


def test_reciprocity():
    rng = random.Random(1)
    for _ in range(1000):
        f = lambert(rng.random())
        a, b = random_dir(rng), random_dir(rng)
        assert f(a, b) == f(b, a)


def test_albedo_by_quadrature_equals_rho():
    # Energy conservation: the hemisphere integral of f cos is rho, at most 1, for every wo.
    rng = random.Random(2)
    for rho in (0.0, 0.18, 0.5, 0.8, 1.0):
        f = lambert(rho)
        for _ in range(3):
            wo = random_dir(rng)
            a = albedo_quadrature(f, wo, 60, 8)
            assert abs(a - rho) < 1e-12
            assert a <= 1.0 + 1e-12


def test_cosine_sampling_gives_zero_variance_estimator():
    rng = random.Random(3)
    f = lambert(0.7)
    mean, se = albedo_monte_carlo(f, (0.0, 0.0, 1.0), 1000, rng, cosine=True)
    assert abs(mean - 0.7) < 1e-12 and se < 1e-9


def test_uniform_sampling_within_four_standard_errors():
    # Samples 2 rho cos(theta) have the mean rho and the variance rho^2 / 3. With N = 20000 the
    # standard error is rho / sqrt(60000); the test accepts four standard errors, a chance of
    # failure below 1e-4 for a random seed, and the seed is fixed.
    rng = random.Random(4)
    rho = 0.7
    n = 20000
    mean, se = albedo_monte_carlo(lambert(rho), (0.0, 0.0, 1.0), n, rng, cosine=False)
    assert abs(se - rho / math.sqrt(3 * n)) < 0.05 * rho / math.sqrt(3 * n)
    assert abs(mean - rho) < 4 * rho / math.sqrt(3 * n)


def test_cosine_samples_have_the_right_distribution():
    # Under the density cos / pi, P(theta <= a) = sin(a)^2 and E[cos theta] = 2/3 with the
    # variance 1/2 - 4/9 = 1/18. Check both with N = 20000 samples and four standard errors.
    rng = random.Random(5)
    n = 20000
    zs = [sample_cosine(rng)[2] for _ in range(n)]
    assert all(0.0 <= z <= 1.0 for z in zs)
    mean = sum(zs) / n
    assert abs(mean - 2 / 3) < 4 * math.sqrt(1 / 18 / n)
    for a in (0.3, 0.7, 1.1, 1.4):
        p = math.sin(a) ** 2
        frac = sum(1 for z in zs if z >= math.cos(a)) / n
        assert abs(frac - p) < 4 * math.sqrt(p * (1 - p) / n)
    us = [sample_uniform(rng)[2] for _ in range(n)]
    assert abs(sum(us) / n - 0.5) < 4 * math.sqrt(1 / 12 / n)


def test_point_light_and_furnace():
    assert abs(radiance_point_light(0.5, 100.0, 2.0, 0.8) - 10.0 / math.pi) < 1e-12
    assert radiance_point_light(0.5, 100.0, 2.0, -0.3) == 0.0
    # A Lambertian surface under a uniform sky of radiance L reflects rho L in every direction.
    rng = random.Random(6)
    L = 3.0
    for rho in (0.2, 0.9):
        wo = random_dir(rng)
        assert abs(L * albedo_quadrature(lambert(rho), wo, 60, 8) - rho * L) < 1e-12
