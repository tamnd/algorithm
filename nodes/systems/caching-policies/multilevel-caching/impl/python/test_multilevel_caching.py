# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multilevel-caching/. The authors are listed in prov/6DVKBB.jsonl.

import random

import pytest

from multilevel_caching import MODES, TwoLevelCache, amat, lru_hits


def zipf_trace(seed, n, m, s):
    rng = random.Random(seed)
    weights = [1 / (i + 1) ** s for i in range(m)]
    return rng.choices(range(m), weights, k=n)


def test_inclusive_keeps_l1_inside_l2() -> None:
    rng = random.Random(1)
    for c1, c2 in [(1, 1), (2, 3), (4, 8), (8, 9)]:
        cache = TwoLevelCache(c1, c2, "inclusive")
        for _ in range(3000):
            cache.access(rng.randrange(30))
            assert set(cache.l1) <= set(cache.l2)
            assert len(cache.l1) <= c1 and len(cache.l2) <= c2


def test_exclusive_keeps_levels_disjoint() -> None:
    rng = random.Random(2)
    for c1, c2 in [(1, 1), (2, 3), (4, 8), (8, 2)]:
        cache = TwoLevelCache(c1, c2, "exclusive")
        for _ in range(3000):
            cache.access(rng.randrange(30))
            assert not set(cache.l1) & set(cache.l2)
            assert len(cache.l1) <= c1 and len(cache.l2) <= c2


def test_nine_is_neither() -> None:
    # a miss fills both levels, so the levels share blocks: not exclusive
    cache = TwoLevelCache(2, 2, "nine").feed("abcd")
    assert set(cache.l1) == {"c", "d"} and set(cache.l2) == {"c", "d"}
    # a hits in L1 each time, so L2 never sees it again and ages it out: not inclusive
    cache = TwoLevelCache(2, 3, "nine").feed("aabacadae")
    assert set(cache.l1) == {"a", "e"} and set(cache.l2) == {"c", "d", "e"}


def test_back_invalidation_evicts_a_hot_block() -> None:
    # a is used on every other request, so it always hits in L1 and L2 never sees it again.
    trace = []
    for i in range(10):
        trace += ["a", f"b{i}"]
    inclusive = TwoLevelCache(2, 3, "inclusive").feed(trace)
    nine = TwoLevelCache(2, 3, "nine").feed(trace)
    exclusive = TwoLevelCache(2, 3, "exclusive").feed(trace)
    assert nine.l1_hits == 9 and exclusive.l1_hits == 9  # a misses only once
    assert inclusive.back_invalidations == 3
    assert inclusive.l1_hits == 6  # a was thrown out of L1 three times


def test_exclusive_hierarchy_holds_the_lru_contents_of_the_sum() -> None:
    # The union of L1 and L2 is always the c1 + c2 most recent blocks, so the requests that
    # reach memory are exactly the misses of one LRU cache of size c1 + c2.
    rng = random.Random(3)
    for c1, c2 in [(1, 1), (2, 5), (8, 3), (16, 48)]:
        trace = [rng.randrange(80) for _ in range(5000)]
        cache = TwoLevelCache(c1, c2, "exclusive").feed(trace)
        assert len(trace) - cache.memory == lru_hits(c1 + c2, trace)
        assert cache.l1_hits == lru_hits(c1, trace)


def test_l2_sees_a_stream_with_weak_locality() -> None:
    trace = zipf_trace(4, 100_000, 5000, 0.9)
    cache = TwoLevelCache(100, 400, "nine").feed(trace)
    stream = cache.l2_stream
    near_original = lru_hits(100, trace) / len(trace)
    near_filtered = lru_hits(100, stream) / len(stream)
    # Measured: an LRU cache of 100 blocks hits about 31% of the original requests,
    # but only about 1% of the L1 misses that reach L2.
    assert near_original > 0.28
    assert near_filtered < 0.03
    # the L2 hits all come from blocks that L1 dropped long ago
    assert cache.l2_hits / len(stream) > 0.2


def test_amat_matches_the_mean_cost() -> None:
    trace = zipf_trace(5, 20_000, 2000, 0.9)
    times = {1: 1, 2: 1 + 10, 3: 1 + 10 + 100}  # each level adds its own hit time
    for mode in MODES:
        cache = TwoLevelCache(50, 200, mode)
        cost = sum(times[cache.access(x)] for x in trace)
        n, n2 = len(trace), len(cache.l2_stream)
        m1 = n2 / n  # local (and global) miss rate of L1
        m2 = cache.memory / n2  # local miss rate of L2
        assert amat(1, 10, 100, m1, m2) == pytest.approx(cost / n)
        assert m1 * m2 == pytest.approx(cache.memory / n)  # the global miss rate of L2


def test_rejects_bad_input() -> None:
    with pytest.raises(ValueError):
        TwoLevelCache(4, 2, "inclusive")
    with pytest.raises(ValueError):
        TwoLevelCache(2, 4, "mostly")
