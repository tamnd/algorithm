# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterated-one-steiner/. The authors are listed in prov/S1Z8DM.jsonl.

import random
from itertools import combinations

from iterated_one_steiner import iterated_one_steiner, l1, length, mst


def exact_rsmt(pins: list[tuple[int, int]]) -> int:
    """Brute force: the least MST length over pins plus at most n - 2 points of the Hanan grid."""
    xs = sorted({p[0] for p in pins})
    ys = sorted({p[1] for p in pins})
    cand = [(x, y) for x in xs for y in ys if (x, y) not in set(pins)]
    best = length(mst(pins))
    for k in range(1, max(len(pins) - 1, 1)):
        for extra in combinations(cand, k):
            best = min(best, length(mst(pins + list(extra))))
    return best


def is_tree_on(pts: list[tuple[int, int]], tree: list[tuple[int, int, int]]) -> bool:
    n = len(pts)
    if len(tree) != max(n - 1, 0):
        return False
    parent = list(range(n))

    def find(a: int) -> int:
        while parent[a] != a:
            a = parent[a]
        return a

    for d, a, b in tree:
        if d != l1(pts[a], pts[b]) or find(a) == find(b):
            return False
        parent[find(a)] = find(b)
    return True


def test_plus() -> None:
    pins = [(1, 0), (0, 1), (2, 1), (1, 2)]
    pts, tree = iterated_one_steiner(pins)
    assert pts == pins + [(1, 1)]
    assert length(tree) == 4 == exact_rsmt(pins)


def test_five_points() -> None:
    pins = [(0, 0), (4, 1), (1, 4), (5, 5), (2, 3)]
    pts, tree = iterated_one_steiner(pins)
    assert length(mst(pins)) == 16
    assert length(tree) == 13 == exact_rsmt(pins)
    assert is_tree_on(pts, tree)


def test_edges() -> None:
    assert iterated_one_steiner([]) == ([], [])
    assert iterated_one_steiner([(2, 2)]) == ([(2, 2)], [])
    pts, tree = iterated_one_steiner([(0, 0), (3, 4)])
    assert length(tree) == 7 and len(pts) == 2


def test_against_exact(seed: int = 23) -> None:
    rng = random.Random(seed)
    for _ in range(150):
        n = rng.randint(2, 5)
        pins = [(rng.randint(0, 9), rng.randint(0, 9)) for _ in range(n)]
        pins = list(dict.fromkeys(pins))
        pts, tree = iterated_one_steiner(pins)
        assert pts[: len(pins)] == pins and is_tree_on(pts, tree)
        opt = exact_rsmt(pins)
        assert opt <= length(tree) <= length(mst(pins))
        if len(pins) <= 3:
            assert length(tree) == opt
    for _ in range(4):
        pins = list(dict.fromkeys((rng.randint(0, 20), rng.randint(0, 20)) for _ in range(6)))
        pts, tree = iterated_one_steiner(pins)
        assert exact_rsmt(pins) <= length(tree) <= length(mst(pins))
