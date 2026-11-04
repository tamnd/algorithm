# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/segment-tree-beats/. The authors are listed in prov/4S5W6M.jsonl.

import math
import random

import pytest

from segment_tree_beats import NEG, SegmentTreeBeats


def test_example() -> None:
    st = SegmentTreeBeats([5, 2, 8, 1, 9, 3, 7, 4])
    assert (st.mx1[1], st.mx2[1], st.cnt[1], st.sum[1]) == (9, 8, 1, 39)
    st.visits = 0
    st.chmin(0, 7, 6)
    assert st.visits == 5
    assert (st.mx1[1], st.mx2[1], st.cnt[1], st.sum[1]) == (6, 5, 3, 33)
    assert (st.mx1[2], st.sum[2]) == (6, 14)
    assert st.mx1[5] == 8  # pending: node 5 still stores the old maximum
    assert st.query_sum(2, 5) == 16
    assert st.mx1[5] == 6  # the query pushed the cap down
    assert st.values() == [5, 2, 6, 1, 6, 3, 6, 4]
    st.chmin(1, 6, 3)
    assert st.values() == [5, 2, 3, 1, 3, 3, 3, 4]
    assert st.query_sum(0, 7) == 24
    assert st.query_max(1, 6) == 3
    st.check_invariant()


def test_single_and_equal() -> None:
    st = SegmentTreeBeats([4])
    assert st.mx2[1] == NEG
    st.chmin(0, 0, 10)
    assert st.query_sum(0, 0) == 4
    st.chmin(0, 0, -2)
    assert st.query_max(0, 0) == -2
    eq = SegmentTreeBeats([7] * 5)
    eq.chmin(0, 4, 3)
    assert eq.query_sum(0, 4) == 15
    eq.check_invariant()
    with pytest.raises(IndexError):
        eq.chmin(2, 5, 0)
    with pytest.raises(ValueError):
        SegmentTreeBeats([])


def test_random_against_brute_force() -> None:
    rng = random.Random(4565)
    for _ in range(40):
        n = rng.randint(1, 40)
        a = [rng.randint(-50, 50) for _ in range(n)]
        st = SegmentTreeBeats(a)
        for _ in range(40):
            l = rng.randrange(n)
            r = rng.randrange(l, n)
            kind = rng.randrange(3)
            if kind == 0:
                x = rng.randint(-60, 60)
                st.chmin(l, r, x)
                for i in range(l, r + 1):
                    a[i] = min(a[i], x)
            elif kind == 1:
                assert st.query_sum(l, r) == sum(a[l : r + 1])
            else:
                assert st.query_max(l, r) == max(a[l : r + 1])
        st.check_invariant()
        assert st.values() == a


def test_amortized_visit_bound() -> None:
    rng = random.Random(99)
    for n in (64, 200, 513):
        q = 2 * n
        st = SegmentTreeBeats([rng.randint(0, 10**6) for _ in range(n)])
        st.visits = 0
        for _ in range(q):
            l = rng.randrange(n)
            r = rng.randrange(l, n)
            st.chmin(l, r, rng.randint(0, 10**6))
        lg = math.ceil(math.log2(n))
        extra = n * (lg + 1) + q * (2 * lg + 1)
        assert st.visits <= q * (4 * lg + 1) + 2 * extra
