# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tournament-lock/. The authors are listed in prov/RBPQNE.jsonl.
from explorer import W, Explorer, procs, walk
from tournament_lock import make, path


def explore(n, rounds, unlock=None, **kw):
    lock, unlock0, mem = make(n, fence=kw.pop("fence", False))
    return Explorer(procs(lock, unlock or unlock0, n, rounds), mem, **kw).explore()


def test_two_processes_is_peterson():
    ex = explore(2, -1)
    assert ex.bad is None and len(ex.states) == 117
    assert ex.deadlock() is None and all(ex.starvation(p) is None for p in (0, 1))
    assert [ex.bypass(p) for p in (0, 1)] == [1, 1] and ex.fcfs(0) and ex.fcfs(1)


def test_exhaustive_three_processes():
    for rounds, states in ((1, 3262), (-1, 6466)):
        ex = explore(3, rounds)
        assert ex.bad is None and len(ex.states) == states
        assert ex.deadlock() is None
        assert all(ex.starvation(p) is None for p in range(3))
        assert not any(ex.fcfs(p) for p in range(3))
    # Counted from the doorway at the lowest node, the bypass has no bound.
    assert [ex.bypass(p) for p in range(3)] == [64, 64, 64]


def test_exhaustive_four_processes():
    ex = explore(4, 1)
    assert ex.bad is None and len(ex.states) == 58387
    assert ex.deadlock() is None


def test_worked_example():
    lock, unlock, mem = make(4)
    ex = Explorer(procs(lock, unlock, 4, -1), mem)
    s = ex.run([0, 0, 0, 1, 1, 1, 2, 2, 2])  # steps 1 to 3
    s = ex.run([0] * 4 + [1] * 2 + [2] * 3, s)  # steps 4 to 6: 0 and 2 win their nodes, 1 waits
    assert ex.value(s, ("turn", 1)) == 0
    s = ex.run([0, 0], s)  # step 7: 0 reads turn[1] = 0, which is not 1, and enters
    assert ex.inside(s) == [0]
    s = ex.run([2, 2, 0, 0, 0], s)  # steps 8 and 9: 2 waits, 0 leaves (root first)
    s = ex.run([2], s)  # step 10: 2 reads flag[1][0] = false and enters
    assert ex.inside(s) == [2]
    s = ex.run([1] * 5, s)  # step 11: 1 wins node 2 and waits at the root
    assert ex.inside(s) == [2] and s[1][1][2] == "T"
    s = ex.run([2, 2, 2, 1], s)  # steps 12 and 13
    assert ex.inside(s) == [1]


def drive(ex, s, p, done, limit=100):
    for _ in range(limit):
        if done(s):
            return s
        s = ex.move(s, p)
    raise AssertionError("no progress")


def test_unbounded_bypass():
    # Process 0 finishes its doorway at node 2 and then is slow. Process 2
    # comes up the other side of the tree and finds flag[1][0] = false each time.
    lock, unlock, mem = make(3)
    ex = Explorer(procs(lock, unlock, 3, -1), mem)
    s = drive(ex, ex.s0, 0, lambda s: s[1][0][3])
    for _ in range(20):
        s = drive(ex, s, 2, lambda s: s[1][2][2] == "C")
        s = drive(ex, s, 2, lambda s: s[1][2][2] == "R")
    assert s[1][0][2] == "T"
    s = drive(ex, s, 0, lambda s: s[1][0][2] == "C")


def test_solo_steps():
    # Three steps at each of the ceil(log2 n) nodes to enter, and one write per node to leave.
    for n, depth in ((2, 1), (3, 2), (4, 2), (5, 3), (8, 3)):
        lock, unlock, mem = make(n)
        ex = Explorer(procs(lock, unlock, n, 1), mem)
        s = ex.run([0] * (1 + 3 * depth))
        assert s[1][0][2] == "C"
        s = ex.run([0] * (1 + depth), s)
        assert s[1][0][2] == "F"


def test_release_from_the_leaf_breaks_mutual_exclusion():
    size = 4

    def up(i):  # the wrong order: the lowest node first
        for x, s in path(i, size):
            v = yield W(("flag", x, s), False)

    ex = explore(3, 2, unlock=up)
    assert ex.bad is not None
    # 0 frees node 2; 1 wins it and raises flag[1][0]; 0 then lowers the same flag.
    assert ex.bad[8:15] == [
        (0, ("w", ("flag", 2, 0), False)), (1, ("rem",)), (1, ("w", ("flag", 2, 1), True)),
        (1, ("w", ("turn", 2), 0)), (1, ("r", ("flag", 2, 0), False)), (1, ("w", ("flag", 1, 0), True)),
        (0, ("w", ("flag", 1, 0), False)),
    ]


def test_cc_rmr():
    ex = explore(2, -1, rmr="cc")
    assert [ex.max_cost(p) for p in (0, 1)] == [5, 5]
    ex = explore(3, -1, rmr="cc")
    assert [ex.max_cost(p) for p in range(3)] == [10, 10, 8]
    home = {("flag", 1, 0): 0, ("flag", 1, 1): 1, ("turn", 1): 0}
    assert explore(2, -1, rmr="dsm", home=home).max_cost(1) == float("inf")


def test_tso_needs_a_fence():
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
