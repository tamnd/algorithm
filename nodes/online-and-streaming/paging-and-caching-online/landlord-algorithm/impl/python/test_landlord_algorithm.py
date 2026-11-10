# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/landlord-algorithm/. The authors are listed in prov/ESNB1H.jsonl.

import itertools
import random
from fractions import Fraction

from landlord_algorithm import landlord


def offline_opt(requests, size, cost, h):
    """Least fetch cost with a cache of total size h, by a dynamic program over cache contents."""
    layer = {frozenset(): 0}
    for f in requests:
        nxt = {}
        for cache, c in layer.items():
            paid = c if f in cache else c + cost[f]
            pool = [g for g in cache | {f} if g != f]
            for r in range(len(pool) + 1):
                for keep in itertools.combinations(pool, r):
                    new = frozenset(keep) | {f}
                    if sum(size[g] for g in new) <= h and (new not in nxt or paid < nxt[new]):
                        nxt[new] = paid
        layer = nxt
    return min(layer.values())


def lru_faults(requests, k):
    cache, faults = [], 0
    for f in requests:
        if f in cache:
            cache.remove(f)
        else:
            faults += 1
            if len(cache) == k:
                cache.pop(0)
        cache.append(f)
    return faults


def random_instance(rng):
    u = rng.randint(2, 6)
    size = {f: rng.randint(1, 3) for f in range(u)}
    cost = {f: rng.randint(0, 9) for f in range(u)}
    k = rng.randint(max(size.values()), 7)
    requests = [rng.randrange(u) for _ in range(rng.randint(0, 14))]
    return requests, size, cost, k


def test_example() -> None:
    size = {"a": 1, "b": 2, "c": 1, "d": 2}
    cost = {"a": 4, "b": 6, "c": 1, "d": 2}
    total, log = landlord(["a", "b", "c", "d", "a", "c", "b"], size, cost, 4)
    assert total == 4 + 6 + 1 + 2 + 1 + 6
    assert log == [("a", []), ("b", []), ("c", []), ("d", ["c", "b"]), ("c", []), ("b", ["d"])]
    assert offline_opt(["a", "b", "c", "d", "a", "c", "b"], size, cost, 4) == 18


def test_k_competitive_against_offline_optimum() -> None:
    rng = random.Random(7)
    for _ in range(300):
        requests, size, cost, k = random_instance(rng)
        opt = offline_opt(requests, size, cost, k)
        for reset in ("full", "keep"):
            total, _ = landlord(requests, size, cost, k, reset)
            assert total <= k * opt


def test_resource_augmentation() -> None:
    rng = random.Random(8)
    for _ in range(300):
        requests, size, cost, k = random_instance(rng)
        h = rng.randint(max(size.values()), k)
        opt = offline_opt(requests, size, cost, h)
        for reset in ("full", "keep"):
            total, _ = landlord(requests, size, cost, k, reset)
            assert total * (k - h + 1) <= k * opt


def test_unit_sizes_and_costs_is_lru() -> None:
    rng = random.Random(9)
    for _ in range(200):
        k = rng.randint(1, 4)
        u = rng.randint(1, 7)
        requests = [rng.randrange(u) for _ in range(rng.randint(0, 30))]
        ones = {f: 1 for f in range(u)}
        total, _ = landlord(requests, ones, ones, k, "full")
        assert total == lru_faults(requests, k)


def test_edges() -> None:
    assert landlord([], {}, {}, 3) == (Fraction(0), [])
    total, log = landlord([0, 0, 0], {0: 2}, {0: 5}, 2)
    assert total == 5 and log == [(0, [])]
    try:
        landlord([0], {0: 4}, {0: 1}, 3)
    except ValueError:
        pass
    else:
        raise AssertionError("an oversized file must be rejected")
