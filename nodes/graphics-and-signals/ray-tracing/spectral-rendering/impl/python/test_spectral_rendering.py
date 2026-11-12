# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spectral-rendering/. The authors are listed in prov/F2PT3X.jsonl.

import math
import random

from spectral_rendering import (
    LAMBDA_MAX,
    LAMBDA_MIN,
    cauchy_index,
    cmf_xyz,
    estimate_xyz,
    hero_wavelengths,
    refraction_angle,
    spectrum_to_xyz,
    xyz_to_linear_srgb,
)

# Tabulated CIE 1931 values, the reference for the fit: the integral of y-bar over 360 to 830 nm,
# and the values at the peak of y-bar.
CIE_INTEGRAL_YBAR = 106.857
CIE_YBAR_555 = 1.0


def flat(lam):
    return 1.0


def green(lam):
    return math.exp(-0.5 * ((lam - 520.0) / 30.0) ** 2)


def gram_null_vector():
    """A reflectance change on a 1 nm grid that is orthogonal to all three color matching functions.

    Built by Gram-Schmidt style projection: a sine is reduced by its least squares fit in the span
    of the color matching functions, solved by Gaussian elimination on the 3 x 3 normal equations.
    """
    grid = [LAMBDA_MIN + 0.5 + i for i in range(int(LAMBDA_MAX - LAMBDA_MIN))]
    cm = [cmf_xyz(lam) for lam in grid]
    base = [math.sin(2.0 * math.pi * (lam - 400.0) / 80.0) for lam in grid]
    g = [[sum(c[i] * c[j] for c in cm) for j in range(3)] for i in range(3)]
    r = [sum(c[i] * b for c, b in zip(cm, base)) for i in range(3)]
    for i in range(3):
        for j in range(i + 1, 3):
            f = g[j][i] / g[i][i]
            for k in range(3):
                g[j][k] -= f * g[i][k]
            r[j] -= f * r[i]
    coef = [0.0, 0.0, 0.0]
    for i in (2, 1, 0):
        coef[i] = (r[i] - sum(g[i][j] * coef[j] for j in range(i + 1, 3))) / g[i][i]
    m = [b - sum(coef[i] * c[i] for i in range(3)) for b, c in zip(base, cm)]
    return grid, m


def grid_xyz(grid, values):
    sx = sy = sz = 0.0
    for lam, v in zip(grid, values):
        cx, cy, cz = cmf_xyz(lam)
        sx += cx * v
        sy += cy * v
        sz += cz * v
    return (sx, sy, sz)


def test_fit_matches_cie_tables():
    y = spectrum_to_xyz(flat)[1]
    assert abs(y - CIE_INTEGRAL_YBAR) / CIE_INTEGRAL_YBAR < 1e-3
    assert abs(cmf_xyz(555.0)[1] - CIE_YBAR_555) < 0.01
    # The equal energy white has the chromaticity (1/3, 1/3) in CIE 1931.
    x, y, z = spectrum_to_xyz(flat)
    assert abs(x / (x + y + z) - 1.0 / 3.0) < 2e-3
    assert abs(y / (x + y + z) - 1.0 / 3.0) < 2e-3


def test_hero_wavelengths_are_equally_spaced():
    for u in (0.0, 0.3, 0.99):
        ws = sorted(hero_wavelengths(u, 4))
        assert all(LAMBDA_MIN <= w < LAMBDA_MAX for w in ws)
        gaps = [b - a for a, b in zip(ws, ws[1:])] + [ws[0] + (LAMBDA_MAX - LAMBDA_MIN) - ws[-1]]
        for gap in gaps:
            assert abs(gap - (LAMBDA_MAX - LAMBDA_MIN) / 4) < 1e-9


