# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/saft/. The authors are listed in prov/4W5EDR.jsonl.

import cmath
import math
import random

from saft import envelope_bscan, saft, saft_adjoint, saft_complex, scan_positions, simulate_bscan

F0, SIGMA, FS, T0, NS = 5.0, 0.1, 40.0, 7.0, 140
XS = [round(-0.7 + 0.1 * k, 10) for k in range(15)]


def test_peak_at_the_scatterer_with_gain_equal_to_the_number_of_positions() -> None:
    pos = scan_positions(21, 0.15)
    tr = simulate_bscan(pos, [(0.0, 6.0, 1.0)], F0, SIGMA, FS, T0, NS)
    zs = [5.9, 5.95, 6.0, 6.05, 6.1]
    img = saft(tr, pos, XS, zs, T0, FS, F0)
    v, i, j = max((v, i, j) for i, row in enumerate(img) for j, v in enumerate(row))
    assert (zs[i], XS[j]) == (6.0, 0.0)
    assert abs(v - 21) < 0.01 * 21


def test_matches_the_analytic_sum_without_sampling() -> None:
    pos = scan_positions(15, 0.2)
    scat = [(0.0, 6.0, 1.0), (0.5, 6.3, 0.6)]
    tr = simulate_bscan(pos, scat, F0, SIGMA, FS, T0, NS)
    zs = [5.95, 6.0, 6.3]
    got = saft_complex(tr, pos, XS[::2], zs, T0, FS, F0)
    for a, pz in enumerate(zs):
        for b, px in enumerate(XS[::2]):
            want = 0j
            for xk in pos:
                t = 2 * math.hypot(px - xk, pz) / 1.54
                for sx, sz, amp in scat:
                    dt = t - 2 * math.hypot(sx - xk, sz) / 1.54
                    want += amp * math.exp(-dt * dt / (2 * SIGMA ** 2)) * cmath.exp(2j * math.pi * F0 * dt)
            assert abs(got[a][b] - want) < 0.01 * len(pos)


def test_adjoint() -> None:
    rng = random.Random(4402)
    pos = scan_positions(7, 0.3)
    ns = 50
    xs, zs = [-0.4, 0.0, 0.3], [4.0, 4.2]
    t0 = 5.0
    tr = [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(ns)] for _ in pos]
    img = [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in xs] for _ in zs]
    for half in (None, 0.12):
        a = saft_complex(tr, pos, xs, zs, t0, FS, F0, half)
        b = saft_adjoint(img, pos, xs, zs, t0, FS, F0, ns, half)
        lhs = sum(a[i][j].conjugate() * img[i][j] for i in range(len(zs)) for j in range(len(xs)))
        rhs = sum(tr[k][q].conjugate() * b[k][q] for k in range(len(pos)) for q in range(ns))
        na = math.sqrt(sum(abs(v) ** 2 for row in a for v in row))
        ni = math.sqrt(sum(abs(v) ** 2 for row in img for v in row))
        assert abs(lhs - rhs) <= 1e-10 * na * ni


def test_longer_synthetic_aperture_gives_a_narrower_peak() -> None:
    widths = []
    for k_count in (5, 11, 21, 41):
        pos = scan_positions(k_count, 0.15)
        tr = simulate_bscan(pos, [(0.0, 6.0, 1.0)], F0, SIGMA, FS, T0, NS)
        prof = saft(tr, pos, XS, [6.0], T0, FS, F0)[0]
        widths.append(sum(1 for v in prof if v >= 0.5 * max(prof)))
    assert all(w1 > w2 for w1, w2 in zip(widths, widths[1:]))


def test_narrower_than_the_unfocused_bscan() -> None:
    pos = scan_positions(21, 0.15)
    tr = simulate_bscan(pos, [(0.0, 6.0, 1.0)], F0, SIGMA, FS, T0, NS)
    focused = saft(tr, pos, XS, [6.0], T0, FS, F0)[0]
    raw = envelope_bscan(tr, pos, XS, [6.0], T0, FS, F0)[0]
    assert sum(1 for v in focused if v >= 0.5 * max(focused)) <= 3
    assert sum(1 for v in raw if v >= 0.5 * max(raw)) == len(XS)


def test_half_angle_limits_the_positions_in_the_sum() -> None:
    pos = scan_positions(21, 0.15)
    tr = simulate_bscan(pos, [(0.0, 6.0, 1.0)], F0, SIGMA, FS, T0, NS)
    half = math.atan(0.8 / 6.0)  # positions with |x_k| <= 0.8 mm: 11 of them
    used = sum(1 for xk in pos if abs(xk) <= 6.0 * math.tan(half))
    assert used == 11
    v = saft(tr, pos, [0.0], [6.0], T0, FS, F0, half)[0][0]
    assert abs(v - used) < 0.01 * used
