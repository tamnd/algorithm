# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/closest-pair-sweep-line/. The authors are listed in prov/12AV55.jsonl.

import itertools
import random
from fractions import Fraction

from closest_pair_sweep_line import _ActiveSet, closest_pair_sweep_line, dist2


def brute(points):
    if len(points) < 2:
        return None
    return min(dist2(p, q) for p, q in itertools.combinations(points, 2))


def check(points) -> None:
    got = closest_pair_sweep_line(points)
    want = brute(points)
    if want is None:
        assert got is None
        return
    d2, p, q = got
    assert d2 == want
    assert dist2(p, q) == d2
    assert p in points and q in points
    if p == q:
        assert points.count(p) >= 2


def test_example() -> None:
    pts = [(0, 0), (1, 9), (3, 6), (4, 2), (5, 3), (7, 0), (8, 8), (9, 5)]
    d2, p, q = closest_pair_sweep_line(pts)
    assert d2 == 2 and {p, q} == {(4, 2), (5, 3)}


def test_small_sizes() -> None:
    assert closest_pair_sweep_line([]) is None
    assert closest_pair_sweep_line([(3, 4)]) is None
    assert closest_pair_sweep_line([(0, 0), (3, 4)])[0] == 25
    check([(0, 0), (5, 5), (1, 1)])


def test_duplicates() -> None:
    assert closest_pair_sweep_line([(1, 1), (7, 3), (2, 9), (7, 3), (0, 5)])[0] == 0
    assert closest_pair_sweep_line([(4, 4)] * 7)[0] == 0


def test_collinear_and_same_coordinate() -> None:
    check([(0, y) for y in (0, 10, 3, 7, 20, 21, 40)])
    check([(x, 0) for x in (5, 1, 9, 13, 2, 30)])
    check([(x, 3 * x - 2) for x in range(-20, 20, 3)])
    check([(x % 4, x // 4) for x in range(40)])


def test_float_root_pitfall() -> None:
    a, b, c = (0, 0), (10**8, 1), (-(10**8), 0)
    d2, p, q = closest_pair_sweep_line([a, b, c])
    assert d2 == 10**16 and {p, q} == {a, c}


def test_fractions() -> None:
    check([(Fraction(1, 3), Fraction(0)), (Fraction(2, 3), Fraction(1, 7)), (Fraction(5), Fraction(5)), (Fraction(1, 2), Fraction(1, 9))])


def test_active_set_against_sorted_list() -> None:
    rng = random.Random(5)
    for _ in range(50):
        n = rng.randint(1, 40)
        s = _ActiveSet(n)
        active = set()
        for _ in range(200):
            r = rng.randrange(n)
            if r in active:
                s.delete(r)
                active.discard(r)
            else:
                s.insert(r)
                active.add(r)
            q = rng.randrange(n)
            above = [x for x in active if x > q]
            below = [x for x in active if x < q]
            assert s.successor(q) == (min(above) if above else None)
            assert s.predecessor(q) == (max(below) if below else None)


def test_random_against_all_pairs() -> None:
    rng = random.Random(1988)
    for _ in range(700):
        n = rng.randint(0, 40)
        r = rng.choice([1, 3, 10, 1000])
        pts = [(rng.randint(-r, r), rng.randint(-r, r)) for _ in range(n)]
        check(pts)


def test_packing_bound() -> None:
    rng = random.Random(77)
    worst = 0
    for _ in range(300):
        n = rng.randint(2, 80)
        r = rng.choice([3, 6, 30])
        pts = list({(rng.randint(-r, r), rng.randint(-r, r)) for _ in range(n)})
        stats: list[int] = []
        closest_pair_sweep_line(pts, stats)
        worst = max([worst] + stats)
    stats = []
    closest_pair_sweep_line([(x, y) for x in range(9) for y in range(9)], stats)
    worst = max([worst] + stats)
    assert worst <= 8
