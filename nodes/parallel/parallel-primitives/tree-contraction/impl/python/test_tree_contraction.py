# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tree-contraction/. The authors are listed in prov/TWC8P7.jsonl.

import math
import random

import pytest

from tree_contraction import Stats, subtree_sums


def relabel(parent: list[int | None], rng: random.Random) -> list[int | None]:
    n = len(parent)
    perm = list(range(n))
    rng.shuffle(perm)
    out: list[int | None] = [None] * n
    for v in range(n):
        p = parent[v]
        out[perm[v]] = None if p is None else perm[p]
    return out


def random_binary_tree(n: int, rng: random.Random) -> list[int | None]:
    parent: list[int | None] = [None] * n
    free = [0] if n else []  # nodes with fewer than two children
    count = [0] * n
    for v in range(1, n):
        p = rng.choice(free)
        parent[v] = p
        count[p] += 1
        if count[p] == 2:
            free.remove(p)
        free.append(v)
    return parent


def path(n: int) -> list[int | None]:
    return [None] + list(range(n - 1)) if n else []


def complete(n: int) -> list[int | None]:
    return [None] + [(v - 1) // 2 for v in range(1, n)] if n else []


def caterpillar(n: int) -> list[int | None]:
    # a spine 0, 2, 4, ... and a leaf hanging from each spine node
    parent: list[int | None] = [None] * n
    for v in range(1, n):
        parent[v] = v - 2 if v % 2 == 0 else v - 1
    return parent


def stack_sums(parent: list[int | None], weight: list[int]) -> list[int]:
    """Reference: a postorder walk with an explicit stack."""
    n = len(parent)
    children: list[list[int]] = [[] for _ in range(n)]
    for v in range(n):
        if parent[v] is not None:
            children[parent[v]].append(v)  # type: ignore[index]
    sub = [0] * n
    for r in range(n):
        if parent[r] is None:
            stack = [(r, False)]
            while stack:
                v, done = stack.pop()
                if done:
                    sub[v] = weight[v] + sum(sub[c] for c in children[v])
                else:
                    stack.append((v, True))
                    stack.extend((c, False) for c in children[v])
    return sub


def test_example() -> None:
    parent = [None, 0, 0, 1, 3, 3, 2, 6, 7]
    weight = [1] * 9
    assert subtree_sums(parent, weight, random.Random(0)) == [9, 4, 4, 3, 1, 1, 3, 2, 1]


def test_edges() -> None:
    rng = random.Random(0)
    assert subtree_sums([], [], rng) == []
    assert subtree_sums([None], [5], rng) == [5]
    assert subtree_sums([None, 0], [2, 3], rng) == [5, 3]
    assert subtree_sums([None, None], [2, 3], rng) == [2, 3]
    with pytest.raises(ValueError):
        subtree_sums([None, 0, 0, 0], [1, 1, 1, 1], rng)


def test_random_against_stack() -> None:
    rng = random.Random(1985)
    shapes = [random_binary_tree, path, complete, caterpillar]
    for k in range(600):
        n = rng.choice([1, 2, 3, 4, 5, 7, 8, 9, 16, 31, 32, 50, 100])
        parent = relabel(shapes[k % 4](n) if k % 4 else random_binary_tree(n, rng), rng)
        weight = [rng.randint(-50, 50) for _ in range(n)]
        assert subtree_sums(parent, weight, rng) == stack_sums(parent, weight)


def test_forest() -> None:
    rng = random.Random(2)
    for _ in range(100):
        a, b = random_binary_tree(rng.randint(1, 20), rng), random_binary_tree(rng.randint(1, 20), rng)
        shift = len(a)
        parent = relabel(a + [None if p is None else p + shift for p in b], rng)
        weight = [rng.randint(0, 9) for _ in parent]
        assert subtree_sums(parent, weight, rng) == stack_sums(parent, weight)


def test_fraction_removed_and_rounds() -> None:
    # each round removes at least m / 8 non-root nodes in expectation, m = live - 1,
    # so the mean number of rounds is at most log_{8/7}(n - 1) + 9
    rng = random.Random(4)
    for n in [2, 16, 100, 1000]:
        for shape in ["random", "path", "complete", "caterpillar"]:
            rounds, ratio, count = 0, 0.0, 0
            trials = 10
            for _ in range(trials):
                parent = {
                    "random": lambda: random_binary_tree(n, rng),
                    "path": lambda: path(n),
                    "complete": lambda: complete(n),
                    "caterpillar": lambda: caterpillar(n),
                }[shape]()
                st = Stats()
                subtree_sums(relabel(parent, rng), [1] * n, rng, st)
                rounds += len(st.live)
                for lv, r, c in zip(st.live, st.raked, st.compressed):
                    ratio += (r + c) / (lv - 1)
                    count += 1
            assert ratio / count >= 1 / 8
            assert rounds / trials <= math.log(n - 1, 8 / 7) + 9 if n > 2 else rounds / trials <= 9
