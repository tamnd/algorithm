# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cartesian-tree/. The authors are listed in prov/3X8X1H.jsonl.

import random

import pytest

from cartesian_tree import CartesianTree

EXAMPLE = [3, 1, 4, 1, 5, 9, 2, 6]


def brute_parent(a: list) -> list[int]:
    """Parent array by the definition: the root of a[lo..hi] is its leftmost minimum."""
    n = len(a)
    parent = [-1] * n
    work = [(0, n - 1, -1)] if n else []
    while work:
        lo, hi, p = work.pop()
        if lo > hi:
            continue
        m = min(range(lo, hi + 1), key=lambda k: (a[k], k))
        parent[m] = p
        work.append((lo, m - 1, m))
        work.append((m + 1, hi, m))
    return parent


def test_page_example():
    t = CartesianTree(EXAMPLE)
    assert t.root == 1
    assert t.parent == [1, -1, 3, 1, 6, 4, 3, 6]
    assert t.left == [-1, 0, -1, 2, -1, -1, 4, -1]
    assert t.right == [-1, 3, -1, 6, 5, -1, 7, -1]
    assert t.depth == [1, 0, 2, 1, 3, 4, 2, 3]
    assert t.inorder() == list(range(8))
    assert t.range_min_index(4, 7) == 6
    assert t.range_min_index(2, 5) == 3
    assert t.range_min_index(0, 7) == 1
    assert t.range_min_index(5, 5) == 5


def test_empty_and_single():
    t = CartesianTree([])
    assert t.root == -1 and t.inorder() == []
    t = CartesianTree([42])
    assert t.root == 0 and t.parent == [-1] and t.inorder() == [0]
    assert t.range_min_index(0, 0) == 0


def test_increasing_is_right_path():
    n = 100_000
    t = CartesianTree(list(range(n)))
    assert t.root == 0
    assert t.right[:-1] == list(range(1, n))
    assert all(x == -1 for x in t.left)
    assert t.depth[-1] == n - 1
    assert t.inorder() == list(range(n))


def test_decreasing_is_left_path():
    n = 100_000
    t = CartesianTree(list(range(n, 0, -1)))
    assert t.root == n - 1
    assert t.left[1:] == list(range(n - 1))
    assert t.inorder() == list(range(n))


def test_equal_values_go_right():
    t = CartesianTree([7] * 5)
    assert t.root == 0 and t.parent == [-1, 0, 1, 2, 3]
    assert t.range_min_index(2, 4) == 2


def test_star_shape():
    # A small minimum in the middle with larger values on both sides.
    t = CartesianTree([5, 0, 5])
    assert t.root == 1 and t.left[1] == 0 and t.right[1] == 2


def test_bad_query():
    t = CartesianTree(EXAMPLE)
    with pytest.raises(IndexError):
        t.range_min_index(3, 2)
    with pytest.raises(IndexError):
        t.range_min_index(0, 8)


def test_random_against_definition():
    rng = random.Random(3)
    for _ in range(700):
        n = rng.randrange(0, 30)
        a = [rng.randrange(0, rng.choice([3, 10, 1000])) for _ in range(n)]
        t = CartesianTree(a)
        assert t.parent == brute_parent(a)
        assert t.inorder() == list(range(n))
        for x in range(n):
            if t.parent[x] != -1:
                assert a[t.parent[x]] <= a[x]
        for _ in range(5):
            if n:
                i = rng.randrange(n)
                j = rng.randrange(i, n)
                assert t.range_min_index(i, j) == min(range(i, j + 1), key=lambda k: (a[k], k))
