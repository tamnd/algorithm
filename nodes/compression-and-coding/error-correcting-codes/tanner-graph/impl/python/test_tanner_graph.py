# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tanner-graph/. The authors are listed in prov/68B1G5.jsonl.

import itertools
import random
from collections import deque

from tanner_graph import TannerGraph

H74 = [[1, 0, 1, 1, 1, 0, 0], [1, 1, 1, 0, 0, 1, 0], [0, 1, 1, 1, 0, 0, 1]]


def girth_by_edge_removal(h):
    """Oracle: for each edge (i, j), remove it and find the distance from
    check i to variable j by BFS; the girth is the least distance + 1."""
    m, n = len(h), len(h[0])
    best = None
    for i in range(m):
        for j in range(n):
            if not h[i][j]:
                continue
            start, goal = ("c", i), ("v", j)
            dist = {start: 0}
            q = deque([start])
            while q:
                kind, x = q.popleft()
                nb = [("v", y) for y in range(n) if h[x][y]] if kind == "c" else [("c", y) for y in range(m) if h[y][x]]
                for w in nb:
                    if (kind, x) == start and w == goal:
                        continue
                    if w not in dist:
                        dist[w] = dist[(kind, x)] + 1
                        q.append(w)
            if goal in dist:
                c = dist[goal] + 1
                best = c if best is None else min(best, c)
    return best


def largest_stopping_subset(g, erased):
    best = set()
    for r in range(len(erased) + 1):
        for s in itertools.combinations(sorted(erased), r):
            if g.is_stopping_set(set(s)):
                best |= set(s)
    return best


def test_hamming_example() -> None:
    g = TannerGraph(H74)
    assert g.check_invariant()
    assert g.edges() == 12
    assert g.var_adj[2] == [0, 1, 2] and g.chk_adj[0] == [0, 2, 3, 4]
    assert g.girth() == 4
    assert g.syndrome([1, 0, 1, 1, 1, 0, 0]) == [0, 0, 0]
    assert g.syndrome([0, 0, 1, 0, 0, 0, 0]) == [1, 1, 1]
    # Positions 0, 1, 2 erased: every check sees two or three of them, so peeling stops.
    assert g.is_stopping_set({0, 1, 2})
    assert g.peel({0, 1, 2}) == {0, 1, 2}
    assert g.peel({0, 1, 4}) == set()


def test_tree_and_edge_cases() -> None:
    tree = [[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1]]
    assert TannerGraph(tree).girth() is None
    assert TannerGraph([[1, 1, 1]]).girth() is None
    assert TannerGraph([[1, 1], [1, 1]]).girth() == 4
    six = [[1, 1, 0], [0, 1, 1], [1, 0, 1]]
    assert TannerGraph(six).girth() == 6
    g = TannerGraph([[0, 0, 0]])
    assert g.edges() == 0 and g.girth() is None and g.peel({0, 1}) == {0, 1}


def test_girth_against_oracle() -> None:
    rng = random.Random(17)
    for _ in range(500):
        m, n = rng.randrange(1, 6), rng.randrange(1, 8)
        p = rng.uniform(0.2, 0.6)
        h = [[int(rng.random() < p) for _ in range(n)] for _ in range(m)]
        g = TannerGraph(h)
        assert g.check_invariant()
        assert g.girth() == girth_by_edge_removal(h)


def test_peeling_leaves_largest_stopping_set() -> None:
    rng = random.Random(23)
    for _ in range(500):
        m, n = rng.randrange(1, 5), rng.randrange(1, 9)
        h = [[rng.randrange(2) for _ in range(n)] for _ in range(m)]
        g = TannerGraph(h)
        erased = {j for j in range(n) if rng.random() < 0.5}
        left = g.peel(erased)
        assert g.is_stopping_set(left)
        assert left == largest_stopping_subset(g, erased)
