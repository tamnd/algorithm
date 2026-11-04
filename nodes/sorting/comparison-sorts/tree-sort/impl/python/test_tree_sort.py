# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tree-sort/. The authors are listed in prov/P5E3N3.jsonl.

import random

from tree_sort import inorder, insert, tree_sort


def test_example() -> None:
    a = [5, 3, 8, 1, 4, 7, 9, 2, 6]
    assert tree_sort(a) == 16
    assert a == list(range(1, 10))


def test_sorted_input_is_quadratic() -> None:
    a = list(range(10))
    assert tree_sort(a) == 45
    a = list(range(3000))
    assert tree_sort(a) == 3000 * 2999 // 2


def test_inorder() -> None:
    root = None
    for x in [2, 1, 3]:
        root, _ = insert(root, x)
    assert inorder(root) == [1, 2, 3]
    assert inorder(None) == []


def test_edges() -> None:
    for a in ([], [1], [2, 1], [1, 1, 1], [3, 2, 1]):
        b = list(a)
        tree_sort(b)
        assert b == sorted(a)


def test_stable() -> None:
    class Key:
        def __init__(self, k: int, tag: int) -> None:
            self.k, self.tag = k, tag

        def __lt__(self, other: "Key") -> bool:
            return self.k < other.k

    rng = random.Random(4)
    for _ in range(200):
        pairs = [(rng.randint(0, 4), i) for i in range(rng.randint(0, 30))]
        b = [Key(k, t) for k, t in pairs]
        tree_sort(b)
        assert [(x.k, x.tag) for x in b] == sorted(pairs)


def test_random_against_sorted() -> None:
    rng = random.Random(9)
    for _ in range(100):
        a = [rng.randint(-50, 50) for _ in range(rng.randint(0, 200))]
        b = list(a)
        tree_sort(b)
        assert b == sorted(a)
