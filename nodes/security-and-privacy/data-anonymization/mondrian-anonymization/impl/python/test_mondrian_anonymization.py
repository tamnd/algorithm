# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mondrian-anonymization/. The authors are listed in prov/EV1MMH.jsonl.
import random
from collections import Counter

from mondrian_anonymization import best_cut, mondrian, summarize

TABLE = [
    (25, 53711), (25, 53712), (26, 53711), (27, 53710), (29, 53712),
    (61, 53706), (62, 53706), (63, 53710), (64, 53712), (64, 53711),
]


def test_page_example() -> None:
    regions = mondrian(TABLE, 2)
    assert regions == [[0, 2, 3], [1, 4], [5, 6], [7, 8, 9]]
    assert summarize(TABLE, regions) == [
        ((25, 27), (53710, 53711)),
        ((25, 29), (53712, 53712)),
        ((61, 62), (53706, 53706)),
        ((63, 64), (53710, 53712)),
    ]
    assert mondrian(TABLE, 3) == [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]


def test_duplicates_pitfall() -> None:
    rows = [(1,), (1,), (1,), (2,), (2,), (2,), (2,), (2,)]
    # The median value is 2, and the cut "<= 2" leaves nothing on the right.
    assert best_cut(rows, list(range(8)), 0, 3) == 1
    assert mondrian(rows, 3) == [[0, 1, 2], [3, 4, 5, 6, 7]]


def test_edge_cases() -> None:
    assert mondrian([], 2) == []
    assert mondrian([(5, 5)], 1) == [[0]]
    assert mondrian([(5, 5)] * 4, 2) == [[0, 1, 2, 3]]
    assert mondrian(TABLE, 1) == [[i] for i in range(10)]
    assert mondrian(TABLE, 10) == [list(range(10))]
    assert mondrian(TABLE, 6) == [list(range(10))]


def allowable(table, region, a, k):
    for x in {table[i][a] for i in region}:
        left = sum(1 for i in region if table[i][a] <= x)
        if left >= k and len(region) - left >= k:
            return True
    return False


def reference(table, region, k, full):
    """The same greedy rule, written as a plain recursion with integer comparisons."""
    d = len(table[0])

    def ratio(a):
        # IEEE division is correctly rounded, so equal ratios of small integers compare equal.
        if full[a] == 0:
            return 0.0
        return (max(table[i][a] for i in region) - min(table[i][a] for i in region)) / full[a]

    order = sorted(range(d), key=lambda a: (-ratio(a), a))
    for a in order:
        best, score = None, -1
        for x in sorted({table[i][a] for i in region}):
            left = [i for i in region if table[i][a] <= x]
            right = [i for i in region if table[i][a] > x]
            if len(left) >= k and len(right) >= k and min(len(left), len(right)) > score:
                best, score = (left, right), min(len(left), len(right))
        if best is not None:
            return reference(table, best[0], k, full) + reference(table, best[1], k, full)
    return [sorted(region)]


def test_random_against_reference_and_bound() -> None:
    rng = random.Random(2006)
    for _ in range(700):
        d = rng.randint(1, 4)
        k = rng.randint(1, 4)
        n = rng.randint(k, 30)
        spread = rng.randint(1, 6)
        table = [tuple(rng.randint(0, spread) for _ in range(d)) for _ in range(n)]
        regions = mondrian(table, k)
        assert sorted(i for reg in regions for i in reg) == list(range(n))
        m = max(Counter(table).values())
        for reg in regions:
            assert len(reg) >= k
            assert len(reg) <= 2 * d * (k - 1) + m
            assert not any(allowable(table, reg, a, k) for a in range(d))
        full = [max(r[a] for r in table) - min(r[a] for r in table) for a in range(d)]
        assert regions == sorted(reference(table, list(range(n)), k, full))
