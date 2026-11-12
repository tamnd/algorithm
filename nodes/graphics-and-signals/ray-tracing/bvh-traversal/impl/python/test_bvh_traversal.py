# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bvh-traversal/. The authors are listed in prov/2KJ4A7.jsonl.

import math
import random
from fractions import Fraction

from bvh_traversal import Counts, Node, any_hit, closest_hit, hit_triangle


def box_of(tris, ids):
    lo = tuple(min(p[a] for i in ids for p in tris[i]) for a in range(3))
    hi = tuple(max(p[a] for i in ids for p in tris[i]) for a in range(3))
    return lo, hi


def build_median(tris, leaf_size=1):
    """Object median build on the longest centroid axis, depth-first layout (a test fixture)."""
    refs = list(range(len(tris)))
    cen = [tuple(sum(p[a] for p in t) for a in range(3)) for t in tris]
    nodes = []
    stack = [(0, len(tris), -1, False)]
    while stack:
        first, count, parent, is_right = stack.pop()
        part = refs[first : first + count]
        idx = len(nodes)
        nodes.append(Node(*box_of(tris, part), first=first, count=count))
        if parent >= 0:
            setattr(nodes[parent], "right" if is_right else "left", idx)
        ext = [max(cen[r][a] for r in part) - min(cen[r][a] for r in part) for a in range(3)]
        axis = max(range(3), key=lambda a: ext[a])
        if count <= leaf_size or ext[axis] == 0:
            continue
        part.sort(key=lambda r: cen[r][axis])
        refs[first : first + count] = part
        nodes[idx].count = 0
        half = count // 2
        stack.append((first + half, count - half, idx, True))
        stack.append((first, half, idx, False))
    return nodes, refs


def brute_closest(tris, o, d):
    ts = [t for t in (hit_triangle(tr, o, d) for tr in tris) if t is not None]
    return min(ts) if ts else None


def brute_any(tris, o, d, tmax):
    return any(t is not None and t <= tmax for t in (hit_triangle(tr, o, d) for tr in tris))


def walls():
    return [((c, 0, 0), (c, 4, 0), (c, 0, 4)) for c in (1, 3, 5, 7)]


def test_example() -> None:
    tris = walls()
    nodes, refs = build_median(tris)
    assert [(nd.lo[0], nd.hi[0]) for nd in nodes] == [(1, 7), (1, 3), (1, 1), (3, 3), (5, 7), (5, 5), (7, 7)]
    c = Counts()
    assert closest_hit(nodes, refs, tris, (10, 1, 1), (-1, 0, 0), c) == (3, 3)
    assert (c.pops, c.boxes, c.prims) == ([0, 4, 6], 5, 1)
    c = Counts()
    assert closest_hit(nodes, refs, tris, (0, 1, 1), (1, 0, 0), c) == (1, 0)
    assert (c.pops, c.prims) == ([0, 1, 2], 1)
    c = Counts()
    assert any_hit(nodes, refs, tris, (10, 1, 1), (-1, 0, 0), 2, c) is False
    assert c.prims == 0
    assert any_hit(nodes, refs, tris, (10, 1, 1), (-1, 0, 0), 3) is True


def test_worst_case_visits_every_node() -> None:
    for n in (1, 2, 5, 16, 33):
        tris = [((0, 0, z), (10, 0, z), (10, 10, z)) for z in range(n)]
        nodes, refs = build_median(tris)
        c = Counts()
        assert closest_hit(nodes, refs, tris, (1, 9, -1), (0, 0, 1), c) is None
        assert c.nodes == 2 * n - 1 and c.prims == n and c.boxes == 2 * n - 1


def test_edges() -> None:
    tris = walls()
    nodes, refs = build_median(tris)
    assert closest_hit(nodes, refs, tris, (3, 1, 1), (1, 0, 0)) == (0, 1)  # origin on a triangle
    assert closest_hit(nodes, refs, tris, (0, 1, 1), (-1, 0, 0)) is None  # box behind the ray
    assert closest_hit(nodes, refs, tris, (0, 5, 5), (1, 0, 0)) is None  # misses the root box
    assert closest_hit(nodes, refs, tris, (2, 1, 1), (0, 1, 0)) is None  # parallel, between walls
    assert closest_hit(nodes, refs, tris, (3, -1, 1), (0, 1, 0)) is None  # in the plane of a wall


def test_against_brute_force() -> None:
    rng = random.Random(7)
    for _ in range(150):
        n = rng.randint(1, 14)
        tris = [tuple(tuple(rng.randint(0, 16) for _ in range(3)) for _ in range(3)) for _ in range(n)]
        nodes, refs = build_median(tris, rng.randint(1, 3))
        for _ in range(5):
            o = [rng.randint(-4, 20) for _ in range(3)]
            if rng.random() < 0.5:
                a, b, cc = rng.choice(tris)
                d = [a[i] + b[i] + cc[i] - 3 * o[i] for i in range(3)]
            else:
                d = [rng.randint(-3, 3) for _ in range(3)]
            if rng.random() < 0.3:
                d[rng.randrange(3)] = 0
            if rng.random() < 0.3:
                k = rng.randrange(3)
                o[k] = rng.choice(rng.choice(tris))[k]
            if all(x == 0 for x in d):
                d = [0, 0, 1]
            o, d = tuple(o), tuple(d)
            got = closest_hit(nodes, refs, tris, o, d)
            want = brute_closest(tris, o, d)
            assert (got[0] if got else None) == want
            if got:
                assert hit_triangle(tris[got[1]], o, d) == got[0]
            tmax = rng.choice([math.inf, Fraction(rng.randint(0, 10), rng.randint(1, 3))])
            assert any_hit(nodes, refs, tris, o, d, tmax) == brute_any(tris, o, d, tmax)
