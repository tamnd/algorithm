# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slice-grappa/. The authors are listed in prov/863VBG.jsonl.

import cmath
import functools
import math
import random

from imgkit import MODIFIED_SHEPP_LOGAN, dft2, disk_phantom, ellipse_phantom, idft2, pixel_centers
from slice_grappa import caipi_shift, collapse, slice_grappa

N = 32
P0 = [(0.0, 0.8, 4, 0.3, 16), (1.0, 0.8, 28, 0.2, 12), (2.0, 0.3, 16, 0.8, 4), (-1.5, 0.25, 20, 0.8, 28)]
P1 = [(0.5, 0.6, 8, 0.4, 20), (-0.7, 0.7, 24, 0.3, 8), (1.4, 0.4, 12, 0.7, 10), (2.5, 0.3, 26, 0.6, 24)]


def band_maps(n, params):
    """Coil maps with image frequencies 0 and 1 on each axis."""
    out = []
    for psi, a, col, b, row in params:
        u, v = 2 * math.pi * col / n, 2 * math.pi * row / n
        out.append([[cmath.exp(1j * psi) * (1 + a * cmath.exp(1j * (2 * math.pi * j / n - u)))
                     * (1 + b * cmath.exp(1j * (2 * math.pi * i / n - v))) for j in range(n)] for i in range(n)])
    return out


def ring_maps(n, rot, c=4):
    """Smooth Gaussian coil profiles around the object, with a phase ramp."""
    xs, ys = pixel_centers(n)
    maps = []
    for k in range(c):
        ang = math.radians(rot + 360.0 * k / c)
        cx, cy = 1.2 * math.cos(ang), 1.2 * math.sin(ang)
        maps.append([[math.exp(-((x - cx) ** 2 + (y - cy) ** 2) / 1.2) * cmath.exp(1j * (0.9 * k + 0.4 * x - 0.3 * y))
                      for x in xs] for y in ys])
    return maps


def ksp_of(maps, img):
    n = len(img)
    return [[[v / n for v in row] for row in dft2([[s * p for s, p in zip(sr, pr)] for sr, pr in zip(mp, img)])] for mp in maps]


def rel(a, b):
    num = sum(abs(x - y) ** 2 for aa, bb in zip(a, b) for ra, rb in zip(aa, bb) for x, y in zip(ra, rb))
    den = sum(abs(y) ** 2 for bb in b for rb in bb for y in rb)
    return math.sqrt(num / den)


@functools.lru_cache(maxsize=None)
def slices(kind):
    ph0 = ellipse_phantom(N, MODIFIED_SHEPP_LOGAN)
    d1, d2 = disk_phantom(N, 0.7), disk_phantom(N, 0.3)
    ph1 = [[a - 0.5 * b for a, b in zip(r1, r2)] for r1, r2 in zip(d1, d2)]
    if kind == "band":
        m0, m1 = band_maps(N, P0), band_maps(N, P1)
    else:
        m0, m1 = ring_maps(N, 20), ring_maps(N, 65)
    return ksp_of(m0, ph0), ksp_of(m1, ph1)


def separate(kind, shift):
    k0, k1 = slices(kind)
    shifts = [0, shift]
    out = slice_grappa(collapse([k0, k1], shifts), [k0, k1], shifts, acs=16)
    return rel(out[0], k0), rel(out[1], k1)


def test_caipi_shift_moves_the_image_by_whole_rows():
    rng = random.Random(1)
    img = [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(8)] for _ in range(8)]
    for s in (1, 3, 4):
        back = idft2(caipi_shift(dft2(img), s))
        for i in range(8):
            for j in range(8):
                assert abs(back[i][j] - img[(i - s) % 8][j]) < 1e-12


def test_collapse_is_the_sum_of_the_shifted_slices():
    k0, k1 = slices("band")
    y = collapse([k0, k1], [0, N // 2])
    for c in (0, 3):
        for kap in (0, 1, 5):
            sign = 1 if kap % 2 == 0 else -1
            for l in (0, 7):
                assert abs(y[c][kap][l] - (k0[c][kap][l] + sign * k1[c][kap][l])) < 1e-12


def test_band_maps_slices_separate():
    e0, e1 = separate("band", N // 2)
    assert e0 < 1e-3 and e1 < 1e-3


def test_ring_maps_caipi_shift_lowers_the_error():
    plain = separate("ring", 0)
    caipi = separate("ring", N // 2)
    assert max(plain) < 0.2
    assert caipi[0] < plain[0] and caipi[1] < plain[1]
