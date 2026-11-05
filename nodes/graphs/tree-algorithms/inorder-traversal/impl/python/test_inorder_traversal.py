# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/inorder-traversal/. The authors are listed in prov/JDE4T3.jsonl.

import random

import pytest

from inorder_traversal import inorder, inorder_keys

LEFT = [1, 3, -1, -1, -1, -1]
RIGHT = [2, 4, 5, -1, -1, -1]
KEY = [50, 30, 70, 20, 40, 80]


def recursive_inorder(left: list[int], right: list[int], x: int) -> list[int]:
    if x == -1:
        return []
    return recursive_inorder(left, right, left[x]) + [x] + recursive_inorder(left, right, right[x])


def random_binary_tree(rng: random.Random, n: int) -> tuple[list[int], list[int], int]:
    """A random binary tree on 0 .. n-1 with a random root and random labels."""
    if n == 0:
        return [], [], -1
    labels = list(range(n))
    rng.shuffle(labels)
    left = [-1] * n
    right = [-1] * n
    free = [(labels[0], 0), (labels[0], 1)]
    for v in labels[1:]:
        i = rng.randrange(len(free))
        u, side = free[i]
        free[i] = free[-1]
        free.pop()
        if side == 0:
            left[u] = v
        else:
            right[u] = v
        free.append((v, 0))
        free.append((v, 1))
    return left, right, labels[0]


def test_page_example():
    assert inorder(LEFT, RIGHT, 0) == [3, 1, 4, 0, 2, 5]
    assert inorder_keys(LEFT, RIGHT, 0, KEY) == [20, 30, 40, 50, 70, 80]


def test_empty_and_single():
    assert inorder([], [], -1) == []
    assert inorder([-1], [-1], 0) == [0]


def test_star():
    # The largest star that is a binary tree: a root with two leaves.
    assert inorder([1, -1, -1], [2, -1, -1], 0) == [1, 0, 2]


def test_deep_left_path():
    n = 100_000
    left = [i + 1 for i in range(n - 1)] + [-1]
    right = [-1] * n
    assert inorder(left, right, 0) == list(range(n - 1, -1, -1))


def test_deep_right_path():
    n = 100_000
    left = [-1] * n
    right = [i + 1 for i in range(n - 1)] + [-1]
    assert inorder(left, right, 0) == list(range(n))


def test_zigzag_path():
    n = 100_001
    left = [-1] * n
    right = [-1] * n
    for i in range(n - 1):
        if i % 2 == 0:
            left[i] = i + 1
        else:
            right[i] = i + 1
    out = inorder(left, right, 0)
    assert sorted(out) == list(range(n))
    assert out[0] == 1 and out[-1] == 0


def test_bad_input():
    with pytest.raises(ValueError):
        inorder([0], [-1], 0)
    with pytest.raises(ValueError):
        inorder([-1], [-1, -1], 0)
    with pytest.raises(ValueError):
        inorder([-1], [-1], 1)


def test_random_against_recursive():
    rng = random.Random(5)
    for _ in range(600):
        n = rng.randrange(0, 40)
        left, right, root = random_binary_tree(rng, n)
        assert inorder(left, right, root) == recursive_inorder(left, right, root)


def test_bst_gives_sorted_keys():
    rng = random.Random(9)
    for _ in range(200):
        keys = rng.sample(range(1000), rng.randrange(1, 60))
        left = [-1] * len(keys)
        right = [-1] * len(keys)
        for v in range(1, len(keys)):
            x = 0
            while True:
                side = left if keys[v] < keys[x] else right
                if side[x] == -1:
                    side[x] = v
                    break
                x = side[x]
        assert inorder_keys(left, right, 0, keys) == sorted(keys)
