# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bounding-interval-hierarchy/. The authors are listed in prov/P0KNZR.jsonl.

import math
import random
from fractions import Fraction

from bounding_interval_hierarchy import any_hit, build, closest_hit, hit_triangle, implicit_boxes, tri_box

EXAMPLE = [
    ((0, 0, 0), (3, 1, 0), (0, 0, 1)),  # A: box [0, 3] in x
    ((7, 0, 0), (2, 1, 0), (7, 0, 1)),  # B: box [2, 7] in x
    ((6, 0, 0), (9, 1, 0), (6, 0, 1)),  # C: box [6, 9] in x
    ((12, 0, 0), (16, 1, 0), (12, 0, 1)),  # D: box [12, 16] in x
]


def leaves(bih, i):
    out, stack = [], [i]
    while stack:
        nd = bih.nodes[stack.pop()]
        if nd.axis < 0:
            out += bih.refs[nd.first : nd.first + nd.count]
        else:
            stack += [nd.left, nd.right]
    return out


def test_example() -> None:
    bih = build(EXAMPLE)
    root = bih.nodes[0]
    assert (root.axis, root.lclip, root.rclip) == (0, 9, 12)
    assert sorted(leaves(bih, root.left)) == [0, 1, 2] and leaves(bih, root.right) == [3]
    n1 = bih.nodes[root.left]
    assert (n1.axis, n1.lclip, n1.rclip) == (0, 3, 2)  # the children overlap in [2, 3]
    n2 = bih.nodes[n1.right]
    assert (n2.axis, n2.lclip, n2.rclip) == (0, 7, 6)
    assert leaves(bih, n1.left) == [0] and leaves(bih, n2.left) == [1] and leaves(bih, n2.right) == [2]
    o, d = (-1, Fraction(9, 10), Fraction(1, 20)), (1, 0, 0)
    assert [hit_triangle(t, o, d) for t in EXAMPLE] == [Fraction(37, 10), Fraction(7, 2), Fraction(97, 10), Fraction(83, 5)]
    assert closest_hit(bih, EXAMPLE, o, d) == (Fraction(7, 2), 1)  # A is met first in the walk, B is nearer


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
    rng = random.Random(5)
    for trial in range(150):
        n = rng.randint(1, 25)
        if trial % 3 == 0:  # small triangles
            tris = []
            for _ in range(n):
                b = [rng.randint(0, 14) for _ in range(3)]
                tris.append(tuple(tuple(b[a] + rng.randint(0, 2) for a in range(3)) for _ in range(3)))
        else:
            tris = [tuple(tuple(rng.randint(0, 16) for _ in range(3)) for _ in range(3)) for _ in range(n)]
        if rng.random() < 0.2:
            tris = tris + tris[: rng.randint(1, n)]  # equal boxes
            n = len(tris)
        bih = build(tris, max_leaf=rng.choice([1, 2, 3]))
        assert sorted(bih.refs) == list(range(n))
        found = leaves(bih, 0)
        assert sorted(found) == list(range(n))  # each triangle is in exactly one leaf
        assert len(bih.nodes) <= 2 * n - 1
        boxes = implicit_boxes(bih)
        for i, nd in enumerate(bih.nodes):
            lo, hi = boxes[i]
            for r in leaves(bih, i):  # every triangle lies in the implicit box of each node above it
                blo, bhi = tri_box(tris[r])
                assert all(lo[a] <= blo[a] and bhi[a] <= hi[a] for a in range(3))
            if nd.axis >= 0:  # the clip planes are tight
                assert nd.lclip == max(tri_box(tris[r])[1][nd.axis] for r in leaves(bih, nd.left))
                assert nd.rclip == min(tri_box(tris[r])[0][nd.axis] for r in leaves(bih, nd.right))
        for _ in range(6):
            o, d = random_ray(rng, tris)
            ts = [t for t in (hit_triangle(tr, o, d) for tr in tris) if t is not None]
            got = closest_hit(bih, tris, o, d)
            assert (got[0] if got else None) == (min(ts) if ts else None)
            tmax = rng.choice([math.inf, Fraction(rng.randint(0, 10), rng.randint(1, 3))])
            assert any_hit(bih, tris, o, d, tmax) == any(t <= tmax for t in ts)


def test_close_centers_need_many_halvings() -> None:
    e = Fraction(1, 64)  # the first two boxes differ by a shift of 1/64 in x
    tris = [((0, 0, 0), (1, 1, 1), (0, 1, 0)), ((e, 0, 0), (1 + e, 1, 1), (e, 1, 0)), ((1023, 0, 0), (1024, 1, 1), (1023, 1, 0))]
    bih = build(tris)
    assert sorted(leaves(bih, 0)) == [0, 1, 2] and len(bih.nodes) == 5
    assert [nd.count for nd in bih.nodes if nd.axis < 0] == [1, 1, 1]
    o, d = (Fraction(1, 2), Fraction(1, 2), -2), (0, 0, 1)
    ts = [t for t in (hit_triangle(tr, o, d) for tr in tris) if t is not None]
    got = closest_hit(bih, tris, o, d)
    assert ts and got is not None and got[0] == min(ts)
