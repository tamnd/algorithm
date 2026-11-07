# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/non-restoring-division/. The authors are listed in prov/HPV12R.jsonl.

import random

import pytest

from non_restoring_division import (
    from_limbs,
    non_restoring_divide,
    signed_digit_quotient,
    to_limbs,
)


def check(a: int, b: int, w: int) -> None:
    q, r = non_restoring_divide(to_limbs(a, w), to_limbs(b, w), w)
    assert (from_limbs(q, w), from_limbs(r, w)) == divmod(a, b)
    assert not q or q[-1] != 0
    assert not r or r[-1] != 0


def test_example() -> None:
    # 100 = 14 * 7 + 2: 7 steps, and the last remainder -5 needs the correction.
    stats: dict = {}
    assert non_restoring_divide([100], [7], 8, stats) == ([14], [2])
    assert stats == {"steps": 7, "corrections": 1}
    digits, r0 = signed_digit_quotient(100, 7)
    assert digits == [1, -1, -1, -1, 1, 1, 1]
    assert r0 == -5
    assert sum(d << (len(digits) - 1 - k) for k, d in enumerate(digits)) == 15


def test_edges() -> None:
    for w in (2, 4, 8):
        B = 1 << w
        for a in [0, 1, 2, B - 1, B, B + 1, B * B - 1, B**3, B**4 - 1]:
            for b in [1, 2, 3, B - 1, B, B + 1, B * B - 1, a if a else 1, a + 1]:
                check(a, b, w)


def test_errors() -> None:
    with pytest.raises(ZeroDivisionError):
        non_restoring_divide([5], [0], 8)
    with pytest.raises(ValueError):
        non_restoring_divide([1], [1], 1)


def test_exhaustive_small() -> None:
    for a in range(256):
        for b in range(1, 40):
            check(a, b, 4)


def test_random() -> None:
    rng = random.Random(1958)
    for w in (4, 8):
        for _ in range(600):
            a = rng.getrandbits(rng.randint(0, 160))
            b = rng.getrandbits(rng.randint(1, 100)) or 1
            check(a, b, w)
            check(a, a // 5 + 1, w)


def test_signed_digit_form() -> None:
    rng = random.Random(3)
    for _ in range(2000):
        a = rng.getrandbits(rng.randint(1, 64))
        b = rng.randint(1, 1 << rng.randint(1, 40))
        digits, r0 = signed_digit_quotient(a, b)
        d = sum(x << (len(digits) - 1 - k) for k, x in enumerate(digits))
        assert a == d * b + r0
        assert -b <= r0 < b
        q, r = divmod(a, b)
        assert (q, r) == ((d, r0) if r0 >= 0 else (d - 1, r0 + b))
