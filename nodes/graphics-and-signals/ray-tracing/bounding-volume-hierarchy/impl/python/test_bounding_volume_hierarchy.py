# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bounding-volume-hierarchy/. The authors are listed in prov/NZ1MVD.jsonl.

import math
import random
from fractions import Fraction

from bounding_volume_hierarchy import any_hit, build, closest_hit, hit_triangle, refit, tri_box, union


def brute_closest(tris, o, d):
    ts = [t for t in (hit_triangle(tr, o, d) for tr in tris) if t is not None]
    return min(ts) if ts else None


def brute_any(tris, o, d, tmax):
    return any(t is not None and t <= tmax for t in (hit_triangle(tr, o, d) for tr in tris))


def random_scene(rng, n, size=16):
    return [tuple(tuple(rng.randint(0, size) for _ in range(3)) for _ in range(3)) for _ in range(n)]


def random_ray(rng, tris):
    o = [rng.randint(-4, 20) for _ in range(3)]
    if rng.random() < 0.5:
        a, b, c = rng.choice(tris)
        d = [a[i] + b[i] + c[i] - 3 * o[i] for i in range(3)]  # aim at a centroid
    else:
        d = [rng.randint(-3, 3) for _ in range(3)]
    if rng.random() < 0.3:
        d[rng.randrange(3)] = 0  # parallel to a slab
    if rng.random() < 0.3:
        a = rng.randrange(3)
        o[a] = rng.choice(rng.choice(tris))[a]  # origin on a plane of some box
    if all(x == 0 for x in d):
        d = [1, 0, 0]
    return tuple(o), tuple(d)


def check_structure(nodes, refs, tris):
    seen = []
    stack = [0]
    while stack:
        i = stack.pop()
        nd = nodes[i]
        if nd.left < 0:
            assert nd.count > 0
            part = refs[nd.first : nd.first + nd.count]
            seen.extend(part)
            box = tri_box(tris[part[0]])
            for r in part[1:]:
                box = union(box, tri_box(tris[r]))
        else:
            assert nd.left > i and nd.right > i  # depth-first order
            a, b = nodes[nd.left], nodes[nd.right]
            box = union((a.lo, a.hi), (b.lo, b.hi))
            stack += [nd.left, nd.right]
        assert (nd.lo, nd.hi) == box  # each box is the tight union of its children
    assert sorted(seen) == list(range(len(tris)))  # each triangle in exactly one leaf


def test_example() -> None:
    tris = [
        ((0, 0, 0), (2, 0, 0), (0, 2, 0)),
        ((3, 0, 0), (5, 0, 0), (3, 2, 0)),
        ((6, 0, 0), (8, 0, 0), (6, 2, 0)),
        ((9, 0, 0), (11, 0, 0), (9, 2, 0)),
    ]
    nodes, refs = build(tris, leaf_size=1)
    assert len(nodes) == 7
    assert (nodes[0].lo, nodes[0].hi) == ((0, 0, 0), (11, 2, 0))
    assert [(nd.lo[0], nd.hi[0]) for nd in nodes] == [(0, 11), (0, 5), (0, 2), (3, 5), (6, 11), (6, 8), (9, 11)]
    check_structure(nodes, refs, tris)
    assert closest_hit(nodes, refs, tris, (8, 1, 5), (0, 0, -1)) is None  # inside a box, misses the triangle
    assert closest_hit(nodes, refs, tris, (6, 1, 5), (0, 0, -1)) == (5, 2)
    assert closest_hit(nodes, refs, tris, (1, 1, -2), (0, 0, 1)) == (2, 0)
    assert closest_hit(nodes, refs, tris, (-1, 1, 0), (1, 0, 0)) is None  # in the plane of all triangles
    assert any_hit(nodes, refs, tris, (6, 1, 5), (0, 0, -1), 4) is False


def test_edges() -> None:
    one = [((0, 0, 0), (1, 0, 0), (0, 1, 0))]
    nodes, refs = build(one)
    assert len(nodes) == 1 and refs == [0]
    assert closest_hit(nodes, refs, one, (0, 0, 1), (0, 0, -1)) == (1, 0)
    same = [((0, 0, 0), (3, 0, 0), (0, 3, 0))] * 5  # equal centroids: one leaf
    nodes, refs = build(same)
    assert len(nodes) == 1
    flat = [((0, 0, z), (4, 0, z), (0, 4, z)) for z in range(6)]  # flat boxes
    nodes, refs = build(flat)
    check_structure(nodes, refs, flat)
    assert closest_hit(nodes, refs, flat, (1, 1, 10), (0, 0, -1)) == (5, 5)


def test_against_brute_force() -> None:
    rng = random.Random(5)
    for _ in range(150):
        tris = random_scene(rng, rng.randint(1, 12))
        nodes, refs = build(tris, leaf_size=rng.randint(1, 3))
        check_structure(nodes, refs, tris)
        for _ in range(5):
            o, d = random_ray(rng, tris)
            got = closest_hit(nodes, refs, tris, o, d)
            want = brute_closest(tris, o, d)
            assert (got and got[0]) == want
            if got is not None:
                assert hit_triangle(tris[got[1]], o, d) == got[0]
            tmax = rng.choice([math.inf, Fraction(rng.randint(0, 8), rng.randint(1, 3))])
            assert any_hit(nodes, refs, tris, o, d, tmax) == brute_any(tris, o, d, tmax)


def test_refit_matches_fresh_bounds() -> None:
    rng = random.Random(6)
    for _ in range(150):
        tris = random_scene(rng, rng.randint(1, 12))
        nodes, refs = build(tris)
        moved = [tuple(tuple(p[i] + rng.randint(-3, 3) for i in range(3)) for p in t) for t in tris]
        refit(nodes, refs, moved)
        check_structure(nodes, refs, moved)
        fresh, _ = build(moved)
        assert (nodes[0].lo, nodes[0].hi) == (fresh[0].lo, fresh[0].hi)
        for _ in range(4):
            o, d = random_ray(rng, moved)
            got = closest_hit(nodes, refs, moved, o, d)
            assert (got and got[0]) == brute_closest(moved, o, d)
