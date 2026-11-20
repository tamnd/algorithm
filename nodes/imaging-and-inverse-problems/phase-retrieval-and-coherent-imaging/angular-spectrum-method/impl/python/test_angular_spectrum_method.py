# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/angular-spectrum-method/. The authors are listed in prov/BPG5QE.jsonl.

import cmath
import math
import random

from angular_spectrum_method import (
    angular_spectrum,
    angular_spectrum_padded,
    band_limit,
    frequencies,
    fresnel_transfer,
    transfer_function,
)
from imgkit import dft2, img_dot, img_norm


def rand_field(rng, n1, n2):
    return [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(n2)] for _ in range(n1)]


def max_diff(a, b):
    return max(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb))


def direct_propagation(u, d, wavelength, z):
    """Reference: the sum of plane waves with explicit O(n^4) Fourier sums, no FFT."""
    n1, n2 = len(u), len(u[0])
    fys, fxs = frequencies(n1, d), frequencies(n2, d)
    coef = {}
    for k in range(n1):
        for l in range(n2):
            c = sum(u[i][j] * cmath.exp(-2j * math.pi * (i * k / n1 + j * l / n2)) for i in range(n1) for j in range(n2))
            w = 1.0 / wavelength ** 2 - fxs[l] ** 2 - fys[k] ** 2
            coef[k, l] = c * cmath.exp(2j * math.pi * z * math.sqrt(w)) if w > 0 else 0j
    out = []
    for i in range(n1):
        row = []
        for j in range(n2):
            row.append(sum(v * cmath.exp(2j * math.pi * (i * k / n1 + j * l / n2)) for (k, l), v in coef.items()) / (n1 * n2))
        out.append(row)
    return out


def test_plane_wave_gets_the_phase_of_h():
    n, d, lam, z = 8, 1.0, 0.5, 3.7
    for kx, ky in ((0, 0), (1, 0), (2, -3), (-4, 3)):
        fx, fy = kx / (n * d), ky / (n * d)
        u = [[cmath.exp(2j * math.pi * (fx * j * d + fy * i * d)) for j in range(n)] for i in range(n)]
        out = angular_spectrum(u, d, lam, z)
        g = cmath.exp(2j * math.pi * z * math.sqrt(1 / lam ** 2 - fx * fx - fy * fy))
        assert max_diff(out, [[g * v for v in row] for row in u]) < 1e-12


def test_matches_direct_plane_wave_sum():
    rng = random.Random(3)
    u = rand_field(rng, 6, 8)
    for d, lam in ((1.0, 0.5), (0.3, 0.5)):  # all waves propagate; some are evanescent
        a = angular_spectrum(u, d, lam, 2.5)
        b = direct_propagation(u, d, lam, 2.5)
        assert max_diff(a, b) < 1e-10


def test_worked_example():
    out = angular_spectrum([[0, 0, 0, 1, 1, 0, 0, 0]], 1.0, 0.5, 10.0)
    inten = [abs(v) ** 2 for v in out[0]]
    want = [0.0025, 0.0405, 0.2465, 0.7105, 0.7105, 0.2465, 0.0405, 0.0025]
    assert all(abs(a - b) < 5e-5 for a, b in zip(inten, want))
    assert abs(sum(inten) - 2.0) < 1e-12


def test_parseval_on_propagating_band():
    rng = random.Random(5)
    u = rand_field(rng, 8, 8)
    # d = 1 and lambda = 0.5: every grid frequency propagates, so the energy is kept.
    out = angular_spectrum(u, 1.0, 0.5, 7.0)
    assert abs(img_norm(out) - img_norm(u)) < 1e-10 * img_norm(u)


def test_evanescent_energy_is_removed():
    rng = random.Random(6)
    u = rand_field(rng, 8, 8)
    d, lam = 0.2, 0.5  # max |f| = 2.5 * sqrt(2) > 1 / lambda = 2
    spec = dft2(u)
    fs = frequencies(8, d)
    band = sum(abs(spec[k][l]) ** 2 for k in range(8) for l in range(8) if fs[k] ** 2 + fs[l] ** 2 < 1 / lam ** 2) / 64
    out = angular_spectrum(u, d, lam, 1.3)
    assert abs(img_norm(out) ** 2 - band) < 1e-9 * band
    assert img_norm(out) < img_norm(u)


