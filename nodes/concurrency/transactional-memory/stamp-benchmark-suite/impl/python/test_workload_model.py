# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stamp-benchmark-suite/. The authors are listed in prov/A9KZDJ.jsonl.

import random

from htmsim import HTM
from sched import random_run
from workload_model import (LOCK, kmeans_like, kmeans_memory, labyrinth_like, labyrinth_memory,
                            vacation_like, vacation_memory)

THREADS = 4


def run_kmeans(seed, k):
    r = random.Random(seed)
    points = [[r.randrange(100) for _ in range(6)] for _ in range(THREADS)]

    def make():
        stats = {}
        h = HTM(THREADS, kmeans_memory(k))
        return (h, stats), [kmeans_like(h, p, points[p], k, stats) for p in range(THREADS)]

    (h, stats), sys = random_run(make, r)
    return h, stats, sys, points


def test_kmeans_like_is_exact_and_contention_falls_with_k():
    conflicts = {1: 0, 8: 0}
    for i in range(200):
        k = 1 if i % 2 else 8
        h, stats, sys, points = run_kmeans(i, k)
        assert sys.finished() and all(e is None for e in sys.error)
        flat = [x for pts in points for x in pts]
        for c in range(k):
            mine = [x for x in flat if x % k == c]
            assert h.mem[("n", c)] == len(mine) and h.mem[("sum", c)] == sum(mine)
        assert h.mem[LOCK] == 0
        assert stats.get("htm", 0) + stats.get("lock", 0) == len(flat)
        conflicts[k] += stats.get("conflict", 0)
    assert conflicts[1] > 2 * conflicts[8]


def test_vacation_like_never_oversells():
    items, cap = 5, 3
    overflows = 0
    for seed in range(200):
        r = random.Random(seed)
        sessions = [[r.sample(range(items), r.choice([1, 2, 3])) for _ in range(3)]
                    for _ in range(THREADS)]
        results = []

        def make():
            stats = {}
            h = HTM(THREADS, vacation_memory(items, cap, THREADS), read_cap=8, write_cap=3)
            procs = [vacation_like(h, p, sessions[p], stats, results) for p in range(THREADS)]
            return (h, stats), procs

        (h, stats), sys = random_run(make, r)
        assert sys.finished() and all(e is None for e in sys.error)
        for i in range(items):
            sold = sum(1 for _, want, ok in results if ok and i in want)
            assert h.mem[("free", i)] == cap - sold >= 0
        for p in range(THREADS):
            assert h.mem[("booked", p)] == sum(len(w) for q, w, ok in results if ok and q == p)
        for _, want, ok in results:
            if not ok:                 # stock never grows, so it is still sold out
                assert min(h.mem[("free", i)] for i in want) == 0
        # A booking of 3 items writes 3 counts and the record: 4 lines, more
        # than the write buffer holds, so it can only finish under the lock.
        big = sum(1 for _, want, ok in results if ok and len(want) == 3)
        assert big <= stats.get("lock", 0)
        overflows += stats.get("capacity", 0)
    assert overflows > 0


def run_labyrinth(seed, length):
    r = random.Random(seed)
    cells = 24
    paths = [[sorted(r.sample(range(cells), length)) for _ in range(2)] for _ in range(THREADS)]
    results = []

    def make():
        stats = {}
        h = HTM(THREADS, labyrinth_memory(cells), read_cap=16, write_cap=4)
        return (h, stats), [labyrinth_like(h, p, paths[p], stats, results) for p in range(THREADS)]

    (h, stats), sys = random_run(make, r)
    return h, stats, sys, results, cells


def test_labyrinth_like_paths_are_disjoint_and_long_paths_overflow():
    totals = {2: {}, 6: {}}
    for i in range(150):
        length = 2 if i % 2 else 6
        h, stats, sys, results, cells = run_labyrinth(i, length)
        assert sys.finished() and all(e is None for e in sys.error)
        owner = {}
        for p, path, ok in results:
            if ok:
                for c in path:
                    assert c not in owner          # no cell is claimed twice
                    owner[c] = p
            else:
                assert any(h.mem[("cell", c)] != 0 for c in path)
        for c in range(cells):
            assert h.mem[("cell", c)] == (owner[c] + 1 if c in owner else 0)
        for key, value in stats.items():
            totals[length][key] = totals[length].get(key, 0) + value
        totals[length]["won"] = totals[length].get("won", 0) + sum(ok for _, _, ok in results)
    # Paths of 6 cells never fit a write buffer of 4 lines: every claim that
    # gets as far as writing aborts on capacity and takes the lock. Only a
    # claim that finds a taken cell (and writes nothing) commits in hardware.
    # (A claim can also use up its tries on conflicts before it writes.)
    assert 0 < totals[6]["won"] <= totals[6].get("lock", 0)
    assert totals[6].get("capacity", 0) > 0
    assert totals[2].get("capacity", 0) == 0
    assert totals[2].get("htm", 0) > totals[2].get("lock", 0)


def test_same_seed_same_run():
    a = run_kmeans(7, 2)
    b = run_kmeans(7, 2)
    assert a[1] == b[1] and a[0].mem == b[0].mem and a[2].trace == b[2].trace
