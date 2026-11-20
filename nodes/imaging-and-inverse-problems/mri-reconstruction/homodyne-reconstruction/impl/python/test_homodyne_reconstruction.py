# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/homodyne-reconstruction/. The authors are listed in prov/4ZY7XX.jsonl.

import cmath
import math
import random

import pytest

from homodyne_reconstruction import (
    homodyne_1d,
    homodyne_2d,
    homodyne_weights,
    partial_mask,
    signed_freq,
    triangle_window,
    unitary_dft,
    unitary_dft2,
    zero_filled_1d,
)
from imgkit import ellipse_phantom, MODIFIED_SHEPP_LOGAN, pixel_centers


def direct_homodyne(y, k0, kind="step"):
    """The same method with explicit O(n^2) sums instead of the FFT."""
    n = len(y)
    h = homodyne_weights(n, k0, kind)
    t = triangle_window(n, k0)
    s = 1.0 / math.sqrt(n)
    out = []
    for j in range(n):
        z = sum(h[k] * y[k] * cmath.exp(2j * math.pi * j * k / n) for k in range(n)) * s
        low = sum(t[k] * y[k] * cmath.exp(2j * math.pi * j * k / n) for k in range(n)) * s
        out.append(0.0 if low == 0 else (low.conjugate() * z).real / abs(low))
    return out


def masked(y, k0):
    """Keep the acquired samples; put garbage in the missing ones to show they are never read."""
    m = partial_mask(len(y), k0)
    return [v if a else complex(1e6, -1e6) for v, a in zip(y, m)]


def test_filter_sums_to_two():
    for n, k0 in ((8, 1), (16, 3), (32, 0), (32, 14)):
        for kind in ("step", "ramp"):
            h = homodyne_weights(n, k0, kind)
            for k in range(n):
                f = signed_freq(k, n)
                g = (-f) % n
                assert h[k] + h[g] == pytest.approx(2.0, abs=1e-15)


def test_constant_phase_nonnegative_is_exact():
    rng = random.Random(1)
    for n, k0 in ((8, 1), (16, 2), (32, 5), (64, 9)):
        for kind in ("step", "ramp"):
            rho = [rng.uniform(0.0, 2.0) for _ in range(n)]
            phase = cmath.exp(1j * rng.uniform(-math.pi, math.pi))
            y = unitary_dft([phase * r for r in rho])
            out = homodyne_1d(masked(y, k0), k0, kind)
            assert max(abs(a - b) for a, b in zip(out, rho)) < 1e-10


def test_signed_real_image_gives_sign_of_lowres():
    rng = random.Random(2)
    n, k0 = 32, 4
    rho = [rng.uniform(-1.0, 1.0) for _ in range(n)]
    phase = cmath.exp(0.7j)
    y = unitary_dft([phase * r for r in rho])
    out = homodyne_1d(masked(y, k0), k0)
    t = triangle_window(n, k0)
    # Low-resolution real image r = F_u^H T F_u rho by direct sums.
    yr = unitary_dft(rho)
    r = [sum(t[k] * yr[k] * cmath.exp(2j * math.pi * j * k / n) for k in range(n)).real / math.sqrt(n) for j in range(n)]
    for j in range(n):
        if abs(r[j]) > 1e-9:
            assert out[j] == pytest.approx(math.copysign(1.0, r[j]) * rho[j], abs=1e-10)


def test_matches_direct_sums_on_random_data():
    rng = random.Random(3)
    for n, k0 in ((16, 3), (12, 2)):
        y = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(n)]
        y = masked(y, k0)
        for kind in ("step", "ramp"):
            a = homodyne_1d(y, k0, kind)
            b = direct_homodyne(y, k0, kind)
            assert max(abs(u - v) for u, v in zip(a, b)) < 1e-9


def test_full_band_limits():
    with pytest.raises(ValueError):
        homodyne_1d([0j] * 8, 3)
    with pytest.raises(ValueError):
        homodyne_1d([0j] * 7, 1)


def phantom_with_phase(n):
    rho = ellipse_phantom(n, MODIFIED_SHEPP_LOGAN)
    xs, ys = pixel_centers(n)
    return rho, [[rho[i][j] * cmath.exp(1j * (0.4 + 0.5 * xs[j] - 0.6 * ys[i] + 0.2 * xs[j] * ys[i])) for j in range(n)] for i in range(n)]


def test_2d_smooth_phase_beats_zero_filling():
    n, k0 = 16, 3
    rho, x = phantom_with_phase(n)
    ks = unitary_dft2(x)
    keep = partial_mask(n, k0)
    ks = [ks[a] if keep[a] else [complex(9.0, 9.0)] * n for a in range(n)]
    out = homodyne_2d(ks, k0)
    err_h = math.sqrt(sum((out[i][j] - rho[i][j]) ** 2 for i in range(n) for j in range(n)))
    # Zero filling, column by column, then the magnitude.
    zf = [[0.0] * n for _ in range(n)]
    for j in range(n):
        col = [sum(ks[a][b] * cmath.exp(2j * math.pi * j * b / n) for b in range(n)) / math.sqrt(n) for a in range(n)]
        img = zero_filled_1d(col, k0)
        for i in range(n):
            zf[i][j] = abs(img[i])
    err_z = math.sqrt(sum((zf[i][j] - rho[i][j]) ** 2 for i in range(n) for j in range(n)))
    norm = math.sqrt(sum(v * v for row in rho for v in row))
    assert err_h < err_z
    assert err_h / norm < 0.35


def test_2d_constant_phase_exact():
    n, k0 = 16, 2
    rho = ellipse_phantom(n, MODIFIED_SHEPP_LOGAN)
    ks = unitary_dft2([[cmath.exp(-1.1j) * v for v in row] for row in rho])
    out = homodyne_2d(ks, k0, "ramp")
    assert max(abs(out[i][j] - rho[i][j]) for i in range(n) for j in range(n)) < 1e-10
