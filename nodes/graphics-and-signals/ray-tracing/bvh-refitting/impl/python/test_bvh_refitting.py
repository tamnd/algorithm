# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bvh-refitting/. The authors are listed in prov/5ASM9T.jsonl.

import copy
import math
import random
from fractions import Fraction

from bvh_refitting import (
    any_hit,
    build,
    closest_hit,
    hit_triangle,
    needs_rebuild,
    parents_and_leaves,
    refit,
    refit_moved,
    sah_cost,
    tri_box,
    union,
)


def cube_tri(c):
    """A triangle whose box is [c, c + 1] x [0, 1] x [0, 1], with area 6."""
    return ((c, 0, 0), (c + 1, 1, 0), (c, 0, 1))


def boxes_of(nodes):
    return [(nd.lo, nd.hi) for nd in nodes]


def below(nodes, refs, i):
    out, stack = [], [i]
    while stack:
        nd = nodes[stack.pop()]
        if nd.left < 0:
            out += refs[nd.first : nd.first + nd.count]
        else:
            stack += [nd.left, nd.right]
    return out


def tight(nodes, refs, tris, i):
    box = None
    for r in below(nodes, refs, i):
        box = union(box, tri_box(tris[r]))
    return box


def test_example_swap() -> None:
    tris = [cube_tri(c) for c in (0, 1, 10, 11)]
    nodes, refs = build(tris, max_leaf=1)
    leaves = sorted(sorted(below(nodes, refs, i)) for i in (nodes[0].left, nodes[0].right))
    assert leaves == [[0, 1], [2, 3]]
    built = sah_cost(nodes)
    assert built == Fraction(94, 50)
    moved = [cube_tri(c) for c in (0, 10, 1, 11)]  # triangles 1 and 2 change places
    refit(nodes, refs, moved)
    assert [(nodes[i].lo, nodes[i].hi) for i in (nodes[0].left, nodes[0].right)] in (
        [((0, 0, 0), (11, 1, 1)), ((1, 0, 0), (12, 1, 1))],
        [((1, 0, 0), (12, 1, 1)), ((0, 0, 0), (11, 1, 1))],
    )
    assert sah_cost(nodes) == Fraction(166, 50)
    fresh, _ = build(moved, max_leaf=1)
    assert sah_cost(fresh) == Fraction(94, 50)
    assert needs_rebuild(nodes, built, Fraction(3, 2)) and not needs_rebuild(nodes, built, 2)


def random_scene(rng, n):
    return [tuple(tuple(rng.randint(0, 16) for _ in range(3)) for _ in range(3)) for _ in range(n)]


def move(rng, tris, step):
    out = []
    for t in tris:
        s = [rng.randint(-step, step) for _ in range(3)]
        out.append(tuple(tuple(p[a] + s[a] + rng.randint(-1, 1) for a in range(3)) for p in t))
    return out


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


def test_refit_without_motion_gives_the_built_boxes() -> None:
    rng = random.Random(1)
    for _ in range(60):
        tris = random_scene(rng, rng.randint(1, 25))
        nodes, refs = build(tris, max_leaf=rng.choice([1, 2, 4]))
        before = boxes_of(nodes)
        refit(nodes, refs, tris)
        assert boxes_of(nodes) == before


def test_random_motion() -> None:
    rng = random.Random(2)
    for _ in range(100):
        n = rng.randint(1, 25)
        tris = random_scene(rng, n)
        nodes, refs = build(tris, max_leaf=rng.choice([1, 2, 4]))
        shape = [(nd.left, nd.right, nd.first, nd.count) for nd in nodes]
        parent, leaf_of = parents_and_leaves(nodes, refs)
        partial = copy.deepcopy(nodes)
        new = move(rng, tris, rng.choice([0, 1, 3, 8]))
        k = rng.randint(0, n)
        moved_ids = rng.sample(range(n), k)
        partial_tris = list(tris)
        for r in moved_ids:
            partial_tris[r] = new[r]
        refit(nodes, refs, new)
        assert [(nd.left, nd.right, nd.first, nd.count) for nd in nodes] == shape  # the shape is kept
        for i in range(len(nodes)):  # each box is the tight box of the triangles below it
            assert (nodes[i].lo, nodes[i].hi) == tight(nodes, refs, new, i)
        fresh, _ = build(new)
        assert (nodes[0].lo, nodes[0].hi) == (fresh[0].lo, fresh[0].hi)  # the root equals a fresh build's root
        refit_moved(partial, refs, partial_tris, moved_ids, parent, leaf_of)
        full = copy.deepcopy(partial)
        refit(full, refs, partial_tris)
        assert boxes_of(partial) == boxes_of(full)  # refitting only the moved paths gives the full refit
        for _ in range(6):
            o, d = random_ray(rng, new)
            ts = [t for t in (hit_triangle(tr, o, d) for tr in new) if t is not None]
            got = closest_hit(nodes, refs, new, o, d)
            assert (got[0] if got else None) == (min(ts) if ts else None)
            tmax = rng.choice([math.inf, Fraction(rng.randint(0, 10), rng.randint(1, 3))])
            assert any_hit(nodes, refs, new, o, d, tmax) == any(t <= tmax for t in ts)


def test_quality_decays_under_motion() -> None:
    rng = random.Random(3)
    tris = []
    for _ in range(60):  # small triangles spread over [0, 43]^3
        base = [rng.randint(0, 40) for _ in range(3)]
        tris.append(tuple(tuple(base[a] + rng.randint(0, 3) for a in range(3)) for _ in range(3)))
    nodes, refs = build(tris, max_leaf=2)
    built = sah_cost(nodes)
    ratios = []
    for _ in range(12):
        tris = move(rng, tris, 3)
        refit(nodes, refs, tris)
        fresh, _ = build(tris, max_leaf=2)
        ratios.append(sah_cost(nodes) / sah_cost(fresh))
    assert ratios[-1] > Fraction(7, 5) and ratios[-1] > ratios[0]  # about 1.08 after one step, 1.53 after 12
    assert not needs_rebuild(nodes, built, 2) and needs_rebuild(nodes, built, Fraction(3, 2))  # 11.84 against 6.48
