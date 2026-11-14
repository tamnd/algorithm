# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dexel-representation/. The authors are listed in prov/QH2CZJ.jsonl.

import random
from fractions import Fraction as F
from math import inf

from dexel_representation import (DexelModel, combine, difference, intersection,
                                  tool_segment, union)

OPS = {
    "union": (union, lambda a, b: a or b),
    "intersection": (intersection, lambda a, b: a and b),
    "difference": (difference, lambda a, b: a and not b),
}
EPS = 1e-9


def rand_dexel(rng, n_max=4, span=12):
    """A random valid dexel with Fraction endpoints (sorted, disjoint, not touching)."""
    k = rng.randint(0, n_max)
    pts = sorted(rng.sample(range(span * 2), 2 * k))
    return [(F(pts[2 * m], 2), F(pts[2 * m + 1], 2)) for m in range(k)]


def member(I, z):
    return any(lo <= z <= hi for lo, hi in I)


def valid(I):
    return all(lo < hi for lo, hi in I) and all(I[m][1] < I[m + 1][0] for m in range(len(I) - 1))


def check_against_pointwise(I, J, fn, op):
    R = fn(I, J)
    assert valid(R)
    ends = sorted({e for iv in I + J for e in iv})
    if not ends:
        assert R == []
        return
    probes = [ends[0] - 1, ends[-1] + 1] + [(a + b) / 2 for a, b in zip(ends, ends[1:])]
    for z in probes:  # interior points of the open cells: exact agreement
        assert member(R, z) == op(member(I, z), member(J, z))
    for m, e in enumerate(ends):  # endpoints: the closure of the interior
        left = (ends[m - 1] + e) / 2 if m > 0 else e - 1
        right = (ends[m + 1] + e) / 2 if m + 1 < len(ends) else e + 1
        want = op(member(I, left), member(J, left)) or op(member(I, right), member(J, right))
        assert member(R, e) == want


def test_small_cases():
    a, b = [(F(0), F(2)), (F(4), F(6))], [(F(1), F(5))]
    assert union(a, b) == [(0, 6)]
    assert intersection(a, b) == [(1, 2), (4, 5)]
    assert difference(a, b) == [(0, 1), (5, 6)]
    assert difference(b, a) == [(2, 4)]
    # touching pieces merge in a union and vanish in an intersection
    assert union([(F(0), F(1))], [(F(1), F(2))]) == [(0, 2)]
    assert intersection([(F(0), F(1))], [(F(1), F(2))]) == []
    assert difference([(F(0), F(2))], [(F(0), F(2))]) == []
    assert union([], []) == [] and difference([(F(0), F(1))], []) == [(0, 1)]


def test_booleans_against_pointwise_membership():
    rng = random.Random(41)
    for _ in range(1500):
        I, J = rand_dexel(rng), rand_dexel(rng)
        for fn, op in OPS.values():
            check_against_pointwise(I, J, fn, op)


def test_xor_and_identities():
    rng = random.Random(9)
    for _ in range(300):
        I, J, K = rand_dexel(rng), rand_dexel(rng), rand_dexel(rng)
        assert union(difference(I, J), intersection(I, J)) == I
        assert difference(I, union(J, K)) == difference(difference(I, J), K)
        x = combine(I, J, lambda a, b: a != b)
        assert x == union(difference(I, J), difference(J, I))


def removed(p, c0, c1, r, shank):
    """Exact test (Fractions): is p in the swept ball-end tool?"""
    def min_quad(a, b, lo, hi):
        bb = sum(x * x for x in b)
        t = lo if bb == 0 else min(max(-sum(x * y for x, y in zip(a, b)) / bb, lo), hi)
        return sum((x + t * y) ** 2 for x, y in zip(a, b))
    v = tuple(c1[i] - c0[i] for i in range(3))
    w = tuple(c0[i] - p[i] for i in range(3))
    if min_quad(w, v, F(0), F(1)) <= r * r:
        return True
    if not shank:
        return False
    s, dz = v[2], p[2] - c0[2]
    if s == 0:
        lo, hi = (F(0), F(1)) if dz >= 0 else (F(1), F(0))
    elif s > 0:
        lo, hi = F(0), min(F(1), dz / s)
    else:
        lo, hi = max(F(0), dz / s), F(1)
    return lo <= hi and min_quad(w[:2], v[:2], lo, hi) <= r * r


