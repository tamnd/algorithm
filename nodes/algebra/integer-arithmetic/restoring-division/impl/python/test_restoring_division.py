# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/restoring-division/. The authors are listed in prov/7J9632.jsonl.

import random

import pytest

from restoring_division import (
    divide_signed,
    from_limbs,
    nonperforming_divide,
    restoring_divide,
    to_limbs,
)


def check(a: int, b: int, w: int) -> None:
    q, r = restoring_divide(to_limbs(a, w), to_limbs(b, w), w)
    assert (from_limbs(q, w), from_limbs(r, w)) == divmod(a, b)
    assert not q or q[-1] != 0
    assert not r or r[-1] != 0
    q2, r2 = nonperforming_divide(to_limbs(a, w), to_limbs(b, w), w)
    assert (q2, r2) == (q, r)


def test_example() -> None:
    # 100 = 14 * 7 + 2: 7 steps for the 7 binary digits of 100, and 4 restores (quotient bits 0001110).
    stats: dict = {}
    q, r = restoring_divide([100], [7], 8, stats)
    assert (q, r) == ([14], [2])
    assert stats == {"steps": 7, "restores": 4}


def test_edges() -> None:
    for w in (4, 8):
        B = 1 << w
        for a in [0, 1, 2, B - 1, B, B + 1, B * B - 1, B**3, B**4 - 1]:
            for b in [1, 2, 3, B - 1, B, B + 1, B * B - 1, a if a else 1, a + 1]:
                check(a, b, w)


def test_zero_divisor() -> None:
    with pytest.raises(ZeroDivisionError):
        restoring_divide([5], [], 8)
    with pytest.raises(ZeroDivisionError):
        restoring_divide([5], [0, 0], 8)


def test_leading_zero_limbs() -> None:
    q, r = restoring_divide([100, 0, 0], [7, 0], 8)
    assert (q, r) == ([14], [2])


def test_exhaustive_small() -> None:
    for a in range(256):
        for b in range(1, 40):
            check(a, b, 4)


def test_random() -> None:
    rng = random.Random(1946)
    for w in (4, 8):
        for _ in range(600):
            a = rng.getrandbits(rng.randint(0, 160))
            b = rng.getrandbits(rng.randint(1, 100)) or 1
            check(a, b, w)
            check(a, a // 3 + 1, w)


def test_signed() -> None:
    rng = random.Random(7)
    for _ in range(400):
        a = rng.randint(-(10**12), 10**12)
        b = rng.choice([-1, 1]) * rng.randint(1, 10**6)
        q, r = divide_signed(a, b)
        assert q * b + r == a
        assert abs(r) < abs(b)
        assert r == 0 or (r < 0) == (a < 0)
        assert q == int(a / b) or abs(a) > 2**52
