# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/no-random-access-algorithm/. The authors are listed in prov/29R7VV.jsonl.

import math
import random

import pytest

from no_random_access_algorithm import no_random_access

AGGS = [sum, min, max, lambda g: g[0] + 2 * g[-1], lambda g: math.prod(x + 1 for x in g)]

# The example of the page: NRA returns a without learning its grade in L2.
EXAMPLE = [
    [("a", 9), ("b", 3), ("c", 2), ("d", 1)],
    [("b", 5), ("c", 4), ("d", 3), ("a", 0)],
]


def make_db(rng, n, m, levels):
    grades = {obj: tuple(rng.randrange(levels) for _ in range(m)) for obj in range(n)}
    lists = []
    for i in range(m):
        objs = list(grades)
        rng.shuffle(objs)
        objs.sort(key=lambda o: -grades[o][i])
        lists.append([(o, grades[o][i]) for o in objs])
    return grades, lists


def ta_depth(lists, grades, t, k):
    """Depth at which the threshold algorithm stops, computed from full grades."""
    seen: set = set()
    n = len(lists[0])
    for d in range(n):
        for lst in lists:
            seen.add(lst[d][0])
        tau = t(tuple(lst[d][1] for lst in lists))
        scores = sorted((t(grades[o]) for o in seen), reverse=True)
        if len(scores) >= k and scores[k - 1] >= tau:
            return d + 1
    return n


def check_result(result, grades, t, k):
    assert len(result) == min(max(k, 0), len(grades))
    chosen = {o for o, _, _ in result}
    assert len(chosen) == len(result)
    for o, w, b in result:
        assert w <= t(grades[o]) <= b
    if chosen and len(chosen) < len(grades):
        # The set is a top-k set; the bounds need not be exact.
        assert min(t(grades[o]) for o in chosen) >= max(
            t(g) for o, g in grades.items() if o not in chosen)


def test_example_bounds_not_exact() -> None:
    st = {}
    assert no_random_access(EXAMPLE, sum, 1, st) == [("a", 9, 13)]
    assert st == {"depth": 2, "sorted": 4, "random": 0}


def test_example_of_threshold_page() -> None:
    lists = [
        [("a", 9), ("b", 8), ("c", 7), ("d", 6), ("e", 1)],
        [("c", 9), ("a", 8), ("e", 7), ("b", 4), ("d", 2)],
    ]
    st = {}
    assert [o for o, _, _ in no_random_access(lists, sum, 2, st)] == ["a", "c"]
    assert st["depth"] == 3                      # TA stops at depth 2 here


def test_random_against_brute_force_and_ta() -> None:
    rng = random.Random(11)
    for _ in range(600):
        n, m = rng.randrange(1, 30), rng.randrange(1, 5)
        grades, lists = make_db(rng, n, m, rng.choice([2, 4, 100]))
        t = rng.choice(AGGS)
        k = rng.randrange(0, n + 2)
        st = {}
        check_result(no_random_access(lists, t, k, st), grades, t, k)
        assert st["random"] == 0
        assert st["sorted"] == m * st["depth"]
        if 0 < k < n:
            assert ta_depth(lists, grades, t, k) <= st["depth"]


def test_larger_independent_lists() -> None:
    rng = random.Random(5)
    grades, lists = make_db(rng, 2000, 2, 10 ** 9)
    st = {}
    check_result(no_random_access(lists, sum, 5, st), grades, sum, 5)
    assert ta_depth(lists, grades, sum, 5) <= st["depth"] < 2000


def test_floor() -> None:
    lists = [[("a", -1), ("b", -3)], [("b", -2), ("a", -5)]]
    grades = {"a": (-1, -5), "b": (-3, -2)}
    check_result(no_random_access(lists, sum, 1, floor=-10), grades, sum, 1)
    with pytest.raises(ValueError):
        no_random_access(lists, sum, 1)
