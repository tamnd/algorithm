# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/swisstm/. The authors are listed in prov/DS6V72.jsonl.

from stmsim import (Memory, Run, atomically, audit, bank, count, explore, list_contains, list_insert,
                    list_keys, list_remove, opaque, random_run, read_sums, sorted_list, transfer)
from swisstm import SwissTM


def setup_of(make, bodies, data, tries=2):
    def setup():
        stm = make()
        procs = [atomically(stm, p, b, tries=tries) for p, b in enumerate(bodies)]
        return Memory(stm.memory(data)), procs
    return setup


def inc(a):
    def body(tx):
        v = yield from tx.read(a)
        yield from tx.write(a, v + 1)
    return body


def skew(a, b):
    def body(tx):
        v = yield from tx.read(a)
        yield from tx.write(b, v + 1)
    return body


def put(*pairs):
    def body(tx):
        for a, v in pairs:
            yield from tx.write(a, v)
    return body


def get(*addrs):
    def body(tx):
        out = []
        for a in addrs:
            out.append((yield from tx.read(a)))
        return tuple(out)
    return body


def check_all(data):
    def check(run, truncated):
        if truncated or run.blocked():
            return "a process is stuck"
        return None if opaque(run.history, data) else "not opaque"
    return check


XY = {"x": 0, "y": 0}


def test_eager_write_write_detection():
    stm = SwissTM()
    run = Run(lambda: (Memory(stm.memory(XY)), [atomically(stm, 0, put(("x", 1))),
                                                 atomically(stm, 1, put(("x", 2)), tries=1)]))
    run.steps(0, 5)  # T1: status, clock, alive check, wlock read, CAS: T1 owns wlock(x)
    assert run.mem.w[("wlock", "x")] == (0, 0)
    assert run.finish(1)  # T2 is timid: it finds the owner at its write and aborts itself
    assert [ev[1] for ev in run.history if ev[0][0] == 1] == ["begin", "abort"]
    assert run.finish(0) and run.mem.w["x"] == 1


def test_lazy_read_write_detection():
    stm = SwissTM()
    run = Run(lambda: (Memory(stm.memory(XY)), [atomically(stm, 0, put(("x", 1))), atomically(stm, 1, get("x"))]))
    run.steps(0, 5)  # T1 owns wlock(x) but has not committed
    assert run.finish(1)  # the reader ignores the write lock, reads x = 0 and commits
    assert run.out[1] == (0,) and count(run.history, "abort") == 0
    assert run.finish(0) and run.mem.w["x"] == 1
    assert opaque(run.history, XY)


def test_worked_example_greedy_phase():
    # greedy_after = 1: a transaction becomes greedy after its first write.
    stm = SwissTM(greedy_after=1)
    run = Run(lambda: (Memory(stm.memory(XY)), [atomically(stm, 0, put(("x", 1), ("y", 1))),
                                                 atomically(stm, 1, put(("y", 2), ("x", 2)))]))
    run.steps(1, 7)  # T2 writes y and takes greedy timestamp 1
    assert run.mem.w[("status", 1)] == (0, "active", 1)
    run.steps(0, 7)  # T1 writes x and takes greedy timestamp 2
    assert run.mem.w[("status", 0)] == (0, "active", 2)
    run.steps(1, 4)  # T2 writes x: the owner T1 is younger, so T2 aborts it by CAS on its status
    assert run.mem.w[("status", 0)] == (0, "aborted", 2) and stm.kills == 1
    assert run.blocked() == [1]  # T2 waits until T1 releases wlock(x)
    run.steps(0, 1)  # T1 checks its status at its next write, sees "aborted"
    run.steps(0, 2)  # and releases wlock(x) in its rollback
    assert run.finish(1)  # T2 takes wlock(x) and commits x = y = 2
    assert run.mem.w["x"] == 2 and run.mem.w["y"] == 2
    assert run.finish(0)  # T1 retries after T2 and commits x = y = 1
    assert run.mem.w["x"] == 1 and run.mem.w["y"] == 1
    assert count(run.history, "abort") == 1 and opaque(run.history, XY)


def test_exhaustive_two_transactions():
    for g in (1, 10):
        make = lambda: SwissTM(nprocs=2, greedy_after=g)
        for bodies, data, tries in [([skew("x", "y"), skew("y", "x")], XY, 2), ([inc("x"), inc("x")], XY, 2),
                                    ([put(("x", 1), ("y", 1)), put(("y", 2), ("x", 2))], XY, 1),
                                    ([transfer(0, 1, 3), audit(2)], bank(2, 10), 1)]:
            st = explore(setup_of(make, bodies, data, tries), check_all(data))
            assert st.failure is None and st.runs > 1, (g, st.failure)


def test_seeded_three_transactions():
    # a reader and two greedy writers of the same word: kills, waits and lazy read-write detection
    # together. The exhaustive search of this case takes too long for a unit test, so it is seeded.
    check = check_all(XY)
    setup = setup_of(lambda: SwissTM(greedy_after=1), [get("x"), put(("x", 4)), put(("x", 5))], XY, tries=1)
    for seed in range(300):
        run = random_run(setup, seed)
        assert check(run, False) is None, seed


def test_increments_are_not_lost():
    def check(run, truncated):
        return None if run.mem.w["x"] == count(run.history, "commit") else "lost update"
    for g in (1, 10):
        st = explore(setup_of(lambda: SwissTM(nprocs=2, greedy_after=g), [inc("x"), inc("x")], XY, tries=2), check)
        assert st.failure is None


def test_bank_random_schedules():
    m, data = 3, bank(3, 10)
    for g in (1, 10):
        aborts = 0
        for seed in range(100):
            def setup():
                stm = SwissTM(greedy_after=g)
                def proc(p):
                    for k in range(3):
                        yield from atomically(stm, p, transfer((p + k) % m, (p + k + 1) % m, k + 1))
                    return (yield from atomically(stm, p, audit(m)))
                return Memory(stm.memory(data)), [proc(p) for p in range(3)]
            run = random_run(setup, seed)
            assert all(r is None for r in run.pending)
            assert sum(run.mem.w[f"a{i}"] for i in range(m)) == 30
            assert run.out == [30, 30, 30]
            assert all(s == 30 for s in read_sums(run.history, m))
            assert opaque(run.history, data), (g, seed)
            aborts += count(run.history, "abort")
        assert aborts > 20


def test_linked_list_random_schedules():
    data = sorted_list([2, 5], spare=3)
    for g in (1, 10):
        for seed in range(60):
            def setup():
                stm = SwissTM(greedy_after=g)
                ops = [[list_insert(3, 4), list_contains(5)], [list_remove(2), list_insert(4, 5)],
                       [list_remove(5), list_insert(1, 6)]]
                def proc(p):
                    out = []
                    for body in ops[p]:
                        out.append((yield from atomically(stm, p, body)))
                    return out
                return Memory(stm.memory(data)), [proc(p) for p in range(3)]
            run = random_run(setup, seed)
            assert all(r is None for r in run.pending)
            keys = list_keys(run.mem.w)
            assert set(keys) == {1, 3, 4} and keys == sorted(keys)
            assert opaque(run.history, data), (g, seed)
