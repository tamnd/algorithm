# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bst-search/. The authors are listed in prov/EJR7Z3.jsonl.

import random

from bst_search import Node, insert, tree_search, tree_search_path


def build(keys: list[int]) -> Node[int, int] | None:
    root = None
    for k in keys:
        root = insert(root, k, 10 * k)
    return root


def test_example() -> None:
    root = build([15, 6, 18, 3, 7, 17, 20, 2, 4, 13, 9])
    x = tree_search(root, 13)
    assert x is not None and x.value == 130
    assert tree_search_path(root, 13) == [15, 6, 7, 13]
    assert tree_search(root, 8) is None
    assert tree_search_path(root, 8) == [15, 6, 7, 13, 9]
    assert tree_search_path(root, 15) == [15]


def test_edges() -> None:
    assert tree_search(None, 1) is None
    root = build([5])
    assert tree_search(root, 5) is root
    assert tree_search(root, 4) is None and tree_search(root, 6) is None


def test_chain_is_linear() -> None:
    root = build(list(range(5000)))
    assert tree_search(root, 4999) is not None
    assert len(tree_search_path(root, 4999)) == 5000
    assert tree_search(root, 5000) is None


def test_random_against_set() -> None:
    rng = random.Random(7351)
    for _ in range(600):
        keys = [rng.randint(-40, 40) for _ in range(rng.randint(0, 30))]
        root = build(keys)
        s = set(keys)
        for q in range(-45, 46):
            x = tree_search(root, q)
            assert (x is not None) == (q in s)
            if x is not None:
                assert x.key == q and x.value == 10 * q
