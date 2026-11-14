# SPDX-License-Identifier: MIT
# Shared helper of the pe1 statistics pages of https://algorithm.tamnd.com/. The authors are listed in prov/.

import math

from stdist import (
    beta_inc, chi2_cdf, chi2_ppf, chi2_sf, f_cdf, f_ppf, f_sf, gamma_p, gamma_q,
    norm_cdf, norm_ppf, norm_sf, t_cdf, t_ppf, t_sf,
)

XS = [0.001, 0.01, 0.1, 0.3, 0.5, 1.0, 1.7, 2.5, 4.0, 7.0, 12.0, 30.0, 80.0]


def test_chi2_two_degrees_of_freedom() -> None:
    for x in XS:
        assert abs(chi2_cdf(x, 2) - (1.0 - math.exp(-x / 2.0))) < 1e-13
        assert abs(chi2_sf(x, 2) - math.exp(-x / 2.0)) <= 1e-12 * math.exp(-x / 2.0)


def test_t_one_and_two_degrees_of_freedom() -> None:
    for x in XS + [-v for v in XS] + [0.0]:
        assert abs(t_cdf(x, 1) - (0.5 + math.atan(x) / math.pi)) < 1e-13
        assert abs(t_cdf(x, 2) - (0.5 + x / (2.0 * math.sqrt(2.0 + x * x)))) < 1e-13
        assert abs(t_cdf(x, 3) + t_sf(x, 3) - 1.0) < 1e-14


def test_f_is_square_of_t() -> None:
    for k in [1, 2, 3, 5, 10, 30]:
        for x in XS:
            two_sided = 2.0 * t_sf(math.sqrt(x), k)
            assert abs(f_sf(x, 1, k) - two_sided) < 1e-13
            assert abs(f_cdf(x, 1, k) + f_sf(x, 1, k) - 1.0) < 1e-14


def test_gamma_and_beta_identities() -> None:
    for a in [0.5, 1.0, 2.5, 10.0, 50.0]:
        for x in XS:
            assert abs(gamma_p(a, x) + gamma_q(a, x) - 1.0) < 1e-14
    # P(1, x) = 1 - e^(-x); I_x(a, 1) = x^a; I_x(1, b) = 1 - (1 - x)^b.
    for x in [0.05, 0.3, 0.5, 0.8, 0.99]:
        assert abs(gamma_p(1.0, x) - (1.0 - math.exp(-x))) < 1e-14
        for a in [0.5, 2.0, 7.0]:
            assert abs(beta_inc(a, 1.0, x) - x**a) < 1e-13
            assert abs(beta_inc(1.0, a, x) - (1.0 - (1.0 - x) ** a)) < 1e-13


def test_upper_tails_do_not_cancel() -> None:
    assert abs(norm_sf(10.0) / 7.619853024160527e-24 - 1.0) < 1e-12
    assert abs(chi2_sf(200.0, 2) / math.exp(-100.0) - 1.0) < 1e-12
    assert norm_cdf(-30.0) > 0.0

def test_quantiles() -> None:
    assert abs(norm_ppf(0.975) - 1.959963985) < 1e-8
    assert abs(chi2_ppf(0.95, 1) - 3.841458821) < 1e-8
    assert abs(t_ppf(0.975, 10) - 2.228138852) < 1e-8
    for p in [1e-6, 0.01, 0.2, 0.5, 0.8, 0.99, 1.0 - 1e-6]:
        for k in [1, 4, 25]:
            assert abs(chi2_cdf(chi2_ppf(p, k), k) - p) < 1e-12
            assert abs(t_cdf(t_ppf(p, k), k) - p) < 1e-12
            assert abs(f_cdf(f_ppf(p, k, 7), k, 7) - p) < 1e-12
