# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hamming-weight/. The authors are listed in prov/N2T38H.jsonl.

import itertools
import random

from hamming_weight import codewords, hamming_weight, hamming_weight_bits, minimum_weight, weight_distribution


def bits(s: str) -> int:
    """A word written left to right as coordinate 0, 1, ...; bit i of the integer is coordinate i."""
    return sum(1 << i for i, ch in enumerate(s) if ch == "1")


# The [7, 4] Hamming code with G = [I | P] (Lin and Costello, Section 3.1).
HAMMING_7_4 = [bits("1000110"), bits("0100011"), bits("0010111"), bits("0001101")]


def golay_23_rows() -> list:
    # g(x) = x^11 + x^10 + x^6 + x^5 + x^4 + x^2 + 1 generates the binary [23, 12, 7] Golay code
    g = (1 << 11) | (1 << 10) | (1 << 6) | (1 << 5) | (1 << 4) | (1 << 2) | 1
    return [g << i for i in range(12)]


def test_weights() -> None:
    assert hamming_weight([0, 3, 0, 1, 4]) == 3
    assert hamming_weight([]) == 0
    assert hamming_weight_bits(0b1011101) == 5
    assert hamming_weight_bits(0) == 0


def test_hamming_7_4_distribution() -> None:
    # known weight distribution 1, 7, 7, 1 at weights 0, 3, 4, 7
    assert weight_distribution(HAMMING_7_4, 7) == [1, 0, 0, 7, 7, 0, 0, 1]
    assert minimum_weight(HAMMING_7_4, 7) == 3


def test_golay_distributions() -> None:
    rows = golay_23_rows()
    a = weight_distribution(rows, 23)
    expected = {0: 1, 7: 253, 8: 506, 11: 1288, 12: 1288, 15: 506, 16: 253, 23: 1}
    assert a == [expected.get(w, 0) for w in range(24)]
    ext = [r | ((r.bit_count() & 1) << 23) for r in rows]  # add an overall parity bit
    a24 = weight_distribution(ext, 24)
    expected24 = {0: 1, 8: 759, 12: 2576, 16: 759, 24: 1}
    assert a24 == [expected24.get(w, 0) for w in range(25)]


def test_gray_order_lists_every_codeword_once() -> None:
    rng = random.Random(5)
    for _ in range(50):
        k = rng.randrange(1, 7)
        rows = [1 << i | (rng.getrandbits(5) << 6) for i in range(k)]  # independent: identity part
        cw = codewords(rows)
        brute = set()
        for m in range(1 << k):
            c = 0
            for i in range(k):
                if m >> i & 1:
                    c ^= rows[i]
            brute.add(c)
        assert len(cw) == 1 << k and set(cw) == brute


def test_min_weight_equals_min_distance_for_linear_codes() -> None:
    rng = random.Random(77)
    for _ in range(500):
        n = rng.randrange(2, 9)
        k = rng.randrange(1, n)
        rows = [(1 << i) | (rng.getrandbits(n - k) << k) for i in range(k)]
        cw = codewords(rows)
        dmin = min(hamming_weight_bits(a ^ b) for a, b in itertools.combinations(cw, 2))
        assert dmin == minimum_weight(rows, n)


def test_nonlinear_code_counterexample() -> None:
    # this set holds 0 but is not closed under XOR (110 ^ 101 = 011 is missing),
    # and its minimum distance (1) differs from its least nonzero weight (2)
    code = [0b000, 0b110, 0b101, 0b111]
    dmin = min(hamming_weight_bits(a ^ b) for a, b in itertools.combinations(code, 2))
    wmin = min(hamming_weight_bits(c) for c in code if c)
    assert dmin == 1 and wmin == 2


def test_even_weight_property() -> None:
    # in a binary linear code, all weights are even, or exactly half of them are
    rng = random.Random(3)
    for _ in range(500):
        n = rng.randrange(2, 10)
        k = rng.randrange(1, n)
        rows = [(1 << i) | (rng.getrandbits(n - k) << k) for i in range(k)]
        a = weight_distribution(rows, n)
        even = sum(a[0::2])
        assert even == 1 << k or even == 1 << (k - 1)


def test_weight_of_sum_identity() -> None:
    rng = random.Random(9)
    for _ in range(1000):
        x, y = rng.getrandbits(40), rng.getrandbits(40)
        assert hamming_weight_bits(x ^ y) == hamming_weight_bits(x) + hamming_weight_bits(y) - 2 * hamming_weight_bits(x & y)
