# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/direct-fourier-reconstruction/. The authors are listed in prov/1BAE5C.jsonl.

import cmath
import math
import random

import imgkit as ik
from direct_fourier_reconstruction import (
    direct_fourier_reconstruction,
    polar_spectra,
    polar_value,
    spectrum_to_image,
)

A, D, N = 32, 47, 32
TAU = 2.0 * math.sqrt(2.0) / D  # the bins cover [-sqrt(2), sqrt(2)], as in imgkit
W = 0.5  # f(x) = exp(-pi |x|^2 / W^2), R f = W exp(-pi s^2 / W^2), F f = W^2 exp(-pi W^2 |xi|^2)


def ellipse_projection(table, theta, s):
    """The exact Radon transform of an ellipse table (Kak and Slaney, chapter 3)."""
    total = 0.0
    for rho, a, b, x0, y0, phi in table:
        t = theta - math.radians(phi)
        u = s - (x0 * math.cos(theta) + y0 * math.sin(theta))
        a2 = a * a * math.cos(t) ** 2 + b * b * math.sin(t) ** 2
        if u * u < a2:
            total += 2.0 * rho * a * b / a2 * math.sqrt(a2 - u * u)
    return total


def sinogram(fun, a=A, d=D, tau=TAU):
    return [[fun(k * math.pi / a, (j - (d - 1) / 2.0) * tau) for j in range(d)] for k in range(a)]


def gauss_proj(theta, s):
    return W * math.exp(-math.pi * s * s / (W * W))


def gauss_ft(rho):
    return W * W * math.exp(-math.pi * W * W * rho * rho)


def test_slice_step_matches_analytic_transform() -> None:
    # Fourier slice: the scaled DFT of each projection samples F f on its radial line.
    for d in (47, 48):  # odd and even detectors
        tau = 2.0 * math.sqrt(2.0) / d
        spectra, length = polar_spectra(sinogram(gauss_proj, 4, d, tau), tau)
        for row in spectra:
            for l in range(length):
                sigma = (l if l < length // 2 else l - length) / (length * tau)
                assert abs(row[l] - gauss_ft(sigma)) < 1e-9


def test_grid_to_image_is_exact_on_exact_spectrum() -> None:
    big = 2 * N
    dxi = N / (2.0 * big)
    g = [[0j] * big for _ in range(big)]
    for v in range(-big // 2, big // 2):
        for u in range(-big // 2, big // 2):
            val = gauss_ft(math.hypot(u * dxi, v * dxi))
            g[v % big][u % big] = val * cmath.exp(1j * math.pi * (u + v) / big) * dxi * dxi
    img = spectrum_to_image(g, N)
    xs, ys = ik.pixel_centers(N)
    err = max(abs(img[i][j] - math.exp(-math.pi * (xs[j] ** 2 + ys[i] ** 2) / W ** 2)) for i in range(N) for j in range(N))
    assert err < 1e-12


def test_polar_value_hermitian_and_close_to_truth() -> None:
    spectra, length = polar_spectra(sinogram(gauss_proj), TAU)
    rng = random.Random(7)
    for _ in range(200):
        x, y = rng.uniform(-6, 6), rng.uniform(-6, 6)
        p, m = polar_value(spectra, length, TAU, x, y), polar_value(spectra, length, TAU, -x, -y)
        assert abs(p - m.conjugate()) < 1e-12
        assert abs(p - gauss_ft(math.hypot(x, y))) < 0.01  # bilinear interpolation on the polar grid
    assert polar_value(spectra, length, TAU, 10.0, 0.0) == 0  # outside the band 1 / (2 tau)
    # the wrap at angle pi: the values just above and just below the negative x axis agree
    above = polar_value(spectra, length, TAU, -3.0, 1e-9)
    below = polar_value(spectra, length, TAU, -3.0, -1e-9)
    assert abs(above - below) < 1e-9


def test_gaussian_known_answer() -> None:
    img = direct_fourier_reconstruction(sinogram(gauss_proj), TAU, N)
    xs, ys = ik.pixel_centers(N)
    err = max(abs(img[i][j] - math.exp(-math.pi * (xs[j] ** 2 + ys[i] ** 2) / W ** 2)) for i in range(N) for j in range(N))
    assert err < 0.003  # measured 0.0005 for a = 32, d = 47, n = 32


def test_disk_interior() -> None:
    sino = sinogram(lambda th, s: 2.0 * math.sqrt(0.25 - s * s) if s * s < 0.25 else 0.0)
    img = direct_fourier_reconstruction(sino, TAU, N)
    xs, ys = ik.pixel_centers(N)
    inner = [img[i][j] for i in range(N) for j in range(N) if xs[j] ** 2 + ys[i] ** 2 < 0.35 ** 2]
    outer = [img[i][j] for i in range(N) for j in range(N) if xs[j] ** 2 + ys[i] ** 2 > 0.65 ** 2]
    assert max(abs(v - 1.0) for v in inner) < 0.03  # measured 0.0125
    assert max(abs(v) for v in outer) < 0.06  # measured 0.030


def test_shepp_logan_linear_beats_nearest() -> None:
    sino = sinogram(lambda th, s: ellipse_projection(ik.SHEPP_LOGAN, th, s))
    xs, ys = ik.pixel_centers(N)
    inside = [(i, j) for i in range(N) for j in range(N) if xs[j] ** 2 + ys[i] ** 2 < 0.35 ** 2]
    errs = {}
    for interp in ("linear", "nearest"):
        img = direct_fourier_reconstruction(sino, TAU, N, interp=interp)
        errs[interp] = max(abs(img[i][j] - ik.ellipse_value(xs[j], ys[i], ik.SHEPP_LOGAN)) for i, j in inside)
        if interp == "linear":
            assert abs(img[16][16] - 1.02) < 0.05  # measured 1.048
    assert errs["linear"] < errs["nearest"]  # measured 0.072 and 0.184


def test_linear_and_zero() -> None:
    rng = random.Random(3)
    s1 = [[rng.uniform(0, 1) for _ in range(9)] for _ in range(4)]
    s2 = [[rng.uniform(0, 1) for _ in range(9)] for _ in range(4)]
    s3 = [[u + 2.0 * v for u, v in zip(r1, r2)] for r1, r2 in zip(s1, s2)]
    f1, f2, f3 = (direct_fourier_reconstruction(s, 0.3, 6) for s in (s1, s2, s3))
    assert max(abs(f3[i][j] - f1[i][j] - 2.0 * f2[i][j]) for i in range(6) for j in range(6)) < 1e-12
    z = direct_fourier_reconstruction([[0.0] * 9 for _ in range(4)], 0.3, 6)
    assert all(v == 0.0 for row in z for v in row)
