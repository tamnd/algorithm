# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-dual/. The authors are listed in prov/F080QZ.jsonl.

import random
from collections import OrderedDict
from fractions import Fraction
from itertools import combinations

import pytest

from greedy_dual import (
    GreedyDualSize,
    GreedyDualSizeDecrement,
    greedy_dual,
    greedy_dual_size,
    miss_cost,
)


def random_requests(rng: random.Random, n: int, m: int, max_size: int, max_cost: int):
    size = {x: rng.randint(1, max_size) for x in range(m)}
    cost = {x: rng.randint(0, max_cost) for x in range(m)}
    trace = [rng.randrange(m) for _ in range(n)]
    return [(x, size[x], cost[x]) for x in trace]


def optimal_cost(requests, capacity: int) -> Fraction:
    """Offline optimum of the forced model by search over all cache states."""
    size = {x: s for x, s, _ in requests}
    best = {frozenset(): Fraction(0)}
    for x, s, c in requests:
        nxt: dict = {}
        for state, value in best.items():
            if x in state:
                options = [(state, value)]
            else:
                members = sorted(state)
                used = sum(size[y] for y in state)
                options = []
                for r in range(len(members) + 1):
                    for out in combinations(members, r):
                        if used - sum(size[y] for y in out) + s <= capacity:
                            options.append(((state - set(out)) | {x}, value + c))
            for st, v in options:
                if st not in nxt or v < nxt[st]:
                    nxt[st] = v
        best = nxt
    return min(best.values())


def test_inflation_form_equals_decrement_form() -> None:
    rng = random.Random(1)
    for _ in range(300):
        capacity = rng.randint(1, 12)
        reqs = random_requests(rng, rng.randint(1, 200), rng.randint(1, 15), 6, 9)
        a, b = GreedyDualSize(capacity), GreedyDualSizeDecrement(capacity)
        for key, size, cost in reqs:
            assert a.request(key, size, cost) == b.request(key, size, cost)
            assert a.contents() == b.contents()
            # the stored values differ only by the global offset L
            for q in a.H:
                assert a.H[q] - a.L == b.H[q]


def test_unit_sizes_and_costs_is_lru() -> None:
    rng = random.Random(2)
    for _ in range(100):
        k = rng.randint(1, 8)
        trace = [rng.randrange(12) for _ in range(500)]
        lru: OrderedDict = OrderedDict()
        expected = []
        for x in trace:
            if x in lru:
                lru.move_to_end(x)
                expected.append(True)
            else:
                expected.append(False)
                if len(lru) == k:
                    lru.popitem(last=False)
                lru[x] = None
        assert greedy_dual(k, [(x, 1) for x in trace]) == expected


def test_weighted_paging_bound_against_optimum() -> None:
    # Unit sizes: (k - h + 1) * GD <= k * OPT_h, with both caches empty at the start.
    rng = random.Random(3)
    for _ in range(200):
        k = rng.randint(1, 4)
        h = rng.randint(1, k)
        reqs = random_requests(rng, rng.randint(1, 14), rng.randint(1, 6), 1, 9)
        assert (k - h + 1) * miss_cost(k, reqs) <= k * optimal_cost(reqs, h)


def test_size_bound_against_optimum() -> None:
    # GreedyDual-Size is Landlord with full credit: (k - h + 1) * cost <= k * OPT_h.
    rng = random.Random(4)
    for _ in range(200):
        k = rng.randint(2, 6)
        h = rng.randint(1, k)
        reqs = random_requests(rng, rng.randint(1, 12), rng.randint(1, 5), h, 9)
        assert (k - h + 1) * miss_cost(k, reqs) <= k * optimal_cost(reqs, h)


def test_cheap_object_is_evicted_before_expensive_one() -> None:
    cache = GreedyDualSize(2)
    cache.request("a", 1, 10)
    cache.request("b", 1, 1)
    cache.request("c", 1, 1)
    assert cache.evicted == ["b"]
    assert cache.L == 1
    cache.request("d", 1, 1)
    assert cache.evicted == ["c"]
    cache.request("e", 1, 1)
    assert cache.contents() == {"a", "e"}
    # Each cheap miss raises L by 1. After 6 more cheap misses L = 9 and the newest
    # object has H = 10, equal to H(a); the tie goes to the older value, so a goes next.
    for i in range(6):
        cache.request(i, 1, 1)
        assert "a" in cache
    assert cache.L == 9
    cache.request(6, 1, 1)
    assert cache.evicted == ["a"]


def test_capacity_is_respected() -> None:
    rng = random.Random(5)
    cache = GreedyDualSize(20)
    for key, size, cost in random_requests(rng, 5000, 60, 8, 20):
        cache.request(key, size, cost)
        assert cache.used == sum(cache.size.values()) <= 20
        assert all(h >= cache.L for h in cache.H.values())


def test_large_object_is_not_loaded() -> None:
    assert greedy_dual_size(3, [("a", 1, 1), ("big", 4, 1), ("a", 1, 1)]) == [False, False, True]


def test_rejects_bad_input() -> None:
    with pytest.raises(ValueError):
        GreedyDualSize(0)
    with pytest.raises(ValueError):
        GreedyDualSize(3).request("a", 0, 1)
