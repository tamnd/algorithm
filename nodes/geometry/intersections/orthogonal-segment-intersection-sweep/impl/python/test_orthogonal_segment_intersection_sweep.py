# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/orthogonal-segment-intersection-sweep/. The authors are listed in prov/AM0665.jsonl.

import random
from fractions import Fraction

from orthogonal_segment_intersection_sweep import _YSet, orthogonal_intersections


def brute(hs: list, vs: list) -> list:
    out = []
    for i, (y, a, b) in enumerate(hs):
        for j, (x, c, d) in enumerate(vs):
            if min(a, b) <= x <= max(a, b) and min(c, d) <= y <= max(c, d):
                out.append((i, j))
    return sorted(out)


def test_example() -> None:
    hs = [(1, 0, 6), (3, 2, 9), (5, 1, 4), (3, 7, 8)]
    vs = [(2, 0, 4), (5, 2, 6), (8, 3, 3), (0, 2, 9)]
    got = orthogonal_intersections(hs, vs)
    assert sorted(got) == brute(hs, vs) == [(0, 0), (1, 0), (1, 1), (1, 2), (3, 2)]


def test_small_and_degenerate() -> None:
    assert orthogonal_intersections([], []) == []
    assert orthogonal_intersections([(0, 0, 5)], []) == []
    assert orthogonal_intersections([], [(0, 0, 5)]) == []
    # corner touch, T-junction, a point segment on both lists, reversed end points
    assert orthogonal_intersections([(0, 0, 4)], [(4, 0, 3)]) == [(0, 0)]
    assert orthogonal_intersections([(2, 0, 4)], [(1, 2, 7)]) == [(0, 0)]
    assert orthogonal_intersections([(3, 3, 3)], [(3, 3, 3)]) == [(0, 0)]
    assert orthogonal_intersections([(0, 4, 0)], [(2, 5, -5)]) == [(0, 0)]
    # a vertical segment that ends just below a horizontal one
    assert orthogonal_intersections([(5, 0, 4)], [(2, 0, 4)]) == []
    # equal y values in several horizontals
    hs = [(1, 0, 2), (1, 1, 3), (1, 5, 6)]
    assert sorted(orthogonal_intersections(hs, [(2, 0, 1)])) == [(0, 0), (1, 0)]
    assert orthogonal_intersections([(F := Fraction(1, 3), 0, 1)], [(Fraction(1, 2), 0, F)]) == [(0, 0)]


def test_grid() -> None:
    m = 7
    hs = [(i, 0, m) for i in range(m)]
    vs = [(i, 0, m) for i in range(m)]
    assert sorted(orthogonal_intersections(hs, vs)) == brute(hs, vs)
    assert len(brute(hs, vs)) == m * m


def test_random_against_brute_force() -> None:
    rng = random.Random(1980)
    for _ in range(1500):
        r = rng.choice([2, 3, 5, 10, 40])
        hs = [(rng.randint(0, r), rng.randint(0, r), rng.randint(0, r)) for _ in range(rng.randint(0, 8))]
        vs = [(rng.randint(0, r), rng.randint(0, r), rng.randint(0, r)) for _ in range(rng.randint(0, 8))]
        assert sorted(orthogonal_intersections(hs, vs)) == brute(hs, vs)


def test_yset_invariant() -> None:
    rng = random.Random(5)
    for _ in range(200):
        ys = sorted(rng.sample(range(50), rng.randint(1, 12)))
        t = _YSet(ys)
        model: dict[int, set] = {}
        for step in range(40):
            i = rng.randrange(len(ys))
            if model.get(i) and rng.random() < 0.5:
                h = model[i].pop()
                t.delete(i, h)
            else:
                model.setdefault(i, set()).add(step)
                t.insert(i, step)
            t.check_invariant()
            q = rng.randrange(len(ys) + 1)
            want = min([j for j in model if model[j] and j >= q], default=-1)
            assert t.first_at_least(q) == want
