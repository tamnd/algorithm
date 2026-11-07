# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/digit-by-digit-square-root/. The authors are listed in prov/SH6MP2.jsonl.

import math
import random

from digit_by_digit_square_root import digit_sqrt, from_digits, to_digits


def check(x: int, base: int) -> None:
    root_digits, r = digit_sqrt(to_digits(x, base), base)
    q = from_digits(root_digits, base)
    assert q == math.isqrt(x)
    assert r == x - q * q
    assert 0 <= r <= 2 * q
    assert all(0 <= d < base for d in root_digits)


def test_example() -> None:
    root, r = digit_sqrt(to_digits(152399025, 10), 10)
    assert root == [5, 4, 3, 2, 1] and r == 0
    root, r = digit_sqrt(to_digits(200, 2), 2)
    assert from_digits(root, 2) == 14 and r == 4


def test_edges() -> None:
    for base in (2, 3, 10, 16, 256):
        assert digit_sqrt([], base) == ([], 0)
        for x in (0, 1, 2, 3, 4, base - 1, base, base * base - 1, base * base):
            check(x, base)
        for length in (1, 2, 3, 7, 8):
            check(base**length - 1, base)  # all digits base - 1
            check(base**length, base)


def test_squares_and_neighbours() -> None:
    rng = random.Random(77)
    for base in (2, 10, 16, 256):
        for _ in range(60):
            q = rng.randrange(1, 1 << rng.randint(1, 120))
            for x in (q * q - 1, q * q, q * q + 2 * q, (q + 1) ** 2):
                check(x, base)


def test_float_trap() -> None:
    a = (2**27 + 1) ** 2 - 1
    root, r = digit_sqrt(to_digits(a, 16), 16)
    assert from_digits(root, 16) == 2**27 and r == 2**28


def test_exhaustive_small() -> None:
    for base in (2, 3, 4, 10):
        for x in range(2000):
            check(x, base)


def test_random_against_isqrt() -> None:
    rng = random.Random(9001)
    for _ in range(600):
        base = rng.choice((2, 3, 7, 10, 16, 256))
        x = rng.randrange(1 << rng.randint(1, 400))
        check(x, base)


def test_bad_digits() -> None:
    for a, base in (([2], 2), ([0, -1], 10), ([1], 1)):
        try:
            digit_sqrt(a, base)
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")
