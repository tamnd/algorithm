# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kogge-stone-adder/. The authors are listed in prov/PABN90.jsonl.

import math
import random

import pytest

from kogge_stone_adder import Stats, add_limbs, from_bits, kogge_stone_add, kogge_stone_word, to_bits


def limbs(x: int, w: int, n: int) -> list[int]:
    return [(x >> (w * i)) & ((1 << w) - 1) for i in range(n)]


def value(d: list[int], w: int) -> int:
    v = 0
    for x in reversed(d):
        v = (v << w) | x
    return v


def test_example() -> None:
    s, depth = kogge_stone_add(to_bits(182, 8), to_bits(91, 8))
    assert from_bits(s) == 273
    assert depth == 9
    assert kogge_stone_word(182, 91, 8) == 273


def test_size_and_depth() -> None:
    for n in range(1, 130):
        st = Stats()
        s, depth = kogge_stone_add([1] * n, [0] * n, 1, st)
        assert from_bits(s) == 1 << n
        L = math.ceil(math.log2(n)) if n > 1 else 0
        assert st.levels == L
        assert st.cells == n * L - (1 << L) + 1
        assert depth <= 2 * L + 3
        if n & (n - 1) == 0:
            assert depth == 2 * L + 3


def test_exhaustive_small() -> None:
    for n in (1, 2, 3, 4, 5):
        for x in range(1 << n):
            for y in range(1 << n):
                for c in (0, 1):
                    s, _ = kogge_stone_add(to_bits(x, n), to_bits(y, n), c)
                    assert from_bits(s) == x + y + c
                    assert kogge_stone_word(x, y, n, c) == x + y + c


def test_edges() -> None:
    assert kogge_stone_add([], [], 1)[0] == [1]
    for n in (1, 7, 8, 9, 31, 64):
        top = (1 << n) - 1
        for x, y, c in [(0, 0, 0), (top, 0, 1), (top, 1, 0), (top, top, 1), (top, top, 0), (top >> 1, 1, 0)]:
            s, _ = kogge_stone_add(to_bits(x, n), to_bits(y, n), c)
            assert from_bits(s) == x + y + c
    with pytest.raises(ValueError):
        kogge_stone_add([1, 0], [1], 0)


def test_random_limbs() -> None:
    rng = random.Random(1973)
    for w in (4, 8):
        for _ in range(300):
            n = rng.randint(1, 12)
            x = rng.getrandbits(n * w)
            y = rng.getrandbits(n * w)
            c = rng.randint(0, 1)
            out = add_limbs(limbs(x, w, n), limbs(y, w, n), w, c)
            assert len(out) == n + 1
            assert value(out, w) == x + y + c


def test_random_words() -> None:
    rng = random.Random(7)
    for _ in range(3000):
        n = rng.randint(1, 200)
        x, y, c = rng.getrandbits(n), rng.getrandbits(n), rng.randint(0, 1)
        assert kogge_stone_word(x, y, n, c) == x + y + c
