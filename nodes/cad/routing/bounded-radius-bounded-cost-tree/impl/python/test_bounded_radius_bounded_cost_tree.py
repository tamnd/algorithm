# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bounded-radius-bounded-cost-tree/. The authors are listed in prov/58DVMM.jsonl.

import random
from fractions import Fraction

from bounded_radius_bounded_cost_tree import brbc, l1, tree_cost


def mst_length(pts: list[tuple[int, int]]) -> int:
    """Kruskal on all pairs, written apart from the tree builder."""
    n = len(pts)
    parent = list(range(n))

    def find(a: int) -> int:
        while parent[a] != a:
            a = parent[a]
        return a

    total = 0
    for d, i, j in sorted((l1(pts[i], pts[j]), i, j) for i in range(n) for j in range(i + 1, n)):
        if find(i) != find(j):
            parent[find(i)] = find(j)
            total += d
    return total


def path_lengths(pts: list[tuple[int, int]], parent: list[int], source: int) -> list[int]:
    """Length of the tree path from the source to each point, by walking up the parents."""
    out = []
    for v in range(len(pts)):
        total, seen = 0, set()
        while v != source:
            assert v not in seen and parent[v] >= 0
            seen.add(v)
            total += l1(pts[v], pts[parent[v]])
            v = parent[v]
        out.append(total)
    return out


EXAMPLE = [(0, 0), (1, 3), (2, 6), (3, 9), (6, 9), (9, 9), (9, 6), (9, 3), (9, 0)]


def test_example() -> None:
    parent, d, cuts = brbc(EXAMPLE, 1)
    assert mst_length(EXAMPLE) == 27 and max(l1(EXAMPLE[0], p) for p in EXAMPLE) == 18
    assert cuts == [6, 3]
    assert d == [0, 4, 8, 12, 15, 18, 15, 18, 21]
    assert tree_cost(EXAMPLE, parent) == 47
    parent, d, cuts = brbc(EXAMPLE, 100)
    assert cuts == [] and tree_cost(EXAMPLE, parent) == 27 and max(d) == 27


def test_edges() -> None:
    assert brbc([], 1) == ([], [], [])
    assert brbc([(5, 5)], 1) == ([-1], [0], [])
    parent, d, _ = brbc([(0, 0), (3, 1)], Fraction(1, 4))
    assert parent == [-1, 0] and d == [0, 4]


def test_bounds(seed: int = 37) -> None:
    rng = random.Random(seed)
    for _ in range(300):
        n = rng.randint(1, 16)
        pts = [(rng.randint(0, 40), rng.randint(0, 40)) for _ in range(n)]
        s = rng.randrange(n)
        eps = rng.choice([Fraction(1, 10), Fraction(1, 4), Fraction(1, 2), Fraction(1), Fraction(3)])
        parent, d, _ = brbc(pts, eps, s)
        assert d == path_lengths(pts, parent, s)
        R = max(l1(pts[s], p) for p in pts)
        assert all(x <= (1 + eps) * R for x in d)
        assert tree_cost(pts, parent) <= (1 + 2 / eps) * mst_length(pts)
