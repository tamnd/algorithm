# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/newton-raphson-division/. The authors are listed in prov/NDCZEW.jsonl.

import math
import random

import pytest

from newton_raphson_division import (
    Stats,
    divide,
    divide_block,
    divide_limbs,
    from_limbs,
    mul,
    reciprocal,
    to_limbs,
)


def test_mul_against_python():
    rng = random.Random(1)
    for _ in range(200):
        x = rng.getrandbits(rng.randint(0, 1000))
        y = rng.getrandbits(rng.randint(0, 1000))
        assert mul(x, y) == x * y
    for x in (0, 1, 255, 256, (1 << 800) - 1):
        for y in (0, 1, (1 << 800) - 1, 1 << 799):
            assert mul(x, y) == x * y


def test_reciprocal_exhaustive_small():
    for D in range(1, 1 << 12):
        st = Stats()
        B = D.bit_length()
        assert reciprocal(D, st) == (1 << (2 * B)) // D
        assert st.max_corrections <= 16


def test_reciprocal_random_and_extremes():
    rng = random.Random(2)
    worst = 0
    for B in list(range(9, 130)) + [256, 511, 512, 513, 1024, 2048]:
        cases = [1 << (B - 1), (1 << B) - 1, (1 << (B - 1)) + 1, (3 << (B - 2))]
        cases += [rng.randint(1 << (B - 1), (1 << B) - 1) for _ in range(2 if B > 300 else 6)]
        for D in cases:
            st = Stats()
            R = reciprocal(D, st)
            assert R == (1 << (2 * B)) // D
            assert st.max_corrections <= 16  # proved
            assert st.depth <= max(0, math.ceil(math.log2(B)))  # logarithmic depth
            worst = max(worst, st.max_corrections)
    assert worst <= 16


def test_line_l6_never_overshoots():
    # After line L6, X <= floor(4^B / D), so line L7 only counts up.
    import newton_raphson_division as m

    rng = random.Random(3)
    for _ in range(400):
        B = rng.randint(9, 300)
        D = rng.randint(1 << (B - 1), (1 << B) - 1)
        h = (B + 1) // 2
        X = reciprocal(D >> (B - h)) << (B - h)
        E = (1 << (2 * B)) - D * X
        if E >= 0:
            X1 = X + ((X * E) >> (2 * B))
        else:
            X1 = X - ((X * -E + (1 << (2 * B)) - 1) >> (2 * B))
        R = (1 << (2 * B)) // D
        assert R - 16 <= X1 <= R
        t = 1 << (B - h)
        assert -4 * D * t < E < D * t  # the start: -t < X - 4^B / D < 4t
    assert m.reciprocal(5) == 64 // 5


def test_divide_block_one_correction():
    rng = random.Random(4)
    for _ in range(3000):
        B = rng.randint(1, 120)
        D = rng.randint(1 << (B - 1), (1 << B) - 1)
        R = (1 << (2 * B)) // D
        U = rng.choice([0, D - 1, D, D * (1 << B) - 1, rng.randint(0, D * (1 << B) - 1)])
        q0 = (U * R) >> (2 * B)
        assert U // D - 1 <= q0 <= U // D
        assert divide_block(U, D, R, B) == divmod(U, D)


def test_divide_random_against_divmod():
    rng = random.Random(5)
    for _ in range(150):
        a = rng.getrandbits(rng.randint(0, 1200))
        d = rng.getrandbits(rng.randint(1, 600)) or 1
        assert divide(a, d) == divmod(a, d)


def test_divide_edge_cases():
    for a, d in [
        (0, 1), (1, 1), (5, 7), (7, 7), (1 << 1000, 1), (1 << 1000, 3),
        ((1 << 999) - 1, (1 << 500) - 1), ((1 << 999), (1 << 499)),
        (10**300, 10**150 + 7), (2**512 - 1, 2**256 + 1),
    ]:
        assert divide(a, d) == divmod(a, d)
    with pytest.raises(ZeroDivisionError):
        divide(5, 0)
    with pytest.raises(ZeroDivisionError):
        reciprocal(0)


@pytest.mark.parametrize("w", [4, 8])
def test_limbs_against_python(w):
    rng = random.Random(6 + w)
    for _ in range(200):
        na, nd = rng.randint(0, 48), rng.randint(1, 32)
        a = [rng.randrange(1 << w) for _ in range(na)]
        d = [rng.randrange(1 << w) for _ in range(nd)]
        if rng.random() < 0.2:
            a = [(1 << w) - 1] * na
        if from_limbs(d, w) == 0:
            d[-1] = 1
        A, D = from_limbs(a, w), from_limbs(d, w)
        q, r = divide_limbs(a, d, w)
        assert len(q) == na and len(r) == nd
        assert (from_limbs(q, w), from_limbs(r, w)) == divmod(A, D)
        assert all(0 <= x < (1 << w) for x in q + r)
    assert to_limbs(0) == []


def test_worked_example():
    D = 50000
    B, h = 16, 8
    Dh = D >> (B - h)
    assert Dh == 195
    Xh = reciprocal(Dh)
    assert Xh == 336
    X0 = Xh << (B - h)
    assert X0 == 86016
    E = (1 << 32) - D * X0
    assert E == -5832704
    step = -((X0 * E) // (1 << 32))  # ceil(X0 |E| / 2^32)
    assert step == 117 and abs(X0 * -E / 2**32 - 116.8125) < 1e-9
    st = Stats()
    assert reciprocal(D, st) == 85899 == (1 << 32) // D
    assert st.corrections == 0
    assert (1 << 32) - D * 85899 == 17296
    A = 3141592653
    q0 = (A * 85899) >> 32
    assert q0 == 62831 and A - q0 * D == 42653
    assert divide_block(A, D, 85899, B) == (62831, 42653)
    # the float view: the miss 1 - d x squares each step
    d, x, misses = 0.76, 1.0, []
    for _ in range(5):
        misses.append(1 - d * x)
        x = x + x * (1 - d * x)
    assert [round(e, 4) for e in misses[:3]] == [0.24, 0.0576, 0.0033]
    assert abs(misses[3] - 1.10e-5) < 1e-7 and abs(misses[4] - 1.21e-10) < 1e-11


def test_cost_shape():
    rng = random.Random(7)
    prev = None
    for B in (1024, 4096):
        D = rng.randint(1 << (B - 1), (1 << B) - 1)
        st = Stats()
        assert reciprocal(D, st) == (1 << (2 * B)) // D
        # three products per level, depth about log2(B / 8)
        assert st.products == 3 * st.depth
        assert st.depth == math.ceil(math.log2(B)) - 3
        assert st.product_digits <= 8 * B
        if prev is not None:
            assert st.products == prev + 6
        prev = st.products
