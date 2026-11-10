# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/erew-pram/. The authors are listed in prov/Z1W3PV.jsonl.

import math
import random

import pytest

from erew_pram import (AccessError, affected_counts, broadcast_steps, is_exclusive, naive_broadcast_steps, run,
                       tree_sum_steps)

SIZES = list(range(0, 70)) + [127, 128, 129, 1000]


def test_broadcast_by_doubling():
    for p in SIZES:
        mem, trace = run({"x": 42}, broadcast_steps(p))
        assert all(mem[("B", i)] == 42 for i in range(p))
        assert len(trace) == (1 + math.ceil(math.log2(p)) if p else 0)
        assert sum(len(s) for s in broadcast_steps(p)) == p  # work p
        for readers, writers in trace:
            assert is_exclusive(readers, writers)


def test_naive_broadcast_needs_concurrent_read():
    for p in range(2, 20):
        with pytest.raises(AccessError):
            run({"x": 1}, naive_broadcast_steps(p))
        mem, trace = run({"x": 1}, naive_broadcast_steps(p), concurrent_read=True)
        assert all(mem[("B", i)] == 1 for i in range(p))
        assert len(trace) == 1 and not is_exclusive(*trace[0])


def test_tree_sum():
    rng = random.Random(1)
    for n in SIZES:
        xs = [rng.randint(-9, 9) for _ in range(n)]
        mem, trace = run({("A", i): x for i, x in enumerate(xs)}, tree_sum_steps(n))
        assert mem.get(("A", 0), 0) == sum(xs)
        assert len(trace) == (math.ceil(math.log2(n)) if n > 1 else 0)
        assert all(is_exclusive(r, w) for r, w in trace)


def test_affected_cells_in_broadcast():
    for p in (1, 2, 5, 16, 100):
        cells, _ = affected_counts({"x": 0}, {"x": 1}, broadcast_steps(p))
        # x and the filled prefix of B differ: 1, then 1 + 1, then 1 + min(2^k, p)
        assert cells[0] == 1
        assert all(c <= 4 ** t for t, c in enumerate(cells))


def random_erew_program(rng, cells, steps, procs):
    """Random steps with exclusive reads and writes on every input.

    Each processor reads distinct cells and writes one of its own two private cells,
    chosen by the values it reads, so the write is exclusive for every input.
    """
    prog = []
    for _ in range(steps):
        addrs = list(range(cells))
        rng.shuffle(addrs)
        k = rng.randint(1, procs)
        step = {}
        free_writes = list(range(cells))
        rng.shuffle(free_writes)
        for pid in range(k):
            reads = tuple(addrs[pid * 2:pid * 2 + rng.randint(0, 2)])
            if len(free_writes) < 2:
                break
            w0, w1 = free_writes.pop(), free_writes.pop()
            c = rng.randint(0, 3)
            step[pid] = (reads, lambda v, w0=w0, w1=w1, c=c: [((w0 if sum(v) % 2 else w1), (sum(v) + c) % 4)])
        prog.append(step)
    return prog


def test_lower_bound_inequalities():
    # EREW: k[t+1] <= c[t] (each differing cell has at most one reader),
    # c[t+1] <= c[t] + 2 k[t+1] (each processor that differs writes one cell in each run),
    # so c[t] <= 3^t c[0] <= 4^t, and a broadcast to p cells needs t >= log_4 p steps.
    rng = random.Random(2)
    for _ in range(400):
        prog = random_erew_program(rng, cells=24, steps=4, procs=8)
        mem0 = {a: rng.randint(0, 3) for a in range(24)}
        mem1 = dict(mem0)
        mem1[rng.randrange(24)] += 1
        cells, procs = affected_counts(mem0, mem1, prog)
        assert cells[0] == 1
        for t in range(len(prog)):
            assert procs[t + 1] <= cells[t]
            assert cells[t + 1] <= cells[t] + 2 * procs[t + 1]
            assert cells[t + 1] <= 4 ** (t + 1)
