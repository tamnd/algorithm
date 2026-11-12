# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/write-around/. The authors are listed in prov/ECHMAV.jsonl.

import random

from write_around import WriteAroundCache, run


def random_trace(rng, n, addrs, p_write):
    out = []
    for i in range(n):
        a = rng.randrange(addrs)
        out.append(("W", a, i + 1) if rng.random() < p_write else ("R", a))
    return out


def naive(trace, k, block, on_write_hit):
    """Reference on a plain LRU list, most recent last. Return (read hits, line reads, lines)."""
    order, hits, rd = [], 0, 0
    for req in trace:
        line = req[1] // block
        if req[0] == "R":
            if line in order:
                hits += 1
                order.remove(line)
            else:
                rd += 1
                if len(order) == k:
                    order.pop(0)
            order.append(line)
        elif line in order:
            order.remove(line)
            if on_write_hit == "update":
                order.append(line)
    return hits, rd, order


def write_allocate_reads(trace, k):
    """Read hits of a write-allocate LRU cache, for the pollution example."""
    order, hits = [], 0
    for req in trace:
        x = req[1]
        if x in order:
            hits += req[0] == "R"
            order.remove(x)
        elif len(order) == k:
            order.pop(0)
        order.append(x)
    return hits


def test_matches_naive_reference():
    for seed in range(40):
        rng = random.Random(seed)
        block = rng.choice([1, 2, 4])
        k = rng.randint(1, 5)
        trace = random_trace(rng, 300, 24, rng.choice([0.2, 0.5, 0.8]))
        for mode in ("invalidate", "update"):
            c = run(trace, k, block, mode)
            hits, rd, lines = naive(trace, k, block, mode)
            assert (c.stats.read_hits, c.stats.line_reads, list(c.lines)) == (hits, rd, lines)
            assert c.stats.store_writes == sum(1 for r in trace if r[0] == "W")


def test_writes_never_bring_a_line_in_and_cache_agrees():
    for seed in range(30):
        rng = random.Random(300 + seed)
        for mode in ("invalidate", "update"):
            c = WriteAroundCache(3, 2, mode)
            memory = {}
            for req in random_trace(rng, 200, 16, 0.5):
                before = set(c.lines)
                if req[0] == "R":
                    assert c.read(req[1]) == memory.get(req[1], 0)
                else:
                    c.write(req[1], req[2])
                    memory[req[1]] = req[2]
                    assert set(c.lines) <= before
                assert c.consistent()


def test_worked_example():
    names = "abc"
    trace = [("W", names.index(t[1]), i + 1) if t[0] == "W" else ("R", names.index(t[1]))
             for i, t in enumerate("Wa Wa Ra Wb Rc Wa Rb Ra".split())]
    inv = run(trace, 2).stats
    upd = run(trace, 2, on_write_hit="update").stats
    assert (inv.read_hits, inv.line_reads, inv.store_writes) == (0, 4, 4)
    assert (upd.read_hits, upd.line_reads, upd.store_writes) == (1, 3, 4)


def test_write_stream_does_not_pollute():
    # a hot set of 4 lines read in turn, with a stream of new lines written once between reads
    k, trace, nxt = 4, [], 100
    for r in range(50):
        for x in range(4):
            trace.append(("R", x))
            trace.append(("W", nxt, nxt))
            nxt += 1
    reads = sum(1 for t in trace if t[0] == "R")
    assert run(trace, k).stats.read_hits == reads - 4
    assert write_allocate_reads(trace, k) == 0
