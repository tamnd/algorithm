# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/srt-division/. The authors are listed in prov/732WBN.jsonl.

import math
import random
from fractions import Fraction

import pytest

from srt_division import RHO, TABLE, build_table, srt_divide_fixed, srt_float_divide, trace


def test_example_trace():
    rows = trace(Fraction(3, 4), Fraction(5, 8), 6)
    assert [q for _, _, q in rows] == [1, 1, -1, 1, -1, 1]
    Q, W = srt_divide_fixed(3 << 8, 5 << 7, 10, 8)
    assert (Q, W) == (19660, 2048)
    assert Fraction(Q, 4**8) + Fraction(W, 2**12) / (4**8 * Fraction(5, 8)) == Fraction(3, 10)


def test_table_size_and_coarser_estimates_fail():
    assert len(TABLE) == 275
    with pytest.raises(ValueError):
        build_table(4, 2)  # two fractional bits of 4w are not enough
    with pytest.raises(ValueError):
        build_table(3, 3)  # nor are two bits of d after the leading one


def test_remainder_stays_bounded():
    rng = random.Random(11)
    for _ in range(400):
        x = Fraction(rng.randrange(2**30, 2**31), 2**31)
        d = Fraction(rng.randrange(2**30, 2**31), 2**31)
        w = x / 4
        for y, est, q in trace(x, d, 20):
            assert est <= y < est + Fraction(1, 8)
            w = y - q * d
            assert abs(w) <= RHO * d


def test_fixed_point_identity():
    rng = random.Random(12)
    F = 40
    for _ in range(2000):
        X, D = rng.randrange(2 ** (F - 1), 2**F), rng.randrange(2 ** (F - 1), 2**F)
        n = rng.randrange(1, 30)
        Q, W = srt_divide_fixed(X, D, F, n)
        x, d, w = Fraction(X, 2**F), Fraction(D, 2**F), Fraction(W, 2 ** (F + 2))
        assert 0 <= w < d
        assert x / (4 * d) == Fraction(Q, 4**n) + w / (4**n * d)


def test_float_division_correctly_rounded():
    rng = random.Random(13)
    for _ in range(20000):
        a = math.ldexp(rng.uniform(0.5, 1.0), rng.randint(-400, 400))
        b = math.ldexp(rng.uniform(0.5, 1.0), rng.randint(-400, 400))
        assert srt_float_divide(a, b) == a / b
    for a, b in [(1.0, 3.0), (3.0, 1.5), (1.0, 1.0), (2.0 - 2.0**-52, 1.0 + 2.0**-52), (4195835.0, 3145727.0)]:
        assert srt_float_divide(a, b) == a / b


def test_missing_table_entries_give_wrong_quotients():
    # Pentium-style fault: five rarely used cells near the top of the table return 0 instead of 2
    bad = dict(TABLE)
    for cell in [(11, 13), (12, 15), (13, 15), (14, 15), (15, 19)]:
        assert bad[cell] == 2
        bad[cell] = 0
    rng = random.Random(14)
    wrong = 0
    for _ in range(3000):
        X, D = rng.randrange(2**52, 2**53), rng.randrange(2**52, 2**53)
        exact = (X * 4**28) // (4 * D)
        assert srt_divide_fixed(X, D, 53, 28)[0] == exact
        try:
            wrong += srt_divide_fixed(X, D, 53, 28, table=bad)[0] != exact
        except KeyError:  # the remainder left the range the table covers
            wrong += 1
    assert 0 < wrong < 3000
