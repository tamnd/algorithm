# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ripple-carry-adder/. The authors are listed in prov/0BHM0W.jsonl.

import random

from ripple_carry_adder import (
    add_signed,
    carry_chain_length,
    full_adder,
    ripple_carry_add,
    ripple_carry_add_limbs,
    subtract,
)


def bits(x: int, n: int) -> list[int]:
    return [(x >> i) & 1 for i in range(n)]


def limbs(x: int, w: int, n: int) -> list[int]:
    return [(x >> (w * i)) & ((1 << w) - 1) for i in range(n)]


def value(d: list[int], w: int = 1) -> int:
    v = 0
    for x in reversed(d):
        v = (v << w) | x
    return v


def signed(d: list[int]) -> int:
    v = value(d)
    return v - (1 << len(d)) if d and d[-1] else v


def test_full_adder_truth_table() -> None:
    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):
                s, co = full_adder(a, b, c)
                assert s + 2 * co == a + b + c


def test_example() -> None:
    s = ripple_carry_add(bits(11, 4), bits(6, 4))
    assert s == [1, 0, 0, 0, 1] and value(s) == 17
    assert carry_chain_length(bits(11, 4), bits(6, 4)) == 3


def test_edges_bits() -> None:
    for n in (1, 2, 8, 33):
        top = (1 << n) - 1
        for x, y, c in [(0, 0, 0), (0, 0, 1), (1, 0, 0), (top, 0, 1), (top, 1, 0), (top, top, 1), (top, top, 0)]:
            x &= top
            y &= top
            assert value(ripple_carry_add(bits(x, n), bits(y, n), c)) == x + y + c
    # the longest carry chain: all ones plus one
    assert carry_chain_length(bits(255, 8), bits(1, 8)) == 8
    assert ripple_carry_add([], []) == [0]


def test_random_bits() -> None:
    rng = random.Random(4096)
    for _ in range(3000):
        n = rng.randint(1, 70)
        x, y, c = rng.getrandbits(n), rng.getrandbits(n), rng.randint(0, 1)
        assert value(ripple_carry_add(bits(x, n), bits(y, n), c)) == x + y + c


def test_limbs() -> None:
    rng = random.Random(1946)
    for w in (4, 8):
        base = 1 << w
        top = base - 1
        cases = [(0, 0, 1), (1, 1, 1), (top, 1, 1), (top, top, 1), (base**5 - 1, 1, 5), (base**5 - 1, base**5 - 1, 5)]
        for x, y, n in cases:
            assert value(ripple_carry_add_limbs(limbs(x, w, n), limbs(y, w, n), w), w) == x + y
        for _ in range(1500):
            n = rng.randint(1, 20)
            x, y = rng.getrandbits(w * n), rng.getrandbits(w * n)
            if rng.random() < 0.2:
                x = base**n - 1
            s = ripple_carry_add_limbs(limbs(x, w, n), limbs(y, w, n), w)
            assert len(s) == n + 1 and value(s, w) == x + y


def test_signed_and_subtract() -> None:
    for n in (1, 2, 3, 4, 8):
        lo, hi = -(1 << (n - 1)), (1 << (n - 1)) - 1
        for x in range(lo, hi + 1):
            for y in range(lo, hi + 1):
                s, ov = add_signed(bits(x, n), bits(y, n))
                exact = x + y
                assert ov == (not lo <= exact <= hi)
                assert (signed(s) - exact) % (1 << n) == 0
    for n in (1, 4, 8):
        for x in range(1 << n):
            for y in range(1 << n):
                d, c = subtract(bits(x, n), bits(y, n))
                assert value(d) == (x - y) % (1 << n) and c == (1 if x >= y else 0)
