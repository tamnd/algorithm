# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/knuth-mutex-algorithm/. The authors are listed in prov/YTPF2R.jsonl.
from explorer import START, Explorer, procs, walk
from knuth_mutex_algorithm import make


def explore(n, rounds, **kw):
    lock, unlock, mem = make(n)
    return Explorer(procs(lock, unlock, n, rounds), mem, **kw).explore()


def test_exhaustive_two_processes():
    for rounds, states in ((1, 256), (-1, 622)):
        ex = explore(2, rounds)
        assert ex.bad is None and len(ex.states) == states
        assert ex.deadlock() is None and all(ex.starvation(p) is None for p in (0, 1))
        # Counted from the write control[i] = 1: at most 2^(n-1) - 1 = 1 entry of the other.
        assert [ex.bypass(p) for p in (0, 1)] == [1, 1]


def test_exhaustive_three_processes():
    ex = explore(3, 1)
    assert ex.bad is None and len(ex.states) == 11504
    ex = explore(3, -1)
    assert ex.bad is None and len(ex.states) == 52250
    assert ex.deadlock() is None
    assert all(ex.starvation(p) is None for p in range(3))
    # 2^(n-1) - 1 = 3 entries of others after the doorway, and this is reached.
    assert [ex.bypass(p) for p in range(3)] == [3, 3, 3]
    assert not any(ex.fcfs(p) for p in range(3))
    # Before its first write a process is invisible, so from the start of the
    # entry section there is no bound.
    assert ex.bypass(0, frm=START) == 64


def test_worked_example():
    lock, unlock, mem = make(2)
    ex = Explorer(procs(lock, unlock, 2, -1), mem)
    s = ex.run([1] * 4)  # 1: control[1] = 1, reads k = 0 and control[0] = 0: phase 1 done
    s = ex.run([0] * 6, s)  # 0: control[0] = 1, k = 0 is itself, control[0] = 2, reads control[1] = 1, k = 0
    assert ex.inside(s) == [0]
    s = ex.run([1] * 5, s)  # 1: control[1] = 2, sees control[0] = 2, back to 1; reads k = 0, control[0] = 2
    assert s[1][1][2] == "T" and ex.value(s, ("control", 1)) == 1
    s = ex.run([0] * 3, s)  # 0 leaves: k = 1, control[0] = 0
    assert ex.value(s, "k") == 1
    s = ex.run([0] * 4, s)  # 0 again: control[0] = 1, reads k = 1 and control[1] = 1: blocked
    s = ex.run([1] * 4, s)  # 1: k = 1 is itself, control[1] = 2, reads control[0] = 1, k = 1
    assert ex.inside(s) == [1]


def test_solo_steps():
    for n in (2, 3, 5, 8):
        lock, unlock, mem = make(n)
        # k = 0 at the start. Process 0 scans nothing in phase 1.
        ex = Explorer(procs(lock, unlock, n, 1), mem)
        s = ex.run([0] * (n + 4))
        assert s[1][0][2] == "C"
        # Process 1 scans 0, n - 1, ..., 2 in phase 1: n - 1 reads.
        ex = Explorer(procs(lock, unlock, n, 1), mem)
        s = ex.run([1] * (2 * n + 3))
        assert s[1][1][2] == "C"
        s = ex.run([1] * 3, s)
        assert s[1][1][2] == "F"


def test_tso_breaks_it():
    # Only safety is checked under TSO: the explorer does not force buffers to drain.
    assert explore(2, 1, mode="tso").bad is not None


def test_cc_rmr_unbounded():
    # A process that fails phase 2 writes control[i] again, so a wait can cost any number of RMRs.
    assert explore(2, -1, rmr="cc").max_cost(0) == float("inf")


def test_random_schedules():
    for n in (4, 6):
        lock, unlock, mem = make(n)
        for seed in range(3):
            res = walk(procs(lock, unlock, n, -1), mem, seed, 4000)
            assert res["most_in_cs"] == 1 and min(res["entries"]) > 0
            assert res["max_bypass"] <= 2 ** (n - 1) - 1
