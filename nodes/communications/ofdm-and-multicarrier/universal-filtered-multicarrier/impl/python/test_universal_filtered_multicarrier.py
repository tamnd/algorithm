# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/universal-filtered-multicarrier/. The authors are listed in prov/45M7YX.jsonl.

import cmath
import math
import random

from universal_filtered_multicarrier import (
    channel,
    dolph_chebyshev,
    fft,
    ofdm_block,
    receive,
    spectrum,
    subband_filters,
    transmit,
)

N = 64
BANDS = [list(range(-12 + 6 * i, -6 + 6 * i)) for i in range(4)]
USED = [k for b in BANDS for k in b]
QPSK = [complex(a, b) / math.sqrt(2) for a in (-1, 1) for b in (-1, 1)]


def random_bins(rng):
    X = [0j] * N
    for k in USED:
        X[k % N] = rng.choice(QPSK)
    return X


def test_fft_matches_direct_sum():
    rng = random.Random(1)
    a = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(16)]
    A = fft(a)
    for k in range(16):
        d = sum(a[n] * cmath.exp(-2j * math.pi * k * n / 16) for n in range(16))
        assert abs(A[k] - d) < 1e-12
    b = fft(A, inverse=True)
    assert max(abs(u / 16 - v) for u, v in zip(b, a)) < 1e-12


def test_dolph_chebyshev_is_equiripple():
    for length, att in ((17, 40), (9, 40), (33, 60)):
        w = dolph_chebyshev(length, att)
        assert abs(sum(w) - 1) < 1e-12
        assert max(abs(w[n] - w[length - 1 - n]) for n in range(length)) < 1e-12
        x0 = math.cosh(math.acosh(10 ** (att / 20)) / (length - 1))
        null = 2 * math.acos(math.cos(math.pi / (2 * (length - 1))) / x0)
        c = (length - 1) / 2
        grid = [null + (math.pi - null) * i / 400 for i in range(401)]
        peak = max(abs(sum(v * cmath.exp(-1j * om * (t - c)) for t, v in enumerate(w))) for om in grid)
        assert abs(20 * math.log10(peak) + att) < 0.01


def test_round_trip_without_channel():
    rng = random.Random(2)
    for length in (9, 17, 33):
        f = subband_filters(BANDS, N, dolph_chebyshev(length, 40))
        X = random_bins(rng)
        x = transmit(X, BANDS, f)
        assert len(x) == N + length - 1
        Xh = receive(x, N, BANDS, f)
        assert max(abs(Xh[k % N] - X[k % N]) for k in USED) < 1e-9


def test_round_trip_through_a_channel():
    rng = random.Random(3)
    f = subband_filters(BANDS, N, dolph_chebyshev(17, 40))
    for _ in range(3):
        h = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(8)]
        X = random_bins(rng)
        y = channel(transmit(X, BANDS, f), h)
        Xh = receive(y, N, BANDS, f, h)
        assert max(abs(Xh[k % N] - X[k % N]) for k in USED) < 1e-9


def test_even_bins_carry_the_data():
    rng = random.Random(4)
    f = subband_filters(BANDS, N, dolph_chebyshev(17, 40))
    X = random_bins(rng)
    Y = fft(transmit(X, BANDS, f) + [0j] * (N - 16))
    for band, fi in zip(BANDS, f):
        F = fft(fi + [0j] * (2 * N - len(fi)))
        for k in band:
            i = (2 * k) % (2 * N)
            assert abs(Y[i] - math.sqrt(N) * F[i] * X[k % N]) < 1e-9


def test_less_out_of_band_power_than_ofdm():
    rng = random.Random(5)
    length = 17
    f = subband_filters(BANDS, N, dolph_chebyshev(length, 40))
    su = [0.0] * 256
    so = [0.0] * 256
    for _ in range(20):
        X = random_bins(rng)
        su = [a + b for a, b in zip(su, spectrum(transmit(X, BANDS, f), 256))]
        so = [a + b for a, b in zip(so, spectrum(ofdm_block(X, USED, length - 1), 256))]

    def leak(s):
        inband = sum(s[i % 256] for i in range(-48, 48)) / 96
        far = max(s[i % 256] for i in range(-128, 128) if i < -64 or i >= 64)
        return 10 * math.log10(far / inband)

    assert leak(su) < -45
    assert leak(so) > -25
