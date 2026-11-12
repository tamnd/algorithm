# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/slru/. The authors are listed in prov/1K8PDH.jsonl.

import random
from collections import OrderedDict

import pytest

from slru import SLRU, slru_hits


def naive_slru(trace, k, p):
    """SLRU with plain lists; index 0 is the MRU end of each segment."""
    prob, prot, out, victims = [], [], [], []
    for x in trace:
        if x in prot:
            prot.remove(x)
            prot.insert(0, x)
            out.append(True)
        elif x in prob:
            prob.remove(x)
            prot.insert(0, x)
            if len(prot) > p:
                prob.insert(0, prot.pop())
            out.append(True)
        else:
            if len(prob) + len(prot) == k:
                victims.append(prob.pop())
            prob.insert(0, x)
            out.append(False)
    return out, victims


def lru_hits(trace, k):
    c, out = OrderedDict(), []
    for x in trace:
        if x in c:
            c.move_to_end(x)
            out.append(True)
            continue
        if len(c) == k:
            c.popitem(last=False)
        c[x] = None
        out.append(False)
    return out


def min_misses(trace, k):
    """Belady's MIN: evict the page whose next request is furthest away."""
    cache, m = set(), 0
    for i, x in enumerate(trace):
        if x in cache:
            continue
        m += 1
        if len(cache) == k:

            def nxt(q):
                for j in range(i + 1, len(trace)):
                    if trace[j] == q:
                        return j
                return len(trace) + 1

            cache.remove(max(cache, key=nxt))
        cache.add(x)
    return m


def run(trace, k, p):
    c = SLRU(k, p)
    out, victims = [], []
    for x in trace:
        out.append(c.access(x))
        if c.evicted is not None:
            victims.append(c.evicted)
        assert x in c and len(c) <= k and len(c.prot) <= p
        assert not set(c.prob) & set(c.prot)
    return c, out, victims


def test_example_of_the_page():
    trace = list("ababcdefab")
    c, out, victims = run(trace, 4, 2)
    assert victims == ["c", "d"]
    assert out.count(False) == 6 and out[-2:] == [True, True]
    assert list(c.prot) == ["a", "b"] and list(c.prob) == ["e", "f"]
    assert lru_hits(trace, 4).count(False) == 8


def test_matches_naive():
    rng = random.Random(91)
    for _ in range(400):
        k = rng.randint(1, 6)
        p = rng.randrange(k)
        trace = [rng.randrange(10) for _ in range(rng.randint(0, 80))]
        _, out, victims = run(trace, k, p)
        assert (out, victims) == naive_slru(trace, k, p)


def test_empty_protected_segment_is_lru():
    rng = random.Random(92)
    for _ in range(200):
        k = rng.randint(1, 6)
        trace = [rng.randrange(9) for _ in range(rng.randint(0, 60))]
        assert slru_hits(trace, k, 0) == lru_hits(trace, k)


def test_scan_does_not_touch_protected_pages():
    c = SLRU(8, 4)
    hot = ["h0", "h1", "h2", "h3"]
    for x in hot + hot:
        c.access(x)
    assert set(c.prot) == set(hot)
    for i in range(200):
        c.access(f"s{i}")
    assert set(c.prot) == set(hot)
    assert all(c.access(x) for x in hot)


def test_not_competitive():
    # Stale protected pages hold p slots; two pages fight for the rest.
    for m in (10, 40, 160):
        trace = ["a", "a"] + ["x", "y"] * m
        assert slru_hits(trace, 2, 1).count(False) == 1 + 2 * m
        assert min_misses(trace, 2) == 3


def test_larger_cache_can_miss_more():
    trace = [2, 4, 6, 6, 2, 0, 3, 6, 5, 0, 4, 6, 1]
    assert slru_hits(trace, 2, 1).count(False) == 10
    assert slru_hits(trace, 3, 1).count(False) == 11


def test_bad_arguments():
    with pytest.raises(ValueError):
        SLRU(0, 0)
    with pytest.raises(ValueError):
        SLRU(3, 3)
    with pytest.raises(ValueError):
        SLRU(3, -1)
