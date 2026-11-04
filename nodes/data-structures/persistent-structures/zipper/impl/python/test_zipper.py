# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zipper/. The authors are listed in prov/T3A6Y3.jsonl.

import random

import pytest

from zipper import Zipper, inorder, node


def leaf(x):
    return node(None, x, None)


def example_tree():
    return node(node(leaf(1), 2, leaf(3)), 4, node(leaf(5), 6, leaf(7)))


def test_example() -> None:
    t = example_tree()
    z = Zipper(t).left().right()
    assert z.value() == 3 and z.depth == 2 and list(z.path_values()) == [2, 4]
    z2 = z.set_value(30)
    t2 = z2.to_tree()
    assert inorder(t2) == [1, 2, 30, 4, 5, 6, 7]
    assert inorder(t) == [1, 2, 3, 4, 5, 6, 7]  # the old tree is unchanged
    assert t2[2] is t[2]  # the right subtree 6 is shared
    assert t2[0][0] is t[0][0]  # the leaf 1 is shared
    assert t2 is not t and t2[0] is not t[0]
    # Going up without a change rebuilds equal nodes.
    assert inorder(z.to_tree()) == inorder(t)
    z.check_invariant()
    z2.check_invariant()


def test_edges() -> None:
    e = Zipper(None)
    assert e.at_top() and e.to_tree() is None
    with pytest.raises(ValueError):
        e.left()
    with pytest.raises(ValueError):
        e.up()
    with pytest.raises(ValueError):
        e.value()
    z = e.replace(leaf(8))
    assert z.value() == 8
    w = z.left().replace(leaf(3)).up()
    assert inorder(w.to_tree()) == [3, 8]
    assert inorder(z.to_tree()) == [8]
    w.check_invariant()


def test_deep() -> None:
    n = 200000
    z = Zipper(None)
    for i in range(n):  # build a left spine by going down
        z = z.replace(node(None, i, None)).left()
    assert z.depth == n
    t = z.to_tree()  # iterative top
    assert inorder(t)[:3] == [n - 1, n - 2, n - 3]
    assert len(inorder(t)) == n
    z.check_invariant()


def random_tree(rng, size):
    if size == 0:
        return None
    k = rng.randrange(size)
    return node(random_tree(rng, k), rng.randint(0, 99), random_tree(rng, size - 1 - k))


def test_random_against_model() -> None:
    # Model: a tree as nested lists, and the focus as a list of directions.
    rng = random.Random(5150)

    def get_at(t, dirs):
        for d in dirs:
            t = t[0] if d == 0 else t[2]
        return t

    def put_at(t, dirs, s):
        if not dirs:
            return s
        l, x, r = t
        if dirs[0] == 0:
            return (put_at(l, dirs[1:], s), x, r)
        return (l, x, put_at(r, dirs[1:], s))

    for _ in range(500):
        t = random_tree(rng, rng.randint(0, 15))
        z, dirs, model = Zipper(t), [], t
        saved = []
        for _ in range(rng.randint(1, 30)):
            op = rng.randrange(5)
            if op == 0 and z.focus is not None:
                z, dirs = z.left(), dirs + [0]
            elif op == 1 and z.focus is not None:
                z, dirs = z.right(), dirs + [1]
            elif op == 2 and not z.at_top():
                z, dirs = z.up(), dirs[:-1]
            elif op == 3:
                s = random_tree(rng, rng.randint(0, 3))
                z = z.replace(s)
                model = put_at(model, dirs, s)
            else:
                saved.append((z, list(dirs), model))
            assert z.focus == get_at(model, dirs)
            assert z.depth == len(dirs)
            assert z.to_tree() == model
        for oz, od, om in saved:  # old zippers are untouched
            assert oz.to_tree() == om and oz.depth == len(od)
            oz.check_invariant()
