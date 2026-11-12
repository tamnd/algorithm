# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/microfacet-brdf/. The authors are listed in prov/TTFZZ6.jsonl.

import math
import random

from microfacet_brdf import (
    albedo_monte_carlo,
    albedo_quadrature,
    cook_torrance,
    d_beckmann,
    d_ggx,
    dot,
    g1_ggx,
    hemisphere_integral,
    sample_ggx_normal,
)


def wdir(deg):
    t = math.radians(deg)
    return (math.sin(t), 0.0, math.cos(t))


def random_dir(rng):
    while True:
        v = (rng.gauss(0, 1), rng.gauss(0, 1), abs(rng.gauss(0, 1)))
        s = math.sqrt(dot(v, v))
        if s > 1e-9 and v[2] / s > 1e-3:
            return (v[0] / s, v[1] / s, v[2] / s)


def test_reciprocity():
    rng = random.Random(1)
    for _ in range(2000):
        a, b = random_dir(rng), random_dir(rng)
        alpha = rng.uniform(0.05, 1.0)
        for eta in (1.5, None):
            for corr in (True, False):
                x = cook_torrance(a, b, alpha, eta, corr)
                y = cook_torrance(b, a, alpha, eta, corr)
                assert abs(x - y) <= 1e-12 * max(1.0, abs(x))


def test_distributions_are_normalized():
    # The projected facet area adds up to the macro surface: integral of D(h) cos(theta_h) = 1.
    for alpha in (0.1, 0.3, 0.5, 1.0):
        assert abs(hemisphere_integral(lambda h: d_ggx(h, alpha) * h[2], 400, 4) - 1.0) < 1e-9
        assert abs(hemisphere_integral(lambda h: d_beckmann(h, alpha) * h[2], 400, 4) - 1.0) < 1e-9


def test_weak_white_furnace():
    # The facets seen from wo project to the macro surface: integral of G1(wo, h) max(0, wo.h) D(h) dh
    # equals cos(theta_o) for the Smith G1 of the same distribution.
    for alpha in (0.3, 1.0):
        for deg in (0, 45, 80):
            wo = wdir(deg)
            val = hemisphere_integral(lambda h: g1_ggx(wo, h, alpha) * max(0.0, dot(wo, h)) * d_ggx(h, alpha), 120, 120)
            assert abs(val - wo[2]) < 1e-5


def test_energy_conservation_by_quadrature():
    # With F = 1 the directional albedo is at most 1, and it falls as the roughness grows, because
    # this single-scattering model drops the light that leaves after more than one bounce.
    for deg in (0, 45, 80):
        wo = wdir(deg)
        prev = 2.0
        for alpha in (0.3, 0.5, 1.0):
            a_corr = albedo_quadrature(wo, alpha, None, True, 120, 120)
            a_sep = albedo_quadrature(wo, alpha, None, False, 120, 120)
            assert 0.0 < a_sep <= a_corr + 1e-9 <= 1.0
            if deg == 0:
                assert a_corr < prev
                prev = a_corr
    # A dielectric reflects far less: about R0 = 0.04 at normal incidence for a smooth lobe.
    assert albedo_quadrature(wdir(0), 0.3, 1.5, True, 120, 120) < 0.04


def test_closed_form_alpha_one_normal_view():
    # For alpha = 1, D = 1/pi and G = 2 mu / (1 + mu) at normal view, so the albedo is 1 - ln 2.
    assert abs(albedo_quadrature(wdir(0), 1.0, None, True, 120, 8) - (1.0 - math.log(2.0))) < 1e-9


def test_sampled_normals_follow_d_cos():
    # Under the density D(h) cos(theta_h), P(theta_h <= a) = tan^2 a / (alpha^2 + tan^2 a).
    # Check it at four angles with N = 20000 and four standard errors.
    rng = random.Random(2)
    alpha, n = 0.4, 20000
    hs = [sample_ggx_normal(rng, alpha) for _ in range(n)]
    for a in (0.2, 0.4, 0.8, 1.2):
        t2 = math.tan(a) ** 2
        p = t2 / (alpha * alpha + t2)
        frac = sum(1 for h in hs if h[2] >= math.cos(a)) / n
        assert abs(frac - p) < 4 * math.sqrt(p * (1 - p) / n)


def test_monte_carlo_albedo_matches_quadrature():
    # The sampled estimator is unbiased; with N = 20000 its mean must lie within four standard
    # errors of the quadrature value, which is accurate to about 1e-6 here.
    rng = random.Random(3)
    for alpha, deg in ((0.5, 45), (0.3, 0), (1.0, 80)):
        wo = wdir(deg)
        mean, se = albedo_monte_carlo(wo, alpha, 20000, rng)
        ref = albedo_quadrature(wo, alpha, None, True, 120, 120)
        assert se < 0.02
        assert abs(mean - ref) < 4 * se


def test_worked_values():
    wi = wdir(30)
    mirror = (-wi[0], 0.0, wi[2])
    assert abs(d_ggx((0.0, 0.0, 1.0), 0.3) - 1 / (math.pi * 0.09)) < 1e-12
    assert abs(cook_torrance(wi, mirror, 0.3) - 0.04823392038228543) < 1e-12
    assert abs(cook_torrance(wi, wdir(-60), 0.3) - 0.03404949486972981) < 1e-12
