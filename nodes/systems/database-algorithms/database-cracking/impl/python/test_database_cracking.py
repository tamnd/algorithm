# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/database-cracking/. The authors are listed in prov/N3RJND.jsonl.

import random

from database_cracking import CrackerColumn, crack_in_three, crack_in_two

COL = [13, 16, 4, 9, 2, 12, 7, 1, 19, 3, 14, 11, 8, 6]


def scan(col, lo, hi):
    return sorted(r for r, v in enumerate(col) if lo <= v < hi)


def test_example():
    cc = CrackerColumn(COL)
    res = cc.query(10, 14)
    assert sorted(COL[r] for r in res) == [11, 12, 13]
    assert [v for v, _ in cc.c] == [6, 4, 9, 2, 7, 1, 8, 3, 13, 12, 11, 14, 19, 16]
    assert list(zip(cc.piv, cc.pos)) == [(10, 8), (14, 11)]
    assert cc.touched == 14
    res = cc.query(7, 16)
    assert sorted(COL[r] for r in res) == [7, 8, 9, 11, 12, 13, 14]
    assert [v for v, _ in cc.c] == [6, 4, 3, 2, 1, 7, 8, 9, 13, 12, 11, 14, 19, 16]
    assert cc.touched == 14 + 11
    res = cc.query(1, 8)
    assert sorted(COL[r] for r in res) == [1, 2, 3, 4, 6, 7]
    assert list(zip(cc.piv, cc.pos)) == [(1, 0), (7, 5), (8, 6), (10, 8), (14, 11), (16, 12)]
    assert cc.touched == 14 + 11 + 8
    cc.check_invariant()


def test_partitions():
    rng = random.Random(11)
    for _ in range(300):
        c = [(rng.randint(0, 9), i) for i in range(rng.randint(0, 20))]
        a = rng.randint(0, len(c))
        b = rng.randint(a, len(c))
        v = rng.randint(-1, 10)
        d = list(c)
        p = crack_in_two(d, a, b, v)
        assert d[:a] == c[:a] and d[b:] == c[b:] and sorted(d) == sorted(c)
        assert a <= p <= b
        assert all(x < v for x, _ in d[a:p]) and all(x >= v for x, _ in d[p:b])
        lo = rng.randint(-1, 10)
        hi = rng.randint(lo, 11)
        d = list(c)
        p, q = crack_in_three(d, a, b, lo, hi)
        assert d[:a] == c[:a] and d[b:] == c[b:] and sorted(d) == sorted(c)
        assert all(x < lo for x, _ in d[a:p])
        assert all(lo <= x < hi for x, _ in d[p:q])
        assert all(x >= hi for x, _ in d[q:b])


def test_every_query_equals_a_scan_and_invariant_holds():
    rng = random.Random(2007)
    for _ in range(150):
        n = rng.randint(0, 80)
        col = [rng.randint(0, 40) for _ in range(n)]
        cc = CrackerColumn(col)
        for _ in range(25):
            lo = rng.randint(-3, 43)
            hi = rng.randint(-3, 43)
            assert sorted(cc.query(lo, hi)) == scan(col, lo, hi)
            cc.check_invariant()


def test_repeated_query_does_no_work():
    cc = CrackerColumn(COL)
    first = sorted(cc.query(5, 12))
    t = cc.touched
    assert sorted(cc.query(5, 12)) == first
    assert cc.touched == t
    assert cc.query(9, 9) == [] and cc.query(12, 3) == []


def test_random_workload_costs_less_than_sequential():
    rng = random.Random(6)
    n, q = 4000, 200
    col = [rng.randrange(10 ** 5) for _ in range(n)]
    rand = CrackerColumn(col)
    for _ in range(q):
        a, b = rng.randrange(10 ** 5), rng.randrange(10 ** 5)
        rand.query(min(a, b), max(a, b) + 1)
    seq = CrackerColumn(col)
    w = 10 ** 5 // q
    for j in range(q):
        seq.query(j * w, (j + 1) * w)
    harmonic = sum(1 / k for k in range(1, q + 1))
    assert rand.touched < 3 * n * harmonic
    assert seq.touched > n * q // 3
    assert seq.touched > 10 * rand.touched
