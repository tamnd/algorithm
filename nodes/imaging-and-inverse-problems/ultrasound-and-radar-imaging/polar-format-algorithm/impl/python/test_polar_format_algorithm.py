# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/polar-format-algorithm/. The authors are listed in prov/8JG48Y.jsonl.

import math

from polar_format_algorithm import Spotlight, cartesian_grid, pfa, pixel_coords, polar_sum, simulate_dechirped

G = Spotlight()
YS, XS = pixel_coords(G)
TARGETS = [(XS[16], YS[16], 1.0), (XS[20], YS[10], 0.5), (XS[9], YS[24], 0.8j)]
GAIN = G.n_fast * G.n_pulses
PLANE = simulate_dechirped(G, TARGETS, plane_wave=True)
IMG = pfa(G, PLANE)


def peak(img):
    return max((abs(v), i, j) for i, row in enumerate(img) for j, v in enumerate(row))


def test_targets_focus_at_their_pixels_with_their_amplitudes() -> None:
    for x, y, amp in TARGETS:
        i, j = YS.index(y), XS.index(x)
        assert abs(IMG[i][j] / GAIN - amp) < 0.02


def test_matches_the_direct_polar_fourier_sum() -> None:
    on = [(16, 16), (10, 20), (24, 9)]
    off = [(i, j) for i in range(8, 25, 4) for j in range(8, 25, 4) if (i, j) not in on]
    ref = polar_sum(G, PLANE, [(XS[j], YS[i]) for i, j in on + off])
    for (i, j), r in zip(on, ref):
        assert abs(IMG[i][j] - r) < 0.01 * GAIN
    # Away from the targets: the direct sum uses the whole annular sector and
    # PFA the inscribed rectangle, so their sidelobes differ, but both are low.
    for (i, j), r in zip(off, ref[len(on):]):
        assert abs(IMG[i][j]) < 0.07 * GAIN and abs(r) < 0.07 * GAIN


def test_keystone_grid_lies_inside_the_polar_annulus() -> None:
    kys, kxs = cartesian_grid(G)
    u_lo, u_hi = G.u(0), G.u(G.n_fast - 1)
    for ky in (kys[0], kys[-1]):
        for kx in (kxs[0], kxs[-1]):
            assert u_lo - 1e-9 <= math.hypot(kx, ky) <= u_hi + 1e-9
            assert abs(math.atan2(kx, ky)) <= G.span / 2 + 1e-12


def test_wavefront_curvature_lowers_off_center_peaks() -> None:
    """Measurement: exact spherical ranges at a short range break the plane-wave model.

    At rc = 30 m the corner target moves by about a third of a pixel (geometric
    distortion), so the largest pixel value drops; the down-range target does not move.
    """
    far = Spotlight(rc=1000.0)
    near = Spotlight(rc=30.0)
    corner, down_range = (24, 24), (24, 16)
    for g, low in ((far, 0.98), (near, None)):
        ys, xs = pixel_coords(g)
        for i, j in (corner, down_range):
            img = pfa(g, simulate_dechirped(g, [(xs[j], ys[i], 1.0)]))
            value = peak(img)[0] / GAIN
            if low is not None or (i, j) == down_range:
                assert value > 0.98
            else:
                assert value < 0.9


def test_linear_in_the_data() -> None:
    a = pfa(G, simulate_dechirped(G, TARGETS[:1], plane_wave=True))
    b = pfa(G, simulate_dechirped(G, TARGETS[1:], plane_wave=True))
    assert max(abs(a[i][j] + b[i][j] - IMG[i][j]) for i in range(32) for j in range(32)) < 1e-9 * GAIN