def test_tool_segment_against_exact_membership():
    rng = random.Random(13)
    for _ in range(300):
        c0 = tuple(F(rng.randint(-12, 12), 4) for _ in range(3))
        c1 = tuple(F(rng.randint(-12, 12), 4) for _ in range(3))
        if rng.random() < 0.2:
            c1 = (c0[0], c0[1], c1[2])
        r = F(rng.randint(2, 8), 4)
        for _ in range(6):
            q = (F(rng.randint(-16, 16), 4), F(rng.randint(-16, 16), 4))
            for shank in (False, True):
                seg = tool_segment(tuple(map(float, q)), tuple(map(float, c0)), tuple(map(float, c1)), float(r), shank)
                at = lambda z: removed((q[0], q[1], F(z)), c0, c1, r, shank)
                if seg is None:
                    assert not at(-100) and not at(0) and not at(100)
                    continue
                lo, hi = seg
                assert not at(lo - EPS)
                if shank:
                    assert hi == inf and at(1000) and at(lo + EPS)
                    continue
                assert not at(hi + EPS)
                if hi - lo > 1e-6:  # not a tangent line, which meets the tool in one point
                    assert at(lo + EPS) and at(hi - EPS)


def test_cut_against_exact_membership():
    rng = random.Random(29)
    for _ in range(4):
        m = DexelModel.box(9, 9, 0.5, -2.0, 2.0)
        r = F(rng.randint(3, 6), 4)
        path = [tuple(F(rng.randint(0, 16), 4) for _ in range(2)) + (F(rng.randint(-8, 8), 4),) for _ in range(3)]
        shank = rng.random() < 0.5
        for c0, c1 in zip(path, path[1:]):
            m.cut_ball_move(tuple(map(float, c0)), tuple(map(float, c1)), float(r), shank)
        for i in range(9):
            for j in range(9):
                q = (F(i, 2), F(j, 2))
                for lo, hi in m.rays[i][j]:
                    assert valid(m.rays[i][j])
                    mid = (F(lo) + F(hi)) / 2
                    gone = any(removed((q[0], q[1], mid), a, b, r, shank) for a, b in zip(path, path[1:]))
                    assert not gone
                    for e, d in ((lo, -EPS), (hi, EPS)):
                        if -2.0 < e < 2.0:  # an end made by the tool: just outside is removed
                            p = (q[0], q[1], F(e + d))
                            assert any(removed(p, a, b, r, shank) for a, b in zip(path, path[1:]))


def test_undercut_needs_two_intervals():
    # a ball with no shank moves inside the block: a closed tunnel
    m = DexelModel.box(5, 3, 1.0, 0.0, 4.0)
    m.cut_ball_move((0.0, 1.0, 2.0), (4.0, 1.0, 2.0), 1.0, shank=False)
    assert m.rays[2][1] == [(0.0, 1.0), (3.0, 4.0)]
    assert m.max_intervals() == 2
    # the ray at distance r from the path is only touched at z = 2: a cut of length zero
    assert m.rays[2][0] == [(0.0, 4.0)]
    # the same move with a shank opens the tunnel to the top
    m2 = DexelModel.box(5, 3, 1.0, 0.0, 4.0)
    m2.cut_ball_move((0.0, 1.0, 2.0), (4.0, 1.0, 2.0), 1.0, shank=True)
    assert m2.rays[2][1] == [(0.0, 1.0)]


def test_box_volume_and_model_boolean():
    a = DexelModel.box(4, 4, 1.0, 0.0, 3.0)
    b = DexelModel.box(4, 4, 1.0, 1.0, 5.0)
    assert a.volume() == 48.0
    assert a.boolean(b, lambda x, y: x or y).volume() == 16 * 5.0
    assert a.boolean(b, lambda x, y: x and y).volume() == 16 * 2.0
    assert a.boolean(b, lambda x, y: x and not y).volume() == 16 * 1.0
    assert a.inside(0, 0, 0.0) and not a.inside(0, 0, 3.5)
