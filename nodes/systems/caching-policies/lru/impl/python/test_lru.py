# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lru/. The authors are listed in prov/C24R9P.jsonl.

import random

from lru import LRU, lru_hits


def naive_lru(trace, k):
    """Reference: keep the last use time of each cached page, evict the smallest."""
    last = {}
    hits = []
    for t, p in enumerate(trace):
        if p in last:
            hits.append(True)
        else:
            hits.append(False)
            if len(last) == k:
                victim = min(last, key=last.get)
                del last[victim]
        last[p] = t
    return hits


def min_misses(trace, k):
    """Belady's MIN: on a miss with a full cache, evict the page used furthest in the future."""
    cache = set()
    misses = 0
    for t, p in enumerate(trace):
        if p in cache:
            continue
        misses += 1
        if len(cache) == k:
            def next_use(q):
                for u in range(t + 1, len(trace)):
                    if trace[u] == q:
                        return u
                return len(trace)
            cache.remove(max(cache, key=next_use))
        cache.add(p)
    return misses


def test_example_trace():
    trace = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
    hits = lru_hits(trace, 3)
    assert hits.count(False) == 12
    assert [i for i, h in enumerate(hits) if h] == [4, 6, 11, 12, 14, 16, 18, 19]
    c = LRU(3)
    victims = []
    for p in trace:
        c.access(p)
        if c.evicted is not None:
            victims.append(c.evicted)
    assert victims == [7, 1, 2, 3, 0, 4, 0, 3, 2]
    assert c.contents() == [7, 0, 1]
    assert min_misses(trace, 3) == 9


def test_against_naive():
    rng = random.Random(1)
    for _ in range(300):
        k = rng.randint(1, 5)
        trace = [rng.randrange(8) for _ in range(rng.randint(0, 60))]
        assert lru_hits(trace, k) == naive_lru(trace, k)


def test_size_and_eviction():
    rng = random.Random(2)
    c = LRU(4)
    for _ in range(500):
        p = rng.randrange(10)
        before = c.contents()
        hit = c.access(p)
        assert len(c) <= 4
        assert c.contents()[-1] == p
        if not hit and len(before) == 4:
            assert c.evicted == before[0]


def test_inclusion_and_stack_property():
    rng = random.Random(3)
    for _ in range(100):
        trace = [rng.randrange(9) for _ in range(80)]
        caches = [LRU(k) for k in range(1, 9)]
        for p in trace:
            for c in caches:
                c.access(p)
            for a, b in zip(caches, caches[1:]):
                assert set(a.contents()) <= set(b.contents())
        counts = [sum(lru_hits(trace, k)) for k in range(1, 9)]
        assert counts == sorted(counts)


def test_loop_of_k_plus_one_pages_misses_always():
    for k in range(1, 8):
        trace = list(range(k + 1)) * 20
        assert not any(lru_hits(trace, k))


def test_k_times_min():
    rng = random.Random(4)
    for _ in range(200):
        k = rng.randint(1, 4)
        trace = [rng.randrange(7) for _ in range(rng.randint(1, 40))]
        lru_misses = len(trace) - sum(lru_hits(trace, k))
        assert lru_misses <= k * min_misses(trace, k)


def test_bad_size():
    try:
        LRU(0)
    except ValueError:
        return
    raise AssertionError("k = 0 must be rejected")
