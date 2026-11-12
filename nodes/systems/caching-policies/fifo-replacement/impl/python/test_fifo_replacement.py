# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fifo-replacement/. The authors are listed in prov/DTB1HB.jsonl.

import random

from fifo_replacement import FIFO, fifo_hits


def naive_fifo(trace, k):
    """Reference: keep the load time of each cached page, evict the smallest."""
    loaded = {}
    hits = []
    for t, p in enumerate(trace):
        if p in loaded:
            hits.append(True)
            continue
        hits.append(False)
        if len(loaded) == k:
            del loaded[min(loaded, key=loaded.get)]
        loaded[p] = t
    return hits


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


def misses(trace, k):
    return len(trace) - sum(fifo_hits(trace, k))


def test_textbook_string():
    trace = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
    assert misses(trace, 3) == 15
    c = FIFO(3)
    victims = []
    for p in trace:
        c.access(p)
        if c.evicted is not None:
            victims.append(c.evicted)
    assert victims == [7, 0, 1, 2, 3, 0, 4, 2, 3, 0, 1, 2]
    assert c.contents() == [7, 0, 1]


def test_belady_anomaly():
    trace = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
    assert misses(trace, 3) == 9
    assert misses(trace, 4) == 10


def test_against_naive():
    rng = random.Random(21)
    for _ in range(300):
        k = rng.randint(1, 5)
        trace = [rng.randrange(8) for _ in range(rng.randint(0, 60))]
        assert fifo_hits(trace, k) == naive_fifo(trace, k)


def test_at_most_k_and_hits_do_not_reorder():
    rng = random.Random(22)
    c = FIFO(4)
    for _ in range(500):
        p = rng.randrange(9)
        before = c.contents()
        if c.access(p):
            assert c.contents() == before
        assert len(c) <= 4


def test_k_times_min():
    rng = random.Random(23)
    for _ in range(200):
        k = rng.randint(1, 4)
        trace = [rng.randrange(7) for _ in range(rng.randint(1, 40))]
        assert misses(trace, k) <= k * min_misses(trace, k)


def test_loop_misses_always():
    for k in range(1, 6):
        trace = list(range(k + 1)) * 10
        assert misses(trace, k) == len(trace)
