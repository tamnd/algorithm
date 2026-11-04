# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/disjoint-sparse-table/. The authors are listed in prov/5HH6N4.jsonl.

import operator
import random

import pytest

from disjoint_sparse_table import DisjointSparseTable

Mat = tuple[int, int, int, int]
MOD = 1_000_003


def matmul(x: Mat, y: Mat) -> Mat:
    a, b, c, d = x
    e, f, g, h = y
    return ((a * e + b * g) % MOD, (a * f + b * h) % MOD, (c * e + d * g) % MOD, (c * f + d * h) % MOD)


def test_example() -> None:
    a = [3, 1, 4, 1, 5, 9, 2, 6]
    t = DisjointSparseTable(a, operator.add)
    assert t.table[1] == [3, 1, 4, 1, 5, 9, 2, 6]
    assert t.table[2] == [4, 1, 4, 5, 14, 9, 2, 8]
    assert t.table[3] == [9, 6, 5, 1, 5, 14, 16, 22]
    assert t.query(2, 5) == 19
    assert t.query(4, 7) == 22
    assert t.query(1, 2) == 5
    assert t.query(3, 3) == 1
    t.check_invariant()


def test_edges() -> None:
    t = DisjointSparseTable(["x"], operator.add)
    assert t.query(0, 0) == "x"
    with pytest.raises(IndexError):
        t.query(0, 1)
    e = DisjointSparseTable([], operator.add)
    with pytest.raises(IndexError):
        e.query(0, 0)
    s = DisjointSparseTable(list("abcde"), operator.add)
    assert s.query(0, 4) == "abcde" and s.query(1, 3) == "bcd" and s.query(3, 4) == "de"
    s.check_invariant()


def test_random_against_brute_force() -> None:
    rng = random.Random(1982)
    for _ in range(500):
        n = rng.randint(1, 40)
        mats = [tuple(rng.randrange(7) for _ in range(4)) for _ in range(n)]
        t = DisjointSparseTable(mats, matmul)
        words = ["".join(rng.choice("ab") for _ in range(rng.randint(0, 2))) for _ in range(n)]
        u = DisjointSparseTable(words, operator.add)
        for _ in range(10):
            l = rng.randrange(n)
            r = rng.randrange(l, n)
            acc = mats[l]
            for j in range(l + 1, r + 1):
                acc = matmul(acc, mats[j])
            assert t.query(l, r) == acc
            assert u.query(l, r) == "".join(words[l : r + 1])
        if n <= 20:
            t.check_invariant()
