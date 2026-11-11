# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lamport-fast-mutex/. The authors are listed in prov/HZ54V5.jsonl.
from explorer import START, Explorer, procs, walk
from lamport_fast_mutex import make


def explore(n, rounds, **kw):
    lock, unlock, mem = make(n)
    return Explorer(procs(lock, unlock, n, rounds), mem, **kw).explore()


def test_exhaustive_two_processes():
    ex = explore(2, 1)
    assert ex.bad is None and len(ex.states) == 342
    assert ex.deadlock() is None
    ex = explore(2, -1)
    assert ex.bad is None and len(ex.states) == 992
    assert ex.deadlock() is None
    # Deadlock free, but each process can starve.
    assert ex.starvation(0) is not None and ex.starvation(1) is not None
    assert [ex.bypass(p, frm=START) for p in (0, 1)] == [64, 64]


def test_exhaustive_three_processes():
    ex = explore(3, 1)
    assert ex.bad is None and len(ex.states) == 23951
    assert ex.deadlock() is None
    assert all(ex.starvation(p) is None for p in range(3))


def test_fast_path_without_contention():
    # Alone, a process makes exactly 5 writes and 2 reads in one passage.
    for n in (2, 3, 8):
        lock, unlock, mem = make(n)
        for p in (0, n - 1):
            ex = Explorer(procs(lock, unlock, n, 1), mem)
            s, labels = ex.s0, []
            while s[1][p][2] != "F":
                mv = [m for m in ex.succ(s) if m[0] == p][0]
                labels.append(mv[1])
                s = mv[2]
            me = p + 1
            assert labels == [
                ("rem",),
                ("w", ("b", p), True),  # L2
                ("w", "x", me),  # L3
                ("r", "y", 0),  # L4
                ("w", "y", me),  # L8
                ("r", "x", me),  # L9
                ("cs",),
                ("w", "y", 0),  # L16
                ("w", ("b", p), False),  # L17
            ]


def test_worked_example_and_starvation():
    lock, unlock, mem = make(2)
    ex = Explorer(procs(lock, unlock, 2, -1), mem)
    s = ex.run([0] * 6)  # 0: b[0], x = 1, reads y = 0, y = 1, reads x = 1: enters
    assert ex.inside(s) == [0]
    s = ex.run([1] * 5, s)  # 1: b[1], x = 2, reads y = 1, b[1] = false; waits at L6
    assert ex.value(s, "x") == 2 and s[1][1][2] == "T"
    start = s
    for _ in range(20):
        s = ex.run([0] * 3, s)  # 0 leaves: y = 0, b[0] = false
        s = ex.run([1], s)  # 1: reads y = 0; back to L2
        s = ex.run([0] * 6, s)  # 0 enters by the fast path again
        assert ex.inside(s) == [0]
        s = ex.run([1] * 4, s)  # 1: b[1], x = 2, reads y = 1, b[1] = false
        assert s == start  # the same state again, so this round can repeat forever


def test_slow_path():
    # Two processes collide: both write x and y, and the slow path lets one in.
    lock, unlock, mem = make(2)
    ex = Explorer(procs(lock, unlock, 2, 1), mem)
    s = ex.run([0] * 4 + [1] * 4)  # both: b true, x, read y = 0
    s = ex.run([0, 1], s)  # 0: y = 1; 1: y = 2
    s = ex.run([0], s)  # 0 reads x = 2: slow path
    s = ex.run([1], s)  # 1 reads x = 2: it enters by the fast path
    assert ex.inside(s) == [1]
    s = ex.run([0] * 3, s)  # 0: b[0] = false, reads b[0] = false, reads b[1] = true
    assert s[1][0][2] == "T"
    s = ex.run([1] * 3, s)  # 1 leaves: y = 0, b[1] = false
    s = ex.run([0] * 3, s)  # 0: reads b[1] = false, y = 0 at L12 (not 1), y = 0 at L13
    s = ex.run([0] * 5, s)  # 0 starts again and enters by the fast path
    assert ex.inside(s) == [0]


def test_safe_registers_small():
    # One passage each with safe registers: the search finds no violation.
    lock, unlock, mem = make(2)
    dom = {("b", 0): (False, True), ("b", 1): (False, True), "x": (0, 1, 2), "y": (0, 1, 2)}
    ex = Explorer(procs(lock, unlock, 2, 1), mem, mode="safe", domain=dom).explore()
    assert ex.bad is None


def test_tso_breaks_it():
    # Only safety is checked under TSO: the explorer does not force buffers to drain.
    assert explore(2, 1, mode="tso").bad is not None


def test_rmr():
    ex = explore(2, -1, rmr="cc")
    assert [ex.max_cost(p) for p in (0, 1)] == [float("inf"), float("inf")]


def test_random_schedules():
    for n in (4, 6):
        lock, unlock, mem = make(n)
        for seed in range(3):
            res = walk(procs(lock, unlock, n, -1), mem, seed, 3000)
            assert res["most_in_cs"] == 1 and max(res["entries"]) > 0
