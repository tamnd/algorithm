# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/arithmetic-coding/. The authors are listed in prov/GC5V3X.jsonl.

import math
import random

from arithmetic_coding import decode, encode, ideal_length, length_bound


def roundtrip(symbols: list[int], sigma: int) -> int:
    data, nbits = encode(symbols, sigma)
    assert decode(data, len(symbols), sigma) == symbols
    assert len(data) == (nbits + 7) // 8
    return nbits


def test_example() -> None:
    # The worked example of the page: "abaca" over the alphabet a=0, b=1, c=2.
    msg = [0, 1, 0, 2, 0]
    nbits = roundtrip(msg, 3)
    assert abs(ideal_length(msg, 3) - math.log2(3 * 4 * 5 * 6 * 7 / (1 * 1 * 2 * 1 * 3))) < 1e-9
    assert nbits == 10


def test_edges() -> None:
    assert roundtrip([], 4) == 2
    for sigma in (1, 2, 3, 256):
        for s in range(min(sigma, 3)):
            roundtrip([s], sigma)
            roundtrip([s] * 500, sigma)


def test_random_roundtrip_and_bound() -> None:
    rng = random.Random(1987)
    for _ in range(300):
        sigma = rng.choice([2, 3, 5, 16, 256])
        n = rng.randint(0, 200)
        weights = [rng.random() ** 3 for _ in range(sigma)]
        msg = rng.choices(range(sigma), weights=weights, k=n)
        nbits = roundtrip(msg, sigma)
        assert nbits <= length_bound(msg, sigma) + 1e-9
        assert nbits >= ideal_length(msg, sigma) - 1e-9 or n == 0 or nbits >= 2


def test_long_skewed_close_to_ideal() -> None:
    # 20000 bits with p(1) = 0.05 and 65000 symbols over 3 letters: halving of counts happens.
    rng = random.Random(30)
    msg = [1 if rng.random() < 0.05 else 0 for _ in range(20000)]
    nbits = roundtrip(msg, 2)
    ideal = ideal_length(msg, 2)
    assert ideal <= nbits <= ideal + 2 + 20000 * 1e-4
    msg = rng.choices(range(3), weights=[8, 1, 1], k=65000)
    nbits = roundtrip(msg, 3)
    assert nbits <= length_bound(msg, 3) + 1e-9


def test_underflow_case() -> None:
    # Two equiprobable symbols in alternation keep the interval near the middle,
    # which exercises the E3 (pending bit) scaling.
    msg = [0, 1] * 3000
    roundtrip(msg, 2)
    msg = [0] * 50 + [1] * 50 + [0, 1, 1, 0] * 500
    roundtrip(msg, 2)


def test_byte_strings() -> None:
    rng = random.Random(7)
    for text in (b"", b"a", b"abracadabra" * 30, bytes(rng.randrange(256) for _ in range(2000))):
        msg = list(text)
        nbits = roundtrip(msg, 256)
        assert nbits <= length_bound(msg, 256) + 1e-9
