# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/eisenberg-mcguire-algorithm/. The authors are listed in prov/Y50GY4.jsonl.
from eisenberg_mcguire_algorithm import ACTIVE, IDLE, WAITING, make
from explorer import START, Explorer, procs, walk


def explore(n, rounds, **kw):
    lock, unlock, mem = make(n)
    return Explorer(procs(lock, unlock, n, rounds), mem, **kw).explore()


def test_exhaustive_two_processes():
    for rounds, states in ((1, 693), (-1, 1829)):
        ex = explore(2, rounds)
        assert ex.bad is None and len(ex.states) == states
        assert ex.deadlock() is None and all(ex.starvation(p) is None for p in (0, 1))
        # Counted from the write flag[i] = WAITING: at most n - 1 = 1 entry of the other.
        assert [ex.bypass(p) for p in (0, 1)] == [1, 1]
    # Before its first write a process is invisible, so from the start there is no bound.
    assert [ex.bypass(p, frm=START) for p in (0, 1)] == [64, 64]
    assert not any(ex.fcfs(p) for p in (0, 1))


def test_exhaustive_three_processes():
    ex = explore(3, 1)
    assert ex.bad is None and len(ex.states) == 40273
    assert ex.deadlock() is None
    assert all(ex.starvation(p) is None for p in range(3))
    # n - 1 = 2 entries of others after the doorway, and this is reached.
    assert [ex.bypass(p) for p in range(3)] == [2, 2, 2]
    assert not any(ex.fcfs(p) for p in range(3))


def test_worked_example():
    lock, unlock, mem = make(3)
    ex = Explorer(procs(lock, unlock, 3, 1), mem)
    s = ex.run([0] * 8)  # 0 alone: turn = 0 is itself, ACTIVE, no clash, turn = 0
    assert ex.inside(s) == [0]
    s = ex.run([2] * 5, s)  # 2: WAITING, reads turn = 0, flag[0] = ACTIVE, reads turn again
    s = ex.run([1] * 5, s)  # 1: the same
    s = ex.run([0] * 5, s)  # 0 leaves: reads turn = 0, flag[1] = WAITING, turn = 1, flag[0] = IDLE
    assert ex.value(s, "turn") == 1 and s[1][0][2] == "F"
    s = ex.run([2] * 3, s)  # 2: flag[0] = IDLE, flag[1] = WAITING, reads turn = 1
    s = ex.run([1] * 6, s)  # 1: flag[0] = IDLE, so j = 1; ACTIVE; no clash; turn = 1 is itself
    assert ex.inside(s) == [1]
    s = ex.run([2] * 2, s)  # 2: flag[1] = ACTIVE, reads turn = 1 again
    s = ex.run([1] * 5, s)  # 1 leaves: reads turn = 1, flag[2] = WAITING, turn = 2, flag[1] = IDLE
    assert ex.value(s, "turn") == 2 and ex.value(s, ("flag", 1)) == IDLE
    assert ex.value(s, ("flag", 2)) == WAITING
    s = ex.run([2] * 6, s)  # 2: flag[1] = IDLE, so j = 2; ACTIVE; no clash; turn = 2 is itself
    assert ex.inside(s) == [2] and ex.value(s, ("flag", 2)) == ACTIVE


def test_solo_steps():
    for n in (2, 3, 5, 8):
        lock, unlock, mem = make(n)
        for p, entry in ((0, n + 4), (1, n + 6)):
            ex = Explorer(procs(lock, unlock, n, 1), mem)
            s = ex.run([p] * (1 + entry))  # the first move leaves the remainder section
            assert s[1][p][2] == "C"
            # The CS is one move; the exit reads turn, scans all n flags, and writes twice.
            s = ex.run([p] * (1 + n + 3), s)
            assert s[1][p][2] == "F"


def test_tso_breaks_it_and_fences_fix_it():
    # Only safety is checked under TSO: the explorer does not force buffers to drain.
    assert explore(2, 1, mode="tso").bad is not None
    for n in (2, 3):
        lock, unlock, mem = make(n, fence=True)
        assert Explorer(procs(lock, unlock, n, 1), mem, mode="tso").explore().bad is None


def test_cc_rmr_unbounded():
    assert explore(2, -1, rmr="cc").max_cost(0) == float("inf")


def test_random_schedules():
    for n in (4, 6):
        lock, unlock, mem = make(n)
        for seed in range(3):
            res = walk(procs(lock, unlock, n, -1), mem, seed, 4000)
            assert res["most_in_cs"] == 1 and min(res["entries"]) > 0
            assert res["max_bypass"] <= n - 1
