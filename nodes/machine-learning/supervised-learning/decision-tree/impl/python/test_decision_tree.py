# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/decision-tree/. The authors are listed in prov/4YYHCQ.jsonl.

import itertools
import random

from decision_tree import DecisionTree


def in_box(x, box):
    return all((lo is None or x[j] > lo) and (hi is None or x[j] <= hi) for j, (lo, hi) in box.items())


def page_example():
    t = DecisionTree("A")
    a, b = t.split_leaf(0, 0, 2.5, "A", "B")
    c, d = t.split_leaf(b, 1, 1.0, "B", "C")
    return t, (a, b, c, d)


def test_page_example():
    t, (a, b, c, d) = page_example()
    t.check_invariant()
    assert t.predict((3.0, 0.5)) == "B"
    assert t.predict((3.0, 2.0)) == "C"
    assert t.predict((1.0, 9.0)) == "A"
    assert t.predict((2.5, 9.0)) == "A"
    assert (t.size(), t.n_leaves(), t.depth()) == (5, 3, 2)
    assert t.cell(c) == {0: [2.5, None], 1: [None, 1.0]}
    t.prune(b, "B")
    t.check_invariant()
    assert (t.size(), t.n_leaves(), t.depth()) == (3, 2, 1)
    assert t.predict((3.0, 2.0)) == "B"


def test_single_leaf():
    t = DecisionTree(7)
    t.check_invariant()
    assert t.predict((0,)) == 7 and t.depth() == 0 and t.size() == 1


def test_parity_needs_all_leaves():
    # The parity of d bits as a tree of depth d with 2^d leaves.
    d = 4
    t = DecisionTree(0)
    frontier = [(0, 0)]
    for j in range(d):
        nxt = []
        for v, par in frontier:
            a, b = t.split_leaf(v, j, 0, par, 1 - par)
            nxt += [(a, par), (b, 1 - par)]
        frontier = nxt
    t.check_invariant()
    assert t.n_leaves() == 2 ** d and t.depth() == d
    for x in itertools.product((0, 1), repeat=d):
        assert t.predict(x) == sum(x) % 2


def test_random_operations_against_box_model():
    rng = random.Random(20261111)
    for _ in range(300):
        t = DecisionTree(0)
        ops = rng.randint(1, 25)
        for step in range(ops):
            leaves = t.leaves()
            if rng.random() < 0.75 or t.size() == 1:
                v = rng.choice(leaves)
                t.split_leaf(v, rng.randrange(3), rng.randint(0, 9) + 0.5, rng.randint(0, 9), rng.randint(0, 9))
            else:
                internal = [u for u in range(len(t.value)) if t.alive[u] and not t.is_leaf(u)]
                t.prune(rng.choice(internal), rng.randint(0, 9))
            t.check_invariant()
            leaves = t.leaves()
            boxes = [(t.cell(v), t.value[v], v) for v in leaves]
            for _ in range(20):
                x = tuple(rng.randint(-1, 11) for _ in range(3))
                hits = [(val, v) for box, val, v in boxes if in_box(x, box)]
                assert len(hits) == 1  # the cells of the leaves partition the space
                assert t.predict(x) == hits[0][0] and t.leaf_of(x) == hits[0][1]
            assert t.size() == 2 * t.n_leaves() - 1
            assert t.n_leaves() <= 2 ** t.depth()
