# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bulk-loading-b-tree/. The authors are listed in prov/BKKK4M.jsonl.

import random
from fractions import Fraction

import pytest

from bulk_loading_b_tree import BPlusTree, pack


def test_example():
    keys = list(range(3, 61, 3))
    random.Random(5).shuffle(keys)
    t = BPlusTree.bulk_load([(k, str(k)) for k in keys], 2, Fraction(3, 4))
    t.check_invariant()
    levels = t.levels()
    assert [len(lv) for lv in levels] == [1, 2, 7]
    assert [n.keys for n in levels[2]] == [
        [3, 6, 9], [12, 15, 18], [21, 24, 27], [30, 33, 36],
        [39, 42, 45], [48, 51, 54], [57, 60]]
    assert [n.keys for n in levels[1]] == [[12, 21], [39, 48, 57]]
    assert levels[0][0].keys == [30]
    assert t.search(42) == "42" and t.search(43) is None


def test_example_repeated_inserts():
    t = BPlusTree(2)
    for k in range(3, 61, 3):
        t.insert(k, str(k))
    t.check_invariant()
    levels = t.levels()
    assert [len(lv) for lv in levels] == [1, 3, 9]
    assert [len(n.keys) for n in levels[-1]] == [2, 2, 2, 2, 2, 2, 2, 2, 4]
    assert t.node_accesses == 54


def test_pack():
    assert pack(list(range(13)), 3, 2, 4) == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11, 12]]
    assert pack(list(range(7)), 4, 3, 5) == [[0, 1, 2, 3], [4, 5, 6]]
    assert pack(list(range(9)), 4, 2, 4) == [[0, 1, 2, 3], [4, 5], [6, 7, 8]]
    assert pack(list(range(5)), 4, 2, 5) == [[0, 1, 2, 3, 4]]
    assert pack([], 3, 2, 4) == []


def test_empty_and_small():
    t = BPlusTree.bulk_load([], 2)
    assert t.root is None and t.search(1) is None and t.items() == []
    t = BPlusTree.bulk_load([(5, "a")], 2)
    t.check_invariant()
    assert t.search(5) == "a" and t.search(4) is None
    with pytest.raises(ValueError):
        BPlusTree.bulk_load([(1, "a"), (1, "b")], 2)


def test_random_trees_are_valid_and_answer_like_a_dict():
    rng = random.Random(1010)
    fills = [Fraction(1), Fraction(1, 2), Fraction(2, 3), Fraction(9, 10), Fraction(1, 10)]
    for _ in range(500):
        d = rng.randint(1, 4)
        n = rng.randint(0, 120)
        ref = {}
        while len(ref) < n:
            ref[rng.randint(-500, 500)] = rng.random()
        fill = rng.choice(fills)
        t = BPlusTree.bulk_load(list(ref.items()), d, fill)
        t.check_invariant()
        assert t.items() == sorted(ref.items())
        for _ in range(10):
            k = rng.randint(-510, 510)
            assert t.search(k) == ref.get(k)
        if n:
            leaves = t.levels()[-1]
            target = max(d, min(2 * d, int(fill * 2 * d)))
            assert all(len(x.keys) == target for x in leaves[:-2])


def test_inserts_after_bulk_load_keep_tree_valid():
    rng = random.Random(77)
    ref = {k: k for k in range(0, 400, 2)}
    t = BPlusTree.bulk_load(list(ref.items()), 3, Fraction(1))
    for _ in range(300):
        k = rng.randint(0, 500)
        t.insert(k, -k)
        ref[k] = -k
    t.check_invariant()
    assert t.items() == sorted(ref.items())


def test_bulk_load_writes_fewer_nodes_than_inserts():
    rng = random.Random(3)
    keys = rng.sample(range(10 ** 6), 5000)
    bulk = BPlusTree.bulk_load([(k, None) for k in keys], 8, Fraction(1))
    nodes = sum(len(lv) for lv in bulk.levels())
    one = BPlusTree(8)
    for k in keys:
        one.insert(k, None)
    one.check_invariant()
    leaves = len(bulk.levels()[-1])
    assert leaves == 313
    assert nodes <= leaves + (leaves + 8 - 2) // 8
    assert one.node_accesses > 5 * nodes
    assert len(one.levels()[-1]) > leaves
