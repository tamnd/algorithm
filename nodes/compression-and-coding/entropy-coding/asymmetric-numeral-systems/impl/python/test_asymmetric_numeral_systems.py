# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/asymmetric-numeral-systems/. The authors are listed in prov/4JH8SV.jsonl.

import math
import random
from fractions import Fraction

import pytest

from asymmetric_numeral_systems import (
    code_length, coding_function, decode, decoding_function, encode, information, length_bound,
)

PROBS = [Fraction(1, 2), Fraction(3, 10), Fraction(1, 7), Fraction(2, 3), Fraction(99, 100), Fraction(1, 1000)]


def test_example() -> None:
    # The worked example of the page: p = 3/10, the states 0..20 and the
    # message 0 1 0 0 1 0 coded last first from the state 1.
    p = Fraction(3, 10)
    assert [decoding_function(y, p)[0] for y in range(21)] == [
        1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1]
    states = [1]
    for s in reversed([0, 1, 0, 0, 1, 0]):
        states.append(coding_function(s, states[-1], p))
    assert states == [1, 2, 6, 9, 14, 46, 67]
    assert encode([0, 1, 0, 0, 1, 0], p) == 67
    assert decode(67, 6, p) == [0, 1, 0, 0, 1, 0]


def test_d_inverts_c_and_c_enumerates_each_class() -> None:
    for p in PROBS:
        for x in range(3000):
            for s in (0, 1):
                assert decoding_function(coding_function(s, x, p), p) == (s, x)
        # D is a bijection from the states onto {0, 1} x N: the states of each
        # symbol, in increasing order, are C(s, 0), C(s, 1), ...
        limit = 3000
        by_symbol: dict[int, list[int]] = {0: [], 1: []}
        for y in range(limit):
            s, x = decoding_function(y, p)
            assert x == len(by_symbol[s])
            by_symbol[s].append(y)
        for s in (0, 1):
            assert by_symbol[s] == [coding_function(s, x, p) for x in range(len(by_symbol[s]))]
        # The symbol 1 has density p among the states.
        assert len(by_symbol[1]) == math.ceil(limit * p)


def test_edges() -> None:
    p = Fraction(1, 3)
    assert encode([], p) == 1 and decode(1, 0, p) == []
    for bits in ([0], [1], [0] * 300, [1] * 300):
        assert decode(encode(bits, p), len(bits), p) == bits
    for bad in (Fraction(0), Fraction(1), Fraction(3, 2)):
        with pytest.raises(ValueError):
            encode([0], bad)


def test_random_roundtrip_and_bound() -> None:
    rng = random.Random(2009)
    for _ in range(300):
        p = Fraction(rng.randint(1, 99), 100)
        x0 = rng.randint(1, 50)
        n = rng.randint(0, 300)
        bits = [1 if rng.random() < rng.random() else 0 for _ in range(n)]
        x = encode(bits, p, x0)
        assert decode(x, n, p, x0) == bits
        assert math.log2(x + 1) <= length_bound(bits, p, x0) + 1e-9


def test_lifo_order() -> None:
    # Coding the bits first to last gives a state that decodes to the reverse.
    p = Fraction(2, 5)
    bits = [0, 0, 1, 0, 1, 1, 1, 0]
    x = 1
    for s in bits:
        x = coding_function(s, x, p)
    assert decode(x, len(bits), p) == bits[::-1]


def test_length_tends_to_the_entropy() -> None:
    p = Fraction(3, 10)
    h = -(0.3 * math.log2(0.3) + 0.7 * math.log2(0.7))
    rng = random.Random(7)
    gaps = []
    for n in (1000, 4000, 16000):
        bits = [1 if rng.random() < 0.3 else 0 for _ in range(n)]
        x = encode(bits, p)
        length = code_length(x)
        info = information(bits, p)
        # The excess over the ideal length stays bounded, so per symbol it goes to 0.
        assert info - 1 <= length <= length_bound(bits, p) + 1
        gaps.append((length - info) / n)
        assert abs(length / n - h) < 4 / math.sqrt(n)
    assert gaps[0] > gaps[1] > gaps[2] > 0
