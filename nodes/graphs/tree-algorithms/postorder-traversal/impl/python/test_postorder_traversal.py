# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/postorder-traversal/. The authors are listed in prov/M0CFJK.jsonl.

import random

from postorder_traversal import evaluate, postorder

INF = float("inf")


def oracle(children: list[list[int]], root: int) -> list[int]:
    # Postorder sorts the root paths (child positions) with an end marker larger than any position.
    key = {root: ()}
    todo = [root]
    while todo:
        v = todo.pop()
        for i, c in enumerate(children[v]):
            key[c] = key[v] + (i,)
            todo.append(c)
    return sorted(key, key=lambda v: key[v] + (INF,))


def test_example() -> None:
    children = [[1, 2], [3, 4], [5], [], [6, 7], [], [], []]
    assert postorder(children, 0) == [3, 6, 7, 4, 1, 5, 2, 0]


def test_expression() -> None:
    # (2 + 3) * (4 + 1 + 5) = 50
    children = [[1, 2], [3, 4], [5, 6, 7], [], [], [], [], []]
    label = ["*", "+", "+", "2", "3", "4", "1", "5"]
    assert evaluate(children, label) == 50


def test_single_vertex_and_empty() -> None:
    assert postorder([[]], 0) == [0]
    assert postorder([], 0) == []


def test_path_long() -> None:
    n = 100_000
    children = [[v + 1] for v in range(n - 1)] + [[]]
    assert postorder(children, 0) == list(range(n - 1, -1, -1))


def test_star() -> None:
    n = 50
    children = [list(range(1, n))] + [[] for _ in range(n - 1)]
    assert postorder(children, 0) == list(range(1, n)) + [0]


def test_children_before_parent() -> None:
    rng = random.Random(11)
    for _ in range(200):
        n = rng.randint(1, 30)
        parent = [-1] + [rng.randrange(i) for i in range(1, n)]
        children = [[] for _ in range(n)]
        for v in range(1, n):
            children[parent[v]].append(v)
        pos = {v: i for i, v in enumerate(postorder(children, 0))}
        assert all(pos[v] < pos[parent[v]] for v in range(1, n))


def test_random_against_oracle() -> None:
    rng = random.Random(4402)
    for _ in range(600):
        n = rng.randint(1, 40)
        perm = list(range(n))
        rng.shuffle(perm)
        children = [[] for _ in range(n)]
        for i in range(1, n):
            children[perm[rng.randrange(i)]].append(perm[i])
        for lst in children:
            rng.shuffle(lst)
        root = perm[0]
        assert postorder(children, root) == oracle(children, root)
