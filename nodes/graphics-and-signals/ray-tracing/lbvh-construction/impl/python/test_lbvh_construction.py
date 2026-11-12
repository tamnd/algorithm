# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lbvh-construction/. The authors are listed in prov/PTNB7Y.jsonl.

import math
import random
from fractions import Fraction

from lbvh_construction import (
    any_hit,
    build,
    closest_hit,
    hit_triangle,
    karras,
    morton3,
    quantize,
    radix_sort,
    radix_tree_reference,
    tri_box,
)


def morton_reference(x, y, z):
    bits = "".join(f"{x:010b}"[k] + f"{y:010b}"[k] + f"{z:010b}"[k] for k in range(10))
    return int(bits, 2)


def test_morton_and_quantize() -> None:
    rng = random.Random(1)
    for _ in range(2000):
        x, y, z = (rng.randrange(1024) for _ in range(3))
        assert morton3(x, y, z) == morton_reference(x, y, z)
    assert morton3(1, 0, 0) == 4 and morton3(0, 1, 0) == 2 and morton3(0, 0, 1) == 1
    assert morton3(1023, 1023, 1023) == 2**30 - 1
    assert quantize(0, 0, 9) == 0 and quantize(9, 0, 9) == 1023 and quantize(3, 3, 3) == 0
    assert quantize(Fraction(9, 2), 0, 9) == 512


def test_radix_sort() -> None:
    rng = random.Random(2)
    for _ in range(200):
        bits = rng.randint(1, 40)
        items = [(rng.randrange(2**bits), i) for i in range(rng.randint(0, 60))]
        assert radix_sort(items, bits, rng.choice([1, 4, 8])) == sorted(items)  # stable on equal keys


def test_example_keys() -> None:
    keys = [0b00001, 0b00010, 0b00100, 0b00101, 0b10011, 0b11000, 0b11001, 0b11110]
    h = karras(keys, 5)
    assert h.span[0] == (0, 7) and h.left[0] == (False, 3) and h.right[0] == (False, 4)
    assert [h.span[i] for i in range(7)] == [(0, 7), (0, 1), (2, 3), (0, 3), (4, 7), (5, 7), (5, 6)]
    assert [h.left[i] for i in range(7)] == [(False, 3), (True, 0), (True, 2), (False, 1), (True, 4), (False, 6), (True, 5)]
    assert [h.right[i] for i in range(7)] == [(False, 4), (True, 1), (True, 3), (False, 2), (False, 5), (True, 7), (True, 6)]
    split = {(h.span[i][0], h.span[i][1], (h.left[i][1])) for i in range(7)}
    assert split == radix_tree_reference(keys, 5)


def test_karras_against_top_down() -> None:
    rng = random.Random(3)
    for _ in range(400):
        width = rng.randint(3, 20)
        n = rng.randint(2, min(40, 2**width))
        keys = sorted(rng.sample(range(2**width), n))
        h = karras(keys, width)
        got = set()
        for i in range(n - 1):
            lo, hi = h.span[i]
            assert i in (lo, hi)  # node i covers a range that starts or ends at i
            gamma = h.left[i][1]
            assert h.right[i][1] == gamma + 1 and lo <= gamma < hi
            got.add((lo, hi, gamma))
        assert got == radix_tree_reference(keys, width)
        assert h.span[0] == (0, n - 1)


def leaves_below(bvh, i):
    out, stack = [], [(False, i)]
    while stack:
        is_leaf, j = stack.pop()
        if is_leaf:
            out.append(bvh.order[j])
        else:
            stack += [bvh.tree.left[j], bvh.tree.right[j]]
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


def test_random_scenes() -> None:
    rng = random.Random(4)
    for _ in range(150):
        n = rng.randint(1, 20)
        tris = [tuple(tuple(rng.randint(0, 16) for _ in range(3)) for _ in range(3)) for _ in range(n)]
        if rng.random() < 0.2:
            tris = tris + tris[: rng.randint(1, n)]  # equal centroids, equal Morton codes
            n = len(tris)
        bvh = build(tris)
        assert sorted(bvh.order) == list(range(n))  # each triangle in exactly one leaf
        assert bvh.keys == sorted(bvh.keys) and len(set(bvh.keys)) == n
        if bvh.tree is not None:
            for i in range(n - 1):
                lo, hi = bvh.box[i]
                below = leaves_below(bvh, i)
                assert sorted(below) == sorted(bvh.order[bvh.tree.span[i][0] : bvh.tree.span[i][1] + 1])
                for p in below:  # the box contains each triangle below it, and is tight
                    blo, bhi = tri_box(tris[p])
                    assert all(lo[a] <= blo[a] and bhi[a] <= hi[a] for a in range(3))
                assert lo == tuple(min(tri_box(tris[p])[0][a] for p in below) for a in range(3))
                assert hi == tuple(max(tri_box(tris[p])[1][a] for p in below) for a in range(3))
        for _ in range(5):
            o, d = random_ray(rng, tris)
            ts = [t for t in (hit_triangle(tr, o, d) for tr in tris) if t is not None]
            got = closest_hit(bvh, tris, o, d)
            assert (got[0] if got else None) == (min(ts) if ts else None)
            tmax = rng.choice([math.inf, Fraction(rng.randint(0, 10), rng.randint(1, 3))])
            assert any_hit(bvh, tris, o, d, tmax) == any(t <= tmax for t in ts)
