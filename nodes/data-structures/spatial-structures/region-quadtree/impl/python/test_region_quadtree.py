# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/region-quadtree/. The authors are listed in prov/74TKQQ.jsonl.
import random

import pytest

from region_quadtree import RegionQuadTree, build, intersection, union

ROWS = ["00000000", "00000000", "00001111", "00001111",
        "00011111", "00111111", "00111100", "00111100"]
IMG = [[int(c) for c in r] for r in ROWS]


def test_page_example():
    t = RegionQuadTree(IMG)
    assert t.root == [0, [0, 0, 1, 1], [0, [0, 1, 1, 1], 0, 1], [1, 1, 1, 0]]
    assert (t.leaf_count(), t.node_count(), t.black_area()) == (16, 21, 27)
    assert t.get(5, 3) == 1 and t.get(1, 1) == 0
    t.set(2, 4, 1)
    assert t.root == [0, [0, 0, 1, 1], [0, 1, 0, 1], [1, 1, 1, 0]]
    assert (t.leaf_count(), t.node_count(), t.black_area()) == (13, 17, 28)
    t.set(2, 4, 0)
    assert t.root == build(IMG)
    t.set(0, 0, 1)
    assert (t.leaf_count(), t.node_count()) == (22, 29)
    t.set(0, 0, 0)
    assert t.root == build(IMG)


def test_edge_cases():
    assert build([[0]]) == 0 and build([[1]]) == 1
    t = RegionQuadTree([[0]])
    t.set(0, 0, 1)
    assert t.root == 1
    assert build([[1, 1], [1, 1]]) == 1
    assert build([[1, 0], [0, 0]]) == [1, 0, 0, 0]
    t = RegionQuadTree([[0] * 4 for _ in range(4)])
    t.set(3, 3, 1)
    assert t.root == [0, 0, 0, [0, 0, 0, 1]]
    with pytest.raises(ValueError):
        build([[0, 0, 0]] * 3)
    with pytest.raises(IndexError):
        t.get(4, 0)


def rand_img(rng, n, p):
    return [[1 if rng.random() < p else 0 for _ in range(n)] for _ in range(n)]


def test_random_against_array():
    rng = random.Random(20261104)
    for _ in range(600):
        n = 1 << rng.randint(0, 4)
        img = rand_img(rng, n, rng.choice([0.05, 0.5, 0.95]))
        t = RegionQuadTree(img)
        t.check_invariant()
        assert t.to_image() == img
        for _ in range(8):
            x, y, c = rng.randrange(n), rng.randrange(n), rng.randint(0, 1)
            t.set(x, y, c)
            img[y][x] = c
            t.check_invariant()
            assert t.get(x, y) == c
        assert t.to_image() == img
        assert t.root == build(img)  # maximal trees are unique
        assert t.black_area() == sum(map(sum, img))
        other = rand_img(rng, n, 0.3)
        b = build(other)
        u = union(t.root, b)
        i = intersection(t.root, b)
        assert u == build([[a | c for a, c in zip(r, s)] for r, s in zip(img, other)])
        assert i == build([[a & c for a, c in zip(r, s)] for r, s in zip(img, other)])
