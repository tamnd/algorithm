# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/progressive-photon-mapping/. The authors are listed in prov/N56HR0.jsonl.

import math
import random
from fractions import Fraction

from progressive_photon_mapping import (
    density_is_kept,
    disc_average,
    irradiance,
    knaus_zwicker_radius2,
    progressive_photon_mapping,
    shrink,
)

PHI, H = 1.0, 1.0
POINTS = [(0.0, 0.0), (0.5, 0.0), (1.0, 0.0)]


def _mean_se(values):
    m = sum(values) / len(values)
    var = sum((v - m) ** 2 for v in values) / (len(values) - 1)
    return m, math.sqrt(var / len(values))


def test_density_is_kept_exactly():
    for n in [Fraction(0), Fraction(3), Fraction(77, 10), Fraction(1000)]:
        for m in [1, 2, 5, 40, 999]:
            for alpha in [Fraction(1, 2), Fraction(7, 10), Fraction(9, 10), Fraction(1)]:
                assert density_is_kept(n, m, Fraction(1, 4), alpha)


def test_shrink_never_grows_the_radius():
    n, r2, tau = 0.0, 0.25, 0.0
    rng = random.Random(1)
    for _ in range(200):
        m = rng.randrange(0, 30)
        n2, r2n, tau2 = shrink(n, m, r2, tau, m * 0.001, 0.7)
        assert r2n <= r2
        assert n2 >= n
        if m > 0:
            assert r2n < r2
        n, r2, tau = n2, r2n, tau2
    assert r2 < 0.25 * 0.2


def test_alpha_one_is_fixed_radius():
    n, r2, tau = shrink(10.0, 7, 0.09, 0.5, 0.25, 1.0)
    assert (n, r2) == (17.0, 0.09)
    assert math.isclose(tau, 0.75, rel_tol=1e-15)


def test_knaus_zwicker_radius_matches_gamma_form():
    alpha = 0.7
    for i in [1, 2, 10, 100, 1000]:
        exact = math.exp(math.lgamma(i + alpha) - math.lgamma(1 + alpha) - math.lgamma(i + 1))
        assert math.isclose(knaus_zwicker_radius2(1.0, i, alpha), exact, rel_tol=1e-12)
    # r_i^2 i^(1 - alpha) tends to 1 / Gamma(1 + alpha), so r_i^2 = O(i^(alpha - 1)).
    big = knaus_zwicker_radius2(1.0, 100000, alpha) * 100000 ** (1 - alpha)
    assert math.isclose(big, 1 / math.gamma(1 + alpha), rel_tol=1e-4)


def _foot_runs(passes, alpha, seeds):
    est, rad = [], []
    for seed in seeds:
        e, hps = progressive_photon_mapping(POINTS[:1], 0.5, passes, 1000, PHI, H, random.Random(seed), alpha=alpha)
        est.append(e[0])
        rad.append(math.sqrt(hps[0].radius2))
    return est, rad


def test_fixed_radius_converges_to_the_disc_average_not_the_answer():
    est, _ = _foot_runs(64, 1.0, range(10))
    m, se = _mean_se(est)
    target = disc_average(PHI, H, 0.5)
    assert abs(m - target) < 4 * se
    assert m / irradiance(PHI, H, 0.0) - 1 < -0.12  # the bias stays near -15.5 %


def test_progressive_bias_shrinks_with_passes():
    exact = irradiance(PHI, H, 0.0)
    fixed, _ = _foot_runs(64, 1.0, range(200, 210))
    ppm, rad = _foot_runs(64, 0.7, range(200, 210))
    m_fixed, _ = _mean_se(fixed)
    m_ppm, se_ppm = _mean_se(ppm)
    err_fixed = m_fixed / exact - 1
    err_ppm = m_ppm / exact - 1
    # The same photons: the fixed radius keeps a bias near -15.5 %, PPM is near -5 % after 64 passes.
    assert sum(rad) / len(rad) < 0.3
    assert abs(err_ppm) < 0.09
    assert abs(err_ppm) < 0.6 * abs(err_fixed)
    # The mean-field model of the recursion predicts -5.4 % at 64 passes.
    assert abs(m_ppm - exact * (1 - 0.054)) < 4 * se_ppm + 0.01 * exact


def test_off_axis_points_get_photons_and_shrink():
    est, hps = progressive_photon_mapping(POINTS, 0.5, 8, 1000, PHI, H, random.Random(7))
    for e, h, (s, _) in zip(est, hps, POINTS):
        assert h.n > 0
        assert h.radius2 < 0.25
        assert abs(e / irradiance(PHI, H, s) - 1) < 0.3
