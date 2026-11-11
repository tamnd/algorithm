# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ones-complement-arithmetic/. The authors are listed in prov/RDWD1R.jsonl.

import random

from ones_complement_arithmetic import (
    add16,
    fold,
    neg16,
    sum16_words,
    sum_wide,
    swap16,
    words_of,
)


def oracle(total: int) -> int:
    """The ones' complement 16-bit value of a non-negative integer sum of words."""
    return 0 if total == 0 else (total - 1) % 0xFFFF + 1


def test_rfc1071_section3_example() -> None:
    # RFC 1071 Section 3: bytes 00 01 f2 03 f4 f5 f6 f7. The normal order sum is
    # ddf2, the swapped order sum is f2dd, and the 32-bit sums fold to the same values.
    data = bytes.fromhex("0001f203f4f5f6f7")
    assert sum16_words(words_of(data, "big")) == 0xDDF2
    assert sum16_words(words_of(data, "little")) == 0xF2DD
    assert sum_wide(data, 4) == 0xDDF2
    assert sum_wide(data, 8) == 0xDDF2
    assert fold(0x2DDF0) == 0xDDF2


def test_two_zeros() -> None:
    assert add16(0x0000, 0x0000) == 0x0000
    assert add16(0xFFFF, 0x0000) == 0xFFFF
    assert add16(0xFFFF, 0xFFFF) == 0xFFFF
    assert add16(0x1234, neg16(0x1234)) == 0xFFFF  # x + (-x) gives -0, not +0
    assert add16(0x8000, 0x8000) == 0x0001  # end-around carry


def test_add16_exhaustive_on_a_grid() -> None:
    vals = list(range(0, 0x10000, 257)) + [0xFFFF, 0xFFFE, 1]
    for a in vals:
        for b in vals:
            r = add16(a, b)
            assert 0 <= r <= 0xFFFF
            assert r % 0xFFFF == (a + b) % 0xFFFF
            assert (r == 0) == (a == 0 and b == 0)


def test_random_sums_against_oracle() -> None:
    rng = random.Random(4201)
    for _ in range(600):
        words = [rng.choice([0, 0xFFFF, rng.randrange(0x10000)]) for _ in range(rng.randrange(0, 30))]
        assert sum16_words(words) == oracle(sum(words))
        order = list(words)
        rng.shuffle(order)
        assert sum16_words(order) == sum16_words(words)  # commutative and associative


def test_byte_order_independence() -> None:
    rng = random.Random(4202)
    for _ in range(600):
        data = bytes(rng.randrange(256) for _ in range(rng.randrange(0, 41)))
        big = sum16_words(words_of(data, "big"))
        little = sum16_words(words_of(data, "little"))
        assert little == swap16(big)


def test_wide_sums_equal_16_bit_sums() -> None:
    rng = random.Random(4203)
    for _ in range(600):
        n = rng.randrange(0, 70)
        data = bytes(rng.choice([0, 255, rng.randrange(256)]) for _ in range(n))
        s16 = sum16_words(words_of(data, "big"))
        assert sum_wide(data, 2) == s16
        assert sum_wide(data, 4) == s16
        assert sum_wide(data, 8) == s16


def test_fold() -> None:
    assert fold(0) == 0
    assert fold(0xFFFF) == 0xFFFF
    assert fold(0x10000) == 0x0001
    assert fold(0xFFFFFFFF) == 0xFFFF
    assert fold((1 << 64) - 1) == 0xFFFF
    rng = random.Random(4204)
    for _ in range(600):
        x = rng.randrange(1 << rng.randrange(1, 80))
        assert fold(x) == oracle(x)
