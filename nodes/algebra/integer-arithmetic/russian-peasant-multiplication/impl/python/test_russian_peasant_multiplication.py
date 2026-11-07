# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/russian-peasant-multiplication/. The authors are listed in prov/ANVYVS.jsonl.

import random

from russian_peasant_multiplication import russian_peasant_multiply


def limbs(x: int, w: int) -> list[int]:
    out = []
    while x:
        out.append(x & ((1 << w) - 1))
        x >>= w
    return out


def value(c: list[int], w: int) -> int:
    v = 0
    for d in reversed(c):
        v = (v << w) | d
    return v


def test_example() -> None:
    assert value(russian_peasant_multiply(limbs(4093, 4), limbs(199, 4), 4), 4) == 814507


def test_edges() -> None:
    for w in (1, 4, 8):
        top = (1 << w) - 1
        assert russian_peasant_multiply([], [], w) == []
        assert russian_peasant_multiply([], [1], w) == []
        assert russian_peasant_multiply([5 % (1 << w)], [], w) == []
        assert russian_peasant_multiply([0, 0], [1], w) == []
        assert russian_peasant_multiply([1], [1], w) == [1]
        assert russian_peasant_multiply([top] * 3, [1], w) == [top] * 3
        for m in range(1, 5):
            for n in range(1, 5):
                x, y = (1 << (w * m)) - 1, (1 << (w * n)) - 1
                r = russian_peasant_multiply(limbs(x, w), limbs(y, w), w)
                assert value(r, w) == x * y and r[-1] != 0
        # a carry into a new limb on doubling
        assert value(russian_peasant_multiply([top], [2], w), w) == 2 * top


def test_very_different_lengths() -> None:
    rng = random.Random(11)
    for _ in range(40):
        x, y = rng.getrandbits(400), rng.randrange(1, 256)
        assert value(russian_peasant_multiply(limbs(x, 8), limbs(y, 8), 8), 8) == x * y
        assert value(russian_peasant_multiply(limbs(y, 8), limbs(x, 8), 8), 8) == x * y


def test_random_against_int() -> None:
    rng = random.Random(1650)
    for _ in range(1200):
        w = rng.choice((1, 2, 4, 8))
        x, y = rng.getrandbits(rng.randint(0, 64)), rng.getrandbits(rng.randint(0, 64))
        r = russian_peasant_multiply(limbs(x, w), limbs(y, w), w)
        assert value(r, w) == x * y
        assert all(0 <= d < 1 << w for d in r) and (not r or r[-1] != 0)
