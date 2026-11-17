# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fagin-algorithm/. The authors are listed in prov/2544V4.jsonl.

import math
import random

from fagin_algorithm import fagin

AGGS = [sum, min, max, lambda g: g[0] + 2 * g[-1], lambda g: math.prod(x + 1 for x in g)]


def make_db(rng, n, m, levels):
    grades = {obj: tuple(rng.randrange(levels) for _ in range(m)) for obj in range(n)}
    lists = []
    for i in range(m):
        objs = list(grades)
        rng.shuffle(objs)                      # random order among equal grades
        objs.sort(key=lambda o: -grades[o][i])
        lists.append([(o, grades[o][i]) for o in objs])
    return grades, lists


def check_topk(result, grades, t, k):
    assert len(result) == min(k, len(grades))
    chosen = {o for o, _ in result}
    assert len(chosen) == len(result)
    for o, s in result:
        assert s == t(grades[o])
    if chosen and len(chosen) < len(grades):
        assert min(s for _, s in result) >= max(t(g) for o, g in grades.items() if o not in chosen)


def test_example() -> None:
    lists = [
        [("a", 0.9), ("b", 0.8), ("c", 0.7), ("d", 0.6), ("e", 0.1)],
        [("c", 0.9), ("a", 0.8), ("e", 0.7), ("b", 0.4), ("d", 0.2)],
    ]
    st = {}
    top = fagin(lists, min, 1, st)
    assert top == [("a", 0.8)]
    assert st == {"depth": 2, "sorted": 4, "random": 2}
    top = fagin(lists, sum, 2, st)
    assert [o for o, _ in top] == ["a", "c"]
    assert st["depth"] == 3


def test_random_against_brute_force() -> None:
    rng = random.Random(5)
    for _ in range(500):
        n, m = rng.randrange(1, 30), rng.randrange(1, 5)
        grades, lists = make_db(rng, n, m, rng.choice([2, 4, 100]))
        t = rng.choice(AGGS)
        k = rng.randrange(0, n + 2)
        st = {}
        check_topk(fagin(lists, t, k, st), grades, t, k)
        assert st["random"] <= (m - 1) * st["sorted"]


def test_depth_scaling() -> None:
    # For independent random lists, FA stops near depth N^((m-1)/m) k^(1/m).
    rng = random.Random(9)
    for n, m, k in [(10000, 2, 10), (8000, 3, 8)]:
        ratios = []
        for _ in range(5):
            grades, lists = make_db(rng, n, m, 10 ** 9)
            st = {}
            fagin(lists, sum, k, st)
            ratios.append(st["depth"] / (n ** ((m - 1) / m) * k ** (1 / m)))
        assert 0.5 < sum(ratios) / len(ratios) < 2
