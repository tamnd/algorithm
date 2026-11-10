# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/franklin/. The authors are listed in prov/PG80TJ.jsonl.

import random
from itertools import permutations

from franklin import franklin, rounds_with_two_or_more


def lg_floor(n: int) -> int:
    return n.bit_length() - 1


def check(ids: list[int], res: dict) -> None:
    n = len(ids)
    top = ids.index(max(ids))
    assert res["leaders"] == [top]
    assert all(s == "non-leader" for i, s in enumerate(res["status"]) if i != top)
    assert res["known"] == [max(ids)] * n
    r = rounds_with_two_or_more(ids)
    assert r <= lg_floor(n)
    assert res["rounds"] == r + 1
    assert res["elect"] == 2 * n * r + 2 * n
    assert res["elect"] <= 2 * n * lg_floor(n) + 2 * n
    assert res["announce"] == n


def test_page_example() -> None:
    ids = [3, 7, 1, 5, 2]
    res = franklin(ids)
    check(ids, res)
    assert res["elect"] == 30 and res["rounds"] == 3


def test_all_orders_small() -> None:
    rng = random.Random(3)
    for n in range(1, 8):
        worst = 0
        for perm in permutations(range(n)):
            ids = list(perm)
            flip = [rng.random() < 0.5 for _ in range(n)]
            for sch in ("first", "last", "random", "slow"):
                res = franklin(ids, sch, seed=n)
                check(ids, res)
            check(ids, franklin(ids, "random", seed=1, flip=flip))
            worst = max(worst, res["elect"])
        assert worst == 2 * n * lg_floor(n) + 2 * n


def test_random_rings_up_to_200() -> None:
    rng = random.Random(11)
    for n in (10, 64, 128, 200):
        for t in range(2):
            ids = rng.sample(range(10 * n), n)
            flip = [rng.random() < 0.5 for _ in range(n)]
            for sch in ("random", "slow", "last"):
                check(ids, franklin(ids, sch, seed=t, flip=flip))


def test_bit_reversal_reaches_bound() -> None:
    for k in range(1, 8):
        n = 2**k
        ids = [int(format(i, f"0{k}b")[::-1], 2) for i in range(n)]
        res = franklin(ids, "random", seed=k)
        check(ids, res)
        assert res["elect"] == 2 * n * k + 2 * n
