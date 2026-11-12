# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/write-back/. The authors are listed in prov/67S2DT.jsonl.

import random

from write_back import WriteBackCache, run


def random_trace(rng, n, addrs, p_write):
    out = []
    for i in range(n):
        a = rng.randrange(addrs)
        out.append(("W", a, i + 1) if rng.random() < p_write else ("R", a))
    return out


def write_through_reference(trace, k, block, write_allocate):
    """Write-through with LRU on a plain list: return (store writes, line reads, final lines)."""
    order, rd, wr = [], 0, 0
    for req in trace:
        line = req[1] // block
        if line in order:
            order.remove(line)
            order.append(line)
        elif req[0] == "R" or write_allocate:
            rd += 1
            if len(order) == k:
                order.pop(0)
            order.append(line)
        if req[0] == "W":
            wr += 1
    return wr, rd, order


def letters(s):
    names = "abc"
    return [("W", names.index(t[1]), i + 1) if t[0] == "W" else ("R", names.index(t[1]))
            for i, t in enumerate(s.split())]


def test_worked_example():
    trace = letters("Wa Wa Wa Ra Wb Wb Rc Wa")
    c = run(trace, 2, flush=False)
    assert c.stats.store_writes == 2 and c.dirty == {0}
    assert c.store[0] == [3] and c.store[1] == [6]
    assert c.crash() == {0: [8]}
    c = run(trace, 2)
    assert (c.stats.store_writes, c.stats.line_reads) == (3, 4)
    assert write_through_reference(trace, 2, 1, False)[0] == 6


def test_never_more_store_writes_than_write_through():
    for seed in range(60):
        rng = random.Random(seed)
        block = rng.choice([1, 2, 4])
        k = rng.randint(1, 6)
        trace = random_trace(rng, 300, 32, rng.choice([0.1, 0.4, 0.7, 0.95]))
        for alloc in (True, False):
            wb = run(trace, k, block, alloc)
            wt_writes, wt_reads, wt_lines = write_through_reference(trace, k, block, alloc)
            assert wb.stats.store_writes <= wt_writes
            # same allocation rule and LRU: the same misses and the same final lines
            assert wb.stats.line_reads == wt_reads
            assert list(wb.lines) == wt_lines


def test_dirty_bit_invariant_and_reads():
    for seed in range(40):
        rng = random.Random(500 + seed)
        block = rng.choice([1, 4])
        for alloc in (True, False):
            c = WriteBackCache(3, block, alloc)
            memory = {}
            for req in random_trace(rng, 200, 20, 0.5):
                if req[0] == "R":
                    assert c.read(req[1]) == memory.get(req[1], 0)
                else:
                    c.write(req[1], req[2])
                    memory[req[1]] = req[2]
                assert c.clean_lines_agree()
                assert c.dirty <= set(c.lines)
                assert len(c.lines) <= 3


def test_flush_makes_store_current():
    rng = random.Random(11)
    trace = random_trace(rng, 400, 40, 0.6)
    memory = {r[1]: r[2] for r in trace if r[0] == "W"}
    c = run(trace, 5, 4)
    assert not c.dirty
    for a, v in memory.items():
        assert c.store[a // 4][a % 4] == v


def test_crash_loses_exactly_the_dirty_updates():
    for seed in range(40):
        rng = random.Random(900 + seed)
        trace = random_trace(rng, 150, 12, 0.6)
        memory = {r[1]: r[2] for r in trace if r[0] == "W"}
        c = run(trace, 4, 2, flush=False)
        dirty = set(c.dirty)
        lost = c.crash()
        assert set(lost) <= dirty
        for a, v in memory.items():
            line, off = divmod(a, 2)
            if line in lost:
                assert lost[line][off] == v
            else:
                assert c.store[line][off] == v  # every update outside a lost line is safe


def test_bytes_can_exceed_write_through():
    # one word written in a line of 8 words: write-back moves the whole line
    c = run([("W", 3, 1)], 1, 8)
    assert (c.stats.store_writes, c.stats.words_written) == (1, 8)
