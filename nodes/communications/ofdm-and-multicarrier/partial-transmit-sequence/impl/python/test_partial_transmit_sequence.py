# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/partial-transmit-sequence/. The authors are listed in prov/JND5P6.jsonl.

import cmath
import itertools
import math
import random

from partial_transmit_sequence import (
    adjacent_partition,
    fft,
    interleaved_partition,
    papr,
    partial_transmit_sequence,
    pts_receive,
    to_bins,
    to_time,
)

QPSK = [complex(a, b) / math.sqrt(2) for a in (1, -1) for b in (1, -1)]
W4 = (1, -1, 1j, -1j)


def block(rng, n):
    return [rng.choice(QPSK) for _ in range(n)]


def direct_time(X, L):
    """The oversampled OFDM symbol from its definition."""
    n = len(X)
    freqs = list(range(n // 2)) + list(range(-(n // 2), 0))
    return [sum(X[i] * cmath.exp(2j * math.pi * f * m / (L * n)) for i, f in enumerate(freqs)) / math.sqrt(n) for m in range(L * n)]


def test_fft_and_oversampled_symbol():
    rng = random.Random(1)
    X = block(rng, 16)
    assert max(abs(a - b) for a, b in zip(to_time(X, 4), direct_time(X, 4))) < 1e-9
    assert max(abs(a - 16 * b) for a, b in zip(fft(fft(X), inverse=True), X)) < 1e-9


def test_partitions():
    assert adjacent_partition(8, 4) == [0, 0, 1, 1, 2, 2, 3, 3]
    assert interleaved_partition(8, 4) == [0, 1, 2, 3, 0, 1, 2, 3]


def test_search_matches_brute_force_with_one_transform_per_candidate():
    rng = random.Random(2)
    for labels in (adjacent_partition(16, 4), interleaved_partition(16, 4)):
        for _ in range(4):
            X = block(rng, 16)
            b, x, r = partial_transmit_sequence(X, labels, W4, 4)
            brute = math.inf
            for tail in itertools.product(W4, repeat=3):
                bb = (1,) + tail
                brute = min(brute, papr(direct_time([xk * bb[lab] for xk, lab in zip(X, labels)], 4)))
            assert abs(r - brute) < 1e-9
            assert b[0] == 1
            rotated = [xk * b[lab] for xk, lab in zip(X, labels)]
            assert max(abs(p - q) for p, q in zip(x, direct_time(rotated, 4))) < 1e-9


def test_never_worse_than_plain_ofdm_and_round_trip():
    rng = random.Random(3)
    labels = adjacent_partition(64, 4)
    for _ in range(10):
        X = block(rng, 64)
        b, x, r = partial_transmit_sequence(X, labels, W4, 4)
        assert r <= papr(to_time(X, 4)) + 1e-12
        assert max(abs(p - q) for p, q in zip(pts_receive(to_bins(x, 4), labels, b), X)) < 1e-9


def test_one_subblock_is_plain_ofdm():
    rng = random.Random(4)
    X = block(rng, 32)
    b, x, r = partial_transmit_sequence(X, [0] * 32, W4, 4)
    assert b == [1]
    assert abs(r - papr(to_time(X, 4))) < 1e-12


def test_average_gain():
    rng = random.Random(5)
    labels = adjacent_partition(64, 4)
    gains = []
    for _ in range(15):
        X = block(rng, 64)
        gains.append(10 * math.log10(papr(to_time(X, 4)) / partial_transmit_sequence(X, labels, W4, 4)[2]))
    assert sum(gains) / len(gains) > 1.5
