# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/method-of-means-and-medians/. The authors are listed in prov/JBVF6M.jsonl.

import random
from fractions import Fraction

from method_of_means_and_medians import depth, l1, mmm, path_lengths, wirelength


def naive(points, idx, axis):
    """Reference: sort the set afresh at each level and split it in two."""
    idx = sorted(idx, key=lambda i: (points[i][axis], points[i][1 - axis], i))
    k = len(idx)
    c = (sum(Fraction(points[i][0]) for i in idx) / k, sum(Fraction(points[i][1]) for i in idx) / k)
    if k == 1:
        return (c, idx[0])
    h = k // 2
    return (c, naive(points, idx[:h], 1 - axis), naive(points, idx[h:], 1 - axis))


def as_tuple(v):
    if not v.kids:
        return (v.pt, v.sinks[0])
    return (v.pt, as_tuple(v.kids[0]), as_tuple(v.kids[1]))


def check_splits(points, v):
    """Brute force: every sink of the low half is at most every sink of the
    high half in the split order, the halves have sizes floor and ceil, and
    the point of each node is the centre of mass of its sinks."""
    k = len(v.sinks)
    assert v.pt == (sum(Fraction(points[i][0]) for i in v.sinks) / k, sum(Fraction(points[i][1]) for i in v.sinks) / k)
    if not v.kids:
        assert k == 1
        return
    lo, hi = v.kids
    assert sorted(lo.sinks + hi.sinks) == sorted(v.sinks)
    assert (len(lo.sinks), len(hi.sinks)) == (k // 2, k - k // 2)
    a = v.axis
    for i in lo.sinks:
        for j in hi.sinks:
            assert (points[i][a], points[i][1 - a], i) < (points[j][a], points[j][1 - a], j)
    for kid in v.kids:
        assert kid.axis is None or kid.axis == 1 - a
        check_splits(points, kid)


def test_against_reference_and_brute_force(rng=random.Random(11)):
    for _ in range(300):
        n = rng.randint(1, 40)
        points = [(rng.randint(0, 6), rng.randint(0, 6)) for _ in range(n)]
        root = mmm(points)
        assert as_tuple(root) == naive(points, list(range(n)), 0)
        check_splits(points, root)
        assert sorted(path_lengths(root)) == list(range(n))


def test_depth_bound():
    rng = random.Random(5)
    for n in range(1, 300):
        points = [(rng.randint(0, 50), rng.randint(0, 50)) for _ in range(n)]
        assert depth(mmm(points)) == (n - 1).bit_length()  # the ceiling of log2 n


def test_grid_gives_h_tree():
    # 4^k sinks at the centres of the cells of a 2^k by 2^k grid on a square of
    # side D: every path has length D (1 - 2^-k), and the total wire is
    # 1.5 D (2^k - 1), the values of the H-tree
    for k in range(0, 4):
        m = 2 ** k
        D = 2 * m
        points = [(2 * i + 1, 2 * j + 1) for i in range(m) for j in range(m)]
        root = mmm(points)
        lengths = set(path_lengths(root).values())
        assert lengths == {Fraction(D) * (1 - Fraction(1, m))}
        assert wirelength(root) == Fraction(3, 2) * D * (m - 1)


def test_skew_not_zero_in_general():
    points = [(0, 6), (0, 7), (2, 3), (8, 6)]
    root = mmm(points)
    assert root.pt == (Fraction(5, 2), Fraction(11, 2))
    assert [k.pt for k in root.kids] == [(0, Fraction(13, 2)), (5, Fraction(9, 2))]
    assert path_lengths(root) == {0: 4, 1: 4, 2: 8, 3: 8}
    assert wirelength(root) == 17
    # every edge is exactly the L1 distance of its ends
    assert l1(root.pt, root.kids[1].pt) == Fraction(7, 2)


def test_four_corner_example():
    root = mmm([(-1, -1), (-1, 1), (1, -1), (1, 1)])
    assert set(path_lengths(root).values()) == {2}
    assert wirelength(root) == 6
