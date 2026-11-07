# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/double-dabble/. The authors are listed in prov/8H3YQ9.jsonl.

import random

from double_dabble import decimal_digits_for, double_dabble, to_bcd


def bits_of(x: int, n: int) -> list[int]:
    return [(x >> k) & 1 for k in range(n - 1, -1, -1)]


def reference_bcd(x: int) -> int:
    """Packed BCD by reading the decimal string, an independent oracle."""
    return int(str(x), 16)


def test_example() -> None:
    assert double_dabble([1, 1, 1, 1, 0, 0, 1, 1]) == [3, 4, 2]
    assert to_bcd(243, 8) == 0x243
    assert to_bcd(65535, 16) == 0x65535


def test_digit_count() -> None:
    assert decimal_digits_for(0) == 1
    assert decimal_digits_for(8) == 3
    assert decimal_digits_for(16) == 5
    for n in range(1, 200):
        assert decimal_digits_for(n) == len(str(2**n - 1))


def test_edges() -> None:
    assert double_dabble([]) == [0]
    assert double_dabble([0]) == [0]
    assert double_dabble([1]) == [1]
    for n in (1, 3, 4, 7, 8, 10, 64, 100):
        top = (1 << n) - 1
        assert to_bcd(top, n) == reference_bcd(top)
        assert to_bcd(0, n) == 0
        assert to_bcd(1 << (n - 1), n) == reference_bcd(1 << (n - 1))


def test_exhaustive_small() -> None:
    for n in range(1, 13):
        for x in range(1 << n):
            digits = double_dabble(bits_of(x, n))
            assert all(0 <= v <= 9 for v in digits)
            assert sum(v * 10**i for i, v in enumerate(digits)) == x


def test_powers_of_ten() -> None:
    for e in range(0, 30):
        x = 10**e
        n = x.bit_length()
        assert to_bcd(x, n) == reference_bcd(x)
        assert to_bcd(x - 1, n) == reference_bcd(x - 1)


def test_random_against_str() -> None:
    rng = random.Random(1243)
    for _ in range(500):
        n = rng.randint(1, 300)
        x = rng.randrange(1 << n)
        assert to_bcd(x, n) == reference_bcd(x)
