# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/red-black-tree-deletion/. The authors are listed in prov/KYJFQJ.jsonl.

import math
import random

import pytest

from red_black_tree_deletion import (
    LeftLeaningRedBlackTree,
    Node,
    delete_min,
    is_red,
    remove,
)


def shape(h: "Node[str] | Node[int] | None") -> object:
    """A node is written key, with * when its link is red."""
    if h is None:
        return None
    s = str(h.key) + ("*" if h.red else "")
    if h.left is None and h.right is None:
        return s
    return (shape(h.left), s, shape(h.right))


def test_page_example() -> None:
    t: LeftLeaningRedBlackTree[str] = LeftLeaningRedBlackTree()
    for k in "SEARCHXMPL":
        t.insert(k)
    assert shape(t.root) == (
        (("A*", "C", None), "E", ("H*", "L", None)),
        "M",
        ("P", "R", ("S*", "X", None)),
    )
    want = {
        "R": ((("A*", "C", None), "E", ("H*", "L", None)), "M", ("P", "S", "X")),
        "M": ((("A*", "C", None), "E*", ("H*", "L", None)), "P", ("S*", "X", None)),
        "A": (("C", "E*", ("H*", "L", None)), "P", ("S*", "X", None)),
    }
    for k, w in want.items():
        assert t.delete(k)
        t.check_invariant()
        assert shape(t.root) == w
    assert "".join(t.keys()) == "CEHLPSX"


def test_delete_min() -> None:
    t: LeftLeaningRedBlackTree[int] = LeftLeaningRedBlackTree()
    for k in range(100):
        t.insert(k)
    for k in range(100):
        assert t.root is not None
        if not is_red(t.root.left) and not is_red(t.root.right):
            t.root.red = True
        t.root = delete_min(t.root)
        if t.root is not None:
            t.root.red = False
        t.size -= 1
        t.check_invariant()
        assert list(t.keys()) == list(range(k + 1, 100))


def test_edge_cases() -> None:
    t: LeftLeaningRedBlackTree[int] = LeftLeaningRedBlackTree()
    assert not t.delete(5)
    assert not t.contains(5)
    assert t.height() == 0
    t.check_invariant()
    assert t.insert(5)
    assert not t.insert(5)
    assert len(t) == 1
    assert t.delete(5)
    assert t.root is None
    t.check_invariant()


def test_root_with_two_black_children() -> None:
    # (1, 2, 3) with black children: delete must first make the root red
    t: LeftLeaningRedBlackTree[int] = LeftLeaningRedBlackTree()
    for k in [1, 2, 3]:
        t.insert(k)
    assert shape(t.root) == ("1", "2", "3")
    assert t.delete(1)
    t.check_invariant()
    assert shape(t.root) == ("2*", "3", None)


def test_remove_needs_a_present_key() -> None:
    # REMOVE assumes the key is there; DELETE searches first
    t: LeftLeaningRedBlackTree[int] = LeftLeaningRedBlackTree()
    for k in [1, 2, 3]:
        t.insert(k)
    assert t.root is not None
    with pytest.raises((AssertionError, AttributeError)):
        remove(t.root, 0)
    t2: LeftLeaningRedBlackTree[int] = LeftLeaningRedBlackTree()
    for k in [1, 2, 3]:
        t2.insert(k)
    assert not t2.delete(0)
    t2.check_invariant()
    assert list(t2.keys()) == [1, 2, 3]


def test_sorted_input_height() -> None:
    t: LeftLeaningRedBlackTree[int] = LeftLeaningRedBlackTree()
    n = 4095
    for k in range(n):
        t.insert(k)
    t.check_invariant()
    assert t.height() <= 2 * math.log2(n + 1)
    for k in range(n - 1, -1, -2):
        assert t.delete(k)
    t.check_invariant()
    assert list(t.keys()) == list(range(1, n, 2))


def test_random_against_set() -> None:
    rng = random.Random(2011)
    for _ in range(600):
        t: LeftLeaningRedBlackTree[int] = LeftLeaningRedBlackTree()
        model: set[int] = set()
        for _ in range(rng.randrange(1, 60)):
            k = rng.randrange(40)
            if rng.random() < 0.6:
                assert t.insert(k) == (k not in model)
                model.add(k)
            else:
                assert t.delete(k) == (k in model)
                model.discard(k)
            t.check_invariant()
        assert list(t.keys()) == sorted(model)
        for k in range(40):
            assert t.contains(k) == (k in model)
        if model:
            assert t.height() <= 2 * math.log2(len(model) + 1)
