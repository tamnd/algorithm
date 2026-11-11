# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/peterson-algorithm/. The authors are listed in prov/SA5BTH.jsonl.
from explorer import DOOR, R, W, Explorer, START, procs, walk
from peterson_algorithm import HOME, MEM, lock, lock_fenced, unlock


def test_exhaustive_safety_and_progress():
    for rounds, states in ((1, 101), (2, 401), (-1, 117)):
        ex = Explorer(procs(lock, unlock, 2, rounds), MEM).explore()
        assert ex.bad is None and len(ex.states) == states
        assert ex.deadlock() is None
        assert all(ex.starvation(p) is None for p in (0, 1))


def test_bypass_one_and_fcfs():
    ex = Explorer(procs(lock, unlock, 2, -1), MEM).explore()
    assert [ex.bypass(p) for p in (0, 1)] == [1, 1]
    assert ex.fcfs(0) and ex.fcfs(1)
    # Counted from the first step of the entry section, a slow process can be passed any number of times.
    assert ex.bypass(0, START) == 64


def test_worked_example():
    ex = Explorer(procs(lock, unlock, 2, -1), MEM)
    # Both raise their flags, p0 writes turn = 1, p1 writes turn = 0, and both read the other flag as true.
    s = ex.run([0, 0, 1, 1, 0, 1, 0, 1])
    assert ex.value(s, "turn") == 0 and ex.inside(s) == []
    s = ex.run([0], s)  # p0 reads turn = 0, which is not 1, and enters
    assert ex.inside(s) == [0]
    s = ex.run([1, 1, 1, 1], s)  # p1 reads turn = 0 = j and flag[0] = true again and again
    assert ex.inside(s) == [0] and s[1][1][2] == "T"
    s = ex.run([0, 0], s)  # p0 leaves the critical section and lowers its flag
    s = ex.run([1, 1], s)  # p1 reads turn, then flag[0] = false, and enters
    assert ex.inside(s) == [1]


def test_tso_breaks_mutual_exclusion():
    ex = Explorer(procs(lock, unlock, 2, 1), MEM, mode="tso").explore()
    assert ex.bad is not None
    # Each process reads the other flag from memory while its own write still waits in its store buffer.
    assert [lab[0] for _, lab in ex.bad] == ["rem", "w", "w", "r", "rem", "w", "w", "r"]


def test_fence_restores_mutual_exclusion():
    # Only safety is checked under TSO: the explorer does not force buffers to drain.
    for rounds in (1, 2, -1):
        ex = Explorer(procs(lock_fenced, unlock, 2, rounds), MEM, mode="tso").explore()
        assert ex.bad is None


def swapped(i):
    """A wrong variant: it writes turn before it raises its flag."""
    j = 1 - i
    v = yield W("turn", j)
    v = yield W(("flag", i), True)
    v = yield DOOR
    while True:
        f = yield R(("flag", j))
        if not f:
            break
        t = yield R("turn")
        if t != j:
            break


def test_swapped_doorway_breaks_mutual_exclusion():
    ex = Explorer(procs(swapped, unlock, 2, 1), MEM).explore()
    assert ex.bad is not None


def test_rmr():
    cc = Explorer(procs(lock, unlock, 2, -1), MEM, rmr="cc").explore()
    assert [cc.max_cost(p) for p in (0, 1)] == [5, 5]
    dsm = Explorer(procs(lock, unlock, 2, -1), MEM, rmr="dsm", home=HOME).explore()
    assert dsm.max_cost(0) == float("inf")


def test_solo_steps():
    ex = Explorer(procs(lock, unlock, 2, 1), MEM)
    s = ex.run([0] * 5)  # remainder step, L1, L2, L4, critical section step
    assert s[1][0][2] == "X"
    s = ex.run([0], s)
    assert s[1][0][2] == "F"


def test_random_schedules():
    for seed in range(5):
        res = walk(procs(lock, unlock, 2, -1), MEM, seed, 3000)
        assert res["most_in_cs"] == 1 and min(res["entries"]) > 0 and res["max_bypass"] <= 1
