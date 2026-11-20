# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/transport-of-intensity-equation/. The authors are listed in prov/5EFCMW.jsonl.

import cmath
import math
import random

from imgkit import dft2, idft2
from transport_of_intensity_equation import divergence, gradient, inverse_laplacian, tie_phase, tie_phase_uniform

N = 32
D = 1.0
WL = 0.5
K = 2.0 * math.pi / WL


def freqs(n, d):
    return [(k if 2 * k < n else k - n) / (n * d) for k in range(n)]


def band_limited(seed, kmax, amp):
    """A real periodic image with random Fourier modes 0 < |k|, |l| <= kmax, mean zero."""
    rng = random.Random(seed)
    spec = [[0j] * N for _ in range(N)]
    for k in range(-kmax, kmax + 1):
        for l in range(-kmax, kmax + 1):
            if (k, l) > (0, 0):
                c = complex(rng.gauss(0, 1), rng.gauss(0, 1))
                spec[k % N][l % N] = c
                spec[-k % N][-l % N] = c.conjugate()
    u = [[v.real for v in row] for row in idft2(spec)]
    s = amp / max(abs(v) for row in u for v in row)
    return [[s * v for v in row] for row in u]


def spectral_laplacian(u):
    fy = fx = freqs(N, D)
    spec = dft2(u)
    for k in range(N):
        for l in range(N):
            spec[k][l] *= -4.0 * math.pi * math.pi * (fx[l] ** 2 + fy[k] ** 2)
    return [[v.real for v in row] for row in idft2(spec)]


def propagate(u, z):
    """Angular spectrum propagation over a distance z (exp(-i omega t) convention)."""
    f = freqs(N, D)
    s = dft2(u)
    for k in range(N):
        for l in range(N):
            s[k][l] *= cmath.exp(2j * math.pi * z * math.sqrt(1.0 / WL ** 2 - f[k] ** 2 - f[l] ** 2))
    return idft2(s)


