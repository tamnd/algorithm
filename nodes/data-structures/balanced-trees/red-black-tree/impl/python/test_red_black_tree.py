# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/red-black-tree/. The authors are listed in prov/WQME6V.jsonl.

import math
import random

from red_black_tree import RED, Node, RedBlackTree


def shape(t: RedBlackTree[int], x: "Node | None" = None) -> object:
    x = t.root if x is None else x
    if x is t.nil:
        return None
    me = f"{x.key}{'r' if x.color == RED else 'b'}"
    if x.left is t.nil and x.right is t.nil:
        return me
    return (shape(t, x.left) if x.left is not t.nil else None, me,
            shape(t, x.right) if x.right is not t.nil else None)


def test_page_example() -> None:
    t: RedBlackTree[int] = RedBlackTree()
    got = []
    for k in [10, 20, 30, 15, 25, 5, 1]:
        t.insert(k)
        t.check_invariant()
        got.append(shape(t))
    assert got[2] == ("10r", "20b", "30r")
    assert got[3] == ((None, "10b", "15r"), "20b", "30b")
    assert got[-1] == ((("1r", "5b", None), "10r", "15b"), "20b", ("25r", "30b", None))
    for k, want in [
        (20, ((("1r", "5b", None), "10r", "15b"), "25b", "30b")),
        (1, (("5b", "10r", "15b"), "25b", "30b")),
        (30, ("5b", "10b", ("15r", "25b", None))),
    ]:
        t.delete(k)
        t.check_invariant()
        assert shape(t) == want


def test_sorted_input() -> None:
    t: RedBlackTree[int] = RedBlackTree()
    for k in range(1, 1001):
        t.insert(k)
    t.check_invariant()
    assert t.height() <= 2 * math.log2(1001)
    for k in range(1, 1001, 2):
        t.delete(k)
    t.check_invariant()
    assert t.keys() == list(range(2, 1001, 2))


def test_edges() -> None:
    t: RedBlackTree[int] = RedBlackTree()
    assert not t.delete(3) and not t.contains(3) and t.height() == 0
    assert t.insert(3) and not t.insert(3) and len(t) == 1
    assert t.delete(3) and len(t) == 0 and t.root is t.nil
    t.check_invariant()


def test_rotation_counts() -> None:
    rng = random.Random(1978)
    t: RedBlackTree[int] = RedBlackTree()
    for _ in range(4000):
        k = rng.randint(0, 3000)
        r0 = t.rotations
        if rng.random() < 0.6:
            t.insert(k)
            assert t.rotations - r0 <= 2
        else:
            t.delete(k)
            assert t.rotations - r0 <= 3
    t.check_invariant()


def test_random_against_set() -> None:
    rng = random.Random(1972)
    for _ in range(500):
        t: RedBlackTree[int] = RedBlackTree()
        model: set[int] = set()
        for _ in range(rng.randint(0, 80)):
            k = rng.randint(0, 40)
            if rng.random() < 0.6:
                assert t.insert(k) == (k not in model)
                model.add(k)
            else:
                assert t.delete(k) == (k in model)
                model.discard(k)
            assert t.contains(k) == (k in model)
        t.check_invariant()
        assert t.keys() == sorted(model)
        n = len(model)
        assert t.height() <= 2 * math.log2(n + 1)
