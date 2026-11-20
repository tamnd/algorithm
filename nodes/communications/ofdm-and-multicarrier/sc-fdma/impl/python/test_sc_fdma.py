# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sc-fdma/. The authors are listed in prov/1A5ZQW.jsonl.

import cmath
import math
import random

from sc_fdma import channel, fft, oversampled, papr, receive, subcarriers, transmit, udft, uidft

QPSK = [complex(a, b) / math.sqrt(2) for a in (1, -1) for b in (1, -1)]


def rule(gamma, n):
    return 1 - (1 - math.exp(-gamma)) ** n


def wilson(k, n, z=3.0):
    p = k / n
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return c - h, c + h


def ofdm_oversampled(X, n, L):
    Z = [0j] * n
    Z[: len(X)] = X
    z = [0j] * (L * n)
    z[: n // 2] = Z[: n // 2]
    z[L * n - n + n // 2:] = Z[n // 2:]
    return [v / math.sqrt(n) for v in fft(z, inverse=True)]


def test_unitary_dft():
    rng = random.Random(1)
    x = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(16)]
    X = udft(x)
    ref = [sum(x[t] * cmath.exp(-2j * math.pi * k * t / 16) for t in range(16)) / 4 for k in range(16)]
    assert max(abs(u - v) for u, v in zip(X, ref)) < 1e-9
    assert max(abs(u - v) for u, v in zip(uidft(X), x)) < 1e-9


def test_round_trip_through_a_channel():
    rng = random.Random(2)
    n, m, cp = 64, 16, 4
    for mapping in ("localized", "interleaved"):
        for offset in (0, 3, 50):
            d = [rng.choice(QPSK) for _ in range(m)]
            h = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(cp + 1)]
            s = transmit(d, n, mapping, offset, cp)
            assert len(s) == n + cp
            r = channel(s, h)
            dh = receive(r, m, n, mapping, offset, cp, h)
            assert max(abs(u - v) for u, v in zip(dh, d)) < 1e-9
            assert max(abs(u - v) for u, v in zip(receive(s, m, n, mapping, offset, cp), d)) < 1e-9


def test_interleaved_is_a_repeated_and_rotated_copy():
    rng = random.Random(3)
    n, m, r = 64, 16, 5
    q = n // m
    d = [rng.choice(QPSK) for _ in range(m)]
    x = transmit(d, n, "interleaved", r)
    for t in range(n):
        want = d[t % m] * cmath.exp(2j * math.pi * r * t / n) / math.sqrt(q)
        assert abs(x[t] - want) < 1e-9
    assert abs(papr(x) - 1) < 1e-9


def test_full_band_is_single_carrier():
    rng = random.Random(4)
    d = [rng.choice(QPSK) for _ in range(32)]
    assert max(abs(u - v) for u, v in zip(transmit(d, 32, "localized"), d)) < 1e-9


def test_subcarrier_maps():
    assert subcarriers(4, 16, "localized", 14) == [14, 15, 0, 1]
    assert subcarriers(4, 16, "interleaved", 1) == [1, 5, 9, 13]


def test_papr_below_ofdm_and_below_the_rule():
    rng = random.Random(5)
    n, m, trials = 64, 16, 400
    sc, of = [], []
    for _ in range(trials):
        d = [rng.choice(QPSK) for _ in range(m)]
        sc.append(papr(oversampled(d, n, "localized", 0, 4)))
        of.append(papr(ofdm_oversampled(d, n, 4)))
    mean_db = lambda v: 10 * math.log10(sum(v) / len(v))
    assert mean_db(of) - mean_db(sc) > 1.0
    g = 10 ** 0.6
    _, hi = wilson(sum(1 for v in sc if v > g), trials)
    lo, _ = wilson(sum(1 for v in of if v > g), trials)
    assert hi < rule(g, m) / 2
    assert lo > rule(g, m)
