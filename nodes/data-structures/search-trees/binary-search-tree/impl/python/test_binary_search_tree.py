# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/binary-search-tree/. The authors are listed in prov/MBF8HP.jsonl.

import bisect
import random

from binary_search_tree import BinarySearchTree

EXAMPLE = [15, 6, 18, 3, 7, 17, 20, 2, 4, 13, 9]


def build(keys: list[int]) -> BinarySearchTree[int, int]:
    t: BinarySearchTree[int, int] = BinarySearchTree()
    for k in keys:
        t.insert(k, 10 * k)
        t.check_invariant()
    return t


def test_example() -> None:
    t = build(EXAMPLE)
    assert t.keys() == sorted(EXAMPLE)
    assert t.height() == 4
    assert t.search(13) == 130
    assert t.search(8) is None
    assert t.minimum() == 2 and t.maximum() == 20
    assert t.successor(13) == 15
    assert t.successor(4) == 6
    assert t.predecessor(17) == 15
    assert t.successor(20) is None
    assert t.delete(6)
    t.check_invariant()
    assert t.root is not None and t.root.left is not None and t.root.left.key == 7
    assert t.delete(15)
    t.check_invariant()
    assert t.root is not None and t.root.key == 17
    assert t.keys() == [2, 3, 4, 7, 9, 13, 17, 18, 20]


def test_edges() -> None:
    t: BinarySearchTree[int, str] = BinarySearchTree()
    assert t.search(1) is None and t.minimum() is None and t.height() == -1
    assert not t.delete(1)
    t.insert(1, "a")
    t.insert(1, "b")
    assert len(t) == 1 and t.search(1) == "b"
    assert t.delete(1) and len(t) == 0 and t.root is None


def test_sorted_input_is_a_path() -> None:
    t = build(list(range(3000)))
    assert t.height() == 2999
    assert t.search(2999) == 29990
    for k in range(0, 3000, 2):
        assert t.delete(k)
    t.check_invariant()
    assert t.keys() == list(range(1, 3000, 2))


def test_random_against_model() -> None:
    rng = random.Random(4127)
    for _ in range(500):
        t: BinarySearchTree[int, int] = BinarySearchTree()
        model: dict[int, int] = {}
        for _ in range(rng.randint(0, 40)):
            k = rng.randint(0, 30)
            op = rng.random()
            if op < 0.5:
                t.insert(k, op.__hash__())
                model[k] = op.__hash__()
            elif op < 0.8:
                assert t.delete(k) == (k in model)
                model.pop(k, None)
            else:
                assert t.search(k) == model.get(k)
            t.check_invariant()
        ks = sorted(model)
        assert t.keys() == ks
        for i, k in enumerate(ks):
            assert t.successor(k) == (ks[i + 1] if i + 1 < len(ks) else None)
            assert t.predecessor(k) == (ks[i - 1] if i > 0 else None)
        assert t.minimum() == (ks[0] if ks else None)
        j = bisect.bisect_left(ks, 15)
        assert (t.search(15) is not None) == (j < len(ks) and ks[j] == 15)
