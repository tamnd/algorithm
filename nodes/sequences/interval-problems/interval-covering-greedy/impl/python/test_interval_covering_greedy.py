# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interval-covering-greedy/. The authors are listed in prov/EYK6H0.jsonl.
import itertools
import random

import pytest

from interval_covering_greedy import interval_covering_greedy


def contains(iv, x, kind):
    l, r = iv
    if kind == "closed":
        return l <= x <= r
    if kind == "half-open":
        return l <= x < r
    return l < x < r


def covers(chosen, s, t, kind):
    """Exact test for integer end points: check every integer and half-integer of the target."""
    pts = [s + h / 2 for h in range(0, int(2 * (t - s)) + 1)]
    if kind == "half-open":
        pts = [x for x in pts if x < t]
    if kind == "open":
        pts = [x for x in pts if s < x < t]
    return all(any(contains(iv, x, kind) for iv in chosen) for x in pts)


def brute(intervals, s, t, kind):
    for size in range(1, len(intervals) + 1):
        for combo in itertools.combinations(intervals, size):
            if covers(combo, s, t, kind):
                return size
    return None


def check(intervals, s, t, kind):
    got = interval_covering_greedy(intervals, s, t, kind)
    want = brute(intervals, s, t, kind)
    if want is None:
        assert got is None
    else:
        assert got is not None and len(got) == want
        assert len(set(got)) == len(got)
        assert covers([intervals[k] for k in got], s, t, kind)
    return got


EXAMPLE = [(0, 4), (1, 3), (4, 7), (2, 6), (6, 10), (7, 9), (8, 12)]


def test_example_closed_and_half_open():
    assert check(EXAMPLE, 0, 10, "closed") == [0, 2, 4]
    assert check(EXAMPLE, 0, 10, "half-open") == [0, 2, 4]


def test_example_open():
    assert check(EXAMPLE, 0, 10, "open") == [0, 3, 2, 4]


def test_touching_cases():
    # touching end points cover a closed or half-open target, not an open one
    assert check([(0, 2), (2, 4)], 0, 4, "closed") == [0, 1]
    assert check([(0, 2), (2, 4)], 0, 4, "half-open") == [0, 1]
    assert check([(0, 2), (2, 4)], 0, 4, "open") is None
    assert check([(0, 2), (2, 4), (1, 3)], 0, 4, "open") == [0, 2, 1]
    # the target end points themselves
    assert check([(1, 4)], 0, 4, "closed") is None
    assert check([(0, 3)], 0, 4, "closed") is None
    assert check([(0, 4)], 0, 4, "half-open") == [0]
    assert check([(0, 4)], 0, 4, "open") == [0]


def test_edge_cases():
    assert interval_covering_greedy([], 0, 1) is None
    assert check([(-5, 5)], 0, 1, "closed") == [0]
    assert check([(0, 1), (3, 4)], 0, 4, "closed") is None  # a gap
    with pytest.raises(ValueError):
        interval_covering_greedy([(0, 1)], 1, 1)


def test_random_against_brute_force():
    rng = random.Random(6006)
    for trial in range(900):
        kind = ("closed", "half-open", "open")[trial % 3]
        n = rng.randint(0, 7)
        span = rng.choice([4, 8, 12])
        ivs = []
        for _ in range(n):
            a = rng.randint(0, span)
            b = rng.randint(a + (0 if kind == "closed" else 1), span + 1)
            ivs.append((a, b))
        s = rng.randint(0, span - 1)
        t = rng.randint(s + 1, span)
        check(ivs, s, t, kind)
