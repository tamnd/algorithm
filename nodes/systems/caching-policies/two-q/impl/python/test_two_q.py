# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-q/. The authors are listed in prov/RTRVA7.jsonl.

import random
from collections import OrderedDict, deque

import pytest

from two_q import SimplifiedTwoQ, TwoQ, two_q_hits


def naive_two_q(trace, k, kin, kout):
    """Full 2Q with plain lists; index 0 is the head (newest) of each queue."""
    a1in, a1out, am, out, victims = [], [], [], [], []

    def reclaim():
        if len(a1in) + len(am) < k:
            return
        if len(a1in) > kin:
            y = a1in.pop()
            a1out.insert(0, y)
            if len(a1out) > kout:
                a1out.pop()
        else:
            y = am.pop()
        victims.append(y)

    for p in trace:
        if p in am:
            am.remove(p)
            am.insert(0, p)
            out.append(True)
        elif p in a1in:
            out.append(True)
        elif p in a1out:
            a1out.remove(p)
            reclaim()
            am.insert(0, p)
            out.append(False)
        else:
            reclaim()
            a1in.insert(0, p)
            out.append(False)
    return out, victims


def lru_misses(trace, k):
    c, m = OrderedDict(), 0
    for p in trace:
        if p in c:
            c.move_to_end(p)
            continue
        m += 1
        if len(c) == k:
            c.popitem(last=False)
        c[p] = None
    return m


def fifo_hits(trace, k):
    q, out = deque(), []
    for p in trace:
        if p in q:
            out.append(True)
            continue
        if len(q) == k:
            q.popleft()
        q.append(p)
        out.append(False)
    return out


def run(trace, k, kin, kout):
    c = TwoQ(k, kin, kout)
    out, victims = [], []
    for p in trace:
        out.append(c.access(p))
        if c.evicted is not None:
            victims.append(c.evicted)
        assert p in c and len(c) <= k
        assert not set(c.a1in) & set(c.am)
        assert not set(c.a1out) & c.contents()
        assert len(c.a1out) <= kout
    return c, out, victims


def test_example_of_the_page():
    trace = list("aabcdeafghia")
    c, out, victims = run(trace, 4, 1, 2)
    assert victims == ["a", "b", "c", "d", "e", "f"]
    assert out.count(False) == 10 and out[1] and out[-1]
    assert list(c.am) == ["a"] and list(c.a1in) == ["g", "h", "i"]
    assert list(c.a1out) == ["e", "f"]
    assert lru_misses(trace, 4) == 11
    s = SimplifiedTwoQ(4, 1)
    assert [s.access(p) for p in trace].count(False) == 9


def test_matches_naive():
    rng = random.Random(81)
    for _ in range(400):
        k = rng.randint(1, 6)
        kin = rng.randrange(k)
        kout = rng.randint(0, 4)
        trace = [rng.randrange(10) for _ in range(rng.randint(0, 80))]
        _, out, victims = run(trace, k, kin, kout)
        assert (out, victims) == naive_two_q(trace, k, kin, kout)


def test_kout_zero_is_fifo():
    rng = random.Random(82)
    for _ in range(200):
        k = rng.randint(1, 6)
        trace = [rng.randrange(9) for _ in range(rng.randint(0, 60))]
        assert two_q_hits(trace, k, rng.randrange(k), 0) == fifo_hits(trace, k)


def test_correlated_hit_does_not_promote():
    c = TwoQ(4, 1, 2)
    for p in "xxx":
        c.access(p)
    assert list(c.a1in) == ["x"] and not c.am
    s = SimplifiedTwoQ(4, 1)
    for p in "xx":
        s.access(p)
    assert list(s.am) == ["x"]


def test_hot_pages_survive_a_long_scan():
    k, kin, kout = 8, 2, 4
    hot = ["h0", "h1", "h2", "h3"]
    warm = [p for p in hot] + [f"w{i}" for i in range(6)] + hot
    c = TwoQ(k, kin, kout)
    for p in warm:
        c.access(p)
    assert set(hot) <= set(c.am)
    for i in range(200):
        c.access(f"s{i}")
    assert set(hot) <= set(c.am)
    assert all(c.access(p) for p in hot)


def test_bad_arguments():
    with pytest.raises(ValueError):
        TwoQ(0, 0, 0)
    with pytest.raises(ValueError):
        TwoQ(4, 4, 2)
    with pytest.raises(ValueError):
        SimplifiedTwoQ(3, 3)
