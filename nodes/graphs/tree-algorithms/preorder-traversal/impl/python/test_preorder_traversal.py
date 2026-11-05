# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/preorder-traversal/. The authors are listed in prov/K1CRY0.jsonl.

import random

from preorder_traversal import children_from_parents, preorder


def oracle(children: list[list[int]], root: int) -> list[int]:
    # Preorder is the lexicographic order of the root paths, written as child positions.
    key = {root: ()}
    todo = [root]
    while todo:
        v = todo.pop()
        for i, c in enumerate(children[v]):
            key[c] = key[v] + (i,)
            todo.append(c)
    return sorted(key, key=lambda v: key[v])


def test_example() -> None:
    children = [[1, 2], [3, 4], [5], [], [6, 7], [], [], []]
    assert preorder(children, 0) == [0, 1, 3, 4, 6, 7, 2, 5]


def test_single_vertex_and_empty() -> None:
    assert preorder([[]], 0) == [0]
    assert preorder([], 0) == []


def test_path_long() -> None:
    n = 100_000
    children = [[v + 1] for v in range(n - 1)] + [[]]
    assert preorder(children, 0) == list(range(n))


def test_star() -> None:
    n = 50
    children = [list(range(1, n))] + [[] for _ in range(n - 1)]
    assert preorder(children, 0) == list(range(n))
    # the same star rooted at the leaf 1
    children = [list(range(2, n)), [0]] + [[] for _ in range(n - 2)]
    assert preorder(children, 1) == [1, 0] + list(range(2, n))


def test_child_order_matters() -> None:
    assert preorder([[2, 1], [], []], 0) == [0, 2, 1]


def test_random_against_oracle() -> None:
    rng = random.Random(7031)
    for _ in range(600):
        n = rng.randint(1, 40)
        perm = list(range(n))
        rng.shuffle(perm)
        parent = [-1] * n
        for i in range(1, n):
            parent[perm[i]] = perm[rng.randrange(i)]
        children, root = children_from_parents(parent)
        for lst in children:
            rng.shuffle(lst)
        got = preorder(children, root)
        assert got == oracle(children, root)
        assert sorted(got) == list(range(n))
