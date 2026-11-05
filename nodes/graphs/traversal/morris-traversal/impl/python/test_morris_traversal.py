# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/morris-traversal/. The authors are listed in prov/V880D8.jsonl.

import random

from morris_traversal import morris_traversal


def oracle(left: list[int], right: list[int], root: int) -> list[int]:
    """Independent oracle: inorder with an explicit stack."""
    out: list[int] = []
    stack: list[int] = []
    x = root
    while stack or x != -1:
        while x != -1:
            stack.append(x)
            x = left[x]
        x = stack.pop()
        out.append(x)
        x = right[x]
    return out


def run(left: list[int], right: list[int], root: int) -> list[int]:
    """Run the traversal and check that the tree is restored."""
    left0, right0 = list(left), list(right)
    order = morris_traversal(left, right, root)
    assert left == left0
    assert right == right0
    return order


def test_example() -> None:
    # 4(1, 5), 1(0, 3), 3(2, -), 5(-, 6).
    left = [-1, 0, -1, 2, 1, -1, -1]
    right = [-1, 3, -1, -1, 5, 6, -1]
    assert run(left, right, 4) == [0, 1, 2, 3, 4, 5, 6]
    # The subtree of 1.
    assert run(left, right, 1) == [0, 1, 2, 3]


def test_small_cases() -> None:
    assert run([], [], -1) == []
    assert run([-1], [-1], 0) == [0]
    assert run([1, -1], [-1, -1], 0) == [1, 0]
    assert run([-1, -1], [1, -1], 0) == [0, 1]
    assert run([1, -1, -1], [2, -1, -1], 0) == [1, 0, 2]


def test_long_chains() -> None:
    n = 100000
    left = [i + 1 for i in range(n - 1)] + [-1]
    right = [-1] * n
    assert run(left, right, 0) == list(range(n - 1, -1, -1))
    left = [-1] * n
    right = [i + 1 for i in range(n - 1)] + [-1]
    assert run(left, right, 0) == list(range(n))
    # A zigzag: each node is the right child of a left child.
    left = [-1] * n
    right = [-1] * n
    for i in range(n - 1):
        if i % 2 == 0:
            left[i] = i + 1
        else:
            right[i] = i + 1
    assert run(left, right, 0) == oracle(left, right, 0)


def random_tree(rng: random.Random, n: int) -> tuple[list[int], list[int], int]:
    left = [-1] * n
    right = [-1] * n
    perm = list(range(n))
    rng.shuffle(perm)
    for i in range(1, n):
        while True:
            parent = perm[rng.randrange(i)]
            side = left if rng.random() < 0.5 else right
            if side[parent] == -1:
                side[parent] = perm[i]
                break
    return left, right, perm[0] if n else -1


def test_random_against_oracle() -> None:
    rng = random.Random(1979)
    for _ in range(600):
        n = rng.randint(0, 40)
        left, right, root = random_tree(rng, n)
        assert run(left, right, root) == oracle(left, right, root)


def test_bst_gives_sorted_order() -> None:
    rng = random.Random(197)
    keys = rng.sample(range(10000), 500)
    left = [-1] * len(keys)
    right = [-1] * len(keys)
    for i in range(1, len(keys)):
        x = 0
        while True:
            side = left if keys[i] < keys[x] else right
            if side[x] == -1:
                side[x] = i
                break
            x = side[x]
    order = run(left, right, 0)
    assert [keys[i] for i in order] == sorted(keys)