def test_estimators_are_unbiased():
    # Reference: the midpoint quadrature. Bound: 4 standard errors of the mean, estimated from
    # independent batches, so a correct estimator fails with probability below 1e-4 per channel.
    for spectrum in (flat, green):
        ref = spectrum_to_xyz(spectrum)
        for count in (1, 4):
            rng = random.Random(2014 + count)
            batches = [estimate_xyz(spectrum, rng, 500, count) for _ in range(40)]
            for ch in range(3):
                vals = [b[ch] for b in batches]
                mean = sum(vals) / len(vals)
                var = sum((v - mean) ** 2 for v in vals) / (len(vals) - 1)
                se = math.sqrt(var / len(vals))
                assert abs(mean - ref[ch]) <= 4.0 * se + 1e-9


def test_hero_sampling_reduces_variance():
    # For the same number of hero samples, four wavelengths per sample must have a smaller spread
    # than one. The measured ratios of the variances are about 140 for the flat spectrum and 10 for
    # the green one; the bounds leave a wide margin for the sampling noise of 200 batches.
    for spectrum, bound in ((flat, 20.0), (green, 3.0)):
        spread = {}
        for count in (1, 4):
            rng = random.Random(7)
            ys = [estimate_xyz(spectrum, rng, 1, count)[1] for _ in range(2000)]
            m = sum(ys) / len(ys)
            spread[count] = sum((y - m) ** 2 for y in ys) / (len(ys) - 1)
        assert spread[1] > bound * spread[4]


def test_metamers_match_under_one_light_only():
    grid, m = gram_null_vector()
    eps = 0.4 / max(abs(v) for v in m)
    ra = [0.5] * len(grid)
    rb = [0.5 + eps * v for v in m]
    assert min(rb) >= 0.0 and max(rb) <= 1.0
    xa = grid_xyz(grid, ra)
    xb = grid_xyz(grid, rb)
    for a, b in zip(xa, xb):
        assert abs(a - b) < 1e-9 * abs(a)

    def lines(lam):
        return 0.2 + sum(math.exp(-0.5 * ((lam - c) / 5.0) ** 2) for c in (436.0, 546.0, 611.0))

    la = grid_xyz(grid, [r * lines(lam) for r, lam in zip(ra, grid)])
    lb = grid_xyz(grid, [r * lines(lam) for r, lam in zip(rb, grid)])
    assert abs(la[1] - lb[1]) / la[1] > 0.1


def test_rgb_product_is_not_the_spectral_product():
    # Light and surface as spectra, against the product of their linear sRGB values.
    def refl(lam):
        return math.exp(-0.5 * ((lam - 600.0) / 20.0) ** 2)

    exact = xyz_to_linear_srgb(spectrum_to_xyz(lambda lam: refl(lam) * green(lam)))
    norm = 1.0 / spectrum_to_xyz(flat)[1]
    r1 = xyz_to_linear_srgb(tuple(norm * c for c in spectrum_to_xyz(refl)))
    r2 = xyz_to_linear_srgb(spectrum_to_xyz(green))
    approx = tuple(a * b for a, b in zip(r1, r2))
    assert exact[0] > 0.0 > approx[0]


def test_dispersion_of_crown_glass():
    # Reference values of BK7: n_d = 1.5168 at 587.6 nm, Abbe number about 64.2.
    nd = cauchy_index(587.6)
    nf = cauchy_index(486.1)
    nc = cauchy_index(656.3)
    assert abs(nd - 1.5168) < 2e-4
    assert abs((nd - 1.0) / (nf - nc) - 64.2) < 1.0
    t_blue = refraction_angle(math.radians(45.0), 1.0, cauchy_index(400.0))
    t_red = refraction_angle(math.radians(45.0), 1.0, cauchy_index(700.0))
    assert t_blue < t_red
    assert abs(math.degrees(t_red - t_blue) - 0.349) < 0.005
    # Snell's law holds at each wavelength.
    for lam in (400.0, 550.0, 700.0):
        n = cauchy_index(lam)
        t = refraction_angle(math.radians(45.0), 1.0, n)
        assert abs(math.sin(math.radians(45.0)) - n * math.sin(t)) < 1e-12
    assert math.isnan(refraction_angle(math.radians(60.0), cauchy_index(550.0), 1.0))
