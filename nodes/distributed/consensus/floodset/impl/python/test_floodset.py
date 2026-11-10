# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/floodset/. The authors are listed in prov/MBNRW2.jsonl.

import random
from itertools import product

from floodset import check_run, crash_patterns, floodset


def test_page_example() -> None:
    # n = 4, f = 2, processes 0 .. 3 are p1 .. p4 of the page.
    inputs = [3, 1, 4, 5]
    crashes = {1: (1, frozenset({2})), 2: (2, frozenset({3}))}
    res = floodset(inputs, 2, crashes, rule="min")
    assert res["w"] == {0: frozenset({1, 3, 4, 5}), 3: frozenset({1, 3, 4, 5})}
    assert res["decisions"] == {0: 1, 3: 1}
    assert res["rounds"] == 3
    short = floodset(inputs, 2, crashes, rounds=2, rule="min")
    assert short["decisions"] == {0: 3, 3: 1}


def test_failure_free_counts() -> None:
    for n in range(1, 7):
        for f in range(n):
            res = floodset(list(range(n)), f)
            assert res["rounds"] == f + 1
            assert res["messages"] == n * (n - 1) * (f + 1)


def exhaustive(n: int, f: int, values: list[int], rule: str) -> int:
    runs = 0
    patterns = list(crash_patterns(n, f, f + 1))
    for inputs in product(values, repeat=n):
        for plan in patterns:
            res = floodset(list(inputs), f, plan, rule=rule)
            assert check_run(list(inputs), res) == [], (inputs, plan)
            # termination: every process that does not crash decides
            assert set(res["decisions"]) == set(range(n)) - set(plan)
            assert res["rounds"] == f + 1
            if rule == "min":
                assert all(v in inputs for v in res["decisions"].values())
            # the sets W of the deciding processes are equal
            assert len(set(res["w"].values())) <= 1
            runs += 1
    return runs


def test_exhaustive_small() -> None:
    assert exhaustive(2, 1, [0, 1], "default") > 0
    assert exhaustive(3, 1, [0, 1, 2], "min") > 0
    assert exhaustive(3, 2, [0, 1], "default") > 0
    assert exhaustive(4, 1, [0, 1], "min") > 0


def test_exhaustive_n4_f2() -> None:
    assert exhaustive(4, 2, [0, 1], "default") == 16 * len(list(crash_patterns(4, 2, 3)))


def count_bad_with_f_rounds(n: int, f: int) -> int:
    bad = 0
    for inputs in product([0, 1], repeat=n):
        for plan in crash_patterns(n, f, f):
            res = floodset(list(inputs), f, plan, rounds=f, rule="min")
            if "agreement" in check_run(list(inputs), res):
                bad += 1
    return bad


def test_f_rounds_are_not_enough() -> None:
    # With only f rounds and f <= n - 2, some crash plan breaks agreement.
    assert count_bad_with_f_rounds(3, 1) == 6
    assert count_bad_with_f_rounds(4, 1) > 0
    assert count_bad_with_f_rounds(4, 2) == 48


def test_f_equal_n_minus_1_needs_only_f_rounds() -> None:
    # The lower bound needs f <= n - 2. With f = n - 1, f rounds are enough.
    for n in (2, 3):
        assert count_bad_with_f_rounds(n, n - 1) == 0


def test_random_larger() -> None:
    rng = random.Random(6202)
    for _ in range(600):
        n = rng.randint(2, 8)
        f = rng.randint(0, n - 1)
        inputs = [rng.randint(0, 3) for _ in range(n)]
        who = rng.sample(range(n), rng.randint(0, f))
        plan = {}
        for p in who:
            others = [q for q in range(n) if q != p]
            plan[p] = (rng.randint(1, f + 1), frozenset(q for q in others if rng.random() < 0.5))
        res = floodset(inputs, f, plan, rule="min")
        assert check_run(inputs, res) == []
        assert set(res["decisions"]) == set(range(n)) - set(plan)
        # independent oracle: with no crash, everyone decides the minimum input
        if not plan:
            assert set(res["decisions"].values()) == {min(inputs)}
