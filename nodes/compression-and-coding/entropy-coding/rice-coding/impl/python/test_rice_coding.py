# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rice-coding/. The authors are listed in prov/3VFKPT.jsonl.

import math
import random

import pytest

from rice_coding import (
    BitReader,
    best_k_for_theta,
    decode_all,
    encode_all,
    fold,
    jpegls_k,
    k_from_mean,
    rice_codeword,
    rice_decode,
    rice_length,
    unfold,
)


def golomb_oracle(x: int, m: int) -> str:
    """Golomb codeword with unary as zeros ended by a one and the remainder in
    truncated binary, written from the definition with string formatting."""
    q, r = divmod(x, m)
    k = math.floor(math.log2(m))
    u = 2 ** (k + 1) - m
    tail = format(r, "b").zfill(k) if r < u else format(r + u, "b").zfill(k + 1)
    return "0" * q + "1" + (tail if k or r >= u else "")


def test_flac_example() -> None:
    # RFC 9639, Section 9.2.7.2 (Rice code), copied by hand: with Rice parameter 3,
    # the folded residual 38 is coded as 0b00001110 (unary 00001 for quotient 4, then 110).
    assert rice_codeword(38, 3) == "00001110"
    # Folding in the same section: v >= 0 -> 2v, v < 0 -> -2v - 1.
    assert [fold(v) for v in (0, -1, 1, -2, 2, 19)] == [0, 1, 2, 3, 4, 38]
    for v in range(-1000, 1000):
        assert unfold(fold(v)) == v


def test_equals_golomb_power_of_two() -> None:
    for k in range(0, 9):
        for x in range(0, 300):
            assert rice_codeword(x, k) == golomb_oracle(x, 2**k)
            assert rice_length(x, k) == len(rice_codeword(x, k))


def expected_length(theta: float, k: int) -> float:
    t = theta ** (2**k)
    return k + 1 + t / (1 - t)


def test_k_rule_against_exhaustive_expected_length() -> None:
    for i in range(1, 4000):
        theta = i / 4000
        best = min(range(0, 25), key=lambda k: (expected_length(theta, k), k))
        assert best_k_for_theta(theta) == best


def test_k_from_sample_mean_against_exhaustive_size() -> None:
    # On samples from geometric sources, k from the sample mean is close to the
    # exhaustive best k for the sample: within 2 percent of the best size.
    rng = random.Random(61)
    hits = 0
    for _ in range(500):
        theta = rng.uniform(0.2, 0.999)
        xs = [int(math.log(1 - rng.random()) / math.log(theta)) for _ in range(200)]
        sizes = [sum(rice_length(x, k) for x in xs) for k in range(25)]
        best = min(sizes)
        k = k_from_mean(sum(xs) / len(xs))
        assert sizes[k] <= 1.02 * best
        hits += sizes[k] == best
    assert hits >= 450


def test_jpegls_rule() -> None:
    # ITU-T T.87 (LOCO-I): smallest k with N * 2^k >= A.
    assert jpegls_k(1, 0) == 0
    assert jpegls_k(4, 4) == 0
    assert jpegls_k(4, 5) == 1
    assert jpegls_k(4, 33) == 4
    for n in range(1, 40):
        for a in range(0, 400):
            k = jpegls_k(n, a)
            assert n * 2**k >= a and (k == 0 or n * 2 ** (k - 1) < a)


def test_round_trip_random() -> None:
    rng = random.Random(67)
    for _ in range(500):
        k = rng.randrange(0, 20)
        values = [rng.randrange(0, 40 << k) for _ in range(rng.randrange(20))]
        data, nbits = encode_all(values, k)
        assert nbits == sum(rice_length(v, k) for v in values)
        assert decode_all(data, nbits, k) == values


def test_worked_example() -> None:
    # k = 2: 9 = 2 * 4 + 1 -> 001 01; 3 -> 1 11; 0 -> 1 00.
    assert rice_codeword(9, 2) == "001" + "01"
    assert rice_codeword(3, 2) == "1" + "11"
    assert decode_all(*encode_all([9, 3, 0], 2), 2) == [9, 3, 0]


def test_edge_cases() -> None:
    assert rice_codeword(0, 0) == "1"
    assert rice_codeword(5, 0) == "000001"
    assert decode_all(*encode_all([], 3), 3) == []
    assert decode_all(*encode_all([2**64 - 1], 60), 60) == [2**64 - 1]
    with pytest.raises(ValueError):
        rice_codeword(-1, 2)
    data, nbits = encode_all([100], 3)
    with pytest.raises(EOFError):
        rice_decode(3, BitReader(data, nbits - 1))
