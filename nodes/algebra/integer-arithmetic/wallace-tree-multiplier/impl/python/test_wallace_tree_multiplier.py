# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wallace-tree-multiplier/. The authors are listed in prov/N0JM8H.jsonl.

import math
import random

import pytest

from wallace_tree_multiplier import (
    Stats,
    from_bits,
    multiply_limbs,
    multiply_signed,
    to_bits,
    tree_levels,
    wallace_multiply,
)


def limbs(x: int, w: int, n: int) -> list[int]:
    return [(x >> (w * i)) & ((1 << w) - 1) for i in range(n)]


def value(d: list[int], w: int) -> int:
    v = 0
    for x in reversed(d):
        v = (v << w) | x
    return v


def test_example() -> None:
    st = Stats()
    s, depth = wallace_multiply(to_bits(182, 8), to_bits(91, 8), st)
    assert from_bits(s) == 16562 == 182 * 91
    assert st.levels == 4
    assert [max(h) for h in st.heights] == [8, 6, 4, 3, 2]
    assert st.heights[0] == [1, 2, 3, 4, 5, 6, 7, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    assert st.heights[1] == [1, 1, 2, 3, 3, 4, 5, 5, 6, 4, 4, 4, 2, 2, 2, 0]
    assert (st.full_adders, st.half_adders, st.gates, depth) == (36, 25, 489, 22)


def test_dadda_numbers() -> None:
    d = [2]
    while len(d) < 11:
        d.append(3 * d[-1] // 2)
    assert d == [2, 3, 4, 6, 9, 13, 19, 28, 42, 63, 94]
    assert [tree_levels(n) for n in (8, 16, 24, 32, 53, 64)] == [4, 6, 7, 8, 9, 10]


def test_levels_and_depth() -> None:
    fewer = []
    for n in range(1, 90):
        st = Stats()
        s, depth = wallace_multiply([1] * n, [1] * n, st)
        assert from_bits(s) == ((1 << n) - 1) ** 2
        L = st.levels
        assert L <= tree_levels(n)
        if L < tree_levels(n):
            fewer.append(n)
        assert max(st.heights[-1]) <= 2
        assert depth <= 3 * L + 2 * math.ceil(math.log2(2 * n)) + 3
        assert st.full_adders < n * n
        assert st.half_adders <= (2 * n + 1) * L
    assert fewer == [20, 29]


def test_measured_sizes() -> None:
    out = {}
    for n in (16, 32, 64):
        st = Stats()
        _, depth = wallace_multiply([1] * n, [1] * n, st)
        out[n] = (st.gates, depth)
    assert out == {16: (1875, 30), 32: (7111, 37), 64: (27111, 45)}


def test_rectangular_shapes() -> None:
    rng = random.Random(7)
    for n in range(1, 13):
        for m in range(1, 13):
            for _ in range(5):
                x, y = rng.randrange(1 << n), rng.randrange(1 << m)
                st = Stats()
                s, _ = wallace_multiply(to_bits(x, n), to_bits(y, m), st)
                assert from_bits(s) == x * y
                assert len(s) == n + m
                assert st.levels <= tree_levels(min(n, m))


def test_exhaustive_small() -> None:
    for n in (1, 2, 3, 4, 5):
        for x in range(1 << n):
            for y in range(1 << n):
                s, _ = wallace_multiply(to_bits(x, n), to_bits(y, n))
                assert from_bits(s) == x * y


@pytest.mark.parametrize("w", [4, 8])
def test_limbs_random(w: int) -> None:
    rng = random.Random(2024 + w)
    for _ in range(300):
        na, nb = rng.randint(1, 6), rng.randint(1, 6)
        x, y = rng.randrange(1 << (w * na)), rng.randrange(1 << (w * nb))
        out = multiply_limbs(limbs(x, w, na), limbs(y, w, nb), w)
        assert len(out) == na + nb
        assert value(out, w) == x * y


@pytest.mark.parametrize("w", [4, 8])
def test_limbs_edges(w: int) -> None:
    B = 1 << w
    for na in (1, 2, 5):
        for nb in (1, 3, 4):
            top_a, top_b = B**na - 1, B**nb - 1
            for x in (0, 1, top_a, B ** (na - 1), top_a - 1):
                for y in (0, 1, top_b, B ** (nb - 1), top_b // 2):
                    out = multiply_limbs(limbs(x, w, na), limbs(y, w, nb), w)
                    assert value(out, w) == x * y
    assert multiply_limbs([], [3], w) == [0]


def test_signed() -> None:
    rng = random.Random(11)
    for n in (2, 4, 8, 16):
        lo, hi = -(1 << (n - 1)), (1 << (n - 1)) - 1
        for x in (lo, -1, 0, 1, hi):
            for y in (lo, -1, 0, 1, hi):
                assert multiply_signed(x, y, n) == x * y
        for _ in range(100):
            x, y = rng.randint(lo, hi), rng.randint(lo, hi)
            assert multiply_signed(x, y, n) == x * y
    with pytest.raises(ValueError):
        multiply_signed(8, 1, 4)


def test_empty() -> None:
    assert wallace_multiply([], [1]) == ([0], 0)
