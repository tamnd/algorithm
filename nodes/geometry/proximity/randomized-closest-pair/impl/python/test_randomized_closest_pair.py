# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/randomized-closest-pair/. The authors are listed in prov/KQN34S.jsonl.

import itertools
import random
from fractions import Fraction

from randomized_closest_pair import _shift, randomized_closest_pair


def d2(p, q):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2


def brute(points):
    if len(points) < 2:
        return None
    return min(d2(p, q) for p, q in itertools.combinations(points, 2))


def check(points, seed=0) -> None:
    got = randomized_closest_pair(points, random.Random(seed))
    want = brute(points)
    if want is None:
        assert got is None
        return
    dd, p, q = got
    assert dd == want
    assert d2(p, q) == dd
    assert p in points and q in points
    if p == q:
        assert points.count(p) >= 2


def test_example_every_order() -> None:
    pts = [(0, 0), (1, 9), (3, 6), (4, 2), (5, 3), (7, 0), (8, 8), (9, 5)]
    for seed in range(50):
        dd, p, q = randomized_closest_pair(pts, random.Random(seed))
        assert dd == 2 and {p, q} == {(4, 2), (5, 3)}


def test_small_and_duplicates() -> None:
    assert randomized_closest_pair([]) is None
    assert randomized_closest_pair([(1, 2)]) is None
    assert randomized_closest_pair([(0, 0), (3, 4)])[0] == 25
    assert randomized_closest_pair([(4, 4)] * 5, random.Random(1))[0] == 0
    check([(1, 1), (7, 3), (2, 9), (7, 3), (0, 5)])


def test_negative_and_collinear() -> None:
    check([(-x, 0) for x in (5, 1, 9, 13, 2, 30)])
    check([(x, -2 * x + 1) for x in range(-30, 30, 7)])
    check([(-(10**8), 0), (0, 0), (10**8, 1)])


def test_fractions() -> None:
    pts = [(Fraction(1, 3), Fraction(0)), (Fraction(2, 3), Fraction(1, 7)), (Fraction(5), Fraction(5)), (Fraction(1, 2), Fraction(1, 9))]
    dd, p, q = randomized_closest_pair(pts, random.Random(3))
    assert dd == brute(pts) and d2(p, q) == dd


def test_shift() -> None:
    for v in range(1, 5000):
        e = _shift(v)
        assert 4**e <= v < 4 ** (e + 1)


def test_random_against_all_pairs() -> None:
    rng = random.Random(1976)
    for t in range(800):
        n = rng.randint(0, 40)
        r = rng.choice([1, 3, 10, 1000, 10**9])
        pts = [(rng.randint(-r, r), rng.randint(-r, r)) for _ in range(n)]
        check(pts, seed=t)


def test_expected_rebuild_work_is_linear() -> None:
    # Backwards analysis: step k rebuilds with probability at most 2/(k+1) at cost k+1, so the
    # expected total rebuild work is at most 2n.
    rng = random.Random(11)
    n = 400
    pts = list({(rng.randint(0, 10**6), rng.randint(0, 10**6)) for _ in range(n)})
    total = 0
    runs = 200
    for s in range(runs):
        st: dict[str, int] = {}
        randomized_closest_pair(pts, random.Random(s), st)
        total += st["work"]
    assert total / runs <= 2.5 * len(pts)
