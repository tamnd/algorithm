# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mq-cache/. The authors are listed in prov/VFWZYA.jsonl.

import math
import random
from collections import OrderedDict

import pytest

from mq_cache import MQ, mq_hits


def naive_mq(trace, k, m, life, h):
    """MQ with plain lists; index 0 of each queue is its head (LRU end)."""
    qs = [[] for _ in range(m)]
    freq, expire, qout = {}, {}, []  # qout: list of (id, freq), oldest first
    out, victims = [], []
    for now, x in enumerate(trace, 1):
        res = [q for q in qs if x in q]
        if res:
            res[0].remove(x)
            freq[x] += 1
            out.append(True)
        else:
            old = [f for y, f in qout if y == x]
            qout = [(y, f) for y, f in qout if y != x]
            freq[x] = old[0] + 1 if old else 1
            if sum(len(q) for q in qs) == k:
                q = next(q for q in qs if q)
                v = q.pop(0)
                victims.append(v)
                if h > 0:
                    if len(qout) == h:
                        qout.pop(0)
                    qout.append((v, freq[v]))
            out.append(False)
        expire[x] = now + life
        qs[min(m - 1, int(math.log2(freq[x])))].append(x)
        for j in range(1, m):
            if qs[j] and expire[qs[j][0]] < now:
                c = qs[j].pop(0)
                qs[j - 1].append(c)
                expire[c] = now + life
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


def run(trace, k, m, life, h):
    c = MQ(k, m, life, h)
    out, victims = [], []
    for x in trace:
        out.append(c.access(x))
        if c.evicted is not None:
            victims.append(c.evicted)
        assert x in c and len(c) <= k and len(c.qout) <= h
        assert sum(len(q) for q in c.q) == len(c)
        assert not set(c.qout) & set(c.where)
    return c, out, victims


def test_example_of_the_page():
    trace = list("aabcdbefgab")
    c, out, victims = run(trace, 3, 2, 6, 2)
    assert victims == ["b", "c", "d", "e", "f"]
    assert out.count(False) == 8 and out[-2:] == [True, True]
    assert list(c.q[0]) == ["g"] and list(c.q[1]) == ["a", "b"]
    assert c.freq["a"] == 3 and c.freq["b"] == 3
    assert list(c.qout) == ["e", "f"]
    assert lru_hits(trace, 3).count(False) == 9


def test_matches_naive():
    rng = random.Random(101)
    for _ in range(400):
        k = rng.randint(1, 6)
        m = rng.randint(1, 4)
        life = rng.randint(0, 12)
        h = rng.randint(0, 5)
        trace = [rng.randrange(10) for _ in range(rng.randint(0, 80))]
        _, out, victims = run(trace, k, m, life, h)
        assert (out, victims) == naive_mq(trace, k, m, life, h)


def test_one_queue_is_lru():
    rng = random.Random(102)
    for _ in range(200):
        k = rng.randint(1, 6)
        trace = [rng.randrange(9) for _ in range(rng.randint(0, 60))]
        assert mq_hits(trace, k, 1, rng.randint(0, 9), rng.randint(0, 5)) == lru_hits(trace, k)


def test_qout_restores_the_count():
    c = MQ(1, 3, 100, 4)
    for x in "aaa":
        c.access(x)
    assert c.where["a"] == 1 and c.freq["a"] == 3
    c.access("b")
    assert c.evicted == "a" and c.qout["a"] == 3
    assert not c.access("a")
    assert c.freq["a"] == 4 and c.where["a"] == 2 and "a" not in c.qout
    d = MQ(1, 3, 100, 0)
    for x in "aaaba":
        d.access(x)
    assert d.freq["a"] == 1 and d.where["a"] == 0


def test_expired_head_moves_down_one_queue():
    c = MQ(4, 3, 2, 0)
    for x in "aaaa":
        c.access(x)
    assert c.where["a"] == 2 and c.expire["a"] == 6
    levels = []
    for x in "bcdefgh":
        c.access(x)
        levels.append(c.where.get("a"))
    # expire 6 < 7 at t = 7, so a moves to Q1; expire 9 < 10 at t = 10, so Q0.
    assert levels == [2, 2, 1, 1, 1, 0, 0] and c.freq["a"] == 4


def test_hot_blocks_survive_a_scan_within_their_lifetime():
    c = MQ(8, 4, 1000, 8)
    hot = ["h0", "h1", "h2", "h3"]
    for x in hot * 4:
        c.access(x)
    for i in range(200):
        c.access(f"s{i}")
    assert all(c.access(x) for x in hot)


def test_no_qout_and_a_long_lifetime_is_not_competitive():
    for r in (10, 40, 160):
        trace = ["a", "a"] + ["x", "y"] * r
        assert mq_hits(trace, 2, 2, 10**9, 0).count(False) == 1 + 2 * r
        # With a Qout, x and y come back with count 2, and a is evicted.
        assert mq_hits(trace, 2, 2, 10**9, 1).count(False) == 5


def test_bad_arguments():
    with pytest.raises(ValueError):
        MQ(0, 1, 1, 1)
    with pytest.raises(ValueError):
        MQ(2, 0, 1, 1)
    with pytest.raises(ValueError):
        MQ(2, 1, -1, 1)
    with pytest.raises(ValueError):
        MQ(2, 1, 1, -1)
