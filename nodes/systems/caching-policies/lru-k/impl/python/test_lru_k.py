# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lru-k/. The authors are listed in prov/YZK836.jsonl.

import math
import random
from collections import OrderedDict

import pytest

from lru_k import LRUK, lru_k_hits


def lru_hits(trace, k):
    c, out = OrderedDict(), []
    for p in trace:
        if p in c:
            c.move_to_end(p)
            out.append(True)
            continue
        if len(c) == k:
            c.popitem(last=False)
        c[p] = None
        out.append(False)
    return out


def naive_lru_k(trace, k, K, rip=math.inf):
    """crp = 0: keep every reference time; evict the largest backward K-distance, LRU on ties."""
    refs, buf, out, victims = {}, set(), [], []
    for t, p in enumerate(trace, 1):
        for q in list(refs):
            if q not in buf and t - refs[q][-1] > rip:
                del refs[q]
        if p in buf:
            refs[p].append(t)
            out.append(True)
            continue
        if len(buf) == k:
            def key(q):
                r = refs[q]
                kth = r[-K] if len(r) >= K else 0
                return (kth, r[-1])
            v = min(buf, key=key)
            buf.remove(v)
            victims.append(v)
        refs.setdefault(p, []).append(t)
        buf.add(p)
        out.append(False)
    return out, victims


def run(trace, k, K=2, crp=0, rip=math.inf):
    c = LRUK(k, K, crp, rip)
    out, victims = [], []
    for p in trace:
        out.append(c.access(p))
        if c.evicted is not None:
            victims.append(c.evicted)
        assert p in c and len(c) <= k
    return c, out, victims


def test_k1_is_lru():
    rng = random.Random(71)
    for _ in range(300):
        k = rng.randint(1, 5)
        trace = [rng.randrange(8) for _ in range(rng.randint(0, 60))]
        assert lru_k_hits(trace, k, K=1) == lru_hits(trace, k)


def test_matches_full_history():
    rng = random.Random(72)
    for _ in range(300):
        k = rng.randint(1, 5)
        K = rng.randint(1, 3)
        trace = [rng.randrange(9) for _ in range(rng.randint(0, 60))]
        _, out, victims = run(trace, k, K)
        assert (out, victims) == naive_lru_k(trace, k, K)


def test_matches_full_history_with_rip():
    rng = random.Random(73)
    for _ in range(300):
        k = rng.randint(1, 4)
        rip = rng.randint(0, 12)
        trace = [rng.randrange(8) for _ in range(rng.randint(0, 60))]
        _, out, victims = run(trace, k, 2, 0, rip)
        assert (out, victims) == naive_lru_k(trace, k, 2, rip)


def test_scan_resistance():
    # a and b are referenced twice; the scan pages once, so LRU-2 evicts scan pages
    trace = list("abab") + ["x1", "x2", "x3", "x4", "x5"] + list("ab")
    _, out, victims = run(trace, 3)
    assert victims == ["x1", "x2", "x3", "x4"]
    assert out[-2:] == [True, True]
    assert lru_hits(trace, 3)[-2:] == [False, False]


def test_correlated_references_count_once():
    c = LRUK(2, K=2, crp=3)
    for p in "aaa":
        c.access(p)  # times 1, 2, 3: one uncorrelated reference
    assert c.hist["a"] == [1, 0] and c.last["a"] == 3
    assert c.distance("a") == math.inf
    for p in "bb":
        c.access(p)  # times 4, 5
    c.access("a")  # time 6: 6 - 3 > 3 is false, still correlated
    assert c.hist["a"] == [1, 0]
    c.access("c")  # time 7: a was referenced 1 ago, b 2 ago: both inside crp
    # nobody is eligible, so the rule falls back to all pages; both distances are
    # infinite, and b is the least recently used
    assert c.evicted == "b"


def test_uncorrelated_reference_shifts_history():
    c = LRUK(2, K=2, crp=2)
    for p in "aa":
        c.access(p)  # times 1, 2: HIST = [1, 0], LAST = 2
    c.access("b")  # time 3
    c.access("b")  # time 4
    c.access("a")  # time 5: 5 - 2 > 2, uncorrelated; period = LAST - HIST1 = 1
    assert c.hist["a"] == [5, 2] and c.last["a"] == 5


def test_crp_protects_recent_pages():
    c = LRUK(2, K=2, crp=1)
    for p in "abab":
        c.access(p)  # a: 1, 3; b: 2, 4
    c.access("x")  # time 5: b was referenced 1 ago, not eligible; a is eligible
    assert c.evicted == "a"


def test_bad_arguments():
    with pytest.raises(ValueError):
        LRUK(0)
    with pytest.raises(ValueError):
        LRUK(2, K=0)
    with pytest.raises(ValueError):
        LRUK(2, crp=-1)
