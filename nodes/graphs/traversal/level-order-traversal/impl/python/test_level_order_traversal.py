# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/level-order-traversal/. The authors are listed in prov/F8MRDB.jsonl.

import random

from level_order_traversal import level_order_traversal


def oracle(left: list[int], right: list[int], root: int) -> list[int]:
    """Independent oracle: sort by (depth, preorder index), found by a recursive walk."""
    key: dict[int, tuple[int, int]] = {}
    counter = [0]

    def walk(x: int, depth: int) -> None:
        if x == -1:
            return
        key[x] = (depth, counter[0])
        counter[0] += 1
        walk(left[x], depth + 1)
        walk(right[x], depth + 1)

    walk(root, 0)
    return sorted(key, key=lambda x: key[x])


def test_example() -> None:
    # A(B, C), B(D, E), C(-, F), E(G, -), F(H, I) with A..I = 0..8.
    left = [1, 3, -1, -1, 6, 7, -1, -1, -1]
    right = [2, 4, 5, -1, -1, 8, -1, -1, -1]
    assert level_order_traversal(left, right, 0) == [0, 1, 2, 3, 4, 5, 6, 7, 8]
    # The subtree of C.
    assert level_order_traversal(left, right, 2) == [2, 5, 7, 8]


def test_small_cases() -> None:
    assert level_order_traversal([], [], -1) == []
    assert level_order_traversal([-1], [-1], 0) == [0]
    assert level_order_traversal([1, -1], [-1, -1], 0) == [0, 1]
    assert level_order_traversal([-1, -1], [1, -1], 0) == [0, 1]


def test_long_chain_and_complete_tree() -> None:
    n = 100000
    left = [i + 1 for i in range(n - 1)] + [-1]
    right = [-1] * n
    assert level_order_traversal(left, right, 0) == list(range(n))
    # A complete tree in heap layout: level order is 0, 1, ..., n-1.
    left = [2 * i + 1 if 2 * i + 1 < n else -1 for i in range(n)]
    right = [2 * i + 2 if 2 * i + 2 < n else -1 for i in range(n)]
    assert level_order_traversal(left, right, 0) == list(range(n))


def random_tree(rng: random.Random, n: int) -> tuple[list[int], list[int], int]:
    labels = list(range(n))
    rng.shuffle(labels)
    left = [-1] * n
    right = [-1] * n
    free = [(labels[0], 0), (labels[0], 1)]
    for x in labels[1:]:
        p, side = free.pop(rng.randrange(len(free)))
        (left if side == 0 else right)[p] = x
        free.extend([(x, 0), (x, 1)])
    return left, right, labels[0]


def test_random_against_oracle() -> None:
    rng = random.Random(2718)
    for _ in range(600):
        n = rng.randint(1, 40)
        left, right, root = random_tree(rng, n)
        got = level_order_traversal(left, right, root)
        assert got == oracle(left, right, root)
        assert sorted(got) == list(range(n))
