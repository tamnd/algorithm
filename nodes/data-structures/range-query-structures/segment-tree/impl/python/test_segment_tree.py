# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/segment-tree/. The authors are listed in prov/P50MYS.jsonl.

import math
import random

import pytest

from segment_tree import SegmentTree


def test_example() -> None:
    st = SegmentTree([5, 2, 8, 1, 9, 3, 7, 4])
    assert st.t[1] == 39
    assert [st.t[2], st.t[3]] == [16, 23]
    assert [st.t[4], st.t[5], st.t[6], st.t[7]] == [7, 9, 12, 11]
    assert st.query(2, 6) == 28
    st.update(3, 6)
    assert [st.t[11], st.t[5], st.t[2], st.t[1]] == [6, 14, 21, 44]
    assert st.query(1, 4) == 25
    st.check_invariant()


def test_edges() -> None:
    empty: SegmentTree[int] = SegmentTree([])
    assert empty.query(0, -1) == 0
    one = SegmentTree([7])
    assert one.query(0, 0) == 7
    one.update(0, -3)
    assert one.query(0, 0) == -3
    same = SegmentTree([4] * 9, min, math.inf)
    assert same.query(2, 7) == 4
    assert same.query(5, 4) == math.inf
    big = SegmentTree([2**63 - 1, 2**63 - 1, -(2**63)])
    assert big.query(0, 2) == 2**63 - 2
    with pytest.raises(IndexError):
        one.query(0, 1)
    with pytest.raises(IndexError):
        one.update(1, 0)


def test_identity_for_min_is_not_zero() -> None:
    st = SegmentTree([5, 6, 7], min, math.inf)
    assert st.query(0, 2) == 5


def test_non_commutative() -> None:
    words = ["ab", "c", "", "de", "f", "gh", "i"]
    st = SegmentTree(words, lambda x, y: x + y, "")
    for l in range(len(words) + 1):
        for r in range(l - 1, len(words)):
            assert st.query(l, r) == "".join(words[l : r + 1])


def test_random_against_list() -> None:
    rng = random.Random(7)
    for _ in range(600):
        n = rng.randrange(1, 18)
        a = [rng.randrange(-50, 50) for _ in range(n)]
        kind = rng.randrange(3)
        if kind == 0:
            st = SegmentTree(a)
            agg = sum
        elif kind == 1:
            st = SegmentTree(a, min, math.inf)
            agg = lambda s: min(s, default=math.inf)  # noqa: E731
        else:
            a = [abs(x) for x in a]
            st = SegmentTree(a, math.gcd, 0)
            agg = lambda s: math.gcd(*s) if s else 0  # noqa: E731
        for _ in range(20):
            if rng.random() < 0.4:
                i = rng.randrange(n)
                a[i] = rng.randrange(0 if kind == 2 else -50, 50)
                st.update(i, a[i])
            else:
                l = rng.randrange(n + 1)
                r = rng.randrange(l - 1, n)
                assert st.query(l, r) == agg(a[l : r + 1])
        st.check_invariant()
