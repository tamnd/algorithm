# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spatial-splits/. The authors are listed in prov/C37NSZ.jsonl.

import math
import random
from fractions import Fraction

from spatial_splits import any_hit, area, build, clip_box, closest_hit, hit_triangle, sah_cost, tri_box


def example():
    return [((0, 0, 0), (16, 8, 0), (16, 8, 1)), ((0, 0, 0), (2, 0, 0), (0, 2, 1)), ((14, 8, 0), (16, 8, 0), (16, 6, 1))]


def inside(lo, hi, LO, HI):
    return all(LO[i] <= lo[i] and hi[i] <= HI[i] for i in range(3))


def test_example() -> None:
    tris = example()
    log = []
    nodes, refs = build(tris, bins=4, max_leaf=1, alpha=Fraction(0), log=log)
    assert area((nodes[0].lo, nodes[0].hi)) == 304
    assert log[0] == (0, "spatial", 1 + Fraction(352, 304))
    assert (nodes[1].lo, nodes[1].hi) == ((0, 0, 0), (8, 4, 1))
    assert (nodes[4].lo, nodes[4].hi) == ((8, 4, 0), (16, 8, 1))
    assert sorted(r[0] for r in refs) == [0, 0, 1, 2]  # the long triangle is in two leaves
    assert [r[1:] for r in refs if r[0] == 0] == [((0, 0, 0), (8, 4, Fraction(1, 2))), ((8, 4, 0), (16, 8, 1))]
    assert sah_cost(nodes) == Fraction(169, 76)
    log = []
    nodes, refs = build(tris, bins=4, max_leaf=1, alpha=Fraction(1), log=log)  # spatial splits off
    assert log[0] == (0, "object", 1 + Fraction(624, 304))
    assert len(refs) == 3 and sah_cost(nodes) == Fraction(59, 19)


def check(tris, nodes, refs, log, rng) -> None:
    for nd in nodes:
        if nd.left >= 0:
            for ch in (nodes[nd.left], nodes[nd.right]):
                assert inside(ch.lo, ch.hi, nd.lo, nd.hi)
        else:
            for t, lo, hi in refs[nd.first : nd.first + nd.count]:
                assert inside(lo, hi, nd.lo, nd.hi)  # every reference box is inside its leaf box
                assert inside(lo, hi, *tri_box(tris[t]))
                assert clip_box(tris[t], lo, hi) == (lo, hi)  # and is tight around its piece
    for i, kind, cost in log:  # the logged cost is the SAH cost of the children that were made
        nd, a, b = nodes[i], nodes[nodes[i].left], nodes[nodes[i].right]
        want = 1 + Fraction(area((a.lo, a.hi)) * a.size + area((b.lo, b.hi)) * b.size) / area((nd.lo, nd.hi))
        assert cost == want
        if kind == "object":
            assert a.size + b.size == nd.size
        else:
            assert a.size < nd.size and b.size < nd.size
    for k, tr in enumerate(tris):  # the pieces cover the triangle
        pieces = [(lo, hi) for t, lo, hi in refs if t == k]
        assert pieces
        for _ in range(4):
            u, v = Fraction(rng.randint(0, 6)), Fraction(rng.randint(0, 6))
            if u + v > 6:
                u, v = 6 - u, 6 - v
            p = tuple(tr[0][i] + (u * (tr[1][i] - tr[0][i]) + v * (tr[2][i] - tr[0][i])) / 6 for i in range(3))
            assert any(inside(p, p, lo, hi) for lo, hi in pieces)


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
    rng = random.Random(3)
    split_seen = 0
    for trial in range(100):
        n = rng.randint(1, 12)
        tris = []
        for _ in range(n):
            if rng.random() < 0.3:  # a long triangle across the scene
                tris.append(tuple(tuple(rng.randint(0, 16) for _ in range(3)) for _ in range(3)))
            else:
                c = [rng.randint(0, 14) for _ in range(3)]
                tris.append(tuple(tuple(c[i] + rng.randint(0, 2) for i in range(3)) for _ in range(3)))
        root = (tuple(min(p[a] for t in tris for p in t) for a in range(3)), tuple(max(p[a] for t in tris for p in t) for a in range(3)))
        if area(root) == 0:
            continue
        log = []
        nodes, refs = build(tris, bins=rng.choice([2, 4, 8]), max_leaf=rng.randint(1, 3), alpha=Fraction(rng.choice([0, 0, 1]), 100), log=log)
        split_seen += len(refs) > n
        check(tris, nodes, refs, log, rng)
        for _ in range(6):
            o, d = random_ray(rng, tris)
            ts = [t for t in (hit_triangle(tr, o, d) for tr in tris) if t is not None]
            got = closest_hit(nodes, refs, tris, o, d)
            assert (got[0] if got else None) == (min(ts) if ts else None)
            tmax = rng.choice([math.inf, Fraction(rng.randint(0, 10), rng.randint(1, 3))])
            assert any_hit(nodes, refs, tris, o, d, tmax) == any(t <= tmax for t in ts)
    assert split_seen >= 5  # some scenes did duplicate references


def test_alpha_one_is_an_object_bvh() -> None:
    rng = random.Random(8)
    for _ in range(30):
        tris = [tuple(tuple(rng.randint(0, 16) for _ in range(3)) for _ in range(3)) for _ in range(rng.randint(2, 10))]
        log = []
        nodes, refs = build(tris, alpha=Fraction(1), log=log)
        assert sorted(r[0] for r in refs) == list(range(len(tris)))
        assert all(kind == "object" for _, kind, _ in log)
