# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mru/. The authors are listed in prov/TH6NND.jsonl.

import random

from mru import MRU, mru_hits


def naive_mru(trace, k):
    """Reference: keep the last use time of each cached page, evict the largest."""
    last = {}
    hits = []
    for t, p in enumerate(trace):
        if p in last:
            hits.append(True)
        else:
            hits.append(False)
            if len(last) == k:
                del last[max(last, key=last.get)]
        last[p] = t
    return hits


def lru_misses(trace, k):
    last, misses = {}, 0
    for t, p in enumerate(trace):
        if p not in last:
            misses += 1
            if len(last) == k:
                del last[min(last, key=last.get)]
        last[p] = t
    return misses


def min_misses(trace, k):
    """Belady's MIN: evict the cached page whose next request is furthest away."""
    cache, misses = set(), 0
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


def test_example():
    trace = [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3]
    assert mru_hits(trace, 3) == [False, False, False, False, True, True, False,
                                  True, True, False, True, True]


def test_against_naive():
    rng = random.Random(11)
    for _ in range(300):
        k = rng.randint(1, 5)
        trace = [rng.randrange(8) for _ in range(rng.randint(0, 60))]
        assert mru_hits(trace, k) == naive_mru(trace, k)


def test_at_most_k_pages():
    rng = random.Random(12)
    c = MRU(3)
    for _ in range(400):
        c.access(rng.randrange(7))
        assert len(c) <= 3


def test_loop_of_k_plus_one():
    for k in range(1, 7):
        for rounds in range(1, 30):
            trace = list(range(k + 1)) * rounds
            n = len(trace)
            mru = n - sum(mru_hits(trace, k))
            assert lru_misses(trace, k) == n
            assert mru == (k + 1) + (n - k - 1) // k
            assert mru == min_misses(trace, k)


def test_loops_of_any_length_match_min():
    for k in range(1, 6):
        for length in range(k + 1, 3 * k + 2):
            trace = list(range(length)) * 6
            assert len(trace) - sum(mru_hits(trace, k)) == min_misses(trace, k)


def test_inclusion():
    rng = random.Random(13)
    for _ in range(200):
        caches = [MRU(k) for k in range(1, 7)]
        for _ in range(40):
            p = rng.randrange(8)
            for c in caches:
                c.access(p)
            for a, b in zip(caches, caches[1:]):
                assert set(a.contents()) <= set(b.contents())


def test_not_competitive():
    k = 3
    for m in (10, 100):
        trace = list(range(1, k + 1)) + [k + 1, k] * m
        assert sum(mru_hits(trace, k)) == 0
        assert min_misses(trace, k) == k + 1
