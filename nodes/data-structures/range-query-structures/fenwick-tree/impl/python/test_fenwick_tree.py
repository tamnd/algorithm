# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fenwick-tree/. The authors are listed in prov/T604D3.jsonl.

import random

import pytest

from fenwick_tree import FenwickTree


def test_example() -> None:
    a = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
    f = FenwickTree.build(a)
    assert f.t[1:] == [3, 4, 4, 9, 5, 14, 2, 31, 5, 8]
    assert f.prefix(7) == 25
    assert f.prefix(10) == 39
    assert f.range_sum(3, 7) == 21
    assert f.search(20) == 6
    f.add(3, 2)
    assert (f.t[3], f.t[4], f.t[8]) == (6, 11, 33)
    assert f.range_sum(3, 7) == 23


def test_edges() -> None:
    f = FenwickTree(0)
    assert f.prefix(0) == 0
    assert f.search(1) == 1
    f = FenwickTree(1)
    f.add(1, -5)
    assert f.prefix(1) == -5 and f.range_sum(1, 1) == -5
    with pytest.raises(IndexError):
        f.add(0, 1)
    big = 2**62
    f = FenwickTree.build([big, big, big])
    assert f.prefix(3) == 3 * big
    f = FenwickTree.build([0, 0, 0, 0])
    assert f.search(0) == 1 and f.search(1) == 5


def test_build_equals_adds() -> None:
    rng = random.Random(7)
    for n in range(40):
        a = [rng.randint(-9, 9) for _ in range(n)]
        g = FenwickTree(n)
        for i, x in enumerate(a, 1):
            g.add(i, x)
        assert FenwickTree.build(a).t == g.t


def test_random_against_list() -> None:
    rng = random.Random(1994)
    for _ in range(500):
        n = rng.randint(1, 40)
        a = [rng.randint(0, 20) for _ in range(n)]
        f = FenwickTree.build(a)
        for _ in range(30):
            op = rng.randrange(4)
            if op == 0:
                i, d = rng.randint(1, n), rng.randint(0, 9)
                f.add(i, d)
                a[i - 1] += d
            elif op == 1:
                l = rng.randint(1, n)
                r = rng.randint(l, n)
                assert f.range_sum(l, r) == sum(a[l - 1 : r])
            elif op == 2:
                i = rng.randint(0, n)
                assert f.prefix(i) == sum(a[:i])
            else:
                s = rng.randint(0, sum(a) + 3)
                want = next((i for i in range(1, n + 1) if sum(a[:i]) >= s), n + 1)
                assert f.search(s) == want
        f.check_invariant(a)
