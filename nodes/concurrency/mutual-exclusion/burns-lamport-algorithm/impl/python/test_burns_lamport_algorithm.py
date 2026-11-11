# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/burns-lamport-algorithm/. The authors are listed in prov/XQXAGT.jsonl.
from explorer import START, Explorer, R, W, procs, walk
from burns_lamport_algorithm import make


def explore(n, rounds, **kw):
    lock, unlock, mem = make(n)
    return Explorer(procs(lock, unlock, n, rounds), mem, **kw).explore()


def test_exhaustive_two_processes():
    ex = explore(2, 1)
    assert ex.bad is None and len(ex.states) == 48
    assert ex.deadlock() is None
    ex = explore(2, -1)
    assert ex.bad is None and len(ex.states) == 60
    assert ex.deadlock() is None
    # Process 0 never starves; process 1 can starve, and its bypass has no bound.
    assert ex.starvation(0) is None and ex.starvation(1) is not None
    assert [ex.bypass(p) for p in (0, 1)] == [0, 64]
    assert [ex.bypass(p, frm=START) for p in (0, 1)] == [64, 64]


def test_exhaustive_three_processes():
    ex = explore(3, 1)
    assert ex.bad is None and len(ex.states) == 675
    assert ex.deadlock() is None
    ex = explore(3, -1)
    assert ex.bad is None and len(ex.states) == 1039
    assert ex.deadlock() is None
    assert [ex.starvation(p) is None for p in range(3)] == [True, False, False]
    # Counted from the first write x[i] = true of the passage.
    assert [ex.bypass(p) for p in range(3)] == [1, 64, 64]
    assert [ex.fcfs(p) for p in range(3)] == [True, False, False]


def test_worked_example_and_starvation():
    lock, unlock, mem = make(2)
    ex = Explorer(procs(lock, unlock, 2, -1), mem)
    s = ex.run([1] * 3)  # 1: x[1] = true; reads x[0] = false; enters
    assert ex.inside(s) == [1]
    s = ex.run([0] * 3, s)  # 0: x[0] = true; reads x[1] = true, waits at L9
    s = ex.run([1] * 2, s)  # 1 leaves: x[1] = false
    s = ex.run([1] * 4, s)  # 1: x[1] = true; reads x[0] = true; x[1] = false; waits at L6
    s = ex.run([0], s)  # 0: reads x[1] = false; enters
    assert ex.inside(s) == [0]
    start = s
    for _ in range(20):
        s = ex.run([0] * 2, s)  # 0 leaves: x[0] = false
        s = ex.run([1], s)  # 1: reads x[0] = false; back to L2
        s = ex.run([0] * 2, s)  # 0: x[0] = true
        s = ex.run([1] * 3, s)  # 1: x[1] = true; reads x[0] = true; x[1] = false; waits at L6
        assert s[1][1][2] == "T"
        s = ex.run([0], s)  # 0: reads x[1] = false; enters
        assert ex.inside(s) == [0]
        assert s == start  # the same state again, so this round can repeat forever


def naive(n):
    # Not the algorithm: a process that finds a lower flag up waits with its own flag still up.
    def lock(i):
        while True:
            v = yield W(("x", i), True)
            blocked = -1
            for j in range(i):
                f = yield R(("x", j))
                if f:
                    blocked = j
                    break
            if blocked < 0:
                break
            while True:
                f = yield R(("x", blocked))
                if not f:
                    break
        for j in range(i + 1, n):
            while True:
                f = yield R(("x", j))
                if not f:
                    break

    def unlock(i):
        v = yield W(("x", i), False)

    return lock, unlock, {("x", i): False for i in range(n)}


def test_naive_two_flag_deadlock():
    lock, unlock, mem = naive(2)
    ex = Explorer(procs(lock, unlock, 2, 1), mem).explore()
    assert ex.bad is None and ex.deadlock() is not None
    s = ex.run([0, 0, 1, 1, 1])  # 0: x[0] = true; 1: x[1] = true, reads x[0] = true
    s = ex.run([0, 1] * 10, s)  # 0 reads x[1] = true; 1 reads x[0] = true; forever
    assert ex.inside(s) == [] and ex.value(s, ("x", 0)) and ex.value(s, ("x", 1))


def test_solo_steps():
    # One write and n - 1 reads to enter, one write to leave.
    for n in (2, 3, 5, 8):
        lock, unlock, mem = make(n)
        for p in (0, 1, n - 1):
            ex = Explorer(procs(lock, unlock, n, 1), mem)
            s = ex.run([p] * (1 + n))  # the first move leaves the remainder
            assert s[1][p][2] == "C"
            s = ex.run([p] * 2, s)
            assert s[1][p][2] == "F"


def test_safe_registers():
    # A read that overlaps a write of x[j] can return true or false.
    for n, rounds in ((2, -1), (3, 1)):
        lock, unlock, mem = make(n)
        dom = {("x", i): (False, True) for i in range(n)}
        ex = Explorer(procs(lock, unlock, n, rounds), mem, mode="safe", domain=dom).explore()
        assert ex.bad is None and ex.deadlock() is None


def test_tso_breaks_it():
    # Only safety is checked under TSO: the explorer does not force buffers to drain.
    assert explore(2, 1, mode="tso").bad is not None


def test_rmr():
    ex = explore(3, -1, rmr="cc")
    assert [ex.max_cost(p) for p in range(3)] == [7, float("inf"), float("inf")]


def test_random_schedules():
    for n in (4, 6):
        lock, unlock, mem = make(n)
        for seed in range(3):
            res = walk(procs(lock, unlock, n, -1), mem, seed, 3000)
            assert res["most_in_cs"] == 1 and res["entries"][0] > 0
