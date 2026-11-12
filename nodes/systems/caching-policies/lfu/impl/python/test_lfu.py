# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lfu/. The authors are listed in prov/4DET4E.jsonl.

import random

import pytest

from lfu import LFU, lfu_hits


def naive_lfu(trace, k):
    """Counts and last use times in a dict; evict the smallest (count, last use)."""
    count, last, out, victims = {}, {}, [], []
    for t, p in enumerate(trace):
        if p in count:
            count[p] += 1
            last[p] = t
            out.append(True)
            continue
        if len(count) == k:
            q = min(count, key=lambda x: (count[x], last[x]))
            del count[q], last[q]
            victims.append(q)
        count[p], last[p] = 1, t
        out.append(False)
    return out, victims


def min_misses(trace, k):
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


def check_structure(c):
    x, freqs, seen = c.head.next, [], 0
    while x is not c.head:
        assert x.items and x.next.prev is x
        freqs.append(x.freq)
        for p in x.items:
            assert c.node[p] is x
        seen += len(x.items)
        x = x.next
    assert freqs == sorted(set(freqs)) and seen == len(c.node) <= c.k


def run(trace, k):
    c = LFU(k)
    out, victims = [], []
    for p in trace:
        out.append(c.access(p))
        if c.evicted is not None:
            victims.append(c.evicted)
        check_structure(c)
        assert p in c
    return c, out, victims


def test_example_with_ties():
    c, out, victims = run("aabbcdaeb", 3)
    # d and c both have count 1: c is older, so the miss on d evicts c; then e evicts d
    assert victims == ["c", "d"]
    assert out == [False, True, False, True, False, False, True, False, True]
    assert c.contents() == {"a", "b", "e"}
    assert (c.count("a"), c.count("b"), c.count("e")) == (3, 3, 1)


def test_matches_naive():
    rng = random.Random(51)
    for _ in range(400):
        k = rng.randint(1, 5)
        trace = [rng.randrange(9) for _ in range(rng.randint(0, 80))]
        _, out, victims = run(trace, k)
        assert (out, victims) == naive_lfu(trace, k)


def test_ties_broken_by_lru():
    c = LFU(3)
    for p in "xyz":
        c.access(p)
    c.access("x")  # x: 2, y: 1, z: 1
    c.access("w")
    assert c.evicted == "y"
    c.access("z")  # z: 2, w: 1
    c.access("v")
    assert c.evicted == "w"


def test_not_competitive():
    # pages 0 and 1 are hot early; then 2 and 3 alternate and evict each other
    k, m, rounds = 3, 50, 40
    trace = [0, 1] * m + [2, 3] * rounds
    misses = lfu_hits(trace, k).count(False)
    assert misses == 2 + 2 * rounds
    assert min_misses(trace, k) == 4


def test_counts_reset_on_eviction():
    c = LFU(1)
    for p in "aaab":
        c.access(p)
    c.access("a")
    assert c.count("a") == 1


def test_bad_size():
    with pytest.raises(ValueError):
        LFU(0)
