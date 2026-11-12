# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bvh-construction/. The authors are listed in prov/TPVQDP.jsonl.

import math
import random
from fractions import Fraction

from bvh_construction import any_hit, area, bin_of, build, closest_hit, hit_triangle, sah_cost, tri_box, union


def cube_tri(c):
    """A triangle with the box [c, c+1] x [0, 1] x [0, 1] and centroid x = c + 1/3."""
    return ((c, 0, 0), (c + 1, 1, 0), (c, 0, 1))


def box_of(tris, ids):
    b = None
    for i in ids:
        b = union(b, tri_box(tris[i]))
    return b


def leaves_of(nodes, refs):
    return [sorted(refs[nd.first : nd.first + nd.count]) for nd in nodes if nd.left < 0]


def direct_best(tris, ids, bins):
    """Least A(L) N(L) + A(R) N(R) over all axes and bin boundaries, each side boxed from scratch."""
    cen = {i: [sum(p[a] for p in tris[i]) for a in range(3)] for i in ids}
    best = None
    for a in range(3):
        lo = min(cen[i][a] for i in ids)
        hi = max(cen[i][a] for i in ids)
        if lo == hi:
            continue
        for j in range(1, bins):
            left = [i for i in ids if bin_of(cen[i][a], lo, hi, bins) < j]
            right = [i for i in ids if i not in left]
            if left and right:
                s = area(box_of(tris, left)) * len(left) + area(box_of(tris, right)) * len(right)
                if best is None or s < best[0]:
                    best = (s, a, j, sorted(left), sorted(right))
    return best


def test_example() -> None:
    tris = [cube_tri(c) for c in (0, 1, 2, 3, 4, 18)]
    log = []
    nodes, refs = build(tris, bins=4, max_leaf=4, log=log)
    assert [(i, a, j) for i, a, j, _ in log] == [(0, 0, 1), (1, 0, 2), (3, 0, 1)]
    assert [c for *_, c in log] == [1 + Fraction(116, 78), 1 + Fraction(62, 22), 1 + Fraction(26, 14)]
    assert leaves_of(nodes, refs) == [[0, 1], [2], [3, 4], [5]]
    # the object median split {0,1,2} | {3,4,5} costs more at the root
    median = area(box_of(tris, [0, 1, 2])) * 3 + area(box_of(tris, [3, 4, 5])) * 3
    assert 1 + Fraction(median, 78) == 1 + Fraction(240, 78)


def check_tree(tris, nodes, refs, bins, max_leaf, log) -> None:
    n = len(tris)
    assert sorted(r for lf in leaves_of(nodes, refs) for r in lf) == list(range(n))  # each triangle in one leaf
    split = {i: (a, j, c) for i, a, j, c in log}
    stack = [(0, list(range(n)))]
    while stack:
        i, ids = stack.pop()
        nd = nodes[i]
        assert (nd.lo, nd.hi) == box_of(tris, ids)  # the box is the tight union of its triangles
        if nd.left >= 0:
            a, j, c = split[i]
            s, ba, bj, left, right = direct_best(tris, ids, bins)
            assert (a, j) == (ba, bj)
            ab = area(box_of(tris, ids))
            if ab > 0:
                assert c == 1 + Fraction(s, ab)
            lids = sorted(refs[nodes[nd.left].first : nodes[nd.left].first + nodes[nd.left].count]) if nodes[nd.left].left < 0 else None
            if lids is not None:
                assert lids == left
            for ch in (nodes[nd.left], nodes[nd.right]):
                assert all(ch.lo[k] >= nd.lo[k] and ch.hi[k] <= nd.hi[k] for k in range(3))
            stack.append((nd.left, left))
            stack.append((nd.right, right))
        else:
            assert sorted(refs[nd.first : nd.first + nd.count]) == sorted(ids)
            cen = [[sum(p[a] for p in tris[r]) for a in range(3)] for r in ids]
            if len(ids) > 1 and any(c != cen[0] for c in cen):
                s, *_ = direct_best(tris, ids, bins)
                ab = area(box_of(tris, ids))
                assert len(ids) <= max_leaf and (ab == 0 or len(ids) <= 1 + Fraction(s, ab))


def random_ray(rng, tris):
    o = [rng.randint(-4, 20) for _ in range(3)]
    if rng.random() < 0.5:
        a, b, c = rng.choice(tris)
        d = [a[i] + b[i] + c[i] - 3 * o[i] for i in range(3)]
    else:
        d = [rng.randint(-3, 3) for _ in range(3)]
    if rng.random() < 0.3:
        d[rng.randrange(3)] = 0
    if rng.random() < 0.3:
        k = rng.randrange(3)
        o[k] = rng.choice(rng.choice(tris))[k]
    if all(x == 0 for x in d):
        d = [0, 0, 1]
    return tuple(o), tuple(d)


def test_random_scenes() -> None:
    rng = random.Random(11)
    for _ in range(120):
        n = rng.randint(1, 24)
        tris = [tuple(tuple(rng.randint(0, 16) for _ in range(3)) for _ in range(3)) for _ in range(n)]
        bins, max_leaf = rng.choice([2, 4, 8, 16]), rng.randint(1, 4)
        log = []
        nodes, refs = build(tris, bins=bins, max_leaf=max_leaf, log=log)
        check_tree(tris, nodes, refs, bins, max_leaf, log)
        for _ in range(5):
            o, d = random_ray(rng, tris)
            ts = [t for t in (hit_triangle(tr, o, d) for tr in tris) if t is not None]
            got = closest_hit(nodes, refs, tris, o, d)
            assert (got[0] if got else None) == (min(ts) if ts else None)
            tmax = rng.choice([math.inf, Fraction(rng.randint(0, 10), rng.randint(1, 3))])
            assert any_hit(nodes, refs, tris, o, d, tmax) == any(t <= tmax for t in ts)


def test_degenerate_inputs() -> None:
    same = [cube_tri(0)] * 7  # all centroids equal: one leaf, whatever max_leaf is
    nodes, refs = build(same, max_leaf=2)
    assert len(nodes) == 1 and nodes[0].count == 7
    line = [((c, 0, 0), (c + 1, 0, 0), (c + 2, 0, 0)) for c in range(9)]  # boxes of area 0
    nodes, refs = build(line, max_leaf=2)
    assert sorted(r for lf in leaves_of(nodes, refs) for r in lf) == list(range(9))
    assert all(nd.count <= 2 for nd in nodes if nd.left < 0)


def test_worst_case_depth() -> None:
    # centroids at powers of two: most of them fall into bin 0, so each split peels off a few
    for n in (40, 80):
        tris = [cube_tri(2**i) for i in range(n)]
        nodes, refs = build(tris, bins=16, max_leaf=1)
        depth = {0: 0}
        for i, nd in enumerate(nodes):
            if nd.left >= 0:
                depth[nd.left] = depth[nd.right] = depth[i] + 1
        assert max(depth.values()) >= n // 4 - 1  # the depth grows linearly with n
    assert sah_cost(nodes) > 0
