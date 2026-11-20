# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/espirit/. The authors are listed in prov/CN1ST0.jsonl.

import cmath
import functools
import math
import random

from espirit import espirit, herm_eig, signal_space
from imgkit import MODIFIED_SHEPP_LOGAN, dft2, disk_phantom, ellipse_phantom, idft2, pixel_centers
from imgla import solve

N = 16
BAND = [(0.0, 0.8, 4, 0.3, 16), (1.0, 0.8, 28, 0.2, 12), (2.0, 0.3, 16, 0.8, 4), (-1.5, 0.25, 20, 0.8, 28)]


def band_maps(n):
    """Coil maps with image frequencies 0 and 1 on each axis: the patch space of a 3 x 3 kernel is exact."""
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


def coil_images(maps, img):
    return [[[s * p for s, p in zip(sr, pr)] for sr, pr in zip(mp, img)] for mp in maps]


def ksp_of(coils):
    n = len(coils[0])
    return [[[v / n for v in row] for row in dft2(f)] for f in coils]


def normalized(s):
    """s / ||s|| with the coil 0 entry made real and positive."""
    nr = math.sqrt(sum(abs(x) ** 2 for x in s))
    ref = s[0] / abs(s[0])
    return [x / nr / ref for x in s]


@functools.lru_cache(maxsize=None)
def band_case():
    maps = band_maps(N)
    coils = coil_images(maps, ellipse_phantom(N, MODIFIED_SHEPP_LOGAN))
    k = ksp_of(coils)
    est, eig = espirit(k, 10)
    return maps, coils, k, est, eig


def test_herm_eig():
    rng = random.Random(1)
    a = [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(6)] for _ in range(6)]
    h = [[a[i][j] + a[j][i].conjugate() for j in range(6)] for i in range(6)]
    w, q = herm_eig(h)
    assert all(x >= y for x, y in zip(w, w[1:]))
    for i in range(6):
        for l in range(6):
            assert abs(sum(h[i][k] * q[k][l] for k in range(6)) - w[l] * q[i][l]) < 1e-12
            assert abs(sum(q[k][i].conjugate() * q[k][l] for k in range(6)) - (1 if i == l else 0)) < 1e-12


def test_signal_space_has_rank_16_for_band_maps():
    _, _, k, _, _ = band_case()
    sig, v = signal_space(k, 10)
    assert len(sig) == 36 and len(v[0]) == 16
    assert sig[15] > 1e4 * sig[16]


def test_band_maps_are_recovered_with_eigenvalue_one():
    maps, _, _, est, eig = band_case()
    for i in range(N):
        for j in range(N):
            assert abs(eig[i][j] - 1.0) < 1e-9
            truth = normalized([m[i][j] for m in maps])
            assert max(abs(a - b[i][j]) for a, b in zip(truth, est)) < 1e-9


def test_sense_with_espirit_maps_is_consistent_with_the_data():
    _, coils, k, est, _ = band_case()
    h = N // 2
    # R = 2: keep the even rows; the inverse DFT of size (n/2) x n gives the folded coil images / n.
    folded = [[[N * v for v in row] for row in idft2([k[c][2 * r] for r in range(h)])] for c in range(4)]
    for i in range(h):
        for j in range(N):
            e = [[est[c][i][j], est[c][i + h][j]] for c in range(4)]
            a = [folded[c][i][j] for c in range(4)]
            gram = [[sum(e[c][p].conjugate() * e[c][q] for c in range(4)) for q in range(2)] for p in range(2)]
            rhs = [sum(e[c][p].conjugate() * a[c] for c in range(4)) for p in range(2)]
            m = solve(gram, rhs)
            for c in range(4):
                assert abs(est[c][i][j] * m[0] - coils[c][i][j]) < 1e-9
                assert abs(est[c][i + h][j] * m[1] - coils[c][i + h][j]) < 1e-9


def test_ring_maps_disk_object():
    maps = ring_maps(N)
    img = disk_phantom(N, 0.75)
    k = ksp_of(coil_images(maps, img))
    est, eig = espirit(k, 10, t_s=0.02, t_e=0.99)
    inside = [(i, j) for i in range(N) for j in range(N) if img[i][j] != 0]
    outside = [(i, j) for i in range(N) for j in range(N) if img[i][j] == 0]
    assert min(eig[i][j] for i, j in inside) > 0.99
    assert sum(eig[i][j] for i, j in outside) / len(outside) < 0.97
    for i, j in inside:
        truth = normalized([m[i][j] for m in maps])
        assert math.sqrt(sum(abs(a - b[i][j]) ** 2 for a, b in zip(truth, est))) < 0.1
    masked = [(i, j) for i, j in outside if all(b[i][j] == 0 for b in est)]
    assert masked
