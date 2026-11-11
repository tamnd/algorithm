# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dijkstra-mutex-algorithm/. The authors are listed in prov/EYD54X.jsonl.
from explorer import START, Explorer, procs, walk
from dijkstra_mutex_algorithm import make


def explore(n, rounds, **kw):
    lock, unlock, mem = make(n)
    return Explorer(procs(lock, unlock, n, rounds), mem, **kw).explore()


def test_exhaustive_two_processes():
    ex = explore(2, 1)
    assert ex.bad is None and len(ex.states) == 290
    assert ex.deadlock() is None
    ex = explore(2, -1)
    assert ex.bad is None and len(ex.states) == 850
    assert ex.deadlock() is None
    # Deadlock free, but each process can starve, and the bypass has no bound.
    assert ex.starvation(0) is not None and ex.starvation(1) is not None
    assert [ex.bypass(p, frm=START) for p in (0, 1)] == [64, 64]


def test_exhaustive_three_processes():
    ex = explore(3, 1)
    assert ex.bad is None and len(ex.states) == 33567
    assert ex.deadlock() is None


def test_worked_example():
    lock, unlock, mem = make(2)
    ex = Explorer(procs(lock, unlock, 2, -1), mem)
    s = ex.run([1] * 7)  # step 1: 1 finds b[0] = true and takes the turn
    assert ex.value(s, "k") == 1
    s = ex.run([0] * 6, s)  # step 2: 0 reads k = 1 and b[1] = false; k stays 1
    s = ex.run([1] * 3, s)  # step 3: 1 has the turn, c[1] = false, reads c[0] = true
    assert ex.inside(s) == [1]
    s = ex.run([0] * 4, s)  # step 4: 0 loops again
    s = ex.run([1] * 3, s)  # step 5: 1 leaves
    assert ex.inside(s) == [] and s[1][1][2] == "R"
    s = ex.run([0] * 5, s)  # step 6: 0 reads b[1] = true and takes the turn
    assert ex.value(s, "k") == 0
    s = ex.run([0] * 3, s)  # step 7: 0 enters
    assert ex.inside(s) == [0]


def drive(ex, s, p, done, limit=100):
    for _ in range(limit):
        if done(s):
            return s
        s = ex.move(s, p)
    raise AssertionError("no progress")


def test_starvation_run():
    # Process 0 holds the turn k = 0 and enters again and again. Process 1
    # takes a step in every round, but it always reads b[0] = false.
    lock, unlock, mem = make(2)
    ex = Explorer(procs(lock, unlock, 2, -1), mem)
    s = drive(ex, ex.s0, 0, lambda s: s[1][0][2] == "C")
    s = ex.run([1] * 6, s)  # 1: b[1] = false, reads k = 0, c[1] = true, reads k = 0 and b[0] = false
    start = s
    for _ in range(20):
        s = ex.run([0] * 3, s)  # 0 leaves: c[0] = true, b[0] = true
        assert s[1][0][2] == "R"
        s = ex.run([0] * 5, s)  # 0: b[0] = false, reads k = 0, c[0] = false, reads c[1] = true, enters
        assert ex.inside(s) == [0]
        s = ex.run([1] * 4, s)  # 1: reads k = 0, c[1] = true, reads k = 0 and b[0] = false
        assert s[1][1][2] == "T"
        assert s == start  # the same state again, so this round can repeat forever


def test_solo_steps():
    # Process 0 has the turn at the start: 1 write, 1 read of k, 1 write, n - 1 reads.
    for n in (2, 3, 5, 8):
        lock, unlock, mem = make(n)
        ex = Explorer(procs(lock, unlock, n, 1), mem)
        s = ex.run([0] * (1 + 3 + (n - 1)))
        assert s[1][0][2] == "C"
        # Process 1 must first take the turn: c[1] = true, reads k and b[0], k = 1,
        # then it reads k again. That is 5 more steps.
        ex = Explorer(procs(lock, unlock, n, 1), mem)
        s = ex.run([1] * (1 + 3 + 5 + (n - 1)))
        assert s[1][1][2] == "C"


def test_tso_breaks_it():
    # Only safety is checked under TSO: the explorer does not force buffers to drain.
    assert explore(2, 1, mode="tso").bad is not None


def test_cc_rmr_unbounded():
    # A waiting process writes c[i] again in every round of the loop.
    ex = explore(2, -1, rmr="cc")
    assert ex.max_cost(1) == float("inf")


def test_random_schedules():
    for n in (4, 6):
        lock, unlock, mem = make(n)
        for seed in range(3):
            res = walk(procs(lock, unlock, n, -1), mem, seed, 4000)
            assert res["most_in_cs"] == 1 and sum(res["entries"]) > 0
