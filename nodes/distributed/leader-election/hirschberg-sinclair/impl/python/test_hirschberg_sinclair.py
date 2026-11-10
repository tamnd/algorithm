# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hirschberg-sinclair/. The authors are listed in prov/41MZQ5.jsonl.

import random
from itertools import permutations

from hirschberg_sinclair import hirschberg_sinclair


def ceil_lg(n: int) -> int:
    return (n - 1).bit_length()


def check(ids: list[int], res: dict) -> None:
    n = len(ids)
    top = ids.index(max(ids))
    assert res["leaders"] == [top]
    assert all(s == "non-leader" for i, s in enumerate(res["status"]) if i != top)
    assert res["known"] == [max(ids)] * n
    assert res["elect"] <= 8 * n * (1 + ceil_lg(n))
    assert res["elect"] <= (8 * n * ceil_lg(n) - 2 * n if n > 1 else 2)
    assert res["announce"] == n
    assert res["phases"] == ceil_lg(n)


def test_page_example() -> None:
    ids = [3, 7, 1, 5, 2]
    res = hirschberg_sinclair(ids, "sync")
    check(ids, res)
    assert res["elect"] == 55
    assert res["status"][1] == "leader"
    assert res["elected_at"] == 2 * (2**3 - 1) + 5


def test_all_orders_small() -> None:
    rng = random.Random(1)
    for n in range(1, 8):
        for perm in permutations(range(n)):
            ids = list(perm)
            flip = [rng.random() < 0.5 for _ in range(n)]
            schedules = ("sync", "any") if n == 7 else ("sync", "first", "last", "random", "any")
            for sch in schedules:
                check(ids, hirschberg_sinclair(ids, sch, seed=n))
            check(ids, hirschberg_sinclair(ids, "any", seed=3, flip=flip))


def test_election_message_count_does_not_depend_on_schedule() -> None:
    rng = random.Random(5)
    for n in range(1, 30):
        ids = rng.sample(range(1000), n)
        counts = {hirschberg_sinclair(ids, s, seed=9)["elect"] for s in ("sync", "first", "last", "random", "any")}
        assert len(counts) == 1


def test_synchronous_time_exact() -> None:
    rng = random.Random(7)
    for n in range(1, 70):
        ids = rng.sample(range(10**6), n)
        res = hirschberg_sinclair(ids, "sync")
        big = 2 ** ceil_lg(n)
        assert res["elected_at"] == 2 * (big - 1) + n
        assert res["elected_at"] < 5 * n
        if n == big:
            assert res["elected_at"] == 3 * n - 2


def test_random_rings_up_to_200() -> None:
    rng = random.Random(2024)
    for n in (16, 50, 128, 200):
        ids = rng.sample(range(10 * n), n)
        flip = [rng.random() < 0.5 for _ in range(n)]
        for sch in ("sync", "random", "last"):
            check(ids, hirschberg_sinclair(ids, sch, seed=n))
        check(ids, hirschberg_sinclair(ids, "random", seed=1, flip=flip))
