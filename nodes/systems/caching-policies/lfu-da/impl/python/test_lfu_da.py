# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lfu-da/. The authors are listed in prov/6K0S3T.jsonl.

import random

import pytest

from lfu_da import LFUDA, lfu_da_hits


def naive_lfu_da(trace, k):
    """Keys in a dict; scan for the smallest (K, time of latest request) at each miss."""
    age, freq, key, last, out, victims = 0, {}, {}, {}, [], []
    for t, p in enumerate(trace):
        if p in freq:
            freq[p] += 1
        else:
            if len(freq) == k:
                q = min(freq, key=lambda x: (key[x], last[x]))
                age = key[q]
                del freq[q], key[q], last[q]
                victims.append(q)
            freq[p] = 1
        key[p] = freq[p] + age
        last[p] = t
        out.append(freq[p] > 1)
    return out, victims


def naive_lfu_misses(trace, k):
    count, last, misses = {}, {}, 0
    for t, p in enumerate(trace):
        if p not in count:
            misses += 1
            if len(count) == k:
                q = min(count, key=lambda x: (count[x], last[x]))
                del count[q], last[q]
            count[p] = 0
        count[p] += 1
        last[p] = t
    return misses


def run(trace, k):
    c = LFUDA(k)
    out, victims, ages = [], [], []
    for p in trace:
        out.append(c.access(p))
        if c.evicted is not None:
            victims.append(c.evicted)
        ages.append(c.age)
        assert p in c and len(c) <= k
        assert all(c.key(q) >= c.age for q in c.contents())
        assert len(c.heap) <= 2 * k + 17
    return c, out, victims, ages


def test_aging_example():
    c, out, victims, ages = run("aaabcbcbcbc", 2)
    assert victims == ["b", "c", "a"]
    assert out.count(False) == 5
    assert ages[-1] == 3
    assert (c.freq["b"], c.key("b"), c.freq["c"], c.key("c")) == (3, 6, 3, 6)
    # plain LFU keeps a forever and misses on every b and c
    assert naive_lfu_misses("aaabcbcbcbc", 2) == 9


def test_matches_naive():
    rng = random.Random(61)
    for _ in range(400):
        k = rng.randint(1, 5)
        trace = [rng.randrange(9) for _ in range(rng.randint(0, 80))]
        _, out, victims, _ = run(trace, k)
        assert (out, victims) == naive_lfu_da(trace, k)


def test_age_never_decreases():
    rng = random.Random(62)
    for _ in range(100):
        k = rng.randint(1, 6)
        trace = [int(rng.paretovariate(1.2)) % 30 for _ in range(300)]
        _, _, _, ages = run(trace, k)
        assert ages == sorted(ages)


def test_old_popular_object_leaves():
    k, m = 3, 20
    # after the hot object, three objects cycle; LFU keeps "hot" and misses on every request
    trace = ["hot"] * m + [i % 3 for i in range(400)]
    c = LFUDA(k)
    for p in trace:
        c.access(p)
    assert "hot" not in c
    assert naive_lfu_misses(trace, k) == 401
    assert lfu_da_hits(trace, k).count(False) < 60


def test_bad_size():
    with pytest.raises(ValueError):
        LFUDA(0)
