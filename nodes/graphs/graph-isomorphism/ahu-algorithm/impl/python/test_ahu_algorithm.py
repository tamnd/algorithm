# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ahu-algorithm/. The authors are listed in prov/9MMJGB.jsonl.

import itertools
import random

from ahu_algorithm import ahu_isomorphic, free_trees_isomorphic, tree_centers


def brute_rooted(n: int, e1: list[tuple[int, int]], r1: int, e2: list[tuple[int, int]], r2: int) -> bool:
    s2 = {frozenset(e) for e in e2}
    for p in itertools.permutations(range(n)):
        if p[r1] == r2 and all(frozenset((p[u], p[v])) in s2 for u, v in e1):
            return True
    return False


def random_tree(rng: random.Random, n: int) -> list[tuple[int, int]]:
    return [(v, rng.randrange(v)) for v in range(1, n)]


def relabel(rng: random.Random, n: int, edges: list[tuple[int, int]]) -> tuple[list[int], list[tuple[int, int]]]:
    p = list(range(n))
    rng.shuffle(p)
    return p, [(p[u], p[v]) for u, v in edges]


def test_page_example() -> None:
    t1 = (8, [(0, 1), (0, 2), (0, 3), (1, 4), (1, 5), (2, 6), (6, 7)], 0)
    t2 = (8, [(7, 5), (7, 3), (7, 0), (5, 1), (5, 6), (3, 2), (2, 4)], 7)
    t3 = (8, [(0, 1), (0, 2), (0, 3), (1, 4), (1, 5), (1, 6), (4, 7)], 0)
    assert ahu_isomorphic(t1, t2)
    assert not ahu_isomorphic(t1, t3)
    assert brute_rooted(8, t1[1], 0, t2[1], 7)
    assert not brute_rooted(8, t1[1], 0, t3[1], 0)


def test_edges() -> None:
    assert ahu_isomorphic((1, [], 0), (1, [], 0))
    assert not ahu_isomorphic((1, [], 0), (2, [(0, 1)], 0))
    path = (4, [(0, 1), (1, 2), (2, 3)], 0)
    star = (4, [(0, 1), (0, 2), (0, 3)], 0)
    assert not ahu_isomorphic(path, star)
    # The same free path rooted at an end and at an inner vertex.
    assert not ahu_isomorphic(path, (4, [(0, 1), (1, 2), (2, 3)], 1))
    assert free_trees_isomorphic((4, path[1]), (4, [(2, 0), (0, 3), (3, 1)]))
    assert not free_trees_isomorphic((4, path[1]), (4, star[1]))
    assert tree_centers(4, path[1]) == [1, 2]
    assert tree_centers(5, [(0, 1), (1, 2), (2, 3), (3, 4)]) == [2]


def test_random_rooted_against_brute_force() -> None:
    rng = random.Random(9031)
    for _ in range(600):
        n = rng.randint(1, 7)
        e1 = random_tree(rng, n)
        r1 = rng.randrange(n)
        if rng.random() < 0.5:
            p, e2 = relabel(rng, n, e1)
            r2 = p[r1]
        else:
            e2 = random_tree(rng, n)
            r2 = rng.randrange(n)
        assert ahu_isomorphic((n, e1, r1), (n, e2, r2)) == brute_rooted(n, e1, r1, e2, r2)


def test_random_free_against_brute_force() -> None:
    rng = random.Random(4417)
    for _ in range(500):
        n = rng.randint(1, 7)
        e1 = random_tree(rng, n)
        e2 = relabel(rng, n, e1)[1] if rng.random() < 0.5 else random_tree(rng, n)
        want = any(brute_rooted(n, e1, 0, e2, r) for r in range(n))
        assert free_trees_isomorphic((n, e1), (n, e2)) == want


def test_large_relabeled() -> None:
    rng = random.Random(77)
    for _ in range(20):
        n = rng.randint(50, 400)
        e1 = random_tree(rng, n)
        p, e2 = relabel(rng, n, e1)
        assert ahu_isomorphic((n, e1, 0), (n, e2, p[0]))
        assert free_trees_isomorphic((n, e1), (n, e2))
        # a deep path does not overflow the stack
    n = 5000
    path = [(i, i + 1) for i in range(n - 1)]
    assert ahu_isomorphic((n, path, 0), (n, list(reversed(path)), n - 1))
