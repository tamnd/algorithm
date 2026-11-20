# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/grappa/. The authors are listed in prov/KY1RH2.jsonl.

import cmath
import functools
import math

import pytest

from grappa import grappa, grappa_mask, source_offsets
from imgkit import MODIFIED_SHEPP_LOGAN, dft2, ellipse_phantom, pixel_centers

N = 32
BAND = [(0.0, 0.8, 4, 0.3, 16), (1.0, 0.8, 28, 0.2, 12), (2.0, 0.3, 16, 0.8, 4), (-1.5, 0.25, 20, 0.8, 28)]


def band_maps(n):
    """Coil maps with image frequencies 0 and 1 on each axis: a small kernel can be exact at R = 2."""
    out = []
    for psi, a, col, b, row in BAND:
        u, v = 2 * math.pi * col / n, 2 * math.pi * row / n
        out.append([[cmath.exp(1j * psi) * (1 + a * cmath.exp(1j * (2 * math.pi * j / n - u)))
                     * (1 + b * cmath.exp(1j * (2 * math.pi * i / n - v))) for j in range(n)] for i in range(n)])
    return out


def ring_maps(n, c=4):
    """Smooth Gaussian coil profiles around the object, with a phase ramp."""
    xs, ys = pixel_centers(n)
    maps = []
    for k in range(c):
        ang = math.radians(20 + 360.0 * k / c)
        cx, cy = 1.2 * math.cos(ang), 1.2 * math.sin(ang)
        maps.append([[math.exp(-((x - cx) ** 2 + (y - cy) ** 2) / 1.2) * cmath.exp(1j * (0.9 * k + 0.4 * x - 0.3 * y))
                      for x in xs] for y in ys])
    return maps


@functools.lru_cache(maxsize=None)
def kspace(kind):
    maps = band_maps(N) if kind == "band" else ring_maps(N)
    ph = ellipse_phantom(N, MODIFIED_SHEPP_LOGAN)
    return [[[v / N for v in row] for row in dft2([[s * p for s, p in zip(sr, pr)] for sr, pr in zip(mp, ph)])] for mp in maps]


def rel(a, b):
    num = sum(abs(x - y) ** 2 for aa, bb in zip(a, b) for ra, rb in zip(aa, bb) for x, y in zip(ra, rb))
    den = sum(abs(y) ** 2 for bb in b for rb in bb for y in rb)
    return math.sqrt(num / den)


def acquire(k, keep, fill=0j):
    return [[list(row) if keep[kap] else [fill] * N for kap, row in enumerate(a)] for a in k]


def test_source_offsets():
    assert source_offsets(2, 1, 2, 1) == [(-1, -1), (-1, 0), (-1, 1), (1, -1), (1, 0), (1, 1)]
    assert [o[0] for o in source_offsets(4, 3, 2, 0)] == [-3, 1]


def test_mask():
    keep = grappa_mask(16, 4, 4)
    assert [kap for kap in range(16) if keep[kap]] == [0, 1, 4, 8, 12, 14, 15]


def test_exact_for_band_maps_and_missing_rows_not_read():
    k = kspace("band")
    keep = grappa_mask(N, 2, 12)
    y = acquire(k, keep, fill=1e6 + 1e6j)
    out = grappa(y, 2, 12)
    assert rel(out, k) < 1e-6
    for a in range(4):
        for kap in range(N):
            if keep[kap]:
                assert out[a][kap] == k[a][kap]


def test_ring_maps_r2_and_r4_beat_zero_filling():
    k = kspace("ring")
    for r, acs, bound in ((2, 12, 0.1), (4, 16, 0.5)):
        keep = grappa_mask(N, r, acs)
        y = acquire(k, keep)
        err = rel(grappa(y, r, acs), k)
        assert err < bound * rel(y, k)


def test_r_must_divide_n():
    k = kspace("band")
    with pytest.raises(ValueError):
        grappa(k, 3, 12)
