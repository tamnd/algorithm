# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/peterson-leader-election/. The authors are listed in prov/M6ANZC.jsonl.

import random
from itertools import permutations

from peterson_leader_election import peterson, phases_with_two_or_more


def lg_floor(n: int) -> int:
    return n.bit_length() - 1


def check(ids: list[int], res: dict) -> None:
    n = len(ids)
    assert len(res["leaders"]) == 1
    lead = res["leaders"][0]
    assert all(s == "non-leader" for i, s in enumerate(res["status"]) if i != lead)
    assert res["known"] == [ids[lead]] * n
    assert res["tid"][lead] == max(ids)
    r = phases_with_two_or_more(ids)
    assert r <= lg_floor(n)
    assert res["elect"] == 2 * n * r + n
    assert res["elect"] <= 2 * n * lg_floor(n) + n
    assert res["announce"] == n
    assert res["phases"] == r + 1


def test_page_example() -> None:
    ids = [3, 7, 1, 5, 2]
    res = peterson(ids, "sync")
    check(ids, res)
    assert res["leaders"] == [4]
    assert res["tid"] == [3, 7, 7, 5, 7]
    assert res["elect"] == 25 and res["announce"] == 5


def test_all_orders_small() -> None:
    for n in range(1, 8):
        worst = 0
        for perm in permutations(range(n)):
            ids = list(perm)
            for sch in ("first", "last", "random", "slow"):
                res = peterson(ids, sch, seed=n)
                check(ids, res)
            worst = max(worst, res["elect"])
        assert worst == 2 * n * lg_floor(n) + n


def test_random_rings_up_to_200() -> None:
    rng = random.Random(2024)
    for n in (10, 64, 100, 200):
        for t in range(3):
            ids = rng.sample(range(10 * n), n)
            for sch in ("random", "slow", "sync", "last"):
                check(ids, peterson(ids, sch, seed=t))


def test_halving_ring_reaches_bound() -> None:
    # bit-reversal orders make exactly half of the active processes survive
    for k in range(1, 8):
        n = 2**k
        ids = [int(format(i, f"0{k}b")[::-1], 2) for i in range(n)]
        res = peterson(ids, "random", seed=k)
        check(ids, res)
        assert res["elect"] == 2 * n * k + n
