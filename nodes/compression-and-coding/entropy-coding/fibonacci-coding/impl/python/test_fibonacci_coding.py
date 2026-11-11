# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fibonacci-coding/. The authors are listed in prov/1ZZ3YB.jsonl.

import math
import random
from fractions import Fraction

import pytest

from fibonacci_coding import (
    FIB,
    BitReader,
    BitWriter,
    decode_all,
    encode_all,
    fib_codeword,
    fib_decode,
    fib_length,
)

# Pibiri and Venturini, Techniques for inverted index compression (arXiv:1908.10598v2),
# Table 4a, the Fibonacci codewords of 1 .. 8, copied by hand.
PV_TABLE_4A = {1: "11", 2: "011", 3: "0011", 4: "1011", 5: "00011", 6: "10011", 7: "01011", 8: "000011"}

PHI = (1 + math.sqrt(5)) / 2


def zeckendorf_oracle(x: int) -> list[int]:
    """Zeckendorf digits by exhaustive search over bit masks (for small x only).

    Digit i of the list is the digit of F_(i+2). The representation is the unique
    mask with no two adjacent ones whose weighted sum is x and whose top digit is 1.
    """
    fibs = [1, 2]
    while fibs[-1] <= x:
        fibs.append(fibs[-1] + fibs[-2])
    found = []
    for mask in range(1, 1 << len(fibs)):
        if mask & (mask >> 1):
            continue
        if sum(f for i, f in enumerate(fibs) if mask >> i & 1) == x:
            found.append([mask >> i & 1 for i in range(mask.bit_length())])
    assert len(found) == 1  # Zeckendorf's theorem: exactly one representation
    return found[0]


def bits_to_stream(bits: str) -> tuple[bytes, int]:
    w = BitWriter()
    for c in bits:
        w.write_bit(int(c))
    return w.getvalue()


def test_survey_table() -> None:
    for x, word in PV_TABLE_4A.items():
        assert fib_codeword(x) == word


def test_zeckendorf_property() -> None:
    for x in range(1, 3000):
        word = fib_codeword(x)
        assert word.endswith("11")
        assert "11" not in word[:-1]  # the pair 11 appears only at the end
        digits = [int(c) for c in word[:-1]]
        assert sum(d * FIB[i + 2] for i, d in enumerate(digits)) == x
        if x < 400:
            assert digits == zeckendorf_oracle(x)


def test_lengths() -> None:
    for x in range(1, 20000):
        k = fib_length(x)
        assert len(fib_codeword(x)) == k
        assert FIB[k] <= x < FIB[k + 1]
        assert math.log(x, PHI) < k <= math.log(x, PHI) + 2 + 1e-9


def test_kraft_sum_tends_to_one() -> None:
    # F_(k-1) codewords have length k, and sum_k F_(k-1) 2^-k = 1.
    for big in range(4, 18):
        s = sum(Fraction(FIB[k - 1], 2**k) for k in range(2, big))
        assert s == sum(Fraction(1, 2 ** fib_length(x)) for x in range(1, FIB[big]))
    s = sum(Fraction(FIB[k - 1], 2**k) for k in range(2, 100))
    assert 0 < 1 - s < Fraction(1, 10**6)


def test_worked_example() -> None:
    # 100 = 89 + 8 + 3 = F_11 + F_6 + F_4.
    assert fib_codeword(100) == "00101000011"
    data, nbits = bits_to_stream("00101000011")
    assert fib_decode(BitReader(data, nbits)) == 100
    assert decode_all(*encode_all([4, 1, 2])) == [4, 1, 2]
    assert encode_all([4, 1, 2]) == bits_to_stream("1011" "11" "011")


def test_round_trip_random() -> None:
    rng = random.Random(41)
    for _ in range(500):
        values = [rng.randrange(1, 1 << rng.randrange(1, 60)) for _ in range(rng.randrange(20))]
        data, nbits = encode_all(values)
        assert nbits == sum(fib_length(v) for v in values)
        assert decode_all(data, nbits) == values


def test_resynchronization_after_bit_error() -> None:
    # Values >= 2, so no codeword is 11. Flip one bit in codeword j (not the last one).
    # The codewords before j and from j + 2 on decode intact; codewords j and j + 1
    # are replaced by one to three wrong values.
    rng = random.Random(43)
    for _ in range(1500):
        values = [rng.randrange(2, 1 << rng.randrange(2, 14)) for _ in range(10)]
        words = [fib_codeword(v) for v in values]
        starts = [sum(len(w) for w in words[:i]) for i in range(len(words))]
        pos = rng.randrange(starts[-1])
        j = max(i for i, s in enumerate(starts) if s <= pos)
        bits = "".join(words)
        bad = bits[:pos] + ("1" if bits[pos] == "0" else "0") + bits[pos + 1 :]
        out = decode_all(*bits_to_stream(bad))
        tail = len(values) - (j + 2)
        assert out[:j] == values[:j]
        assert out[len(out) - tail :] == values[len(values) - tail :]
        middle = len(out) - j - tail  # values decoded in place of the 2 damaged ones
        assert 1 <= middle <= 3


def test_edge_cases() -> None:
    assert decode_all(*encode_all([])) == []
    big = [2**64 - 1, 2**64, 1, 1, 1]
    assert decode_all(*encode_all(big)) == big
    with pytest.raises(ValueError):
        fib_codeword(0)
    data, nbits = encode_all([1000])
    with pytest.raises(EOFError):
        fib_decode(BitReader(data, nbits - 1))
