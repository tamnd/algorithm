# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clustering-feature-tree/. The authors are listed in prov/0PD5NK.jsonl.

import random
from fractions import Fraction

from clustering_feature_tree import CF, CFTree, total


def sq(p, q):
    return sum((a - b) ** 2 for a, b in zip(p, q))


def rand_points(rng, n, d=2):
    return [[Fraction(rng.randint(-40, 40), rng.randint(1, 4)) for _ in range(d)] for _ in range(n)]


def test_radius_and_diameter_from_cf_are_exact():
    rng = random.Random(1)
    for _ in range(200):
        n = rng.randint(1, 8)
        pts = rand_points(rng, n, rng.randint(1, 3))
        cf = total([CF.of_point(p) for p in pts])
        c = [sum(p[i] for p in pts) / n for i in range(len(pts[0]))]
        assert cf.centroid() == c
        assert cf.radius_sq() == sum(sq(p, c) for p in pts) / n
        pairs = sum(sq(p, q) for p in pts for q in pts)
        assert cf.diameter_sq() == (pairs / (n * (n - 1)) if n > 1 else 0)


def test_additivity():
    rng = random.Random(2)
    pts = rand_points(rng, 12, 3)
    a = total([CF.of_point(p) for p in pts[:5]])
    b = total([CF.of_point(p) for p in pts[5:]])
    whole = total([CF.of_point(p) for p in pts])
    assert a + b == whole


def check(tree, n_points, t2):
    depths = []
    stack = [(tree.root, 0)]
    order = []
    while stack:
        node, depth = stack.pop()
        if node.leaf:
            depths.append(depth)
            order.append(node)
            assert 1 <= len(node.entries) <= tree.L or node is tree.root
            assert all(e.radius_sq() <= t2 or e.n == 1 for e in node.entries)
        else:
            # no lower fill bound below the root, as in BIRCH
            assert 1 <= len(node.entries) <= tree.B
            assert node is not tree.root or len(node.entries) >= 2
            for e, child in zip(node.entries, node.children):
                assert e == total(child.entries)
            stack.extend((c, depth + 1) for c in reversed(node.children))
    assert len(set(depths)) <= 1
    # the leaf chain visits each leaf once (in any order)
    chain = tree.leaves()
    assert len(chain) == len(order) and {id(x) for x in chain} == {id(x) for x in order}
    assert sum(e.n for e in tree.leaf_entries()) == n_points


def test_insert_keeps_the_invariants():
    rng = random.Random(3)
    for _ in range(25):
        B, L = rng.randint(2, 4), rng.randint(2, 4)
        t2 = Fraction(rng.randint(0, 20))
        tree = CFTree(B, L, t2)
        pts = rand_points(rng, rng.randint(1, 60))
        for i, p in enumerate(pts, 1):
            tree.insert(p)
            check(tree, i, t2)
        assert total(tree.root.entries) == total([CF.of_point(p) for p in pts])


def test_rebuild_with_larger_threshold():
    rng = random.Random(4)
    for _ in range(15):
        pts = rand_points(rng, 50)
        tree = CFTree(3, 3, Fraction(1))
        for p in pts:
            tree.insert(p)
        bigger = tree.rebuild(Fraction(30))
        check(bigger, 50, Fraction(30))
        assert len(bigger.leaf_entries()) <= len(tree.leaf_entries())
        assert total(bigger.root.entries) == total(tree.root.entries)


def test_example_trace():
    tree = CFTree(2, 2, Fraction(1))
    for x in [0, 1, 10, 11, 20, 5, 21]:
        tree.insert([Fraction(x)])
    leaves = [[(e.n, e.ls[0], e.ss) for e in leaf.entries] for leaf in tree.leaves()]
    assert leaves == [[(2, 1, 1), (1, 5, 25)], [(2, 21, 221), (2, 41, 841)]]
    assert [(e.n, e.ls[0], e.ss) for e in tree.root.entries] == [(3, 6, 26), (4, 62, 1062)]
