# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zip-tree/. The authors are listed in prov/4VXZ7W.jsonl.

import math
import random
from collections import Counter

from zip_tree import Node, ZipTree, random_rank, unzip, zip_trees

RANKS = [(10, 0), (20, 2), (30, 0), (40, 1), (50, 3), (60, 0), (70, 1)]


def shape(t):
    if t is None:
        return None
    if t.left is None and t.right is None:
        return t.key
    return (shape(t.left), t.key, shape(t.right))


def page_tree():
    z = ZipTree()
    for k, r in RANKS:
        z.insert(k, r)
    return z


def test_page_example():
    z = page_tree()
    assert shape(z.root) == ((10, 20, (30, 40, None)), 50, (60, 70, None))
    z.insert(35, 2)  # 20 has the same rank and a smaller key, so 35 goes below it
    assert shape(z.root) == ((10, 20, (30, 35, 40)), 50, (60, 70, None))
    z.delete(50)  # zip the spines 20, 35, 40 and 70
    assert shape(z.root) == (10, 20, (30, 35, (None, 40, (60, 70, None))))
    z.check_invariant()


def test_shape_depends_only_on_keys_and_ranks():
    rng = random.Random(7)
    for _ in range(50):
        pairs = [(k, random_rank(rng)) for k in rng.sample(range(100), 30)]
        a, b = ZipTree(), ZipTree()
        for k, r in pairs:
            a.insert(k, r)
        for k, r in sorted(pairs, reverse=True):
            b.insert(k, r)
        assert shape(a.root) == shape(b.root)


def test_unzip_and_zip_are_inverse():
    z = page_tree()
    p, q = unzip(z.root, 45)
    assert shape(p) == (10, 20, (30, 40, None)) and shape(q) == (None, 50, (60, 70, None))
    assert shape(zip_trees(p, q)) == ((10, 20, (30, 40, None)), 50, (60, 70, None))
    assert unzip(None, 3) == (None, None) and zip_trees(None, None) is None
    n = Node(5, 0)
    assert zip_trees(n, None) is n and zip_trees(None, n) is n


def test_edge_cases_and_rank_distribution():
    z = ZipTree(random.Random(1))
    assert not z.delete(1) and z.height() == -1
    assert z.insert(1) and not z.insert(1) and z.delete(1) and z.root is None
    rng = random.Random(2019)
    c = Counter(random_rank(rng) for _ in range(40000))
    for k in range(4):
        assert abs(c[k] / 40000 - 0.5 ** (k + 1)) < 0.01


def test_expected_depth():
    rng = random.Random(2021)
    n = 1 << 13
    z = ZipTree(rng)
    keys = list(range(n))
    rng.shuffle(keys)
    for k in keys:
        z.insert(k)
    z.check_invariant()
    total, stack = 0, [(z.root, 0)]
    while stack:
        x, d = stack.pop()
        if x is not None:
            total += d
            stack += [(x.left, d + 1), (x.right, d + 1)]
    assert total / n <= 1.5 * math.log2(n) + 2


def test_random_against_set():
    rng = random.Random(1990)
    for case in range(600):
        z = ZipTree(random.Random(case))
        ref = set()
        for _ in range(rng.randint(0, 80)):
            k = rng.randint(0, 40)
            if rng.random() < 0.6:
                assert z.insert(k) == (k not in ref)
                ref.add(k)
            else:
                assert z.delete(k) == (k in ref)
                ref.discard(k)
            z.check_invariant()
        assert z.keys() == sorted(ref)
        for k in range(-1, 42):
            assert (k in z) == (k in ref)
