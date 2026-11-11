# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lamport-bakery-algorithm/. The authors are listed in prov/XJ2MAW.jsonl.
from explorer import Explorer, procs, walk
from lamport_bakery_algorithm import make, safe_domain


def explore(n, rounds, **kw):
    lock, unlock, mem = make(n)
    if kw.get("mode") == "safe":
        kw["domain"] = safe_domain(mem, kw.pop("top"))
    return Explorer(procs(lock, unlock, n, rounds), mem, **kw).explore()


def test_exhaustive_two_and_three_processes():
    # Tickets grow without bound, so each process makes a fixed number of passages.
    for n, rounds, states in ((2, 1, 169), (2, 2, 1025), (2, 3, 3241), (3, 1, 11035)):
        ex = explore(n, rounds)
        assert ex.bad is None and len(ex.states) == states
        assert ex.deadlock() is None
        assert all(ex.starvation(p) is None for p in range(n))
        assert all(ex.fcfs(p) for p in range(n))


def test_bypass_after_the_doorway():
    # With three passages each, process j could pass i twice if it were allowed to; it passes at most once.
    ex = explore(2, 3)
    assert [ex.bypass(p) for p in (0, 1)] == [1, 1]
    ex = explore(3, 1)
    assert [ex.bypass(p) for p in range(3)] == [2, 2, 2]


def test_safe_registers():
    # A read that overlaps a write returns any value of the (cut) domain; mutual exclusion still holds.
    for n, rounds, top, states in ((2, 2, 4, 8666), (3, 1, 3, 171093)):
        ex = explore(n, rounds, mode="safe", top=top)
        assert ex.bad is None and len(ex.states) == states


def test_without_choosing_mutual_exclusion_fails():
    lock, unlock, mem = make(2, choosing=False)
    ex = Explorer(procs(lock, unlock, 2, 1), mem).explore()
    assert len(ex.states) == 51
    # p0 reads number[1] = 0 and stops; p1 takes ticket 1 and enters;
    # p0 writes ticket 1 and enters too, because (1, 0) < (1, 1).
    assert ex.bad == [
        (0, ("rem",)), (0, ("r", ("number", 1), 0)),
        (1, ("rem",)), (1, ("r", ("number", 0), 0)), (1, ("w", ("number", 1), 1)), (1, ("r", ("number", 0), 0)),
        (0, ("w", ("number", 0), 1)), (0, ("r", ("number", 1), 1)),
    ]


def test_tso_needs_two_fences():
    # Only safety is checked under TSO: the explorer does not force buffers to drain.
    lock, unlock, mem = make(2)
    assert Explorer(procs(lock, unlock, 2, 1), mem, mode="tso").explore().bad is not None
    for n, rounds in ((2, 1), (2, 2)):
        lock, unlock, mem = make(n, fence=True)
        assert Explorer(procs(lock, unlock, n, rounds), mem, mode="tso").explore().bad is None


def drive(ex, s, p, done, limit=100):
    for _ in range(limit):
        if done(s):
            return s
        s = ex.move(s, p)
    raise AssertionError("no progress")


def test_worked_example():
    lock, unlock, mem = make(3)
    ex = Explorer(procs(lock, unlock, 3, -1), mem)
    sect = lambda p, x: lambda s: s[1][p][2] == x
    num = lambda s: [ex.value(s, ("number", p)) for p in range(3)]
    s = drive(ex, ex.s0, 2, sect(2, "C"))  # step 1
    # Steps 2 and 3: processes 0 and 1 run their doorways side by side.
    s = ex.run([0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1], s)
    assert num(s) == [2, 2, 1] and s[1][0][3] and s[1][1][3]
    s = ex.run([0] * 6 + [1] * 6, s)  # step 4: both wait
    assert ex.inside(s) == [2]
    s = drive(ex, s, 2, sect(2, "R"))  # step 5
    assert num(s) == [2, 2, 0]
    s = drive(ex, s, 0, sect(0, "C"))  # step 6
    s = ex.run([1] * 6, s)
    assert ex.inside(s) == [0]
    s = drive(ex, s, 2, lambda s: s[1][2][3])  # step 7
    assert num(s) == [2, 2, 3]
    s = drive(ex, s, 0, sect(0, "R"))  # step 8
    s = drive(ex, s, 1, sect(1, "C"))
    s = ex.run([2] * 6, s)
    assert ex.inside(s) == [1] and num(s) == [0, 2, 3]


def test_tickets_grow_without_bound():
    lock, unlock, mem = make(2)
    ex = Explorer(procs(lock, unlock, 2, -1), mem)
    door = lambda p: lambda s: s[1][p][3]
    sect = lambda p, x: lambda s: s[1][p][2] == x
    s = drive(ex, ex.s0, 0, sect(0, "C"))
    seen = [ex.value(s, ("number", 0))]
    p = 1
    for _ in range(8):  # the two processes overlap: one takes a ticket while the other holds one
        s = drive(ex, s, p, door(p))
        seen.append(ex.value(s, ("number", p)))
        s = drive(ex, s, 1 - p, sect(1 - p, "R"))
        s = drive(ex, s, p, sect(p, "C"))
        p = 1 - p
    assert seen == list(range(1, 10))


def test_cc_rmr_does_not_grow_with_passages():
    # The most RMRs in one entry section (CC model) stays 8 for two processes, whatever the number of passages.
    for rounds in (2, 3):
        ex = explore(2, rounds, rmr="cc")
        assert [ex.max_cost(p) for p in (0, 1)] == [8, 8]
    ex = explore(3, 1, rmr="cc")
    assert [ex.max_cost(p) for p in range(3)] == [11, 12, 12]


def test_solo_steps():
    for n in (2, 3, 4):
        lock, unlock, mem = make(n)
        ex = Explorer(procs(lock, unlock, n, 1), mem)
        s = ex.run([0] * (1 + 3 * n))  # remainder step, then 3n shared steps of the entry section
        assert s[1][0][2] == "C"
        s = ex.run([0, 0], s)  # critical section step, then one write
        assert s[1][0][2] == "F"


def test_random_schedules():
    for n in (4, 6):
        lock, unlock, mem = make(n)
        for seed in range(3):
            res = walk(procs(lock, unlock, n, -1), mem, seed, 4000)
            assert res["most_in_cs"] == 1 and res["max_bypass"] <= n - 1
