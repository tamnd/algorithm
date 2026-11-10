# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chang-roberts/. The authors are listed in prov/YMKAJR.jsonl.

import random
from fractions import Fraction
from itertools import permutations
from math import factorial

from chang_roberts import SCHEDULES, chang_roberts, hops_to_larger


def check(ids: list[int], res: dict) -> None:
    n = len(ids)
    top = ids.index(max(ids))
    assert res["leaders"] == [top]
    assert all(s == "non-leader" for i, s in enumerate(res["status"]) if i != top)
    assert res["known"] == [max(ids)] * n
    assert all(res["done"])
    assert res["elect"] == sum(hops_to_larger(ids))
    assert res["elect"] <= n * (n + 1) // 2
    assert res["announce"] == n


def test_page_example() -> None:
    ids = [3, 7, 1, 5, 2]
    assert hops_to_larger(ids) == [1, 5, 1, 3, 1]
    res = chang_roberts(ids)
    check(ids, res)
    assert res["elect"] == 11 and res["announce"] == 5


def test_all_orders_small() -> None:
    for n in range(1, 8):
        for perm in permutations(range(1, n + 1)):
            ids = list(perm)
            for sch in ("first", "last", "random"):
                check(ids, chang_roberts(ids, sch, seed=n))


def test_non_fifo_schedules() -> None:
    for n in range(1, 7):
        for perm in permutations(range(n)):
            for sch in ("any", "lifo", "slow"):
                check(list(perm), chang_roberts(list(perm), sch, seed=7))


def test_worst_and_best_case_exact() -> None:
    for n in range(1, 60):
        down = list(range(n, 0, -1))
        up = list(range(1, n + 1))
        assert chang_roberts(down, "random", n)["elect"] == n * (n + 1) // 2
        assert chang_roberts(up, "lifo", n)["elect"] == 2 * n - 1


def test_worst_case_is_max_over_orders() -> None:
    for n in range(1, 8):
        best = min(sum(hops_to_larger(list(p))) for p in permutations(range(n)))
        worst = max(sum(hops_to_larger(list(p))) for p in permutations(range(n)))
        assert worst == n * (n + 1) // 2
        assert best == 2 * n - 1


def test_average_is_n_harmonic() -> None:
    for n in range(1, 8):
        total = sum(sum(hops_to_larger(list(p))) for p in permutations(range(n)))
        harmonic = sum(Fraction(1, k) for k in range(1, n + 1))
        assert Fraction(total, factorial(n)) == n * harmonic


def test_random_rings_up_to_200() -> None:
    rng = random.Random(2024)
    for n in (10, 50, 100, 200):
        for t in range(3):
            ids = rng.sample(range(10 * n), n)
            for sch in SCHEDULES:
                if sch in ("any", "lifo") and n > 100:
                    continue
                check(ids, chang_roberts(ids, sch, seed=t))


def test_rejects_equal_ids() -> None:
    try:
        chang_roberts([1, 2, 1])
    except ValueError:
        return
    raise AssertionError("equal identifiers accepted")
