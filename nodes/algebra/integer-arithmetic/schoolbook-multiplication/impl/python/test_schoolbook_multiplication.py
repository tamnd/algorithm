# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/schoolbook-multiplication/. The authors are listed in prov/7VTRV2.jsonl.

import random

from schoolbook_multiplication import multiply_signed, schoolbook_multiply, schoolbook_square


def to_limbs(x: int, w: int, n: int | None = None) -> list[int]:
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


def test_example() -> None:
    c = schoolbook_multiply([13, 15, 15], [7, 12], 4)
    assert c == [11, 10, 13, 6, 12] and value(c, 4) == 4093 * 199 == 814507


def test_edges() -> None:
    w = 4
    assert schoolbook_multiply([], [], w) == []
    assert schoolbook_multiply([], [3, 4], w) == [0, 0]
    assert schoolbook_multiply([0], [15], w) == [0, 0]
    assert schoolbook_multiply([1], [9, 9, 9], w) == [9, 9, 9, 0]
    assert schoolbook_multiply([15], [15], w) == [1, 14]
    for w in (1, 4, 8):
        for m in range(1, 6):
            for n in range(1, 6):
                a, b = [(1 << w) - 1] * m, [(1 << w) - 1] * n
                c = schoolbook_multiply(a, b, w)
                assert len(c) == m + n
                assert value(c, w) == ((1 << (w * m)) - 1) * ((1 << (w * n)) - 1)


def test_very_different_lengths() -> None:
    rng = random.Random(5)
    for _ in range(50):
        a = [rng.randrange(256) for _ in range(rng.randint(40, 80))]
        b = [rng.randrange(256)]
        assert value(schoolbook_multiply(a, b, 8), 8) == value(a, 8) * value(b, 8)
        assert value(schoolbook_multiply(b, a, 8), 8) == value(a, 8) * value(b, 8)


def test_random_against_int() -> None:
    rng = random.Random(1962)
    for _ in range(1500):
        w = rng.choice((1, 2, 4, 8, 16))
        m, n = rng.randint(0, 12), rng.randint(0, 12)
        x, y = rng.getrandbits(w * m) if m else 0, rng.getrandbits(w * n) if n else 0
        a, b = to_limbs(x, w, m), to_limbs(y, w, n)
        c = schoolbook_multiply(a, b, w)
        assert len(c) == m + n and all(0 <= d < 1 << w for d in c)
        assert value(c, w) == x * y
        assert value(schoolbook_square(a, w), w) == x * x


def test_square_edges() -> None:
    for w in (1, 4, 8):
        for n in range(0, 7):
            a = [(1 << w) - 1] * n
            assert value(schoolbook_square(a, w), w) == value(a, w) ** 2
            assert len(schoolbook_square(a, w)) == 2 * n


def test_signed() -> None:
    rng = random.Random(9)
    for _ in range(500):
        x, y = rng.randint(-5000, 5000), rng.randint(-5000, 5000)
        sx, sy = (1 if x >= 0 else -1), (1 if y >= 0 else -1)
        s, c = multiply_signed((sx, to_limbs(abs(x), 4)), (sy, to_limbs(abs(y), 4)), 4)
        assert s * value(c, 4) == x * y
        assert (not c and s == 1) or c[-1] != 0
