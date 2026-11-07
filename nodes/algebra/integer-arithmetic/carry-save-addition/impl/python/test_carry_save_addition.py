# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/carry-save-addition/. The authors are listed in prov/KMMETW.jsonl.

import random

import pytest

from carry_save_addition import (
    carry_save_sum,
    carry_save_tree,
    csa,
    from_digits,
    to_digits,
    width_for,
)


def _levels(m: int) -> int:
    """The least L with d_L >= m, where d_0 = 2 and d_{j+1} = floor(3 d_j / 2)."""
    d, level = 2, 0
    while d < m:
        d, level = 3 * d // 2, level + 1
    return level


def test_example_decimal() -> None:
    x, y, z = (to_digits(v, 4, 10) for v in (487, 659, 328))
    s, c = csa(x, y, z, 10)
    assert s == [4, 5, 3, 0] and c == [0, 2, 1, 1]
    assert from_digits(s, 10) + from_digits(c, 10) == 1474


def test_example_binary() -> None:
    x, y, z = (to_digits(v, 6, 2) for v in (13, 11, 7))
    s, c = csa(x, y, z, 2)
    assert from_digits(s, 2) == 1 and from_digits(c, 2) == 30


def test_exhaustive_small() -> None:
    for base in (2, 3, 4):
        n = 3
        top = base ** (n - 1)
        for x in range(top):
            for y in range(top):
                for z in range(top):
                    xs, ys, zs = (to_digits(v, n, base) for v in (x, y, z))
                    s, c = csa(xs, ys, zs, base)
                    assert from_digits(s, base) + from_digits(c, base) == x + y + z
                    assert all(0 <= d < base for d in s)
                    assert all(0 <= d <= 2 for d in c) and c[0] == 0


def test_random_csa_invariant() -> None:
    rng = random.Random(1964)
    for _ in range(1500):
        base = rng.choice((2, 3, 7, 10, 16, 256, 2**16))
        n = rng.randint(1, 30)
        vals = [rng.randrange(base ** n) for _ in range(3)]
        xs, ys, zs = (to_digits(v, n + 1, base) for v in vals)
        s, c = csa(xs, ys, zs, base)
        assert from_digits(s, base) + from_digits(c, base) == sum(vals)
        assert max(c) <= 2


def test_many_operands() -> None:
    rng = random.Random(2026)
    for _ in range(600):
        base = rng.choice((2, 10, 2**8, 2**32))
        n = rng.randint(1, 12)
        m = rng.randint(1, 40)
        vals = [rng.randrange(base ** n) for _ in range(m)]
        w = width_for(m, n, base)
        nums = [to_digits(v, w, base) for v in vals]
        total, steps = carry_save_sum(nums, base)
        assert from_digits(total, base) == sum(vals)
        assert steps == max(0, m - 2)
        total, levels = carry_save_tree(nums, base)
        assert from_digits(total, base) == sum(vals)
        assert levels == _levels(m)


def test_edges() -> None:
    for base in (2, 10, 2**16):
        n = 5
        top = base ** n - 1
        w = width_for(3, n, base)
        xs = to_digits(top, w, base)
        s, c = csa(xs, xs, xs, base)
        assert from_digits(s, base) + from_digits(c, base) == 3 * top
        zero = to_digits(0, w, base)
        s, c = csa(zero, zero, zero, base)
        assert s == zero and c == zero
        total, _ = carry_save_sum([xs] * 3, base)
        assert from_digits(total, base) == 3 * top


def test_overflow_is_reported() -> None:
    with pytest.raises(OverflowError):
        csa([9], [9], [9], 10)


def test_tree_level_counts() -> None:
    assert [_levels(m) for m in (2, 3, 4, 6, 9, 13, 19, 28, 42, 63)] == list(range(10))
    for m in range(1, 200):
        nums = [[1, 0, 0, 0]] * m
        _, levels = carry_save_tree(nums, 1000)
        assert levels == _levels(m)
