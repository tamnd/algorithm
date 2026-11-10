# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dolev-klawe-rodeh/. The authors are listed in prov/2S8HY8.jsonl.

import random
from itertools import permutations

from dolev_klawe_rodeh import dolev_klawe_rodeh, franklin_rounds


def lg_floor(n: int) -> int:
    return n.bit_length() - 1


def check(ids: list[int], res: dict) -> None:
    n = len(ids)
    top = ids.index(max(ids))
    assert res["leaders"] == [top]
    assert all(s == "non-leader" for i, s in enumerate(res["status"]) if i != top)
    assert res["known"] == [max(ids)] * n
    assert len(res["finder"]) == 1
    r = franklin_rounds(ids)
    assert r <= lg_floor(n)
    assert res["one"] == n * r + n
    assert res["two"] == n * r
    assert res["found"] == n
    assert res["one"] + res["two"] + res["found"] <= 2 * n * lg_floor(n) + 2 * n


def test_page_example() -> None:
    ids = [3, 7, 1, 5, 2]
    res = dolev_klawe_rodeh(ids)
    check(ids, res)
    assert res["finder"] == [4]
    assert res["one"] + res["two"] == 25 and res["found"] == 5


def test_all_orders_small() -> None:
    for n in range(1, 8):
        worst = 0
        for perm in permutations(range(n)):
            ids = list(perm)
            for sch in ("first", "last", "random", "slow"):
                res = dolev_klawe_rodeh(ids, sch, seed=n)
                check(ids, res)
            worst = max(worst, res["one"] + res["two"] + res["found"])
        assert worst == 2 * n * lg_floor(n) + 2 * n


def test_random_rings_up_to_200() -> None:
    rng = random.Random(77)
    for n in (10, 64, 128, 200):
        for t in range(3):
            ids = rng.sample(range(10 * n), n)
            for sch in ("random", "slow", "last"):
                check(ids, dolev_klawe_rodeh(ids, sch, seed=t))
