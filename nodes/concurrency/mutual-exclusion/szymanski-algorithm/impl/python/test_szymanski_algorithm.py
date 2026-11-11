# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/szymanski-algorithm/. The authors are listed in prov/PMKEEH.jsonl.
from explorer import START, Explorer, procs, walk
from szymanski_algorithm import make


def explore(n, rounds, **kw):
    lock, unlock, mem = make(n)
    return Explorer(procs(lock, unlock, n, rounds), mem, **kw).explore()


def test_exhaustive_two_processes():
    ex = explore(2, 1)
    assert ex.bad is None and len(ex.states) == 210
    ex = explore(2, -1)
    assert ex.bad is None and len(ex.states) == 240
    assert ex.deadlock() is None and all(ex.starvation(p) is None for p in (0, 1))
    # Counted from the write flag[i] = 1. Process 1 can be passed twice by process 0:
    # once in the batch that is inside, and once more in the next batch, by number.
    assert [ex.bypass(p) for p in (0, 1)] == [1, 2]
    assert [ex.fcfs(p) for p in (0, 1)] == [True, False]


def test_exhaustive_three_processes():
    ex = explore(3, 1)
    assert ex.bad is None and len(ex.states) == 11565
    ex = explore(3, -1)
    assert ex.bad is None and len(ex.states) == 14441
    assert ex.deadlock() is None
    assert all(ex.starvation(p) is None for p in range(3))
    # The largest bypass after the doorway is 2(n - 1) = 4, for process n - 1.
    assert [ex.bypass(p) for p in range(3)] == [2, 3, 4]
    assert [ex.fcfs(p) for p in range(3)] == [True, False, False]
    # Before its first write a process is invisible, so from the start there is no bound.
    assert ex.bypass(0, frm=START) == 64


def test_door_lemma():
    # No process writes 3 at a moment when another process has flag 4.
    for n in (2, 3):
        lock, unlock, mem = make(n)
        ex = Explorer(procs(lock, unlock, n, -1), mem).explore()
        for s in ex.states:
            for p, label, _, _, _ in ex.succ(s):
                if label == ("w", ("flag", p), 3):
                    assert all(ex.value(s, ("flag", q)) != 4 for q in range(n) if q != p)


def test_worked_example():
    lock, unlock, mem = make(2)
    ex = Explorer(procs(lock, unlock, 2, -1), mem)
    s = ex.run([1] * 3)  # 1: flag[1] = 1, reads flag[0] = 0: door_in is open
    s = ex.run([0] * 3, s)  # 0: flag[0] = 1, reads flag[1] = 1 < 3: open
    s = ex.run([1] * 3, s)  # 1: flag[1] = 3, sees flag[0] = 1, so flag[1] = 2
    assert ex.value(s, ("flag", 1)) == 2
    s = ex.run([0] * 3, s)  # 0: flag[0] = 3, sees no 1, flag[0] = 4, no lower process: enters
    assert ex.inside(s) == [0]
    s = ex.run([1] * 3, s)  # 1: sees flag[0] = 4, flag[1] = 4, waits for process 0 at L8
    s = ex.run([0] * 3, s)  # 0 leaves: flag[1] = 4 is fine at L9, flag[0] = 0
    s = ex.run([0] * 3, s)  # 0 again: flag[0] = 1, reads flag[1] = 4: door_in is closed
    assert s[1][0][2] == "T" and ex.value(s, ("flag", 0)) == 1
    s = ex.run([1], s)  # 1: reads flag[0] = 1 < 2: enters
    assert ex.inside(s) == [1]
    s = ex.run([1] * 2, s)  # 1 leaves: flag[1] = 0
    s = ex.run([0] * 4, s)  # 0: reads flag[1] = 0, flag[0] = 3, sees no 1, flag[0] = 4: enters
    assert ex.inside(s) == [0]


def test_solo_steps():
    for n in (2, 3, 5, 8):
        lock, unlock, mem = make(n)
        for p in (0, 1, n - 1):
            ex = Explorer(procs(lock, unlock, n, 1), mem)
            # The first move leaves the remainder; then 2n + 1 + p steps.
            s = ex.run([p] * (2 * n + 2 + p))
            assert s[1][p][2] == "C"
            # The CS is one move; the exit reads the n - 1 - p higher flags and writes once.
            s = ex.run([p] * (1 + n - p), s)
            assert s[1][p][2] == "F"


def test_safe_registers_break_it():
    # With safe registers a read that overlaps a write can return any value 0..4.
    lock, unlock, mem = make(2)
    dom = {("flag", i): range(5) for i in range(2)}
    assert Explorer(procs(lock, unlock, 2, 1), mem, mode="safe", domain=dom).explore().bad is not None


def test_tso_breaks_it():
    # Only safety is checked under TSO: the explorer does not force buffers to drain.
    assert explore(2, 1, mode="tso").bad is not None


def test_rmr():
    # Each wait reads one flag again and again, or scans flags that rarely change.
    ex = explore(2, -1, rmr="cc")
    assert [ex.max_cost(p) for p in (0, 1)] == [10, 11]
    ex = explore(3, -1, rmr="cc")
    assert [ex.max_cost(p) for p in range(3)] == [16, 18, 19]
    lock, unlock, mem = make(2)
    home = {("flag", i): i for i in range(2)}
    ex = Explorer(procs(lock, unlock, 2, -1), mem, rmr="dsm", home=home).explore()
    assert ex.max_cost(0) == float("inf")


def test_random_schedules():
    for n in (4, 6):
        lock, unlock, mem = make(n)
        for seed in range(3):
            res = walk(procs(lock, unlock, n, -1), mem, seed, 4000)
            assert res["most_in_cs"] == 1 and min(res["entries"]) > 0
            assert res["max_bypass"] <= 2 * (n - 1)
