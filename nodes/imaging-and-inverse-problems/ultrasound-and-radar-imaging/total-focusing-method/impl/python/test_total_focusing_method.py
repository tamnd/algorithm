# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/total-focusing-method/. The authors are listed in prov/91YVZD.jsonl.

import cmath
import math
import random

from total_focusing_method import (element_positions, one_way_times, sample, simulate_fmc, tfm,
                                   tfm_adjoint, tfm_complex, tfm_half)

M = 16
PITCH = 0.3
F0, SIGMA, FS, T0, NS = 5.0, 0.1, 40.0, 7.0, 140
ELEMENTS = element_positions(M, PITCH)
XS = [round(-0.7 + 0.1 * k, 10) for k in range(15)]
ZS = [round(5.7 + 0.05 * k, 10) for k in range(13)]


def _peak(img):
    return max((v, i, j) for i, row in enumerate(img) for j, v in enumerate(row))


def test_peak_at_the_scatterer_with_full_coherent_gain() -> None:
    data = simulate_fmc(ELEMENTS, [(0.0, 6.0, 1.0)], F0, SIGMA, FS, T0, NS)
    img = tfm(data, ELEMENTS, XS, ZS, T0, FS, F0)
    v, i, j = _peak(img)
    assert abs(XS[j]) < 1e-9 and abs(ZS[i] - 6.0) < 1e-9
    # every one of the M^2 pairs adds the value 1 in phase; linear interpolation loses under 1 percent
    assert abs(v - M * M) < 0.01 * M * M


def test_matches_the_analytic_sum_without_sampling() -> None:
    scat = [(0.0, 6.0, 1.0), (0.4, 6.2, 0.5)]
    data = simulate_fmc(ELEMENTS, scat, F0, SIGMA, FS, T0, NS)
    got = tfm_complex(data, ELEMENTS, XS[::4], ZS[::4], T0, FS, F0)
    for a, pz in enumerate(ZS[::4]):
        for b, px in enumerate(XS[::4]):
            d = one_way_times(px, pz, ELEMENTS)
            want = 0j
            for sx, sz, amp in scat:
                ds = one_way_times(sx, sz, ELEMENTS)
                for i in range(M):
                    for j in range(M):
                        dt = d[i] + d[j] - ds[i] - ds[j]
                        want += amp * math.exp(-dt * dt / (2 * SIGMA ** 2)) * cmath.exp(2j * math.pi * F0 * dt)
            assert abs(got[a][b] - want) < 0.01 * M * M


def test_half_matrix_equals_full_matrix_for_reciprocal_data() -> None:
    data = simulate_fmc(ELEMENTS, [(0.2, 6.1, 1.0), (-0.3, 6.3, 0.7)], F0, SIGMA, FS, T0, NS)
    full = tfm(data, ELEMENTS, XS[::2], ZS[::2], T0, FS, F0)
    half = tfm_half(data, ELEMENTS, XS[::2], ZS[::2], T0, FS, F0)
    for r1, r2 in zip(full, half):
        for v1, v2 in zip(r1, r2):
            assert abs(v1 - v2) < 1e-9 * M * M


def test_adjoint() -> None:
    rng = random.Random(9101)
    m, ns = 5, 60
    el = element_positions(m, 0.4)
    xs, zs = [-0.3, 0.0, 0.25], [4.0, 4.1]
    t0 = 5.0
    data = [[[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(ns)] for _ in range(m)] for _ in range(m)]
    img = [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in xs] for _ in zs]
    ad = tfm_complex(data, el, xs, zs, t0, FS, F0)
    back = tfm_adjoint(img, el, xs, zs, t0, FS, F0, ns)
    lhs = sum(ad[i][j].conjugate() * img[i][j] for i in range(len(zs)) for j in range(len(xs)))
    rhs = sum(data[i][j][k].conjugate() * back[i][j][k] for i in range(m) for j in range(m) for k in range(ns))
    na = math.sqrt(sum(abs(v) ** 2 for row in ad for v in row))
    ni = math.sqrt(sum(abs(v) ** 2 for row in img for v in row))
    assert abs(lhs - rhs) <= 1e-10 * na * ni


def test_linear_in_the_data() -> None:
    d1 = simulate_fmc(ELEMENTS, [(0.0, 6.0, 1.0)], F0, SIGMA, FS, T0, NS)
    d2 = simulate_fmc(ELEMENTS, [(0.3, 6.2, -0.8)], F0, SIGMA, FS, T0, NS)
    d12 = simulate_fmc(ELEMENTS, [(0.0, 6.0, 1.0), (0.3, 6.2, -0.8)], F0, SIGMA, FS, T0, NS)
    a = tfm_complex(d1, ELEMENTS, XS[::3], ZS[::3], T0, FS, F0)
    b = tfm_complex(d2, ELEMENTS, XS[::3], ZS[::3], T0, FS, F0)
    c = tfm_complex(d12, ELEMENTS, XS[::3], ZS[::3], T0, FS, F0)
    for ra, rb, rc in zip(a, b, c):
        for va, vb, vc in zip(ra, rb, rc):
            assert abs(va + vb - vc) < 1e-9


def test_two_close_scatterers_are_resolved() -> None:
    data = simulate_fmc(ELEMENTS, [(-0.4, 6.0, 1.0), (0.4, 6.0, 1.0)], F0, SIGMA, FS, T0, NS)
    prof = tfm(data, ELEMENTS, XS, [6.0], T0, FS, F0)[0]
    left, mid, right = prof[XS.index(-0.4)], prof[XS.index(0.0)], prof[XS.index(0.4)]
    assert mid < 0.7 * min(left, right)


def test_narrower_than_one_transmit_with_dynamic_receive() -> None:
    data = simulate_fmc(ELEMENTS, [(0.0, 6.0, 1.0)], F0, SIGMA, FS, T0, NS)
    full = tfm(data, ELEMENTS, XS, [6.0], T0, FS, F0)[0]
    tx = M // 2 - 1
    one = []
    for px in XS:
        d = one_way_times(px, 6.0, ELEMENTS)
        one.append(abs(sum(sample(data[tx][j], d[tx] + d[j], T0, FS, F0) for j in range(M))))
    width_full = sum(1 for v in full if v >= 0.5 * max(full))
    width_one = sum(1 for v in one if v >= 0.5 * max(one))
    assert width_full < width_one


def test_pixel_outside_the_recorded_window_is_zero() -> None:
    data = simulate_fmc(ELEMENTS, [(0.0, 6.0, 1.0)], F0, SIGMA, FS, T0, NS)
    img = tfm(data, ELEMENTS, [0.0], [2.0, 12.0], T0, FS, F0)
    assert img[0][0] == 0.0 and img[1][0] == 0.0
