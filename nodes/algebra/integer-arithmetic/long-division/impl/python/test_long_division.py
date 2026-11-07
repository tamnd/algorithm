# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/long-division/. The authors are listed in prov/BHDBGW.jsonl.

import random

import pytest

from long_division import divmod_signed, long_divide, short_divide


def digits(x: int, base: int) -> list[int]:
    out = []
    while x:
        x, t = divmod(x, base)
        out.append(t)
    return out


def value(d: list[int], base: int) -> int:
    x = 0
    for t in reversed(d):
        x = x * base + t
    return x


def check(a: int, b: int, base: int) -> None:
    q, r = long_divide(digits(a, base), digits(b, base), base)
    assert (value(q, base), value(r, base)) == divmod(a, b)
    assert q == digits(a // b, base) and r == digits(a % b, base)


def test_examples() -> None:
    trace: list = []
    q, r = long_divide(digits(814600, 10), digits(199, 10), 10, trace)
    assert value(q, 10) == 4093 and value(r, 10) == 93
    assert [t[2] for t in trace] == [4, 0, 9, 3]
    trace = []
    q, r = long_divide(digits(4100, 10), digits(588, 10), 10, trace)
    assert value(q, 10) == 6 and value(r, 10) == 572
    assert trace[-1] == (0, 8, 6, True)


def test_short_division() -> None:
    assert short_divide([13, 15, 15], 7, 16) == (digits(4093 // 7, 16), 4093 % 7)
    with pytest.raises(ValueError):
        short_divide([1], 0, 16)


def test_edges() -> None:
    for base in (16, 256):
        top = base - 1
        cases = [
            (0, 1), (1, 1), (0, 12345), (5, 7), (top, top), (top, 1), (base, top), (base**4, 1),
            (base**6 - 1, base**3 - 1), (base**6 - 1, base**6 - 1), (base**6, base**6 - 1),
            (base**8 - 1, base // 2), (base**8 - 1, base**2 // 2), (base**9 + 5, base**8 + 1),
            (base**10 - 1, top), (base**7, base**3 + 1), (base**12 - 1, 3 * base**5 + 7),
        ]
        for a, b in cases:
            check(a, b, base)
    with pytest.raises(ZeroDivisionError):
        long_divide([1, 2], [], 16)
    with pytest.raises(ZeroDivisionError):
        long_divide([1, 2], [0, 0], 16)


def test_random() -> None:
    rng = random.Random(1969)
    for base in (16, 256):
        for _ in range(2500):
            nb = rng.randint(1, 12)
            na = rng.randint(0, 24)
            b = rng.getrandbits(nb * (base.bit_length() - 1)) or 1
            a = rng.getrandbits(na * (base.bit_length() - 1))
            if rng.random() < 0.2:
                b = (b | (base - 1)) if rng.random() < 0.5 else b | (1 << (nb * (base.bit_length() - 1) - 1))
                a = base ** (na + 1) - 1
            check(a, b, base)


def test_add_back_happens() -> None:
    rng = random.Random(7)
    seen = 0
    for _ in range(3000):
        b = rng.randint(17, 16**4)
        a = rng.randint(0, 16**9)
        trace: list = []
        q, r = long_divide(digits(a, 16), digits(b, 16), 16, trace)
        assert (value(q, 16), value(r, 16)) == divmod(a, b)
        seen += sum(1 for t in trace if t[3])
    assert seen > 0


def test_signed() -> None:
    rng = random.Random(11)
    for a, b in [(7, 2), (-7, 2), (7, -2), (-7, -2), (0, -3), (-6, 3), (6, -3)]:
        assert divmod_signed(a, b, 16) == divmod(a, b)
    for _ in range(1500):
        a = rng.randint(-(16**10), 16**10)
        b = rng.randint(-(16**5), 16**5) or 1
        assert divmod_signed(a, b, 16) == divmod(a, b)
