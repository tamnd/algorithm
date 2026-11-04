# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sparse-table/. The authors are listed in prov/VSD7FB.jsonl.

import math
import operator
import random
from functools import reduce

import pytest

from sparse_table import SparseTable


def test_example() -> None:
    st = SparseTable([5, 2, 8, 1, 9, 3, 7, 4], min)
    assert st.lg == [0, 0, 1, 1, 2, 2, 2, 2, 3]
    assert st.st[1] == [2, 2, 1, 1, 3, 3, 4]
    assert st.st[2] == [1, 1, 1, 1, 3]
    assert st.st[3] == [1]
    assert st.query(2, 6) == 1
    assert st.query(5, 7) == 3
    assert st.query(4, 4) == 9
    st.check_invariant()
    s = SparseTable([5, 2, 8, 1, 9, 3, 7, 4], operator.add)
    assert s.query_any(1, 6) == 30
    assert s.query(1, 6) == 40  # the overlap is counted twice: the pitfall


def test_edges() -> None:
    empty: SparseTable[int] = SparseTable([], min)
    assert len(empty) == 0
    with pytest.raises(IndexError):
        empty.query(0, 0)
    one = SparseTable([7], max)
    assert one.query(0, 0) == 7 and one.query_any(0, 0) == 7
    same = SparseTable([3] * 13, min)
    assert same.query(0, 12) == 3
    big = SparseTable([2**63 - 1, -(2**63), 0], max)
    assert big.query(0, 2) == 2**63 - 1
    with pytest.raises(IndexError):
        one.query(1, 0)


def test_non_commutative_idempotent() -> None:
    # "keep the left one" is associative and idempotent, not commutative.
    a = list("sparsetable")
    st = SparseTable(a, lambda x, y: x)
    for l in range(len(a)):
        for r in range(l, len(a)):
            assert st.query(l, r) == a[l]
    cat = SparseTable(a, operator.add)
    for l in range(len(a)):
        for r in range(l, len(a)):
            assert cat.query_any(l, r) == "".join(a[l : r + 1])


def test_random_against_brute_force() -> None:
    rng = random.Random(11)
    ops = [min, max, math.gcd, operator.or_, operator.and_]
    for _ in range(700):
        n = rng.randrange(1, 40)
        a = [rng.randrange(0, 64) for _ in range(n)]
        op = rng.choice(ops)
        st = SparseTable(a, op)
        sums = SparseTable(a, operator.add)
        for _ in range(15):
            l = rng.randrange(n)
            r = rng.randrange(l, n)
            assert st.query(l, r) == reduce(op, a[l : r + 1])
            assert sums.query_any(l, r) == sum(a[l : r + 1])
    st.check_invariant()
