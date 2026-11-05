# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interval-piercing-greedy/. The authors are listed in prov/V30M7R.jsonl.
import itertools
import random

from interval_piercing_greedy import interval_piercing_greedy


def contains(iv, x, kind):
    l, r = iv
    if kind == "closed":
        return l <= x <= r
    if kind == "half-open":
        return l <= x < r
    return l < x < r


def pierces(points, intervals, kind):
    return all(any(contains(iv, x, kind) for x in points) for iv in intervals)


def brute(intervals, kind, span):
    """Fewest points, searching the half-integer grid (enough for integer end points)."""
    if not intervals:
        return 0
    grid = [h / 2 for h in range(0, 2 * span + 1)]
    for size in range(1, len(intervals) + 1):
        for pts in itertools.combinations(grid, size):
            if pierces(pts, intervals, kind):
                return size
    raise AssertionError("unreachable")


def check(intervals, kind, span):
    got = interval_piercing_greedy(intervals, kind)
    assert pierces(got, intervals, kind)
    assert len(got) == brute(intervals, kind, span)
    return got


EXAMPLE = [(1, 4), (2, 3), (3, 6), (5, 7), (6, 8), (8, 9), (9, 10)]


def test_example():
    assert check(EXAMPLE, "closed", 10) == [3, 7, 9]
    assert check(EXAMPLE, "half-open", 10) == [2, 5, 6, 8, 9]
    assert check(EXAMPLE, "open", 10) == [2.5, 5.5, 7.0, 8.5, 9.5]


def test_touching_cases():
    assert check([(1, 3), (3, 5)], "closed", 5) == [3]
    assert len(check([(1, 3), (3, 5)], "half-open", 5)) == 2
    assert len(check([(1, 3), (3, 5)], "open", 5)) == 2
    # equal right ends
    assert check([(2, 5), (0, 5), (5, 5)], "closed", 5) == [5]
    assert check([(2, 5), (0, 5)], "half-open", 5) == [2]
    # point intervals (closed only): one point per distinct value
    assert check([(4, 4), (1, 1), (4, 4)], "closed", 4) == [1, 4]


def test_edge_cases():
    assert interval_piercing_greedy([]) == []
    assert check([(0, 1)], "closed", 1) == [1]
    assert check([(0, 1)], "half-open", 1) == [0]
    assert check([(0, 1)], "open", 1) == [0.5]
    nested = [(0, 6), (1, 5), (2, 4)]
    assert len(check(nested, "open", 6)) == 1


def test_random_against_brute_force():
    rng = random.Random(30)
    for trial in range(900):
        kind = ("closed", "half-open", "open")[trial % 3]
        n = rng.randint(0, 6)
        span = 5
        ivs = []
        for _ in range(n):
            a = rng.randint(0, span - 1)
            b = rng.randint(a + (0 if kind == "closed" else 1), span)
            ivs.append((a, b))
        check(ivs, kind, span)
