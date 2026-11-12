# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gradient-temporal-difference/. The authors are listed in prov/065TYG.jsonl.

import math
import random
from fractions import Fraction as F

from gradient_temporal_difference import (
    BAIRD_THETA0,
    as_fractions,
    baird,
    expected_matrices,
    expected_step,
    gradient_td,
    off_policy_semi_gradient_td,
)

G = 0.99
FEATS, SAMPLE = baird()
P_TARGET = [[0.0] * 6 + [1.0] for _ in range(7)]

CHAIN_P = [[0.5, 0.5, 0.0], [0.25, 0.5, 0.25], [0.0, 0.5, 0.5]]
CHAIN_PHI = [[1.0, 0.0], [1.0, 1.0], [1.0, 3.0]]
CHAIN_MU = [0.25, 0.5, 0.25]
THETA_TD = [185 / 109, 70 / 109]


def values(theta):
    return [sum(a * b for a, b in zip(f, theta)) for f in FEATS]


def rms_bellman_error(theta):
    v = values(theta)
    return math.sqrt(sum((G * v[6] - x) ** 2 for x in v) / 7)


def test_semi_gradient_td_diverges_on_baird() -> None:
    for seed in range(3):
        th = off_policy_semi_gradient_td(SAMPLE, BAIRD_THETA0, G, lambda k: 0.01, 3000, random.Random(seed))
        assert math.hypot(*th) > 1000


def test_tdc_and_gtd2_stay_bounded_on_baird() -> None:
    for variant in ("tdc", "gtd2"):
        for seed in range(3):
            th, w = gradient_td(SAMPLE, BAIRD_THETA0, G, lambda k: 0.005, lambda k: 0.05, 10000, random.Random(seed), variant)
            assert math.hypot(*th) < 11 and math.hypot(*w) < 5
            assert rms_bellman_error(th) < 0.05 < rms_bellman_error(BAIRD_THETA0)


def test_expected_updates_on_baird() -> None:
    a, b, c, e = expected_matrices(FEATS, [1 / 7] * 7, P_TARGET, [0.0] * 7, G)
    td, th, w = BAIRD_THETA0, BAIRD_THETA0, [0.0] * 8
    for _ in range(3000):
        td, _ = expected_step(td, None, a, b, c, e, G, 0.01, 0, "td")
        th, w = expected_step(th, w, a, b, c, e, G, 0.005, 0.05, "tdc")
    assert math.hypot(*td) > 1e4
    assert math.hypot(*th) < 11 and rms_bellman_error(th) < 0.05


def test_td_fixed_point_is_stationary_exactly() -> None:
    feats = as_fractions(CHAIN_PHI)
    a, b, c, e = expected_matrices(feats, [F(1, 4), F(1, 2), F(1, 4)], as_fractions(CHAIN_P), [F(0), F(0), F(1)], F(9, 10))
    theta = [F(185, 109), F(70, 109)]
    zero = [F(0), F(0)]
    for variant in ("tdc", "gtd2"):
        th, w = expected_step(theta, zero, a, b, c, e, F(9, 10), F(1, 10), F(1, 10), variant)
        assert th == theta and w == zero
    residual = [b[i] - sum(a[i][j] * theta[j] for j in range(2)) for i in range(2)]
    assert residual == zero  # MSPBE(theta) = residual^T C^(-1) residual = 0


def test_expected_ode_converges_on_chain() -> None:
    a, b, c, e = expected_matrices(CHAIN_PHI, CHAIN_MU, CHAIN_P, [0.0, 0.0, 1.0], 0.9)
    for variant in ("tdc", "gtd2"):
        th, w = [0.0, 0.0], [0.0, 0.0]
        for _ in range(40000):
            th, w = expected_step(th, w, a, b, c, e, 0.9, 0.05, 0.5, variant)
        assert math.dist(th, THETA_TD) < 1e-6 and math.hypot(*w) < 1e-6


def chain_sample(rng):
    s = rng.choices(range(3), weights=CHAIN_MU)[0]
    s2 = rng.choices(range(3), weights=CHAIN_P[s])[0]
    return CHAIN_PHI[s], 1.0, 1.0 if s == 2 else 0.0, CHAIN_PHI[s2]


def test_sampled_on_policy_approaches_td_fixed_point() -> None:
    for variant in ("tdc", "gtd2"):
        runs = [
            gradient_td(chain_sample, [0.0, 0.0], 0.9, lambda k: 0.05 / (1 + k / 2000), lambda k: 0.2 / (1 + k / 2000) ** 0.6, 60000, random.Random(s), variant)[0]
            for s in range(3)
        ]
        mean = [sum(t[i] for t in runs) / 3 for i in range(2)]
        assert math.dist(mean, THETA_TD) < 0.08


def test_rejects_unknown_variant() -> None:
    try:
        gradient_td(chain_sample, [0.0, 0.0], 0.9, lambda k: 0.1, lambda k: 0.1, 1, random.Random(0), "gtd3")
    except ValueError:
        return
    raise AssertionError("expected ValueError")
