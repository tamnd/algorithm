# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sklansky-adder/. The authors are listed in prov/JA4QR9.jsonl.

import math
import random

import pytest

from sklansky_adder import Stats, add_limbs, from_bits, prefix_blocks, sklansky_add, to_bits


def limbs(x: int, w: int, n: int) -> list[int]:
    return [(x >> (w * i)) & ((1 << w) - 1) for i in range(n)]


def value(d: list[int], w: int) -> int:
    v = 0
    for x in reversed(d):
        v = (v << w) | x
    return v


def cells(n: int) -> int:
    if n <= 1:
        return 0
    lo = (n + 1) // 2
    return cells(lo) + cells(n - lo) + (n - lo)


def test_example() -> None:
    s, depth = sklansky_add(to_bits(182, 8), to_bits(91, 8))
    assert from_bits(s) == 273
    assert depth == 10
    assert prefix_blocks(8)[0][5] == (4, 5)
    assert prefix_blocks(8)[1][6] == (4, 6)
    assert prefix_blocks(8)[2][6] == (0, 6)


def test_size_depth_fanout() -> None:
    for n in range(1, 131):
        st = Stats()
        s, depth = sklansky_add([1] * n, [0] * n, 1, st)
        assert from_bits(s) == 1 << n
        L = math.ceil(math.log2(n)) if n > 1 else 0
        assert st.cells == cells(n)
        assert st.cells <= (n * L) // 2 + 1
        assert depth <= 2 * L + 4
        assert st.max_recursion == L
        assert (max(st.fanout.values()) if st.fanout else 0) == n // 2
        if n & (n - 1) == 0:
            assert st.cells == (n // 2) * L


def test_exhaustive_small() -> None:
    for n in (1, 2, 3, 4, 5):
        for x in range(1 << n):
            for y in range(1 << n):
                for c in (0, 1):
                    s, _ = sklansky_add(to_bits(x, n), to_bits(y, n), c)
                    assert from_bits(s) == x + y + c


def test_edges() -> None:
    assert sklansky_add([], [], 1)[0] == [1]
    for n in (1, 7, 8, 9, 31, 64):
        top = (1 << n) - 1
        for x, y, c in [(0, 0, 0), (top, 0, 1), (top, 1, 0), (top, top, 1), (top, top, 0), (top >> 1, 1, 0)]:
            s, _ = sklansky_add(to_bits(x, n), to_bits(y, n), c)
            assert from_bits(s) == x + y + c
    with pytest.raises(ValueError):
        sklansky_add([1, 0], [1], 0)


def test_random_limbs() -> None:
    rng = random.Random(1960)
    for w in (4, 8):
        for _ in range(300):
            n = rng.randint(1, 12)
            x = rng.getrandbits(n * w)
            y = rng.getrandbits(n * w)
            c = rng.randint(0, 1)
            out = add_limbs(limbs(x, w, n), limbs(y, w, n), w, c)
            assert len(out) == n + 1
            assert value(out, w) == x + y + c


def test_wide() -> None:
    rng = random.Random(11)
    for _ in range(20):
        n = rng.randint(200, 1000)
        x, y = rng.getrandbits(n), rng.getrandbits(n)
        s, _ = sklansky_add(to_bits(x, n), to_bits(y, n), 0)
        assert from_bits(s) == x + y
