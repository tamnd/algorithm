# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conjugate-phase-reconstruction/. The authors are listed in prov/ES8X47.jsonl.

import cmath
import math
import random

from conjugate_phase_reconstruction import conjugate_phase, epi_cartesian, forward, pixel_grid
from imgla import adjoint_gap, solve


def rel_err(a, b):
    return math.sqrt(sum(abs(u - v) ** 2 for u, v in zip(a, b))) / math.sqrt(sum(abs(v) ** 2 for v in b))


def disk(n):
    return [1.0 if (c / (n / 2)) ** 2 + (a / (n / 2)) ** 2 < 0.7 else 0.0 for c, a in pixel_grid(n)]


def smooth_field(n, hz):
    return [2 * math.pi * hz * math.exp(-((c - n / 6) ** 2 + (a + n / 8) ** 2) / (2 * (n / 4) ** 2)) for c, a in pixel_grid(n)]


def test_adjoint_of_forward_model():
    rng = random.Random(21)
    n = 6
    pos = pixel_grid(n)
    omega = [rng.uniform(-200, 200) for _ in pos]
    ks = [(rng.uniform(-0.5, 0.5), rng.uniform(-0.5, 0.5)) for _ in range(40)]
    ts = [rng.uniform(0, 0.01) for _ in ks]
    x = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in pos]
    y = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in ks]

    def a(v):
        return forward(v, pos, omega, ks, ts)

    def ah(v):
        return conjugate_phase(v, ks, ts, [1.0] * len(ks), pos, omega)

    assert adjoint_gap(a, ah, x, y) < 1e-12


def test_full_cartesian_without_field_is_inverse_dft():
    rng = random.Random(22)
    n = 8
    pos = pixel_grid(n)
    x = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in pos]
    ks, ts = epi_cartesian(n, float(n))
    zero = [0.0] * len(pos)
    s = forward(x, pos, zero, ks, ts)
    out = conjugate_phase(s, ks, ts, [1.0 / len(ks)] * len(ks), pos, zero)
    assert rel_err(out, x) < 1e-12


def test_constant_field_is_exact():
    rng = random.Random(23)
    n = 8
    pos = pixel_grid(n)
    x = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in pos]
    ks, ts = epi_cartesian(n, float(n), esp=6e-4)
    omega = [2 * math.pi * 75.0] * len(pos)
    s = forward(x, pos, omega, ks, ts)
    out = conjugate_phase(s, ks, ts, [1.0 / len(ks)] * len(ks), pos, omega)
    assert rel_err(out, x) < 1e-12
    # Without the correction the same data give a different image.
    plain = conjugate_phase(s, ks, ts, [1.0 / len(ks)] * len(ks), pos, [0.0] * len(pos))
    assert rel_err(plain, x) > 0.5


def test_smooth_field_map_epi():
    n = 16
    pos = pixel_grid(n)
    x = disk(n)
    omega = smooth_field(n, 40.0)
    ks, ts = epi_cartesian(n, float(n))
    s = forward(x, pos, omega, ks, ts)
    w = [1.0 / len(ks)] * len(ks)
    cp = conjugate_phase(s, ks, ts, w, pos, omega)
    plain = conjugate_phase(s, ks, ts, w, pos, [0.0] * len(pos))
    assert rel_err(cp, x) < 0.06
    assert rel_err(cp, x) < 0.1 * rel_err(plain, x)
    mag_cp = rel_err([abs(v) for v in cp], x)
    mag_plain = rel_err([abs(v) for v in plain], x)
    assert mag_cp < mag_plain


def test_exact_solve_beats_conjugate_phase():
    n = 8
    pos = pixel_grid(n)
    x = disk(n)
    omega = smooth_field(n, 60.0)
    ks, ts = epi_cartesian(n, float(n), esp=8e-4)
    s = forward(x, pos, omega, ks, ts)
    # The square system A x = s, built column by column from unit images.
    m = len(ks)
    cols = []
    for i in range(len(pos)):
        e = [0.0] * len(pos)
        e[i] = 1.0
        cols.append(forward(e, pos, omega, ks, ts))
    a = [[cols[i][j] for i in range(len(pos))] for j in range(m)]
    exact = solve(a, s)
    assert rel_err(exact, x) < 1e-9
    cp = conjugate_phase(s, ks, ts, [1.0 / m] * m, pos, omega)
    e_cp = rel_err(cp, x)
    assert 1e-4 < e_cp < 0.1


def test_phase_of_sample_matches_model():
    # One pixel at r with field omega: s_j = exp(-i (omega t_j + 2 pi k_j . r)).
    pos = [(1.5, -2.0)]
    omega = [300.0]
    ks = [(0.1, 0.2), (-0.3, 0.05)]
    ts = [0.001, 0.004]
    s = forward([1.0], pos, omega, ks, ts)
    for sj, k, t in zip(s, ks, ts):
        want = cmath.exp(-1j * (300.0 * t + 2 * math.pi * (k[0] * 1.5 - k[1] * 2.0)))
        assert abs(sj - want) < 1e-14
