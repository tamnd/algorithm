# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/plane-wave-compounding/. The authors are listed in prov/HTFN8H.jsonl.

import cmath
import math
import random

from plane_wave_compounding import (compound, compound_adjoint, compound_complex, element_positions,
                                    simulate_plane_waves, transmit_time)

F0, SIGMA, FS, T0, NS = 5.0, 0.1, 40.0, 7.0, 120
M = 16
ELEMENTS = element_positions(M, 0.3)
DEG = math.pi / 180
NINE = [k * 2 * DEG for k in range(-4, 5)]
XS = [round(-1.5 + 0.1 * k, 10) for k in range(31)]


def test_peak_at_the_scatterer_with_gain_angles_times_elements() -> None:
    data = simulate_plane_waves(ELEMENTS, NINE, [(0.0, 6.0, 1.0)], F0, SIGMA, FS, T0, NS)
    zs = [5.9, 5.95, 6.0, 6.05, 6.1]
    img = compound(data, ELEMENTS, NINE, XS[10:21], zs, T0, FS, F0)
    v, i, j = max((v, i, j) for i, row in enumerate(img) for j, v in enumerate(row))
    assert (zs[i], XS[10 + j]) == (6.0, 0.0)
    assert abs(v - 9 * M) < 0.01 * 9 * M


def test_steered_wave_focuses_at_the_right_place() -> None:
    # a sign error in the transmit delay moves or smears the point for a tilted wave
    for alpha in (10 * DEG, -10 * DEG):
        data = simulate_plane_waves(ELEMENTS, [alpha], [(0.3, 6.0, 1.0)], F0, SIGMA, FS, T0, NS)
        zs = [5.9, 5.95, 6.0, 6.05, 6.1]
        img = compound(data, ELEMENTS, [alpha], XS, zs, T0, FS, F0)
        v, i, j = max((v, i, j) for i, row in enumerate(img) for j, v in enumerate(row))
        assert (zs[i], XS[j]) == (6.0, 0.3)
        assert abs(v - M) < 0.01 * M


def test_matches_the_analytic_sum_without_sampling() -> None:
    angs = [-5 * DEG, 0.0, 5 * DEG]
    scat = [(0.0, 6.0, 1.0), (0.4, 6.2, 0.5)]
    data = simulate_plane_waves(ELEMENTS, angs, scat, F0, SIGMA, FS, T0, NS)
    xs, zs = XS[10:21:3], [5.95, 6.0, 6.2]
    got = compound_complex(data, ELEMENTS, angs, xs, zs, T0, FS, F0)
    for a, pz in enumerate(zs):
        for b, px in enumerate(xs):
            want = 0j
            for alpha in angs:
                for xj in ELEMENTS:
                    t = transmit_time(px, pz, alpha) + math.hypot(px - xj, pz) / 1.54
                    for sx, sz, amp in scat:
                        dt = t - transmit_time(sx, sz, alpha) - math.hypot(sx - xj, sz) / 1.54
                        want += amp * math.exp(-dt * dt / (2 * SIGMA ** 2)) * cmath.exp(2j * math.pi * F0 * dt)
            assert abs(got[a][b] - want) < 0.01 * len(angs) * M


def test_compound_is_the_sum_of_the_single_angle_images() -> None:
    data = simulate_plane_waves(ELEMENTS, NINE, [(0.2, 6.1, 1.0), (-0.5, 6.0, 0.8)], F0, SIGMA, FS, T0, NS)
    xs, zs = XS[::5], [6.0, 6.1]
    total = compound_complex(data, ELEMENTS, NINE, xs, zs, T0, FS, F0)
    parts = [compound_complex([data[a]], ELEMENTS, [NINE[a]], xs, zs, T0, FS, F0) for a in range(len(NINE))]
    for i in range(len(zs)):
        for j in range(len(xs)):
            assert abs(total[i][j] - sum(p[i][j] for p in parts)) < 1e-9


def test_compounding_lowers_the_sidelobes() -> None:
    def side(angs):
        data = simulate_plane_waves(ELEMENTS, angs, [(0.0, 6.0, 1.0)], F0, SIGMA, FS, T0, NS)
        prof = compound(data, ELEMENTS, angs, XS, [6.0], T0, FS, F0)[0]
        return max(v for x, v in zip(XS, prof) if abs(x) >= 0.6) / max(prof)
    assert side(NINE) < 0.5 * side([0.0])


def test_receive_f_number_limits_the_aperture() -> None:
    data = simulate_plane_waves(ELEMENTS, [0.0], [(0.0, 6.0, 1.0)], F0, SIGMA, FS, T0, NS)
    used = sum(1 for xj in ELEMENTS if abs(xj) <= 6.0 / (2 * 1.5))
    assert used == 14
    v = compound(data, ELEMENTS, [0.0], [0.0], [6.0], T0, FS, F0, fnum=1.5)[0][0]
    assert abs(v - used) < 0.01 * used


def test_adjoint() -> None:
    rng = random.Random(7303)
    el = element_positions(5, 0.4)
    angs = [-6 * DEG, 0.0, 6 * DEG]
    ns, t0 = 50, 5.0
    xs, zs = [-0.3, 0.0, 0.2], [4.0, 4.1]
    data = [[[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(ns)] for _ in el] for _ in angs]
    img = [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in xs] for _ in zs]
    for fnum in (None, 2.0):
        a = compound_complex(data, el, angs, xs, zs, t0, FS, F0, fnum)
        b = compound_adjoint(img, el, angs, xs, zs, t0, FS, F0, ns, fnum)
        lhs = sum(a[i][j].conjugate() * img[i][j] for i in range(len(zs)) for j in range(len(xs)))
        rhs = sum(data[p][j][q].conjugate() * b[p][j][q]
                  for p in range(len(angs)) for j in range(len(el)) for q in range(ns))
        na = math.sqrt(sum(abs(v) ** 2 for row in a for v in row))
        ni = math.sqrt(sum(abs(v) ** 2 for row in img for v in row))
        assert abs(lhs - rhs) <= 1e-10 * na * ni
