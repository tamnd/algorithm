# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dekker-algorithm/. The authors are listed in prov/D4K719.jsonl.
from dekker_algorithm import HOME, MEM, lock, no_turn_lock, no_turn_unlock, unlock
from explorer import FENCE, R, W, Explorer, START, procs, walk


def test_exhaustive_safety_and_progress():
    # Dekker's algorithm is for two processes, so it can only be checked with 2.
    for rounds, states in ((1, 86), (2, 451), (-1, 187)):
        ex = Explorer(procs(lock, unlock, 2, rounds), MEM).explore()
        assert ex.bad is None and len(ex.states) == states
        assert ex.deadlock() is None
        assert all(ex.starvation(p) is None for p in (0, 1))


def test_bypass_is_unbounded():
    ex = Explorer(procs(lock, unlock, 2, -1), MEM).explore()
    # 64 is the cap of the search, which stands for "unbounded".
    assert [ex.bypass(p, START) for p in (0, 1)] == [64, 64]


def section(s, p):
    return s[1][p][2]


def test_scripted_bypass_run():
    ex = Explorer(procs(lock, unlock, 2, -1), MEM)
    s = ex.run([0] * 6)  # p0: one passage; its exit writes turn = 1
    assert ex.value(s, "turn") == 1 and section(s, 0) == "R"
    s = ex.run([1, 1], s)  # p1 starts and raises its flag
    s = ex.run([0, 0, 0, 0, 0], s)  # p0 raises its flag, reads flag[1] and turn = 1, lowers its flag
    assert section(s, 0) == "T" and ex.value(s, ("flag", 0)) is False
    entries, k = 0, 10
    while entries < k:  # p0 takes no step; p1 enters again and again
        before = section(s, 1)
        s = ex.move(s, 1)
        entries += before != "C" and section(s, 1) == "C"
        assert section(s, 0) == "T"
    assert entries == k
    s = ex.run([1, 1, 1], s)  # p1 leaves: critical section step, L7, L8
    assert section(s, 1) == "R"
    for _ in range(40):  # now p0 runs alone and enters
        if section(s, 0) == "C":
            break
        s = ex.move(s, 0)
    assert section(s, 0) == "C"


def test_rmr():
    cc = Explorer(procs(lock, unlock, 2, -1), MEM, rmr="cc").explore()
    assert [cc.max_cost(p) for p in (0, 1)] == [10, 11]
    dsm = Explorer(procs(lock, unlock, 2, -1), MEM, rmr="dsm", home=HOME).explore()
    assert [dsm.max_cost(p) for p in (0, 1)] == [float("inf")] * 2


def test_without_turn_it_deadlocks():
    ex = Explorer(procs(no_turn_lock, no_turn_unlock, 2, 1), MEM).explore()
    assert ex.bad is None and ex.deadlock() is not None


def test_tso_breaks_mutual_exclusion():
    ex = Explorer(procs(lock, unlock, 2, 1), MEM, mode="tso").explore()
    assert [lab[0] for _, lab in ex.bad] == ["rem", "w", "r", "rem", "w", "r"]


def fenced(i):
    """The entry section with a full fence after each write of true to the flag (for TSO)."""
    j = 1 - i
    v = yield W(("flag", i), True)
    v = yield FENCE
    while True:
        f = yield R(("flag", j))
        if not f:
            break
        t = yield R("turn")
        if t == j:
            v = yield W(("flag", i), False)
            while True:
                t = yield R("turn")
                if t != j:
                    break
            v = yield W(("flag", i), True)
            v = yield FENCE


def test_fences_restore_mutual_exclusion():
    # Only safety is checked under TSO: the explorer does not force buffers to drain.
    for rounds in (1, 2, -1):
        assert Explorer(procs(fenced, unlock, 2, rounds), MEM, mode="tso").explore().bad is None


def test_solo_steps():
    ex = Explorer(procs(lock, unlock, 2, 1), MEM)
    s = ex.run([0] * 3)  # remainder step, L1, L2 (reads flag[1] = false)
    assert section(s, 0) == "C"
    s = ex.run([0] * 3, s)  # critical section step, L7, L8
    assert section(s, 0) == "F"


def test_random_schedules():
    for seed in range(5):
        res = walk(procs(lock, unlock, 2, -1), MEM, seed, 3000)
        assert res["most_in_cs"] == 1 and min(res["entries"]) > 0
