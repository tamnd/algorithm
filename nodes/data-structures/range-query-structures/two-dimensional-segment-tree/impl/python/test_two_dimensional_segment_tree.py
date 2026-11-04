# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-dimensional-segment-tree/. The authors are listed in prov/QYYQT1.jsonl.

import math
import random

import pytest

from two_dimensional_segment_tree import SegmentTree2D

M = [[2, 1, 4, 3], [0, 5, 2, 1], [3, 1, 6, 2], [1, 4, 0, 5]]
INF = math.inf


def test_example_min() -> None:
    st = SegmentTree2D(M, min, INF)
    assert st.t[1][1] == 0
    assert st.t[5][5] == 5
    assert st.t[5][3] == 1
    assert st.t[6][5] == 1
    assert st.t[6][3] == 2
    assert st.query(1, 1, 2, 3) == 1
    st.update(2, 1, 7)
    assert st.t[6][5] == 7
    assert st.t[3][5] == 4
    assert st.query(1, 1, 2, 3) == 1
    st.update(1, 3, 9)
    assert st.t[5][3] == 2
    assert st.query(1, 1, 2, 3) == 2
    st.check_invariant()


def test_example_sum() -> None:
    st = SegmentTree2D(M)
    assert st.query(1, 1, 2, 3) == 17
    assert st.query(0, 0, 3, 3) == 40
    st.update(2, 1, 4)
    assert st.query(1, 1, 2, 3) == 20
    st.check_invariant()


def test_edges() -> None:
    one = SegmentTree2D([[7]], min, INF)
    assert one.query(0, 0, 0, 0) == 7
    assert one.query(0, 0, -1, 0) == INF
    row = SegmentTree2D([[5, 2, 8, 1, 9, 3, 7, 4]], max, -INF)
    assert row.query(0, 2, 0, 6) == 9
    col = SegmentTree2D([[5], [2], [8], [1], [9]], math.gcd, 0)
    assert col.query(0, 0, 4, 0) == 1
    with pytest.raises(ValueError):
        SegmentTree2D([])
    with pytest.raises(ValueError):
        SegmentTree2D([[1, 2], [3]])
    with pytest.raises(IndexError):
        row.update(1, 0, 3)
    with pytest.raises(IndexError):
        row.query(0, 0, 0, 8)


@pytest.mark.parametrize("name", ["sum", "min", "max"])
def test_random_against_brute_force(name: str) -> None:
    op, e = {"sum": (lambda a, b: a + b, 0), "min": (min, INF), "max": (max, -INF)}[name]
    rng = random.Random(7 + len(name))
    for _ in range(40):
        n, m = rng.randint(1, 7), rng.randint(1, 7)
        mat = [[rng.randint(-30, 30) for _ in range(m)] for _ in range(n)]
        st = SegmentTree2D(mat, op, e)
        for _ in range(25):
            if rng.random() < 0.4:
                r, c, x = rng.randrange(n), rng.randrange(m), rng.randint(-30, 30)
                mat[r][c] = x
                st.update(r, c, x)
            else:
                r1, r2 = sorted((rng.randrange(n), rng.randrange(n)))
                c1, c2 = sorted((rng.randrange(m), rng.randrange(m)))
                want = e
                for r in range(r1, r2 + 1):
                    for c in range(c1, c2 + 1):
                        want = op(want, mat[r][c])
                assert st.query(r1, c1, r2, c2) == want
        st.check_invariant()
