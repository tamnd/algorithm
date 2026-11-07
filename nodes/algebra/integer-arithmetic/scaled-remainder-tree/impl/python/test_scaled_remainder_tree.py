# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scaled-remainder-tree/. The authors are listed in prov/T3AFQR.jsonl.

import math
import random

import pytest

import scaled_remainder_tree as srt
from scaled_remainder_tree import (
    Stats,
    from_limbs,
    height,
    product_tree,
    remainder_tree,
    scaled_remainders,
    scaled_remainders_limbs,
    to_limbs,
)


def test_random_against_python():
    rng = random.Random(1)
    for _ in range(1500):
        k = rng.randint(1, 40)
        ms = [rng.getrandbits(rng.randint(1, 64)) or 1 for _ in range(k)]
        x = rng.getrandbits(rng.randint(0, 2500))
        want = [x % m for m in ms]
        assert scaled_remainders(x, ms) == want
        assert remainder_tree(x, ms) == want


def test_edge_cases():
    cases = [
        (0, [1]),
        (0, [5, 7]),
        (5, [1, 1, 1]),
        (12345, [12345]),
        (12345 * 7 * 11, [7, 11, 12345]),  # all remainders zero
        ((1 << 200) - 1, [2, 4, 8, (1 << 64) - 1, 1 << 63]),
        (10**50, [10**k for k in range(1, 12)]),
        (2**127 - 1, [3] * 33),  # many equal moduli, height 6
    ]
    for x, ms in cases:
        assert scaled_remainders(x, ms) == [x % m for m in ms]
    rng = random.Random(2)
    for _ in range(300):  # x a multiple of P minus small values: fractions near 0 and 1
        ms = [rng.randint(1, 1000) for _ in range(rng.randint(1, 20))]
        P = math.prod(ms)
        for x in (P, P - 1, P + 1, 3 * P, 3 * P - 1):
            assert scaled_remainders(x, ms) == [x % m for m in ms]
    with pytest.raises(ValueError):
        scaled_remainders(5, [])
    with pytest.raises(ValueError):
        scaled_remainders(5, [3, 0])
    with pytest.raises(ValueError):
        scaled_remainders(-1, [3])


def test_guard_digits_are_needed():
    def run(x, ms, G):
        t = product_tree(ms)
        p = t.q.bit_length() + G
        out = []
        srt._descend(t, ((x % t.q) << p) // t.q, p, G, out, None, 0)
        return out

    rng = random.Random(3)
    bad = {0: 0, 1: 0}
    for _ in range(300):
        ms = [rng.getrandbits(rng.randint(1, 16)) or 1 for _ in range(rng.randint(2, 64))]
        x = rng.getrandbits(rng.randint(0, 800))
        want = [x % m for m in ms]
        for G in (0, 1):
            bad[G] += run(x, ms, G) != want
        d = height(product_tree(ms))
        G = max(1, math.ceil(math.log2(d + 1)))
        assert run(x, ms, G) == want
    assert bad[0] > 150 and bad[1] > 150


def test_worked_example():
    x, ms = 123456, [7, 11, 13, 17]
    t = product_tree(ms)
    assert (t.q, t.left.q, t.right.q, height(t)) == (17017, 77, 221, 2)
    p = 17
    Y = ((x % 17017) << p) // 17017
    assert x % 17017 == 4337 and Y == 33405
    assert 221 * Y == 7382505 and (221 * Y) % (1 << 17) == 42473 and 42473 >> 8 == 165
    assert (77 * Y) % (1 << 17) == 81817 and 81817 >> 7 == 639
    rows = []
    for parent, pp, sib_q, m in ((165, 9, 11, 7), (165, 9, 7, 11), (639, 10, 17, 13), (639, 10, 13, 17)):
        pl = m.bit_length() + 2
        Z = (sib_q * parent) % (1 << pp)
        Yl = Z >> (pp - pl)
        rows.append((pl, Z, Yl, -((-m * Yl) >> pl) % m))
    assert rows == [(5, 279, 17, 4), (6, 131, 16, 3), (6, 623, 38, 8), (7, 115, 14, 2)]
    st = Stats()
    assert scaled_remainders(x, ms, st) == [4, 3, 8, 2]
    assert (st.products, st.divisions) == (13, 1)


def test_counts_and_depth():
    rng = random.Random(4)
    for k in (1, 2, 3, 5, 8, 64, 100, 257):
        ms = [rng.getrandbits(32) | 1 for _ in range(k)]
        st = Stats()
        scaled_remainders(rng.getrandbits(32 * k), ms, st)
        assert st.products == 4 * k - 3 and st.divisions == 1
        assert st.depth == height(product_tree(ms)) == math.ceil(math.log2(k))
        t = product_tree(ms)
        st2 = Stats()
        scaled_remainders(rng.getrandbits(32 * k), ms, st2, tree=t)
        assert st2.products == 3 * k - 2


@pytest.mark.parametrize("w", [4, 8])
def test_limbs_against_python(w):
    rng = random.Random(10 + w)
    for _ in range(400):
        ms = [[rng.randrange(1 << w) for _ in range(rng.randint(1, 6))] for _ in range(rng.randint(1, 20))]
        for m in ms:
            if from_limbs(m, w) == 0:
                m[0] = 1
        x = [rng.randrange(1 << w) for _ in range(rng.randint(0, 80))]
        X = from_limbs(x, w)
        rs = scaled_remainders_limbs(x, ms, w)
        for r, m in zip(rs, ms):
            assert from_limbs(r, w) == X % from_limbs(m, w)
            assert len(r) == len(m) and all(0 <= d < (1 << w) for d in r)
    assert to_limbs(0, w) == []
