# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rectangle-intersection-sweep/. The authors are listed in prov/KGSR21.jsonl.

import random

from rectangle_intersection_sweep import all_intersecting_pairs, find_intersecting_pair


def meets(a, b) -> bool:
    return a[0] <= b[2] and b[0] <= a[2] and a[1] <= b[3] and b[1] <= a[3]


def brute(rects):
    n = len(rects)
    return [(i, j) for i in range(n) for j in range(i + 1, n) if meets(rects[i], rects[j])]


EXAMPLE = [(1, 1, 3, 2), (2, 4, 5, 6), (4, 0, 7, 3), (6, 5, 9, 7), (8, 1, 10, 4)]


def test_example() -> None:
    assert find_intersecting_pair(EXAMPLE) is None
    moved = EXAMPLE + [(5, 3, 6, 4)]
    assert find_intersecting_pair(moved) == (2, 5)
    assert all_intersecting_pairs(moved) == [(1, 5), (2, 5)]


def test_edges() -> None:
    assert find_intersecting_pair([]) is None
    assert find_intersecting_pair([(0, 0, 1, 1)]) is None
    assert find_intersecting_pair([(0, 0, 1, 1), (1, 1, 2, 2)]) == (0, 1)  # corner touch
    assert find_intersecting_pair([(0, 0, 1, 1), (1, 2, 2, 3)]) is None
    assert find_intersecting_pair([(0, 0, 1, 1), (0, 0, 1, 1)]) == (0, 1)  # identical
    assert find_intersecting_pair([(0, 0, 10, 10), (2, 2, 3, 3)]) == (0, 1)  # nested
    # a long thin rectangle crosses a tall thin one: no corner is inside the other
    assert find_intersecting_pair([(0, 4, 10, 5), (4, 0, 5, 10)]) == (0, 1)
    # equal lower edges: the key (y1, index) breaks the tie
    assert find_intersecting_pair([(0, 2, 1, 3), (5, 2, 6, 3), (5.5, 2, 7, 2.5)]) == (1, 2)


def test_against_brute_force() -> None:
    rng = random.Random(7)
    for _ in range(2000):
        n = rng.randrange(0, 9)
        rects = []
        for _ in range(n):
            x1, y1 = rng.randrange(12), rng.randrange(12)
            rects.append((x1, y1, x1 + rng.randrange(0, 4), y1 + rng.randrange(0, 4)))
        want = brute(rects)
        got = find_intersecting_pair(rects)
        if want:
            assert got is not None and meets(rects[got[0]], rects[got[1]]) and got[0] != got[1]
        else:
            assert got is None
        assert all_intersecting_pairs(rects) == want
