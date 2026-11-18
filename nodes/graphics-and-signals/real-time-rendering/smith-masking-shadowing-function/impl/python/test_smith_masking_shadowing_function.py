# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/smith-masking-shadowing-function/. The authors are listed in prov/0245JB.jsonl.

"""Tests of the Smith functions: range, closed forms and the weak white furnace."""

import math
import random

from smith_masking_shadowing_function import (
    g1,
    g1_schlick_ggx,
    g2_height_correlated,
    g2_separable,
    ggx_d,
    lambda_ggx,
    weak_furnace,
)


def cosd(deg: float) -> float:
    return math.cos(math.radians(deg))


def test_range_and_order() -> None:
    rng = random.Random(1)
    for _ in range(2000):
        a = rng.uniform(0.01, 2.0)
        cl, cv = rng.uniform(1e-6, 1.0), rng.uniform(1e-6, 1.0)
        sep = g2_separable(cl, cv, a)
        cor = g2_height_correlated(cl, cv, a)
        assert 0.0 <= sep <= cor <= 1.0
        assert 0.0 <= g1(cv, a) <= 1.0
        assert abs(g2_height_correlated(cl, cv, a) - g2_height_correlated(cv, cl, a)) < 1e-15


def test_end_values() -> None:
    for a in (0.1, 0.5, 1.0):
        assert g1(1.0, a) == 1.0
        assert g1(1e-9, a) < 1e-6
        assert g1(-0.2, a) == 0.0
        assert g1(0.5, a, cos_wm=-0.1) == 0.0
    # A smooth surface hides nothing.
    assert abs(g1(cosd(80.0), 1e-6) - 1.0) < 1e-9


def test_page_values() -> None:
    assert abs(g1(cosd(60.0), 0.5) - 0.8610) < 5e-5
    assert abs(g1(cosd(85.0), 0.5) - 0.2940) < 5e-5
    assert abs(g2_separable(cosd(60.0), cosd(60.0), 0.5) - 0.7413) < 5e-5
    assert abs(g2_height_correlated(cosd(60.0), cosd(60.0), 0.5) - 0.7559) < 5e-5
    # At alpha = 1, Lambda = (1 / mu - 1) / 2 and G1 = 2 mu / (1 + mu).
    for mu in (0.1, 0.5, 0.9):
        assert abs(lambda_ggx(mu, 1.0) - (1.0 / mu - 1.0) / 2.0) < 1e-12
        assert abs(g1(mu, 1.0) - 2.0 * mu / (1.0 + mu)) < 1e-12


def test_schlick_ggx_fit() -> None:
    # Exact at alpha = 1 with k = alpha / 2, and only a fit elsewhere.
    for i in range(1, 1001):
        mu = i / 1000.0
        assert abs(g1_schlick_ggx(mu, 0.5) - g1(mu, 1.0)) < 1e-12
    worst = {}
    for a in (0.1, 0.25, 0.5):
        worst[a] = max(abs(g1_schlick_ggx(i / 10000.0, a / 2.0) - g1(i / 10000.0, a)) for i in range(1, 10001))
    assert abs(worst[0.1] - 0.1401) < 5e-4
    assert abs(worst[0.25] - 0.1095) < 5e-4
    assert abs(worst[0.5] - 0.0664) < 5e-4


def test_weak_white_furnace_quadrature() -> None:
    # Integrate G1(o, m) D(m) max(0, o.m) / (n.o) over the hemisphere of m.
    for a in (0.2, 0.6):
        for deg in (0.0, 45.0, 75.0):
            o = (math.sin(math.radians(deg)), 0.0, cosd(deg))
            nt, npf = 600, 128
            total = 0.0
            for i in range(nt):
                t = (i + 0.5) * (math.pi / 2.0) / nt
                st, ct = math.sin(t), math.cos(t)
                d = ggx_d(ct, a)
                ring = 0.0
                for j in range(npf):
                    p = (j + 0.5) * 2.0 * math.pi / npf
                    om = o[0] * st * math.cos(p) + o[2] * ct
                    ring += max(0.0, om)
                total += d * st * ring
            total *= (math.pi / 2.0 / nt) * (2.0 * math.pi / npf) * g1(o[2], a) / o[2]
            assert abs(total - 1.0) < 2e-3


def test_weak_white_furnace_monte_carlo() -> None:
    rng = random.Random(7)
    for a in (0.3, 1.0):
        for deg in (30.0, 70.0):
            mean, se = weak_furnace(math.radians(deg), a, rng, 20000)
            assert abs(mean - 1.0) < 4.0 * se
