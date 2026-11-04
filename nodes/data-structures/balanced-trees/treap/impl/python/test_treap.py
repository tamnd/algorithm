# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/treap/. The authors are listed in prov/S6DS4V.jsonl.

import itertools
import math
import random

import treap as tr
from treap import Node, Treap


def shape(t: "Node[int] | None") -> object:
    if t is None:
        return None
    if t.left is None and t.right is None:
        return t.key
    return (shape(t.left), t.key, shape(t.right))


EXAMPLE = [(50, 30), (30, 60), (70, 40), (20, 10), (40, 80), (60, 50)]


def test_page_example() -> None:
    t: Treap[int] = Treap()
    want = {
        30: (None, 30, 50),
        70: (None, 30, (50, 70, None)),
        40: ((20, 30, None), 40, (50, 70, None)),
        60: ((20, 30, None), 40, (50, 60, 70)),
    }
    for k, p in EXAMPLE:
        assert t.insert(k, p)
        t.check_invariant()
        if k in want:
            assert shape(t.root) == want[k]
    assert t.delete(40)
    t.check_invariant()
    assert shape(t.root) == (20, 30, (50, 60, 70))
    assert t.delete(30)
    t.check_invariant()
    assert shape(t.root) == ((20, 50, None), 60, 70)


def test_shape_does_not_depend_on_order() -> None:
    # the treap of a set of (key, priority) pairs is unique
    shapes = set()
    for perm in itertools.permutations(EXAMPLE):
        t: Treap[int] = Treap()
        for k, p in perm:
            t.insert(k, p)
        shapes.add(repr(shape(t.root)))
    assert shapes == {repr(((20, 30, None), 40, (50, 60, 70)))}


def test_edge_cases() -> None:
    t: Treap[int] = Treap(seed=0)
    assert not t.contains(3)
    assert not t.delete(3)
    assert t.height() == 0
    t.check_invariant()
    assert t.insert(3)
    assert not t.insert(3)
    assert len(t) == 1
    assert t.delete(3)
    assert t.root is None
    # equal priorities are allowed
    for k in range(10):
        t.insert(k, 0.5)
    t.check_invariant()
    assert list(t.keys()) == list(range(10))


def test_priorities_must_be_random() -> None:
    # priority equal to the key turns the treap into a path
    t: Treap[int] = Treap()
    for k in range(200):
        t.insert(k, float(k))
    assert t.height() == 200
    # random priorities on the same sorted input keep it short
    u: Treap[int] = Treap(seed=1989)
    for k in range(200):
        u.insert(k)
    assert u.height() <= 4 * math.log(200) + 10


def test_expected_rotations() -> None:
    rng = random.Random(7)
    count = [0]
    left, right = tr.rotate_left, tr.rotate_right

    def cl(x: "Node[int]") -> "Node[int]":
        count[0] += 1
        return left(x)

    def cr(x: "Node[int]") -> "Node[int]":
        count[0] += 1
        return right(x)

    tr.rotate_left, tr.rotate_right = cl, cr
    try:
        t: Treap[int] = Treap(seed=11)
        keys = list(range(5000))
        rng.shuffle(keys)
        for k in keys:
            t.insert(k)
        # fewer than 2 rotations for each insertion on average
        assert count[0] < 2 * len(keys)
    finally:
        tr.rotate_left, tr.rotate_right = left, right


def test_random_against_set() -> None:
    rng = random.Random(1996)
    for case in range(600):
        t: Treap[int] = Treap(seed=case)
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
