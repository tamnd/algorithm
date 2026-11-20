# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spirit/. The authors are listed in prov/VXHK1N.jsonl.

import cmath
import functools
import math
import random

from imgkit import MODIFIED_SHEPP_LOGAN, dft2, ellipse_phantom, pixel_centers
from imgla import adjoint_gap
from spirit import apply_g, apply_g_adjoint, calib_rows, calibrate, spirit

N = 16
ACS = 8
BAND = [(0.0, 0.8, 4, 0.3, 16), (1.0, 0.8, 28, 0.2, 12), (2.0, 0.3, 16, 0.8, 4), (-1.5, 0.25, 20, 0.8, 28)]


def band_maps(n):
    """Coil maps with image frequencies 0 and 1 on each axis: a 3 x 3 kernel can be exact."""
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


def ksp_of(maps, img):
    n = len(img)
    return [[[v / n for v in row] for row in dft2([[s * p for s, p in zip(sr, pr)] for sr, pr in zip(mp, img)])] for mp in maps]


def rel(a, b):
    num = sum(abs(x - y) ** 2 for aa, bb in zip(a, b) for ra, rb in zip(aa, bb) for x, y in zip(ra, rb))
    den = sum(abs(y) ** 2 for bb in b for rb in bb for y in rb)
    return math.sqrt(num / den)


def keep(k, mask, fill=0j):
    return [[[v if m else fill for v, m in zip(row, mrow)] for row, mrow in zip(a, mask)] for a in k]


@functools.lru_cache(maxsize=None)
def band_case():
    k = ksp_of(band_maps(N), ellipse_phantom(N, MODIFIED_SHEPP_LOGAN))
    cal = set(calib_rows(N, ACS))
    mask = [[(kap % 2 == 0) or (kap in cal)] * N for kap in range(N)]
    return k, mask


@functools.lru_cache(maxsize=None)
def ring_random_case():
    k = ksp_of(ring_maps(N), ellipse_phantom(N, MODIFIED_SHEPP_LOGAN))
    cal = set(calib_rows(N, ACS))
    rng = random.Random(5)
    mask = [[(kap in cal) or rng.random() < 0.5 for _ in range(N)] for kap in range(N)]
    y = keep(k, mask)
    hist = []
    out = spirit(y, mask, ACS, 25, callback=lambda t, r: hist.append(r))
    return k, mask, y, out, hist


def test_exact_recovery_uniform_r2_and_missing_samples_not_read():
    k, mask = band_case()
    y = keep(k, mask, fill=1e6 + 1e6j)  # junk on the missing samples
    out = spirit(y, mask, ACS, 25)
    assert rel(out, k) < 1e-6
    for a in range(4):
        for kap in range(N):
            for l in range(N):
                if mask[kap][l]:
                    assert out[a][kap][l] == k[a][kap][l]


def test_kernel_leaves_out_the_target_and_truth_is_consistent():
    k, mask = band_case()
    g = calibrate(keep(k, mask), ACS)
    for a in range(4):
        assert (0, 0) not in g[a][a]
        assert (0, 0) in g[a][(a + 1) % 4]
    assert rel(apply_g(k, g), k) < 1e-6


def test_adjoint_of_g():
    k, mask = band_case()
    g = calibrate(keep(k, mask), ACS)
    rng = random.Random(3)

    def rnd():
        return [[[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(N)] for _ in range(N)] for _ in range(4)]

    def flat(f):
        return lambda v: [w for a in f([[v[(c * N + i) * N:(c * N + i + 1) * N] for i in range(N)] for c in range(4)])
                          for row in a for w in row]

    x = [w for a in rnd() for row in a for w in row]
    y = [w for a in rnd() for row in a for w in row]
    assert adjoint_gap(flat(lambda u: apply_g(u, g)), flat(lambda u: apply_g_adjoint(u, g)), x, y) < 1e-12


def test_random_sampling_ring_maps_beats_zero_filling():
    k, mask, y, out, _ = ring_random_case()
    assert rel(out, k) < 0.5 * rel(y, k)


def test_cgls_residual_does_not_increase():
    _, _, _, _, hist = ring_random_case()
    assert len(hist) == 25
    assert all(b <= a * (1 + 1e-12) for a, b in zip(hist, hist[1:]))
    assert hist[-1] < 0.2 * hist[0]
