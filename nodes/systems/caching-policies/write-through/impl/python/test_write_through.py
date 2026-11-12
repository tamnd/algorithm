# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/write-through/. The authors are listed in prov/J9Z92K.jsonl.

import random

from write_through import WriteThroughCache, run


def random_trace(rng, n, addrs, p_write):
    out = []
    for i in range(n):
        a = rng.randrange(addrs)
        out.append(("W", a, i + 1) if rng.random() < p_write else ("R", a))
    return out


def naive(trace, k, block, write_allocate):
    """Reference: a plain list in LRU order, most recent last, and a word-level memory."""
    memory, order, rd, wr, hits = {}, [], 0, 0, 0
    for req in trace:
        line = req[1] // block
        if line in order:
            hits += 1
            order.remove(line)
            order.append(line)
        elif req[0] == "R" or write_allocate:
            rd += 1
            if len(order) == k:
                order.pop(0)
            order.append(line)
        if req[0] == "W":
            memory[req[1]] = req[2]
            wr += 1
    return {"hits": hits, "line_reads": rd, "store_writes": wr, "lines": order, "memory": memory}


def letters(s):
    names = "abc"
    return [("W", names.index(t[1]), i + 1) if t[0] == "W" else ("R", names.index(t[1]))
            for i, t in enumerate(s.split())]


def test_worked_example():
    trace = letters("Wa Wa Ra Wb Rc Wa Rb Ra")
    nwa = run(trace, 2).stats.as_dict()
    assert (nwa["read_hits"], nwa["line_reads"], nwa["store_writes"]) == (1, 3, 4)
    wa = run(trace, 2, write_allocate=True).stats.as_dict()
    assert (wa["read_hits"], wa["line_reads"], wa["store_writes"]) == (2, 5, 4)


def test_matches_naive_reference():
    for seed in range(40):
        rng = random.Random(seed)
        block = rng.choice([1, 2, 4])
        k = rng.randint(1, 5)
        trace = random_trace(rng, 300, 24, rng.choice([0.2, 0.5, 0.8]))
        for alloc in (False, True):
            c = run(trace, k, block, alloc)
            ref = naive(trace, k, block, alloc)
            s = c.stats
            assert s.read_hits + s.write_hits == ref["hits"]
            assert s.line_reads == ref["line_reads"]
            assert s.store_writes == ref["store_writes"]
            assert list(c.lines) == ref["lines"]


def test_store_always_current_and_cache_agrees():
    for seed in range(30):
        rng = random.Random(1000 + seed)
        block = rng.choice([1, 4])
        trace = random_trace(rng, 200, 16, 0.5)
        for alloc in (False, True):
            c = WriteThroughCache(3, block, alloc)
            memory = {}
            for req in trace:
                if req[0] == "R":
                    assert c.read(req[1]) == memory.get(req[1], 0)
                else:
                    c.write(req[1], req[2])
                    memory[req[1]] = req[2]
                # write-through: the store holds every write at once
                for a, v in memory.items():
                    assert c.store[a // block][a % block] == v
                assert c.consistent()


def test_one_store_write_per_write_request():
    rng = random.Random(7)
    trace = random_trace(rng, 500, 30, 0.6)
    writes = sum(1 for r in trace if r[0] == "W")
    for alloc in (False, True):
        s = run(trace, 4, 2, alloc).stats
        assert s.store_writes == writes == s.words_written
        assert s.write_hits + s.write_misses == writes


def test_no_write_allocate_never_fills_on_write():
    c = WriteThroughCache(2)
    for a in range(5):
        c.write(a, a)
    assert len(c.lines) == 0 and c.stats.line_reads == 0
