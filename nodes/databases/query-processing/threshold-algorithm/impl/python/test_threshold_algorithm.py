# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/threshold-algorithm/. The authors are listed in prov/7GGJ22.jsonl.

import math
import random

from threshold_algorithm import threshold_algorithm

AGGS = [sum, min, max, lambda g: g[0] + 2 * g[-1], lambda g: math.prod(x + 1 for x in g)]

# The example of the page, with grades in tenths so that sums are exact.
LISTS = [
    [("a", 9), ("b", 8), ("c", 7), ("d", 6), ("e", 1)],
    [("c", 9), ("a", 8), ("e", 7), ("b", 4), ("d", 2)],
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


def fa_depth(lists, k):
    """Depth at which Fagin's algorithm stops: k objects seen in every list."""
    m, n = len(lists), len(lists[0])
    count: dict = {}
    full = 0
    for d in range(n):
        if full >= k:
            return d
        for i in range(m):
            o = lists[i][d][0]
            count[o] = count.get(o, 0) + 1
            full += count[o] == m
    return n


def check_topk(result, grades, t, k):
    assert len(result) == min(max(k, 0), len(grades))
    chosen = {o for o, _ in result}
    assert len(chosen) == len(result)
    for o, s in result:
        assert s == t(grades[o])
    if chosen and len(chosen) < len(grades):
        assert min(s for _, s in result) >= max(t(g) for o, g in grades.items() if o not in chosen)


def test_example() -> None:
    st = {}
    assert threshold_algorithm(LISTS, sum, 2, st) == [("a", 17), ("c", 16)]
    assert st == {"depth": 2, "sorted": 4, "random": 3}
    assert fa_depth(LISTS, 2) == 3
    assert threshold_algorithm(LISTS, min, 1, st) == [("a", 8)]
    assert st == {"depth": 2, "sorted": 4, "random": 3}


def test_max_stops_at_once() -> None:
    rng = random.Random(2)
    _, lists = make_db(rng, 1000, 3, 10 ** 6)
    st = {}
    threshold_algorithm(lists, max, 1, st)
    assert st["depth"] == 1 < fa_depth(lists, 1)


def test_random_against_brute_force_and_fa() -> None:
    rng = random.Random(8)
    for _ in range(600):
        n, m = rng.randrange(1, 30), rng.randrange(1, 5)
        grades, lists = make_db(rng, n, m, rng.choice([2, 4, 100]))
        t = rng.choice(AGGS)
        k = rng.randrange(0, n + 2)
        st = {}
        check_topk(threshold_algorithm(lists, t, k, st), grades, t, k)
        if k > 0:
            assert st["depth"] <= fa_depth(lists, min(k, n))     # TA stops no later than FA
        assert st["sorted"] == m * st["depth"]
        assert st["random"] <= (m - 1) * st["sorted"]


def test_bounded_buffer_independent_lists() -> None:
    rng = random.Random(4)
    grades, lists = make_db(rng, 5000, 2, 10 ** 9)
    st = {}
    check_topk(threshold_algorithm(lists, sum, 10, st), grades, sum, 10)
    assert st["depth"] <= fa_depth(lists, 10)
