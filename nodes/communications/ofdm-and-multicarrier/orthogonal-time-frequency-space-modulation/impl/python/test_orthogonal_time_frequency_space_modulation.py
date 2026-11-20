# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/orthogonal-time-frequency-space-modulation/. The authors are listed in prov/6XP9EH.jsonl.

import cmath
import math
import random

from orthogonal_time_frequency_space_modulation import (
    channel,
    dd_channel,
    demodulate,
    fft,
    isfft,
    lmmse,
    modulate,
    sfft,
)

QPSK = [complex(a, b) / math.sqrt(2) for a in (-1, 1) for b in (-1, 1)]
PATHS = [(0.8 + 0.1j, 0, 0), (-0.3 + 0.4j, 1, 2), (0.2 - 0.35j, 3, -1)]


def grid(rng, n, m):
    return [[rng.choice(QPSK) for _ in range(m)] for _ in range(n)]


def test_fft_matches_direct_sum():
    rng = random.Random(1)
    a = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(16)]
    A = fft(a)
    for k in range(16):
        assert abs(A[k] - sum(a[t] * cmath.exp(-2j * math.pi * k * t / 16) for t in range(16))) < 1e-12


def test_isfft_formula_and_inverse():
    rng = random.Random(2)
    n, m = 4, 8
    x = grid(rng, n, m)
    X = isfft(x)
    for a in range(n):
        for b in range(m):
            d = sum(x[k][l] * cmath.exp(2j * math.pi * (a * k / n - b * l / m)) for k in range(n) for l in range(m)) / math.sqrt(n * m)
            assert abs(X[a][b] - d) < 1e-12
    back = sfft(X)
    assert max(abs(back[k][l] - x[k][l]) for k in range(n) for l in range(m)) < 1e-12


def test_frame_is_an_inverse_dft_along_doppler():
    rng = random.Random(3)
    n, m = 8, 16
    x = grid(rng, n, m)
    s = modulate(x, 0)
    for a in range(n):
        for l in range(m):
            d = sum(x[k][l] * cmath.exp(2j * math.pi * a * k / n) for k in range(n)) / math.sqrt(n)
            assert abs(s[a * m + l] - d) < 1e-12


def test_peak_power_is_at_most_n_times_the_mean():
    rng = random.Random(7)
    n, m = 8, 16
    for _ in range(20):
        s = modulate(grid(rng, n, m), 0)
        mean = sum(abs(v) ** 2 for v in s) / len(s)
        assert abs(mean - 1) < 1e-9
        assert max(abs(v) ** 2 for v in s) <= n * mean + 1e-9
    s = modulate([[1] * m] + [[0] * m for _ in range(n - 1)], 0)
    assert max(abs(v) ** 2 for v in s) < 1 + 1e-9
    s = modulate([[1] * m for _ in range(n)], 0)
    assert abs(max(abs(v) ** 2 for v in s) - n) < 1e-9


def test_round_trip_without_channel():
    rng = random.Random(4)
    n, m, cp = 8, 16, 4
    x = grid(rng, n, m)
    s = modulate(x, cp)
    assert len(s) == n * m + cp
    y = demodulate(s, n, m, cp)
    assert max(abs(y[k][l] - x[k][l]) for k in range(n) for l in range(m)) < 1e-9


def test_delay_doppler_matrix_matches_the_channel():
    rng = random.Random(5)
    n, m, cp = 8, 16, 4
    x = grid(rng, n, m)
    y = demodulate(channel(modulate(x, cp), PATHS, n, m, cp), n, m, cp)
    G = dd_channel(PATHS, n, m)
    v = [c for row in x for c in row]
    for i in range(n * m):
        assert abs(y[i // m][i % m] - sum(G[i][j] * v[j] for j in range(n * m))) < 1e-9
    for j in range(n * m):
        assert sum(1 for i in range(n * m) if abs(G[i][j]) > 1e-12) == len(PATHS)


def test_a_single_pilot_shows_the_paths():
    n, m, cp = 8, 16, 4
    x = [[0j] * m for _ in range(n)]
    x[2][5] = 1
    y = demodulate(channel(modulate(x, cp), PATHS, n, m, cp), n, m, cp)
    for h, l, k in PATHS:
        assert abs(abs(y[(2 + k) % n][(5 + l) % m]) - abs(h)) < 1e-9
    assert sum(1 for row in y for v in row if abs(v) > 1e-9) == len(PATHS)


def test_equalizer_round_trip():
    rng = random.Random(6)
    n, m, cp = 4, 8, 4
    x = grid(rng, n, m)
    y = demodulate(channel(modulate(x, cp), PATHS, n, m, cp), n, m, cp)
    xh = lmmse(dd_channel(PATHS, n, m), y, 0.0)
    assert max(abs(xh[k][l] - x[k][l]) for k in range(n) for l in range(m)) < 1e-9
