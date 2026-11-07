# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/toom-cook-multiplication/. The authors are listed in prov/KFMRJ2.jsonl.

import math
import random

import pytest

import toom_cook_multiplication as tc
from toom_cook_multiplication import Stats, s_div_exact, toom3, toom3_multiply, toom_k


def limbs(x: int, w: int, n: int) -> list[int]:
    return [(x >> (w * i)) & ((1 << w) - 1) for i in range(n)]


def value(d: list[int], w: int) -> int:
    v = 0
    for x in reversed(d):
        v = (v << w) | x
    return v


def test_example_by_hand() -> None:
    a2, a1, a0, b2, b1, b0 = 12, 34, 56, 78, 90, 12

    def ev(c2, c1, c0):
        p = c0 + c2
        return [c0, p + c1, p - c1, 2 * (p - c1 + c2) - c0, c2]

    assert ev(a2, a1, a0) == [56, 102, 34, 36, 12]
    assert ev(b2, b1, b0) == [12, 180, 0, 144, 78]
    v0, v1, vm1, vm2, vinf = [x * y for x, y in zip(ev(a2, a1, a0), ev(b2, b1, b0))]
    assert (v0, v1, vm1, vm2, vinf) == (672, 18360, 0, 5184, 936)
    r3 = (vm2 - v1) // 3
    r1 = (v1 - vm1) // 2
    r2 = vm1 - v0
    assert (r3, r1, r2) == (-4392, 9180, -672)
    r3 = (r2 - r3) // 2 + 2 * vinf
    r2 = r2 + r1 - vinf
    r1 = r1 - r3
    assert [v0, r1, r2, r3, vinf] == [672, 5448, 7572, 3732, 936]
    assert sum(c * 100**i for i, c in enumerate([v0, r1, r2, r3, vinf])) == 97408265472 == 123456 * 789012


def test_example_on_limbs() -> None:
    # the same product with 8-bit limbs
    x, y = 123456, 789012
    assert value(toom3(limbs(x, 8, 3), limbs(y, 8, 3), 8, 2), 8) == x * y


@pytest.mark.parametrize("w", [4, 8])
def test_random(w: int) -> None:
    rng = random.Random(100 + w)
    for n in range(1, 31):
        for t in range(8):
            x, y = rng.randrange(1 << (w * n)), rng.randrange(1 << (w * n))
            th = 2 if t % 2 else 4
            out = toom3(limbs(x, w, n), limbs(y, w, n), w, th)
            assert len(out) == 2 * n
            assert value(out, w) == x * y


@pytest.mark.parametrize("w", [4, 8])
def test_edges(w: int) -> None:
    B = 1 << w
    for n in (1, 2, 3, 4, 5, 6, 7, 9, 10, 27, 28):
        top = B**n - 1
        for x in (0, 1, top, B ** (n - 1), top - 1, B ** (n // 2)):
            for y in (0, 1, top, B ** (n - 1)):
                assert value(toom3(limbs(x, w, n), limbs(y, w, n), w, 2), w) == x * y


def test_unequal_lengths() -> None:
    rng = random.Random(5)
    for _ in range(200):
        m, n = rng.randint(0, 20), rng.randint(0, 20)
        x, y = rng.randrange(1 << (8 * m)) if m else 0, rng.randrange(1 << (8 * n)) if n else 0
        out = toom3_multiply(limbs(x, 8, m), limbs(y, 8, n), 8, 2)
        assert len(out) == m + n
        assert value(out, 8) == x * y


def test_counts_and_depth() -> None:
    counted = [0]
    orig = tc._schoolbook

    def counting(a, b, w):
        counted[0] += len(a) * len(b)
        return orig(a, b, w)

    tc._schoolbook = counting
    try:
        results = {}
        for n in (729, 2187):
            counted[0] = 0
            st = Stats()
            toom3([255] * n, [255] * n, 8, 8, st)
            results[n] = (counted[0], st.max_depth, st.leaves)
    finally:
        tc._schoolbook = orig
    assert results[729] == (78125, 5, 5**5)
    assert results[2187] == (390625, 6, 5**6)
    for n in (10, 100, 1000):
        st = Stats()
        toom3([1] * n, [1] * n, 8, 2, st)
        assert st.max_depth <= math.ceil(math.log(2 * n, 3)) + 1


def test_exact_division_check() -> None:
    with pytest.raises(ValueError):
        s_div_exact((1, [7]), 3, 8)
    with pytest.raises(ValueError):
        toom3([1], [1, 2], 8)
    with pytest.raises(ValueError):
        toom3([1, 2, 3], [1, 2, 3], 2)


def test_generic_toom_k() -> None:
    rng = random.Random(9)
    for k in (2, 3, 4, 5):
        for d in (1, 4, 9, 30, 70):
            for _ in range(6):
                x, y = rng.randrange(1 << (8 * d)), rng.randrange(1 << (8 * d))
                assert toom_k(x, y, k, d) == x * y
        top = (1 << 240) - 1
        assert toom_k(top, top, k, 30) == top * top
        assert toom_k(0, top, k, 30) == 0


def test_exponents() -> None:
    e = [math.log(2 * k - 1, k) for k in (2, 3, 4, 5)]
    assert [round(v, 3) for v in e] == [1.585, 1.465, 1.404, 1.365]
