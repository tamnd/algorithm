# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gdsf/. The authors are listed in prov/J6DJ3W.jsonl.

import random
from collections import OrderedDict
from fractions import Fraction

import pytest

from gdsf import GDSF, gdsf


def reference(capacity, requests, frequency=True):
    """A direct reading of the rule: sort all candidates, the new file included, at each miss."""
    L = Fraction(0)
    key, freq, size, stamp = {}, {}, {}, {}
    hits = []
    for t, (f, s, c) in enumerate(requests):
        if f in key:
            if frequency:
                freq[f] += 1
            key[f], stamp[f] = L + freq[f] * Fraction(c) / s, t
            hits.append(True)
            continue
        hits.append(False)
        k_new = L + Fraction(c) / s
        order = sorted(list(key) + [f], key=lambda q: (k_new, t) if q == f else (key[q], stamp[q]))
        excess = sum(size.values()) + s - capacity
        chosen = []
        for q in order:
            if excess <= 0:
                break
            if q == f:
                chosen = None
                break
            chosen.append(q)
            excess -= size[q]
        if chosen is None:
            continue
        for q in chosen:
            L = key[q]
            del key[q], freq[q], size[q], stamp[q]
        key[f], freq[f], size[f], stamp[f] = k_new, 1, s, t
    return hits


def gd_size(capacity, requests):
    """Cao and Irani's GreedyDual-Size, for comparison: it always caches the new file."""
    L, H, size, stamp, hits = Fraction(0), {}, {}, {}, []
    for t, (f, s, c) in enumerate(requests):
        if f in H:
            H[f], stamp[f] = L + Fraction(c) / s, t
            hits.append(True)
            continue
        hits.append(False)
        if s > capacity:
            continue
        while sum(size.values()) + s > capacity:
            q = min(H, key=lambda x: (H[x], stamp[x]))
            L = H[q]
            del H[q], size[q], stamp[q]
        H[f], size[f], stamp[f] = L + Fraction(c) / s, s, t
    return hits


def random_requests(rng, n, m, max_size, max_cost):
    size = {x: rng.randint(1, max_size) for x in range(m)}
    cost = {x: rng.randint(0, max_cost) for x in range(m)}
    # a skewed choice, so that some files are hit many times
    weights = [1 / (i + 1) for i in range(m)]
    return [(x, size[x], cost[x]) for x in rng.choices(range(m), weights, k=n)]


@pytest.mark.parametrize("frequency", [True, False])
def test_heap_version_equals_reference(frequency: bool) -> None:
    rng = random.Random(10 + frequency)
    for _ in range(300):
        cap = rng.randint(1, 15)
        reqs = random_requests(rng, rng.randint(1, 250), rng.randint(1, 20), 6, 8)
        assert gdsf(cap, reqs, frequency) == reference(cap, reqs, frequency)


def test_unit_sizes_and_costs_without_frequency_is_lru() -> None:
    rng = random.Random(20)
    for _ in range(100):
        k = rng.randint(1, 8)
        trace = [rng.randrange(12) for _ in range(400)]
        lru: OrderedDict = OrderedDict()
        expected = []
        for x in trace:
            expected.append(x in lru)
            if x in lru:
                lru.move_to_end(x)
                continue
            if len(lru) == k:
                lru.popitem(last=False)
            lru[x] = None
        assert gdsf(k, [(x, 1, 1) for x in trace], frequency=False) == expected


def test_frequency_keeps_a_popular_file() -> None:
    reqs = [(x, 1, 1) for x in "aaabca"]
    assert gdsf(2, reqs) == [False, True, True, False, False, True]
    assert gd_size(2, reqs) == [False, True, True, False, False, False]


def test_large_cold_file_is_not_cached() -> None:
    reqs = [("a", 1, 1), ("a", 1, 1), ("b", 1, 1), ("b", 1, 1), ("c", 2, 1)]
    cache = GDSF(4)
    for f, s, c in reqs:
        cache.request(f, s, c)
    assert cache.contents() == {"a", "b", "c"}
    # z has the key 0 + 1/3, below every cached key: it is not cached and nothing leaves
    assert cache.request("z", 3, 1) is False
    assert cache.contents() == {"a", "b", "c"} and cache.evicted == [] and cache.L == 0
    # GreedyDual-Size caches z, so a second request for z hits
    assert gd_size(4, reqs + [("z", 3, 1), ("z", 3, 1)])[-1] is True


def test_old_popularity_costs_many_misses() -> None:
    # A file requested n times, then never again, costs about 2n misses on a 2-file loop.
    for n in (10, 40, 160):
        reqs = [("a", 1, 1)] * n + [(x, 1, 1) for x in "bc" * n]
        assert gdsf(2, reqs).count(False) == 2 * n + 1
        assert gd_size(2, reqs).count(False) == 3


def test_capacity_and_clock() -> None:
    rng = random.Random(30)
    cache = GDSF(25)
    last_L = cache.L
    for f, s, c in random_requests(rng, 5000, 80, 9, 9):
        cache.request(f, s, c)
        assert cache.used == sum(cache.size.values()) <= 25
        assert all(k >= cache.L for k in cache.key.values())
        assert cache.L >= last_L
        last_L = cache.L


def test_rejects_bad_input() -> None:
    with pytest.raises(ValueError):
        GDSF(0)
    with pytest.raises(ValueError):
        GDSF(2).request("a", 1, -1)
