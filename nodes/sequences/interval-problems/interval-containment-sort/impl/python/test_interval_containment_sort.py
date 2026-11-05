# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/interval-containment-sort/. The authors are listed in prov/8YB754.jsonl.
import random

from interval_containment_sort import has_nested_pair, interval_containment_sort


def contains(outer, inner):
    return outer[0] <= inner[0] and inner[1] <= outer[1]


def check(intervals):
    """Check the parent array against the definition by brute force."""
    parent = interval_containment_sort(intervals)
    n = len(intervals)
    assert len(parent) == n
    for k in range(n):
        p = parent[k]
        if p is not None:
            assert p != k
            assert contains(intervals[p], intervals[k])
            assert parent[p] is None  # the container is a kept maximal interval
        else:
            # k is maximal and no smaller index holds an equal copy
            for j in range(n):
                if j == k:
                    continue
                if contains(intervals[j], intervals[k]):
                    assert intervals[j] == intervals[k] and j > k
    brute = any(j != k and contains(intervals[j], intervals[k]) for j in range(n) for k in range(n))
    assert has_nested_pair(intervals) == brute
    return parent


def test_example():
    family = [(1, 4), (2, 3), (3, 6), (1, 2), (5, 6), (3, 6), (6, 8), (7, 8)]
    assert check(family) == [None, 0, None, 0, 2, 2, None, 6]


def test_touching_cases():
    # shared left end: nested
    assert check([(1, 4), (1, 2)]) == [None, 0]
    assert check([(1, 2), (1, 4)]) == [1, None]
    # shared right end: nested
    assert check([(3, 6), (5, 6)]) == [None, 0]
    # touching at one point only: not nested
    assert check([(3, 6), (6, 8)]) == [None, None]
    assert not has_nested_pair([(1, 3), (3, 5)])
    # duplicates: the first copy is kept
    assert check([(2, 5), (2, 5), (2, 5)]) == [None, 0, 0]
    # point intervals: nested only when equal
    assert check([(4, 4), (1, 1), (4, 4)]) == [None, None, 0]
    # a point at the end of an interval is inside it
    assert check([(4, 4), (1, 4)]) == [1, None]


def test_edge_cases():
    assert interval_containment_sort([]) == []
    assert check([(0, 0)]) == [None]
    assert not has_nested_pair([(1, 3), (2, 4), (3, 5)])  # a proper family


def test_mixed_types_with_keys():
    # left key (x, 0) closed, (x, 1) open; right key (x, 1) closed, (x, 0) open
    closed = ((1, 0), (3, 1))  # [1, 3]
    half_open = ((1, 0), (3, 0))  # [1, 3)
    open_ = ((1, 1), (3, 0))  # (1, 3)
    assert check([half_open, closed]) == [1, None]
    assert check([open_, half_open]) == [1, None]
    assert check([closed, open_]) == [None, 0]


def test_random_against_brute_force():
    rng = random.Random(8754)
    for _ in range(800):
        n = rng.randint(0, 12)
        span = rng.choice([3, 6, 15])
        family = []
        for _ in range(n):
            a, b = rng.randint(0, span), rng.randint(0, span)
            family.append((min(a, b), max(a, b)))
        check(family)
