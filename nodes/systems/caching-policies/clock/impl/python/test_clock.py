# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clock/. The authors are listed in prov/Z35MNC.jsonl.

import random
from collections import OrderedDict, deque

import pytest

from clock import Clock, clock_hits

TEXTBOOK = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]


def second_chance(trace, k):
    """Second chance as a FIFO queue of [page, bit]: a page with a set bit goes to the tail."""
    q, out, victims = deque(), [], []
    for p in trace:
        hit = next((e for e in q if e[0] == p), None)
        if hit is not None:
            hit[1] = 1
            out.append(True)
            continue
        if len(q) == k:
            while q[0][1] == 1:
                e = q.popleft()
                e[1] = 0
                q.append(e)
            victims.append(q.popleft()[0])
        q.append([p, 1])
        out.append(False)
    return out, victims


def fifo(trace, k):
    q, out, victims = deque(), [], []
    for p in trace:
        if p in q:
            out.append(True)
            continue
        if len(q) == k:
            victims.append(q.popleft())
        q.append(p)
        out.append(False)
    return out, victims


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


def run(trace, k, load_bit=1):
    c = Clock(k, load_bit)
    hits, victims = [], []
    for p in trace:
        hits.append(c.access(p))
        if c.evicted is not None:
            victims.append(c.evicted)
        assert p in c and len(c) <= k
    return c, hits, victims


def test_textbook_string():
    c, hits, victims = run(TEXTBOOK, 3)
    assert hits.count(False) == 14
    assert victims == [7, 1, 2, 0, 3, 4, 2, 0, 3, 1, 2]
    assert c.contents() == {0, 1, 7}
    assert lru_hits(TEXTBOOK, 3).count(False) == 12
    assert fifo(TEXTBOOK, 3)[0].count(False) == 15


def test_matches_second_chance_queue():
    rng = random.Random(41)
    for _ in range(300):
        k = rng.randint(1, 5)
        trace = [rng.randrange(8) for _ in range(rng.randint(0, 60))]
        _, hits, victims = run(trace, k)
        assert (hits, victims) == second_chance(trace, k)


def test_equals_fifo_without_rereference_in_window():
    # each page comes back only after at least k other distinct pages
    rng = random.Random(42)
    for _ in range(200):
        k = rng.randint(1, 5)
        trace = []
        while len(trace) < 50:
            p = rng.randrange(3 * k + 2)
            recent = []
            for q in reversed(trace):
                if q == p:
                    break
                if q not in recent:
                    recent.append(q)
            if p not in trace or len(recent) >= k:
                trace.append(p)
        for load_bit in (0, 1):
            _, hits, victims = run(trace, k, load_bit)
            assert not any(hits)
            assert (hits, victims) == fifo(trace, k)


def test_all_bits_set_gives_the_fifo_victim():
    c, _, _ = run("abcabc", 3)
    assert c.ref == [1, 1, 1]
    c.access("d")
    assert c.evicted == "a" and c.frames == ["d", "b", "c"] and c.ref == [1, 0, 0]


def test_differs_from_lru():
    # at the miss on d all bits are set, so CLOCK evicts the oldest load a; LRU evicts b
    _, hits, victims = run("abacda", 3)
    assert victims == ["a", "b"] and hits.count(False) == 5
    assert lru_hits("abacda", 3).count(False) == 4
    _, hits, _ = run("abacdb", 3)
    assert hits.count(False) == 4
    assert lru_hits("abacdb", 3).count(False) == 5


def test_conservative_and_k_competitive():
    rng = random.Random(44)
    for _ in range(300):
        k = rng.randint(1, 4)
        trace = [rng.randrange(k + 3) for _ in range(rng.randint(1, 30))]
        _, hits, _ = run(trace, k)
        for i in range(len(trace)):
            seen, misses = set(), 0
            for j in range(i, len(trace)):
                seen.add(trace[j])
                if len(seen) > k:
                    break
                misses += not hits[j]
            assert misses <= k
        assert hits.count(False) <= k * min_misses(trace, k)


def test_clear_bit_on_load_is_not_k_competitive():
    # with k = 2 the loaded-clear variant has 6 misses per round, MIN has 2
    trace = list("001211020") * 20
    assert clock_hits(trace, 2, load_bit=0).count(False) == 121
    assert min_misses(trace, 2) == 42
    assert clock_hits(trace, 2).count(False) == 61


def test_loop_misses_every_time():
    for k in (1, 2, 4):
        assert not any(clock_hits(list(range(k + 1)) * 6, k))


def test_bad_arguments():
    with pytest.raises(ValueError):
        Clock(0)
    with pytest.raises(ValueError):
        Clock(2, load_bit=2)
