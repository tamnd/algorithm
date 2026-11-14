# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kde-bandwidth-selection/. The authors are listed in prov/677AW6.jsonl.

import math
import random

from kde_bandwidth_selection import (
    RK, dpi_bandwidth, exact_mise_mixture, golden_min, hermite, iqr, kde, lscv,
    lscv_bandwidth, normal_reference, phi, psi_hat, psi_normal, sample_sd, silverman,
)

PAGE = [-1.9, -1.6, -1.5, -1.3, -1.2, -1.0, -0.8, 0.9, 1.1, 1.2, 1.4, 1.5, 1.7, 2.0]


def simpson(f, a, b, m):
    step = (b - a) / m
    s = f(a) + f(b)
    for k in range(1, m):
        s += (4 if k % 2 else 2) * f(a + k * step)
    return s * step / 3


def test_page_example() -> None:
    assert abs(sample_sd(PAGE) - 1.46056) < 1e-5
    assert abs(iqr(PAGE) - 2.625) < 1e-12
    assert abs(normal_reference(PAGE) - 0.9126) < 1e-4
    assert abs(silverman(PAGE) - 0.7754) < 1e-4
    assert abs(lscv_bandwidth(PAGE) - 0.4643) < 1e-4
    assert abs(dpi_bandwidth(PAGE) - 0.5365) < 1e-4


def test_rules_match_their_formulas() -> None:
    rng = random.Random(61)
    for _ in range(20):
        n = rng.randint(5, 60)
        d = [rng.gauss(3, 2) for _ in range(n)]
        s = sample_sd(d)
        assert abs(normal_reference(d) - (4 / 3) ** 0.2 * s * n ** -0.2) < 1e-12
        # The normal reference rule is Theorem 4 of the KDE page with R(f'') of N(0, s^2).
        rf2 = psi_normal(4, s)
        assert abs(normal_reference(d) - (RK / (rf2 * n)) ** 0.2) < 1e-12
        assert abs(silverman(d) - 0.9 * min(s, iqr(d) / 1.34) * n ** -0.2) < 1e-12
    # With one far outlier the IQR branch is used.
    d = [float(v) for v in range(20)] + [1000.0]
    assert iqr(d) / 1.34 < sample_sd(d)
    assert abs(silverman(d) - 0.9 * 10 / 1.34 * 21 ** -0.2) < 1e-12


def test_psi_normal_against_quadrature() -> None:
    # psi_r = integral f^(r) f, and f^(r)(x) = He_r(x) phi(x) for even r and sigma = 1.
    for r in (4, 6, 8):
        num = simpson(lambda x: hermite(r, x) * phi(x) ** 2, -12, 12, 4000)
        assert abs(num - psi_normal(r, 1.0)) < 1e-10
    assert abs(psi_normal(4, 1.0) - 3 / (8 * math.sqrt(math.pi))) < 1e-15


def test_lscv_closed_form_against_definition() -> None:
    rng = random.Random(62)
    d = [rng.gauss(0, 1) for _ in range(25)]
    for h in (0.15, 0.4, 0.9):
        a, b = min(d) - 10 * h, max(d) + 10 * h
        rf = simpson(lambda x: kde(x, d, h) ** 2, a, b, 6000)
        loo = sum(kde(d[i], d[:i] + d[i + 1:], h) for i in range(len(d)))
        assert abs(lscv(h, d) - (rf - 2 * loo / len(d))) < 1e-9


def test_psi_hat_against_quadrature() -> None:
    # n^-2 sum phi_g^(r)(X_i - X_j) = (-1)^(r/2) integral (f_a^(r/2))^2 with a = g / sqrt 2.
    rng = random.Random(63)
    d = [rng.gauss(0, 1) for _ in range(20)]
    for r, g in ((4, 0.5), (6, 0.7)):
        a, s = g / math.sqrt(2), r // 2

        def deriv(x):  # the s-th derivative of the estimate with bandwidth a
            return sum((-1) ** s * hermite(s, (x - xi) / a) * phi((x - xi) / a)
                       for xi in d) / (len(d) * a ** (s + 1))

        num = simpson(lambda x: deriv(x) ** 2, min(d) - 12 * a, max(d) + 12 * a, 6000)
        assert abs(psi_hat(r, g, d) - (-1) ** s * num) < 1e-8 * abs(num)


def test_lscv_bandwidth_is_the_grid_minimum() -> None:
    rng = random.Random(64)
    d = [rng.gauss(0, 1) for _ in range(30)] + [rng.gauss(4, 0.5) for _ in range(15)]
    h = lscv_bandwidth(d)
    s = sample_sd(d)
    best = min(lscv(s * (0.05 + k * 0.005), d) for k in range(391))
    assert lscv(h, d) <= best + 1e-12


def test_exact_mise_against_quadrature() -> None:
    w, mu, sd = [0.3, 0.7], [-1.0, 2.0], [0.6, 1.2]
    f_conv = lambda x, s2: sum(wl * phi((x - m) / math.sqrt(v + s2)) / math.sqrt(v + s2)
                               for wl, m, v in zip(w, mu, [t * t for t in sd]))
    for n, h in ((10, 0.5), (200, 0.3)):
        def mse(x):
            mean = f_conv(x, h * h)
            ek2 = f_conv(x, h * h / 2) / (2 * h * math.sqrt(math.pi))
            return (mean - f_conv(x, 0.0)) ** 2 + (ek2 - mean * mean) / n
        num = simpson(mse, -10, 12, 4000)
        assert abs(exact_mise_mixture(h, n, w, mu, sd) - num) < 1e-10


def test_selectors_on_normal_and_bimodal_data() -> None:
    # Measured behaviour for fixed seeds, not a guarantee.
    rng = random.Random(7)
    n = 300
    d = [rng.gauss(0, 1) for _ in range(n)]
    h_mise = golden_min(lambda h: exact_mise_mixture(h, n, [1], [0], [1]), 0.01, 3)
    assert abs(dpi_bandwidth(d) / h_mise - 1) < 0.1
    assert abs(normal_reference(d) / h_mise - 1) < 0.1
    # Separated bimodal: the normal reference rule oversmooths badly.
    w, mu, sd = [0.5, 0.5], [-1.5, 1.5], [0.5, 0.5]
    rng = random.Random(2)
    n = 200
    d = [rng.gauss(mu[c], sd[c]) for c in (rng.randrange(2) for _ in range(n))]
    h_mise = golden_min(lambda h: exact_mise_mixture(h, n, w, mu, sd), 0.01, 3)
    best = exact_mise_mixture(h_mise, n, w, mu, sd)
    ratio = lambda h: exact_mise_mixture(h, n, w, mu, sd) / best
    assert ratio(normal_reference(d)) > 3
    assert ratio(silverman(d)) > 2
    assert ratio(dpi_bandwidth(d)) < 1.3