def test_forward_then_back_is_projection_on_band():
    rng = random.Random(7)
    u = rand_field(rng, 8, 8)
    d, lam, z = 0.2, 0.5, 4.0
    back = angular_spectrum(angular_spectrum(u, d, lam, z), d, lam, -z)
    proj = angular_spectrum(u, d, lam, 0.0)  # z = 0 keeps exactly the propagating band
    assert max_diff(back, proj) < 1e-11
    # On a grid where every wave propagates, z then -z is the identity.
    back2 = angular_spectrum(angular_spectrum(u, 1.0, lam, z), 1.0, lam, -z)
    assert max_diff(back2, u) < 1e-11


def test_composition_of_distances():
    rng = random.Random(8)
    u = rand_field(rng, 8, 8)
    a = angular_spectrum(angular_spectrum(u, 0.4, 0.5, 1.5), 0.4, 0.5, 2.25)
    b = angular_spectrum(u, 0.4, 0.5, 3.75)
    assert max_diff(a, b) < 1e-11


def test_adjoint_is_back_propagation():
    rng = random.Random(9)
    x, y = rand_field(rng, 8, 8), rand_field(rng, 8, 8)
    d, lam, z = 0.25, 0.5, 2.0
    ax = angular_spectrum(x, d, lam, z)
    ahy = angular_spectrum(y, d, lam, -z)
    gap = abs(img_dot(ax, y) - img_dot(x, ahy))
    assert gap <= 1e-10 * img_norm(ax) * img_norm(y)


def test_band_limit_keeps_phase_steps_below_pi():
    n, d, lam = 16, 1.0, 0.5
    for z in (50.0, 400.0, 3000.0):
        lim = band_limit(n, d, lam, z)
        du = 1.0 / (n * d)
        f = 0.0
        while f + du <= lim:
            p0 = 2 * math.pi * z * math.sqrt(1 / lam ** 2 - f * f)
            p1 = 2 * math.pi * z * math.sqrt(1 / lam ** 2 - (f + du) ** 2)
            assert abs(p1 - p0) <= math.pi + 1e-9
            f += du
        # The local frequency of the phase, |d phase / df| / (2 pi), equals
        # 1 / (2 du) at the limit and is larger past it.
        def slope(f):
            return 2 * math.pi * z * f / math.sqrt(1 / lam ** 2 - f * f)
        assert abs(slope(lim) * du - math.pi) < 1e-9
        assert slope(lim * 1.02) * du > math.pi


def test_band_limited_h_is_zero_outside_limit():
    h = transfer_function(16, 16, 1.0, 0.5, 400.0, limit=True)
    lim = band_limit(16, 1.0, 0.5, 400.0)
    fs = frequencies(16, 1.0)
    for k in range(16):
        for l in range(16):
            inside = abs(fs[k]) <= lim and abs(fs[l]) <= lim
            assert (abs(h[k][l]) > 0.5) == inside


def test_fresnel_agrees_for_small_angles():
    n, d, lam, z = 8, 4.0, 0.5, 20.0  # max |f| lambda = 0.088, paraxial
    h = transfer_function(n, n, d, lam, z)
    hf = fresnel_transfer(n, n, d, lam, z)
    fs = frequencies(n, d)
    for k in range(n):
        for l in range(n):
            f2 = fs[k] ** 2 + fs[l] ** 2
            bound = 2 * math.pi * z * lam ** 3 * f2 * f2 / 8 * 1.05 + 1e-12
            assert abs(h[k][l] - hf[k][l]) <= bound


def test_padded_matches_unpadded_inside_when_no_wrap():
    # A narrow field at a short distance: little light reaches the window edge.
    u = [[0j] * 8 for _ in range(8)]
    u[3][3] = u[3][4] = u[4][3] = u[4][4] = 1 + 0j
    a = angular_spectrum_padded(u, 1.0, 0.5, 0.0)
    assert max_diff(a, u) < 1e-12
