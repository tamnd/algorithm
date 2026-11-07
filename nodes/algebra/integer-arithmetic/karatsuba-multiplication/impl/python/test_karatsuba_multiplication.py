# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/karatsuba-multiplication/. The authors are listed in prov/QWY1MV.jsonl.

import random

import pytest

from karatsuba_multiplication import karatsuba, karatsuba_multiply, karatsuba_square, multiply_signed, schoolbook


def limbs(x: int, w: int, n: int | None = None) -> list[int]:
    out = []
    while x:
        out.append(x & ((1 << w) - 1))
        x >>= w
    if n is not None:
        out += [0] * (n - len(out))
    return out


def value(c: list[int], w: int) -> int:
    v = 0
    for d in reversed(c):
        v = (v << w) | d
    return v


def test_example_base_16() -> None:
    # 4093 = [13, 15, 15, 0] and 199 = [7, 12, 0, 0] in base 16, padded to 4 limbs
    c = karatsuba(limbs(4093, 4, 4), limbs(199, 4, 4), 4, 1)
    assert len(c) == 8 and value(c, 4) == 814507


def test_product_count() -> None:
    for j in range(8):
        counter = [0]
        n = 2**j
        karatsuba([15] * n, [15] * n, 4, 1, counter)
        assert counter[0] == 3**j


def test_edges() -> None:
    for w in (4, 8):
        top = (1 << w) - 1
        for n in (1, 2, 3, 4, 5, 7, 8, 16, 17, 33):
            ones = [top] * n
            for t in (1, 2, 3):
                assert value(karatsuba(ones, ones, w, t), w) == (2 ** (w * n) - 1) ** 2
                assert value(karatsuba([0] * n, ones, w, t), w) == 0
                one = [1] + [0] * (n - 1)
                assert value(karatsuba(one, ones, w, t), w) == 2 ** (w * n) - 1
                assert value(karatsuba_square(ones, w, t), w) == (2 ** (w * n) - 1) ** 2
        assert karatsuba_multiply([], [1, 2], w) == [0, 0]
        assert value(karatsuba_multiply([top], [top], w), w) == top * top
        # a carry into a new limb, and very different lengths
        assert value(karatsuba_multiply([top] * 40, [2], w, 2), w) == (2 ** (40 * w) - 1) * 2
        assert value(karatsuba_multiply([5], [top] * 37, w, 2), w) == 5 * (2 ** (37 * w) - 1)
    with pytest.raises(ValueError):
        karatsuba([1, 2], [1], 8)


def test_random() -> None:
    rng = random.Random(1962)
    for w in (4, 8):
        for _ in range(450):
            m, n = rng.randint(0, 48), rng.randint(0, 48)
            if rng.random() < 0.2:
                n = rng.randint(1, 4)
            x, y = rng.getrandbits(m * w), rng.getrandbits(n * w)
            if rng.random() < 0.15:
                x = 2 ** (m * w) - 1
            a, b = limbs(x, w, m), limbs(y, w, n)
            t = rng.choice((1, 2, 4, 8))
            c = karatsuba_multiply(a, b, w, t)
            assert len(c) == m + n and value(c, w) == x * y
            if m == n:
                assert karatsuba(a, b, w, t) == schoolbook(a, b, w)
            assert value(karatsuba_square(a, w, t), w) == x * x


def test_signed() -> None:
    rng = random.Random(7)
    for x, y in [(0, -5), (-1, -1), (-255, 256), (2**70, -(2**70) + 1)]:
        assert multiply_signed(x, y, 8, 1) == x * y
    for _ in range(500):
        x = rng.randint(-(2**300), 2**300)
        y = rng.randint(-(2**200), 2**200)
        assert multiply_signed(x, y, 4, 2) == x * y
