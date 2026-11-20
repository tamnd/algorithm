# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/selected-mapping/. The authors are listed in prov/GWPD9C.jsonl.

import cmath
import math
import random

from selected_mapping import fft, papr, phase_table, selected_mapping, slm_receive, to_bins, to_time

QPSK = [complex(a, b) / math.sqrt(2) for a in (1, -1) for b in (1, -1)]


def block(rng, n=64):
    return [rng.choice(QPSK) for _ in range(n)]


def direct_time(X, L):
    """The oversampled OFDM symbol from its definition."""
    n = len(X)
    freqs = list(range(n // 2)) + list(range(-(n // 2), 0))
    return [sum(X[i] * cmath.exp(2j * math.pi * f * m / (L * n)) for i, f in enumerate(freqs)) / math.sqrt(n) for m in range(L * n)]


def test_fft_and_oversampled_symbol():
    rng = random.Random(1)
    X = block(rng, 16)
    assert max(abs(a - b) for a, b in zip(to_time(X, 2), direct_time(X, 2))) < 1e-9
    assert max(abs(a - 16 * b) for a, b in zip(fft(fft(X), inverse=True), X)) < 1e-9


def test_table_shape():
    t = phase_table(8, 32, 9)
    assert len(t) == 8 and all(len(r) == 32 for r in t)
    assert all(v == 1 for v in t[0])
    assert all(v in (1, -1, 1j, -1j) for r in t for v in r)


def test_choice_matches_brute_force():
    rng = random.Random(2)
    table = phase_table(6, 16, 3)
    for _ in range(20):
        X = block(rng, 16)
        u, x, ratios = selected_mapping(X, table, 4)
        brute = [papr(direct_time([a * b for a, b in zip(X, p)], 4)) for p in table]
        assert max(abs(a - b) for a, b in zip(ratios, brute)) < 1e-9
        assert u == min(range(6), key=lambda i: (brute[i], i))
        assert abs(papr(x) - min(brute)) < 1e-9


def test_one_candidate_is_plain_ofdm():
    rng = random.Random(4)
    X = block(rng)
    u, x, _ = selected_mapping(X, phase_table(1, 64, 0), 4)
    assert u == 0
    assert max(abs(a - b) for a, b in zip(x, to_time(X, 4))) < 1e-12


def test_round_trip_recovers_the_data():
    rng = random.Random(5)
    table = phase_table(8, 64, 7)
    for _ in range(10):
        X = block(rng)
        u, x, _ = selected_mapping(X, table, 4)
        assert max(abs(a - b) for a, b in zip(slm_receive(to_bins(x, 4), table, u), X)) < 1e-9


def test_more_candidates_never_hurt():
    rng = random.Random(6)
    table = phase_table(8, 64, 11)
    gains = []
    for _ in range(40):
        X = block(rng)
        _, _, r = selected_mapping(X, table, 4)
        best = [min(r[:u]) for u in range(1, 9)]
        assert all(best[i + 1] <= best[i] for i in range(7))
        gains.append(10 * math.log10(r[0] / best[-1]))
    assert sum(gains) / len(gains) > 1.0
