# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/affine-frequency-division-multiplexing/. The authors are listed in prov/94W5XF.jsonl.

import cmath
import math
import random

from affine_frequency_division_multiplexing import (
    c1_for,
    channel,
    demodulate,
    effective_channel,
    fft,
    lmmse,
    modulate,
)

QPSK = [complex(a, b) / math.sqrt(2) for a in (-1, 1) for b in (-1, 1)]
N = 32
C1 = c1_for(1, N)
C2 = math.sqrt(2) / (8 * N)
PATHS = [(0.8 + 0.1j, 0, 0), (-0.3 + 0.4j, 1, 1), (0.2 - 0.35j, 2, -1)]


def symbols(rng, n):
    return [rng.choice(QPSK) for _ in range(n)]


def formula(x, c1, c2, t):
    n = len(x)
    return sum(x[m] * cmath.exp(2j * math.pi * (c1 * t * t + c2 * m * m + t * m / n)) for m in range(n)) / math.sqrt(n)


def test_fft_matches_direct_sum():
    rng = random.Random(1)
    a = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(16)]
    A = fft(a)
    for k in range(16):
        assert abs(A[k] - sum(a[t] * cmath.exp(-2j * math.pi * k * t / 16) for t in range(16))) < 1e-12


def test_block_and_prefix_follow_the_chirp_formula():
    rng = random.Random(2)
    x = symbols(rng, N)
    cp = 6
    s = modulate(x, C1, C2, cp)
    assert len(s) == N + cp
    for t in range(-cp, N):
        assert abs(s[cp + t] - formula(x, C1, C2, t)) < 1e-9


def test_zero_chirps_give_ofdm():
    rng = random.Random(3)
    x = symbols(rng, N)
    s = modulate(x, 0.0, 0.0, 4)
    v = [u / math.sqrt(N) for u in fft(x, inverse=True)]
    assert max(abs(a - b) for a, b in zip(s, v[-4:] + v)) < 1e-12


def test_round_trip_without_channel():
    rng = random.Random(4)
    x = symbols(rng, N)
    y = demodulate(modulate(x, C1, C2, 4), N, C1, C2, 4)
    assert max(abs(a - b) for a, b in zip(y, x)) < 1e-9


def test_effective_channel_matches_the_channel():
    rng = random.Random(5)
    x = symbols(rng, N)
    cp = 4
    y = demodulate(channel(modulate(x, C1, C2, cp), PATHS, N, cp), N, C1, C2, cp)
    H = effective_channel(PATHS, N, C1, C2)
    for q in range(N):
        assert abs(y[q] - sum(H[q][m] * x[m] for m in range(N))) < 1e-9


def test_paths_land_on_distinct_bins():
    cp = 4
    x = [0j] * N
    x[10] = 1
    y = demodulate(channel(modulate(x, C1, C2, cp), PATHS, N, cp), N, C1, C2, cp)
    for h, l, a in PATHS:
        assert abs(abs(y[(10 + a - 3 * l) % N]) - abs(h)) < 1e-9
    assert sum(1 for v in y if abs(v) > 1e-9) == len(PATHS)
    # every delay up to 2 and Doppler up to 1 in size gets its own bin when (2 + 1)(2 + 1) <= N
    bins = {(a - round(2 * N * C1) * l) % N for l in range(3) for a in (-1, 0, 1)}
    assert len(bins) == 9


def test_without_chirp_paths_with_one_doppler_share_a_bin():
    paths = [(1, 0, 1), (0.5, 2, 1)]
    H = effective_channel(paths, N, 0.0, 0.0)
    assert sum(1 for q in range(N) if abs(H[q][10]) > 1e-9) == 1


def test_equalizer_round_trip():
    rng = random.Random(6)
    x = symbols(rng, N)
    cp = 4
    y = demodulate(channel(modulate(x, C1, C2, cp), PATHS, N, cp), N, C1, C2, cp)
    xh = lmmse(effective_channel(PATHS, N, C1, C2), y, 0.0)
    assert max(abs(a - b) for a, b in zip(xh, x)) < 1e-9
