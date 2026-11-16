# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/contract-net-protocol/. The authors are listed in prov/JAEWRV.jsonl.

import itertools
import random
from fractions import Fraction

from contract_net_protocol import contract_net


def random_costs(rng, r, t, gaps=False):
    cost = []
    for _ in range(r):
        row = []
        for _ in range(t):
            if gaps and rng.random() < 0.35:
                row.append(None)
            else:
                row.append(Fraction(rng.randint(1, 50)))
        cost.append(row)
    return cost


def brute_min_cost_all_tasks(cost):
    """Brute force: the cheapest way to give every task to a different robot."""
    r, t = len(cost), len(cost[0])
    best = None
    for robots in itertools.permutations(range(r), t):
        cs = [cost[robots[j]][j] for j in range(t)]
        if any(c is None for c in cs):
            continue
        total = sum(cs)
        if best is None or total < best:
            best = total
    return best


def brute_max_matching(cost):
    """Brute force: the largest number of tasks that robots can do, one each."""
    r, t = len(cost), len(cost[0])
    best = 0
    for choice in itertools.product(range(-1, r), repeat=t):
        used = [i for i in choice if i >= 0]
        if len(used) != len(set(used)):
            continue
        if all(i < 0 or cost[i][j] is not None for j, i in enumerate(choice)):
            best = max(best, len(used))
    return best


def sequential_auctions(cost, order):
    """Reference: announce one task at a time; the cheapest idle robot wins."""
    idle = set(range(len(cost)))
    award = {}
    for j in order:
        bids = [(cost[i][j], i) for i in idle if cost[i][j] is not None]
        if bids:
            c, i = min(bids)
            award[j] = i
            idle.discard(i)
    return award


def check_valid(cost, award):
    robots = list(award.values())
    assert len(robots) == len(set(robots))
    for j, i in award.items():
        assert cost[i][j] is not None


def test_hand_example_parallel_and_sequential():
    cost = [[1, 2], [10, 3], [Fraction(3, 2), Fraction(5, 2)]]
    par = contract_net(cost)
    assert par["award"] == {0: 0, 1: 1}
    assert par["cost"] == 4
    assert par["rounds"] == 1
    assert par["messages"] == {"announce": 6, "bid": 3, "award": 2}
    seq = contract_net(cost, batch=1)
    assert seq["award"] == {0: 0, 1: 2}
    assert seq["cost"] == Fraction(7, 2)
    assert seq["rounds"] == 2
    assert seq["messages"] == {"announce": 6, "bid": 5, "award": 2}
    assert brute_min_cost_all_tasks(cost) == Fraction(7, 2)


def test_ratio_to_optimum_is_unbounded():
    for big in (10, 99, 10**6):
        cost = [[1, 2], [2, big]]
        res = contract_net(cost)
        assert res["award"] == {0: 0, 1: 1}
        assert res["cost"] == 1 + big
        assert brute_min_cost_all_tasks(cost) == 4


def test_cost_at_least_optimum_and_all_tasks_awarded():
    rng = random.Random(7)
    for _ in range(150):
        r = rng.randint(1, 6)
        t = rng.randint(1, r)
        cost = random_costs(rng, r, t)
        res = contract_net(cost)
        check_valid(cost, res["award"])
        assert len(res["award"]) == t
        assert res["cost"] >= brute_min_cost_all_tasks(cost)
        assert res["rounds"] <= t


def test_batch_one_equals_sequential_auctions():
    rng = random.Random(11)
    for _ in range(200):
        r = rng.randint(1, 6)
        t = rng.randint(1, 6)
        cost = random_costs(rng, r, t, gaps=True)
        order = list(range(t))
        rng.shuffle(order)
        res = contract_net(cost, batch=1, order=order)
        assert res["award"] == sequential_auctions(cost, order)


def test_maximal_and_half_of_maximum():
    rng = random.Random(3)
    for _ in range(200):
        r = rng.randint(1, 5)
        t = rng.randint(1, 5)
        cost = random_costs(rng, r, t, gaps=True)
        res = contract_net(cost)
        award = res["award"]
        check_valid(cost, award)
        busy = set(award.values())
        for i in range(r):
            for j in range(t):
                if i not in busy and j not in award:
                    assert cost[i][j] is None
        assert 2 * len(award) >= brute_max_matching(cost)
        assert res["rounds"] <= t
        msgs = res["messages"]
        assert msgs["award"] == len(award)
        assert msgs["bid"] <= r * res["rounds"]


def test_cheapest_pair_always_awarded():
    rng = random.Random(5)
    for _ in range(100):
        r = rng.randint(1, 6)
        t = rng.randint(1, 6)
        cost = random_costs(rng, r, t)
        c, j, i = min((cost[i][j], j, i) for i in range(r) for j in range(t))
        res = contract_net(cost)
        assert res["award"][j] == i


def test_no_robots_or_no_eligible_robot():
    assert contract_net([[None, None], [None, None]])["award"] == {}
    res = contract_net([[None, 4]], batch=1)
    assert res["award"] == {1: 0}
    assert res["rounds"] == 2