def bumps(seed, amp, width):
    """A sum of four periodic Gaussian bumps of random sign."""
    rng = random.Random(seed)
    cs = [(rng.uniform(0, N), rng.uniform(0, N), rng.uniform(-1, 1)) for _ in range(4)]
    out = [[0.0] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            v = 0.0
            for cy, cx, a in cs:
                for sy in (-N, 0, N):
                    for sx in (-N, 0, N):
                        v += a * math.exp(-((i - cy + sy) ** 2 + (j - cx + sx) ** 2) / (2 * width ** 2))
            out[i][j] = amp * v
    return out


def demean(a):
    m = sum(map(sum, a)) / (len(a) * len(a[0]))
    return [[v - m for v in row] for row in a]


def rel_error(a, b):
    """Relative error of a against b after both means are removed (phase is up to a constant)."""
    a, b = demean(a), demean(b)
    num = sum((x - y) ** 2 for ra, rb in zip(a, b) for x, y in zip(ra, rb))
    return math.sqrt(num / sum(y * y for row in b for y in row))


def defocus_series(amp, phi, dz, sigma=0.0, seed=0):
    rng = random.Random(seed)
    u0 = [[a * cmath.exp(1j * p) for a, p in zip(ra, rp)] for ra, rp in zip(amp, phi)]
    i0 = [[abs(v) ** 2 for v in row] for row in u0]
    im = [[abs(v) ** 2 + (rng.gauss(0, sigma) if sigma else 0.0) for v in row] for row in propagate(u0, -dz)]
    ip = [[abs(v) ** 2 + (rng.gauss(0, sigma) if sigma else 0.0) for v in row] for row in propagate(u0, dz)]
    return im, i0, ip


def test_inverse_laplacian_inverts_the_spectral_laplacian():
    u = band_limited(1, 6, 1.0)
    back = inverse_laplacian(spectral_laplacian(u), D)
    assert max(abs(a - b) for ra, rb in zip(back, u) for a, b in zip(ra, rb)) < 1e-12
    assert abs(sum(map(sum, back))) < 1e-10


def test_gradient_and_divergence_of_a_sine():
    u = [[math.sin(2 * math.pi * (3 * j + 2 * i) / N) for j in range(N)] for i in range(N)]
    gx, gy = gradient(u, D)
    for i in range(N):
        for j in range(N):
            c = math.cos(2 * math.pi * (3 * j + 2 * i) / N) * 2 * math.pi / N
            assert abs(gx[i][j] - 3 * c) < 1e-12
            assert abs(gy[i][j] - 2 * c) < 1e-12
    lap = divergence(gx, gy, D)
    want = spectral_laplacian(u)
    assert max(abs(a - b) for ra, rb in zip(lap, want) for a, b in zip(ra, rb)) < 1e-12


def test_uniform_intensity_is_exact_for_tie_data():
    # Data that satisfy the TIE exactly: dI/dz = -(I0 / k) lap phi.
    phi = band_limited(2, 7, 2.0)
    i0 = 0.7
    didz = [[-(i0 / K) * v for v in row] for row in spectral_laplacian(phi)]
    dz = 0.3
    im = [[i0 - dz * v for v in row] for row in didz]
    ip = [[i0 + dz * v for v in row] for row in didz]
    focus = [[i0] * N for _ in range(N)]
    assert rel_error(tie_phase(im, focus, ip, dz, D, WL), phi) < 1e-12
    assert rel_error(tie_phase_uniform(im, ip, i0, dz, D, WL), phi) < 1e-12


def test_curl_free_flux_with_varying_intensity():
    # I = exp(-psi) and phi = exp(psi) give I grad phi = grad psi, so the
    # Teague assumption holds exactly; only the spectral derivative of a
    # function that is not band-limited adds a small error.
    psi = band_limited(3, 3, 0.4)
    intensity = [[math.exp(-v) for v in row] for row in psi]
    phi = [[math.exp(v) for v in row] for row in psi]
    didz = [[-v / K for v in row] for row in spectral_laplacian(psi)]
    dz = 0.5
    im = [[a - dz * v for a, v in zip(ra, rv)] for ra, rv in zip(intensity, didz)]
    ip = [[a + dz * v for a, v in zip(ra, rv)] for ra, rv in zip(intensity, didz)]
    assert rel_error(tie_phase(im, intensity, ip, dz, D, WL), phi) < 1e-6


def test_defocus_series_of_a_phase_object():
    phi = bumps(1, 1.0, 3.0)
    flat = [[1.0] * N for _ in range(N)]
    im, i0, ip = defocus_series(flat, phi, 4.0)
    assert rel_error(tie_phase(im, i0, ip, 4.0, D, WL), phi) < 1e-3
    im, i0, ip = defocus_series(flat, phi, 64.0)
    assert rel_error(tie_phase(im, i0, ip, 64.0, D, WL), phi) > 0.03


def test_absorbing_object_needs_the_full_equation():
    phi = bumps(1, 1.0, 3.0)
    amp = [[math.exp(v) for v in row] for row in bumps(2, 0.3, 4.0)]
    im, i0, ip = defocus_series(amp, phi, 4.0)
    assert rel_error(tie_phase(im, i0, ip, 4.0, D, WL), phi) < 0.02
    mean_i = sum(map(sum, i0)) / (N * N)
    assert rel_error(tie_phase_uniform(im, ip, mean_i, 4.0, D, WL), phi) > 0.05


def test_noise_and_bias_trade_off_in_the_defocus():
    phi = bumps(1, 1.0, 3.0)
    flat = [[1.0] * N for _ in range(N)]
    err = {}
    for dz in (1.0, 16.0, 64.0):
        im, i0, ip = defocus_series(flat, phi, dz, sigma=1e-3, seed=5)
        err[dz] = rel_error(tie_phase(im, i0, ip, dz, D, WL), phi)
    assert err[16.0] < 0.015
    assert err[1.0] > 4 * err[16.0]
    assert err[64.0] > 4 * err[16.0]


def test_constant_phase_does_not_change_the_result():
    phi = bumps(4, 0.8, 3.0)
    flat = [[1.0] * N for _ in range(N)]
    a = tie_phase(*defocus_series(flat, phi, 4.0), 4.0, D, WL)
    b = tie_phase(*defocus_series(flat, [[v + 1.3 for v in row] for row in phi], 4.0), 4.0, D, WL)
    assert max(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb)) < 1e-9
    assert abs(sum(map(sum, a))) < 1e-9
