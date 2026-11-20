# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/digital-holography-reconstruction/. The authors are listed in prov/JPPVSQ.jsonl.

import cmath
import math
import random

from digital_holography_reconstruction import (
    find_carrier,
    propagate,
    reconstruct,
    record_hologram,
    reference_wave,
    signed_index,
)
from imgkit import dft2, idft2, img_norm

N1, N2, D, LAM, Z = 8, 32, 1.0, 0.5, 6.0  # every grid frequency propagates


def band_limited_field(rng, n1, n2, band):
    """A random field whose DFT is zero outside |ky|, |kx| <= band."""
    spec = [[0j] * n2 for _ in range(n1)]
    for k in range(n1):
        for l in range(n2):
            if abs(signed_index(k, n1)) <= band and abs(signed_index(l, n2)) <= band:
                spec[k][l] = complex(rng.gauss(0, 1), rng.gauss(0, 1)) * n1 * n2 / 10.0
    return idft2(spec)


def max_diff(a, b):
    return max(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb))


def sub(a, b):
    return [[x - y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def support(img, tol=1e-9):
    spec = dft2(img)
    n1, n2 = len(img), len(img[0])
    return {(signed_index(k, n1), signed_index(l, n2)) for k in range(n1) for l in range(n2) if abs(spec[k][l]) > tol}


def test_exact_recovery_when_the_sidebands_separate():
    rng = random.Random(1)
    band = 2
    obj = band_limited_field(rng, N1, N2, band)
    at_sensor = propagate(obj, D, LAM, Z)
    for carrier in ((0, 7), (0, 9), (0, 13), (3, 9), (0, -9)):
        for r in (1.0, 4.0):
            h = record_hologram(at_sensor, r, carrier)
            assert max_diff(reconstruct(h, carrier, band, r, D, LAM, 0.0), at_sensor) < 1e-10
            assert max_diff(reconstruct(h, carrier, band, r, D, LAM, Z), obj) < 1e-10


def test_hologram_spectrum_has_the_four_terms_where_the_theorem_says():
    rng = random.Random(2)
    band, c = 2, (0, 9)
    o = band_limited_field(rng, N1, N2, band)
    ref = reference_wave(N1, N2, 1.5, c)
    dc = [[abs(a) ** 2 for a in row] for row in ref]
    auto = [[abs(a) ** 2 for a in row] for row in o]
    side = [[a.conjugate() * b for a, b in zip(ra, rb)] for ra, rb in zip(ref, o)]
    twin = [[a * b.conjugate() for a, b in zip(ra, rb)] for ra, rb in zip(ref, o)]
    h = record_hologram(o, 1.5, c)
    total = [[w + x + y + v for w, x, y, v in zip(*rows)] for rows in zip(dc, auto, side, twin)]
    assert max_diff(h, total) < 1e-10
    assert support(dc) == {(0, 0)}
    assert all(abs(ky) <= 2 * band and abs(kx) <= 2 * band for ky, kx in support(auto))
    assert all(abs(ky + c[0]) <= band and abs(kx + c[1]) <= band for ky, kx in support(side))
    assert all(abs(ky - c[0]) <= band and abs(kx - c[1]) <= band for ky, kx in support(twin))


def test_overlap_breaks_the_reconstruction():
    rng = random.Random(3)
    band = 2
    o = band_limited_field(rng, N1, N2, band)
    good = reconstruct(record_hologram(o, 1.0, (0, 7)), (0, 7), band, 1.0, D, LAM, 0.0)
    bad = reconstruct(record_hologram(o, 1.0, (0, 5)), (0, 5), band, 1.0, D, LAM, 0.0)
    assert max_diff(good, o) < 1e-10
    # c = 5 < 3 B = 6: the window also catches the edge of the |O|^2 term.
    assert img_norm(sub(bad, o)) > 1e-3 * img_norm(o)
    # c + B = 16 = n2 / 2: the sideband and the twin share the Nyquist column.
    bad2 = reconstruct(record_hologram(o, 1.0, (0, 14)), (0, 14), band, 1.0, D, LAM, 0.0)
    assert img_norm(sub(bad2, o)) > 1e-3 * img_norm(o)


def test_find_carrier_up_to_sign():
    rng = random.Random(4)
    # A weak scatterer: a strong unscattered wave plus a small band-limited part.
    o = [[1.0 + 0.2 * v for v in row] for row in band_limited_field(rng, N1, N2, 2)]
    for c in ((0, 9), (2, 10), (0, -11), (-1, -8)):
        h = record_hologram(o, 3.0, c)
        found = find_carrier(h, 4)
        assert found in (c, (-c[0], -c[1]))
        assert found[1] > 0
        # The spectrum of a real hologram is Hermitian, so the two peaks are equal.
        spec = dft2(h)
        assert abs(abs(spec[c[0] % N1][c[1] % N2]) - abs(spec[-c[0] % N1][-c[1] % N2])) < 1e-9


def test_noise_error_is_at_most_noise_over_r():
    rng = random.Random(5)
    band, c, r = 2, (0, 9), 2.0
    obj = band_limited_field(rng, N1, N2, band)
    h = record_hologram(propagate(obj, D, LAM, Z), r, c)
    noise = [[rng.gauss(0, 0.3) for _ in range(N2)] for _ in range(N1)]
    noisy = [[a + b for a, b in zip(ra, rb)] for ra, rb in zip(h, noise)]
    err = img_norm(sub(reconstruct(noisy, c, band, r, D, LAM, Z), obj))
    assert 0 < err <= img_norm(noise) / r + 1e-12


def test_inline_hologram_gives_the_twin_image():
    rng = random.Random(6)
    band, r = 2, 3.0
    obj = band_limited_field(rng, N1, N2, band)
    at_sensor = propagate(obj, D, LAM, Z)
    h = record_hologram(at_sensor, r, (0, 0))
    # Back-propagate (h - r^2) / r over the full grid: object, twin and |O|^2 terms.
    back = propagate([[(v - r * r) / r for v in row] for row in h], D, LAM, -Z)
    twin = propagate([[v.conjugate() for v in row] for row in at_sensor], D, LAM, -Z)
    auto = propagate([[abs(v) ** 2 / r for v in row] for row in at_sensor], D, LAM, -Z)
    total = [[a + b + e for a, b, e in zip(ra, rb, re)] for ra, rb, re in zip(obj, twin, auto)]
    assert max_diff(back, total) < 1e-10
    # The twin is not small: it has the same energy as the object.
    assert abs(img_norm(twin) - img_norm(obj)) < 1e-10 * img_norm(obj)
    # The twin is the conjugate object wave focused at -z: propagating it by +2 z gives conj(obj).
    refocused = propagate(twin, D, LAM, 2 * Z)
    assert max_diff(refocused, [[v.conjugate() for v in row] for row in obj]) < 1e-10


def test_matches_direct_sum_for_one_entry():
    rng = random.Random(7)
    band, c, r = 2, (1, 9), 1.0
    o = band_limited_field(rng, N1, N2, band)
    h = record_hologram(o, r, c)
    out = reconstruct(h, c, band, r, D, LAM, 0.0)
    # Direct sum: demodulate conj(R) O by R / r^2 in real space and low-pass by the band.
    demod = [[h[i][j] * cmath.exp(2j * math.pi * (c[0] * i / N1 + c[1] * j / N2)) / r for j in range(N2)] for i in range(N1)]
    for i, j in ((0, 0), (3, 17), (7, 31)):
        s = 0j
        for ky in range(-band, band + 1):
            for kx in range(-band, band + 1):
                coef = sum(
                    demod[p][q] * cmath.exp(-2j * math.pi * (ky * p / N1 + kx * q / N2)) for p in range(N1) for q in range(N2)
                )
                s += coef * cmath.exp(2j * math.pi * (ky * i / N1 + kx * j / N2))
        assert abs(s / (N1 * N2) - out[i][j]) < 1e-9
