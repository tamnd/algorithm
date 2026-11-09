# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bst-range-search/. The authors are listed in prov/JZANN9.jsonl.

import random

from bst_range_search import build_balanced, height, insert, range_search


def scan(keys, lo, hi):
    return sorted(k for k in keys if lo <= k <= hi)


def test_worked_example():
    keys = [2, 5, 9, 12, 15, 19, 23, 27, 31]
    root = build_balanced(keys)
    assert root.key == 15
    stats = {}
    assert range_search(root, 10, 24, stats) == [12, 15, 19, 23]
    assert stats["visited"] == 6


def test_empty_and_single():
    assert range_search(None, 0, 10) == []
    root = build_balanced([])
    assert root is None
    root = build_balanced([5])
    assert range_search(root, 5, 5) == [5]
    assert range_search(root, 6, 9) == []
    assert range_search(root, 1, 4) == []
    assert range_search(root, 9, 1) == []


def test_closed_boundaries_and_duplicates():
    keys = [3, 3, 3, 7, 7, 10]
    for root in (build_balanced(keys), None):
        if root is None:
            for k in keys:
                root = insert(root, k)
        assert range_search(root, 3, 7) == [3, 3, 3, 7, 7]
        assert range_search(root, 7, 7) == [7, 7]
        assert range_search(root, 4, 6) == []
        assert range_search(root, 10, 10) == [10]


def test_degenerate_tree_no_recursion_limit():
    root = None
    for k in range(5000):
        root = insert(root, k)
    assert height(root) == 5000
    assert range_search(root, 4990, 10000) == list(range(4990, 5000))


def test_random_against_scan_and_visit_bound():
    rng = random.Random(20240611)
    for trial in range(600):
        n = rng.randint(0, 40)
        keys = [rng.randint(0, 20) for _ in range(n)]
        balanced = build_balanced(keys)
        plain = None
        for k in keys:
            plain = insert(plain, k)
        for _ in range(5):
            lo = rng.randint(-2, 22)
            hi = rng.randint(-2, 22)
            want = scan(keys, lo, hi)
            for root in (balanced, plain):
                stats = {}
                got = range_search(root, lo, hi, stats)
                assert got == want
                # Visited nodes: the reported ones plus at most two per level.
                assert stats["visited"] <= len(got) + 2 * height(root)


def test_random_distinct_balanced_logarithmic():
    rng = random.Random(7)
    for trial in range(100):
        n = rng.randint(1, 300)
        keys = rng.sample(range(10 * n), n)
        root = build_balanced(keys)
        h = height(root)
        assert h <= n.bit_length()
        lo = rng.randint(0, 10 * n)
        hi = lo + rng.randint(0, 3 * n)
        stats = {}
        got = range_search(root, lo, hi, stats)
        assert got == scan(keys, lo, hi)
        assert stats["visited"] <= len(got) + 2 * h
