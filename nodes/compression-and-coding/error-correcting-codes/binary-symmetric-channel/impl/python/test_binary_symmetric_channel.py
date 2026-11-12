# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/binary-symmetric-channel/. The authors are listed in prov/F9CZ5N.jsonl.

import math
import random

from binary_symmetric_channel import (
    binary_entropy, block_error_rate, capacity, cascade, exact_block_error_rate, ml_decode,
    mutual_information, nearest_codewords, transition, transmit,
)


def bits(s: str) -> int:
    return sum(1 << i for i, ch in enumerate(s) if ch == "1")


def span(rows):
    words = {0}
    for r in rows:
        words |= {w ^ r for w in words}
    return sorted(words)


HAMMING_7_4 = span([bits("1000110"), bits("0100011"), bits("0010111"), bits("0001101")])


def test_flip_rate_and_independence() -> None:
    rng = random.Random(2024)
    p, n, trials = 0.1, 20, 20000
    flips = 0
    both = 0
    for _ in range(trials):
        e = transmit(0, n, p, rng)
        flips += e.bit_count()
        both += (e & 1) and (e >> 1 & 1)
    # mean number of flips n p = 2; the standard error is tiny at this sample size
    assert abs(flips / (n * trials) - p) < 0.005
    # P(bit 0 and bit 1 both flip) = p^2 for independent flips
    assert abs(both / trials - p * p) < 0.003


def test_transition_rows_sum_to_one() -> None:
    for n in range(1, 7):
        for p in (0.0, 0.1, 0.5, 0.9):
            for x in range(1 << n):
                assert math.isclose(sum(transition(x, y, n, p) for y in range(1 << n)), 1.0)


def test_capacity_values() -> None:
    assert capacity(0.0) == 1.0 and capacity(0.5) == 0.0
    assert math.isclose(capacity(0.11), 1 - binary_entropy(0.11))
    assert abs(capacity(0.11) - 0.5) < 0.001  # h(0.11) is close to 1/2
    assert math.isclose(capacity(0.2), capacity(0.8))
    # the uniform input maximizes I(X; Y): check on a fine grid of input laws
    for p in (0.01, 0.1, 0.25, 0.4):
        grid = max(mutual_information(a / 1000, p) for a in range(1001))
        assert math.isclose(grid, capacity(p), abs_tol=1e-12)
        assert mutual_information(0.3, p) < capacity(p)


def test_cascade() -> None:
    # exact check: compose the 2 x 2 transition matrices
    for p in (0.05, 0.2, 0.4):
        for q in (0.0, 0.1, 0.3):
            m = [[1 - p, p], [p, 1 - p]]
            k = [[1 - q, q], [q, 1 - q]]
            prod = [[sum(m[i][j] * k[j][l] for j in range(2)) for l in range(2)] for i in range(2)]
            r = cascade(p, q)
            assert math.isclose(prod[0][1], r) and math.isclose(prod[1][0], r)
            assert r >= min(p, q) - 1e-15 and r <= 0.5
            assert capacity(r) <= min(capacity(p), capacity(q)) + 1e-12


def test_degraded_from_erasure_channel() -> None:
    # BEC(2p) followed by "replace ? with a fair coin" is BSC(p)
    for p in (0.05, 0.2, 0.45):
        eps = 2 * p
        bec = [[1 - eps, 0.0, eps], [0.0, 1 - eps, eps]]  # outputs 0, 1, ?
        coin = [[1.0, 0.0], [0.0, 1.0], [0.5, 0.5]]  # 0 -> 0, 1 -> 1, ? -> fair coin
        prod = [[sum(bec[i][j] * coin[j][l] for j in range(3)) for l in range(2)] for i in range(2)]
        for i in range(2):
            for l in range(2):
                assert math.isclose(prod[i][l], transition(i, l, 1, p))
        assert capacity(p) <= 1 - eps + 1e-12  # so 1 - h(p) <= 1 - 2p


def test_ml_equals_minimum_distance_exhaustive() -> None:
    for p in (0.01, 0.1, 0.3, 0.49):
        for y in range(1 << 7):
            assert ml_decode(HAMMING_7_4, y, 7, p) == nearest_codewords(HAMMING_7_4, y)
    # with p > 1/2 the order reverses: ML picks the farthest codeword
    y = bits("1000000")
    assert ml_decode(HAMMING_7_4, y, 7, 0.9) != nearest_codewords(HAMMING_7_4, y)


def test_hamming_block_error_rate() -> None:
    # Hamming (7, 4) is perfect: decoding fails exactly when 2 or more bits flip
    p = 0.05
    exact = 1 - (1 - p) ** 7 - 7 * p * (1 - p) ** 6
    assert math.isclose(exact_block_error_rate(HAMMING_7_4, 7, p), exact)
    mc = block_error_rate(HAMMING_7_4, 7, p, 20000, seed=7)
    assert abs(mc - exact) < 0.006
