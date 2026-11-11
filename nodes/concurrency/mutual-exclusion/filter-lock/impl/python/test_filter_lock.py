# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/filter-lock/. The authors are listed in prov/5JN2ZF.jsonl.
from explorer import DOOR, R, W, Explorer, procs, walk
from filter_lock import make


def explore(n, rounds, **kw):
    lock, unlock, mem = make(n, fence=kw.pop("fence", False))
    return Explorer(procs(lock, unlock, n, rounds), mem, **kw).explore()


def test_two_processes_is_peterson():
    # With n = 2 there is one level, and the filter lock is Peterson's algorithm,
    # with the two reads of the waiting loop in the other order.
    for rounds, states in ((1, 105), (2, 409), (-1, 119)):
        ex = explore(2, rounds)
        assert ex.bad is None and len(ex.states) == states
        assert ex.deadlock() is None
        assert all(ex.starvation(p) is None for p in (0, 1))
    assert [ex.bypass(p) for p in (0, 1)] == [1, 1]
    assert ex.fcfs(0) and ex.fcfs(1)


def test_exhaustive_three_processes():
    ex = explore(3, 1)
    assert ex.bad is None and len(ex.states) == 25633
    assert ex.deadlock() is None
    assert all(ex.starvation(p) is None for p in range(3))
    # The doorway (L2 and L3 of level 1) does not give first come, first served order.
    assert not any(ex.fcfs(p) for p in range(3))


def drive(ex, s, p, done, limit=200):
    for _ in range(limit):
        if done(s):
            return s
        s = ex.move(s, p)
    raise AssertionError("no progress")


def test_worked_example():
    lock, unlock, mem = make(3)
    ex = Explorer(procs(lock, unlock, 3, -1), mem)
    lv = lambda s: [ex.value(s, ("level", p)) for p in range(3)]
    s = ex.run([0, 0, 0, 1, 1, 1, 2, 2, 2])  # steps 1 to 3: all three come to level 1
    assert lv(s) == [1, 1, 1] and ex.value(s, ("victim", 1)) == 2
    s = ex.run([0, 0, 0, 1, 1, 1], s)  # steps 4 and 5: 0 and 1 pass level 1
    assert lv(s) == [2, 2, 1] and ex.value(s, ("victim", 2)) == 1
    s = ex.run([2, 2, 0, 1, 1], s)  # steps 6 to 8: 2 waits, 0 enters, 1 waits
    assert ex.inside(s) == [0]
    s = ex.run([0, 0, 1, 1, 1], s)  # steps 9 and 10: 0 leaves, 1 enters
    assert ex.inside(s) == [1] and lv(s) == [0, 2, 1]
    s = ex.run([2, 2, 2, 1, 1], s)  # steps 11 and 12: 2 still waits, 1 leaves
    assert ex.inside(s) == [] and lv(s) == [0, 0, 1]
    s = ex.run([2] * 8, s)  # step 13: 2 passes both levels
    assert ex.inside(s) == [2]


def test_unbounded_bypass():
    # Process 0 finishes its doorway and then does not move. Processes 1 and 2
    # take turns: each one that comes to level 1 frees the other one.
    ex = Explorer(procs(*make(3)[:2], 3, -1), make(3)[2])
    door = lambda p: lambda s: s[1][p][3]
    sect = lambda p, x: lambda s: s[1][p][2] == x
    s = drive(ex, ex.s0, 0, door(0))
    s = drive(ex, s, 1, door(1))
    entries, a, b = 0, 1, 2
    for _ in range(20):
        s = drive(ex, s, b, door(b))  # b writes victim[1] = b, which frees a
        s = drive(ex, s, a, sect(a, "C"))  # a passes both levels and enters
        entries += 1
        s = drive(ex, s, a, sect(a, "R"))
        a, b = b, a
    assert entries == 20 and s[1][0][2] == "T" and ex.value(s, ("level", 0)) == 1
    # Process 1 started its doorway after process 0 finished its own, and still entered first: not FCFS.
    # Process 0 is not the victim of level 1 any more, so it enters when it runs.
    assert ex.value(s, ("victim", 1)) != 0
    s = drive(ex, s, 0, sect(0, "C"))
    assert ex.inside(s) == [0]


def test_solo_steps():
    # Each level costs 2 writes, 1 read of victim and n - 1 reads of level: (n - 1)(n + 2) steps.
    for n in (2, 3, 4, 5):
        lock, unlock, mem = make(n)
        ex = Explorer(procs(lock, unlock, n, 1), mem)
        s = ex.run([0] * (1 + (n - 1) * (n + 2)))  # the remainder step comes first
        assert s[1][0][2] == "C"
        s = ex.run([0, 0], s)  # critical section step, then one write
        assert s[1][0][2] == "F"


def swapped(n):
    """A wrong variant: it writes victim before level at each level."""

    def lock(i):
        for lev in range(1, n):
            v = yield W(("victim", lev), i)
            v = yield W(("level", i), lev)
            if lev == 1:
                v = yield DOOR
            while True:
                vic = yield R(("victim", lev))
                if vic != i:
                    break
                ks = [k for k in range(n) if k != i]
                for k in ks:
                    lk = yield R(("level", k))
                    if lk >= lev:
                        break
                else:
                    break

    return lock


def test_swapped_writes_break_mutual_exclusion():
    for n in (2, 3):
        _, unlock, mem = make(n)
        ex = Explorer(procs(swapped(n), unlock, n, 1), mem).explore()
        assert ex.bad is not None


def test_cc_rmr():
    ex = explore(2, -1, rmr="cc")
    assert [ex.max_cost(p) for p in (0, 1)] == [5, 5]
    ex = explore(3, 1, rmr="cc")
    assert [ex.max_cost(p) for p in range(3)] == [10, 10, 10]
    ex = explore(2, -1, rmr="dsm", home={("level", 0): 0, ("level", 1): 1, ("victim", 1): 0})
    assert ex.max_cost(1) == float("inf")


def test_tso_needs_a_fence():
    # Only safety is checked under TSO: the explorer does not force buffers to drain.
    assert explore(2, 1, mode="tso").bad is not None
    for rounds in (1, 2):
        assert explore(2, rounds, mode="tso", fence=True).bad is None


def test_random_schedules():
    for n in (4, 5):
        lock, unlock, mem = make(n)
        for seed in range(3):
            res = walk(procs(lock, unlock, n, -1), mem, seed, 4000)
            assert res["most_in_cs"] == 1 and min(res["entries"]) > 0
