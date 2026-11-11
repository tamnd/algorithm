# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kessels-algorithm/. The authors are listed in prov/F0CXA1.jsonl.
from explorer import Explorer, procs, walk
from kessels_algorithm import make


def explore(n, rounds, **kw):
    lock, unlock, mem = make(n, fence=kw.pop("fence", False))
    return Explorer(procs(lock, unlock, n, rounds), mem, **kw).explore()


def test_exhaustive_two_processes():
    # The two-process algorithm is one node. It can only be checked with two processes.
    for rounds, states in ((1, 101), (-1, 234)):
        ex = explore(2, rounds)
        assert ex.bad is None and len(ex.states) == states
        assert ex.deadlock() is None and all(ex.starvation(p) is None for p in (0, 1))
        assert [ex.bypass(p) for p in (0, 1)] == [1, 1] and ex.fcfs(0) and ex.fcfs(1)


def test_exhaustive_tree_of_three():
    ex = explore(3, 1)
    assert ex.bad is None and len(ex.states) == 3385
    assert [ex.bypass(p) for p in range(3)] == [2, 2, 2]
    ex = explore(3, -1)
    assert ex.bad is None and len(ex.states) == 20436
    assert ex.deadlock() is None
    assert all(ex.starvation(p) is None for p in range(3))
    # Counted from the doorway at the lowest node, the bypass has no bound.
    assert [ex.bypass(p) for p in range(3)] == [64, 64, 64]
    assert not any(ex.fcfs(p) for p in range(3))


def test_worked_example():
    lock, unlock, mem = make(2)
    ex = Explorer(procs(lock, unlock, 2, -1), mem)
    s = ex.run([0, 0, 0, 0])  # 0: b0 = true, reads t1 = 0, writes t0 = 0
    s = ex.run([1, 1, 1, 1], s)  # 1: b1 = true, reads t0 = 0, writes t1 = 1
    assert [ex.value(s, ("t", 1, k)) for k in (0, 1)] == [0, 1]  # turn = 0 xor 1 = 1
    s = ex.run([1, 1], s)  # 1 sees b0 = true and turn = 1, so it waits
    assert s[1][1][2] == "T"
    s = ex.run([0, 0], s)  # 0 sees b1 = true but turn = 1, so it enters
    assert ex.inside(s) == [0]
    s = ex.run([1, 1, 0, 0], s)  # 1 still waits; 0 leaves and writes b0 = false
    assert ex.inside(s) == [] and s[1][1][2] == "T"
    s = ex.run([1], s)  # 1 sees b0 = false and enters
    assert ex.inside(s) == [1]


def drive(ex, s, p, done, limit=100):
    for _ in range(limit):
        if done(s):
            return s
        s = ex.move(s, p)
    raise AssertionError("no progress")


def test_unbounded_bypass_in_the_tree():
    # Process 0 finishes its doorway at node 2 and then is slow. Process 2
    # comes up the other side of the root and finds b[1][0] = false each time.
    lock, unlock, mem = make(3)
    ex = Explorer(procs(lock, unlock, 3, -1), mem)
    s = drive(ex, ex.s0, 0, lambda s: s[1][0][3])
    for _ in range(20):
        s = drive(ex, s, 2, lambda s: s[1][2][2] == "C")
        s = drive(ex, s, 2, lambda s: s[1][2][2] == "R")
    assert s[1][0][2] == "T"
    s = drive(ex, s, 0, lambda s: s[1][0][2] == "C")


def test_solo_steps():
    # Four accesses at each of the ceil(log2 n) nodes to enter, one write per node to leave.
    for n, depth in ((2, 1), (3, 2), (4, 2), (5, 3), (8, 3)):
        lock, unlock, mem = make(n)
        ex = Explorer(procs(lock, unlock, n, 1), mem)
        s = ex.run([0] * (1 + 4 * depth))
        assert s[1][0][2] == "C"
        s = ex.run([0] * (1 + depth), s)
        assert s[1][0][2] == "F"


def test_safe_registers_break_it():
    # A read that overlaps a write may return any value of the domain, even when
    # the write does not change the value. Process 1 reads t0 = 1 during the
    # write t0 = 0 and enters; process 0 then also enters.
    lock, unlock, mem = make(2)
    dom = {a: ((False, True) if a[0] == "b" else (0, 1)) for a in mem}
    ex = Explorer(procs(lock, unlock, 2, 1), mem, mode="safe", domain=dom).explore()
    assert ex.bad is not None
    assert (0, ("begin", ("t", 1, 0), 0)) in ex.bad
    assert (1, ("r", ("t", 1, 0), 1)) in ex.bad


def test_cc_rmr():
    assert [explore(2, -1, rmr="cc").max_cost(p) for p in (0, 1)] == [7, 7]
    assert [explore(3, 1, rmr="cc").max_cost(p) for p in range(3)] == [10, 11, 11]


def test_tso_needs_two_fences():
    # Only safety is checked under TSO: the explorer does not force buffers to drain.
    assert explore(2, 1, mode="tso").bad is not None
    for n, rounds in ((2, 2), (3, 1)):
        assert explore(n, rounds, mode="tso", fence=True).bad is None


def test_random_schedules():
    for n in (4, 7):
        lock, unlock, mem = make(n)
        for seed in range(3):
            res = walk(procs(lock, unlock, n, -1), mem, seed, 4000)
            assert res["most_in_cs"] == 1 and min(res["entries"]) > 0
