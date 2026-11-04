# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quadratic-split/. The authors are listed in prov/4EXTW1.jsonl.
import itertools
import random

import pytest

from quadratic_split import pick_seeds, quadratic_split, split_cost, waste

# a, b, c, d, e of the page example
RECTS = [(0, 0, 2, 2), (1, 5, 3, 7), (6, 0, 8, 1), (7, 6, 9, 9), (2, 1, 3, 3)]


def test_page_example():
    w = {(i, j): waste(RECTS[i], RECTS[j]) for i in range(5) for j in range(i + 1, 5)}
    assert w[(0, 3)] == 71 and max(w.values()) == 71
    assert pick_seeds(RECTS) == (0, 3)
    g1, g2 = quadratic_split(RECTS, 2)
    assert g1 == [0, 4, 1] and g2 == [3, 2]  # {a, e, b} and {d, c}
    assert split_cost(RECTS, g1, g2) == 21 + 27


def test_edge_cases():
    assert quadratic_split([(0, 0, 1, 1), (5, 5, 6, 6)], 1) == ([0], [1])
    same = [(0, 0, 1, 1)] * 5
    g1, g2 = quadratic_split(same, 2)
    assert sorted(g1 + g2) == list(range(5)) and min(len(g1), len(g2)) >= 2
    pts = [(i, i, i, i) for i in range(6)]  # zero-area rectangles
    g1, g2 = quadratic_split(pts, 3)
    assert len(g1) == 3 and len(g2) == 3
    with pytest.raises(ValueError):
        quadratic_split(RECTS, 3)
    with pytest.raises(ValueError):
        quadratic_split(RECTS[:1], 1)


def best_cost(rects, m):
    n = len(rects)
    best = None
    for size in range(m, n - m + 1):
        for g1 in itertools.combinations(range(n), size):
            g2 = [k for k in range(n) if k not in g1]
            c = split_cost(rects, list(g1), g2)
            best = c if best is None or c < best else best
    return best


def test_random_against_brute_force():
    rng = random.Random(4)
    worse = 0
    for _ in range(600):
        n = rng.randint(2, 9)
        m = rng.randint(1, n // 2)
        rects = []
        for _ in range(n):
            x, y = rng.randint(0, 20), rng.randint(0, 20)
            rects.append((x, y, x + rng.randint(0, 6), y + rng.randint(0, 6)))
        g1, g2 = quadratic_split(rects, m)
        assert sorted(g1 + g2) == list(range(n))
        assert len(g1) >= m and len(g2) >= m
        i, j = pick_seeds(rects)
        assert g1[0] == i and g2[0] == j
        assert waste(rects[i], rects[j]) == max(
            waste(rects[a], rects[b]) for a in range(n) for b in range(a + 1, n))
        opt = best_cost(rects, m)
        assert split_cost(rects, g1, g2) >= opt
        worse += split_cost(rects, g1, g2) > opt
    assert worse > 0  # the heuristic is not optimal
