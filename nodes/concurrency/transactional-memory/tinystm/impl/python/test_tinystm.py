# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tinystm/. The authors are listed in prov/PKTMQN.jsonl.

from stmsim import (Abort, Memory, Run, atomically, audit, bank, count, explore, list_contains, list_insert,
                    list_keys, list_remove, opaque, random_run, read_sums, sorted_list, transfer)
from tinystm import TinySTM

MODES = [dict(write_back=True), dict(write_back=False)]


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


def put(a, v):
    def body(tx):
        yield from tx.write(a, v)
    return body


def opaque_check(data):
    return lambda run, truncated: None if opaque(run.history, data) else "not opaque"


XY = {"x": 0, "y": 0}


def test_worked_example_snapshot_extension():
    data = bank(2, 10)
    for extend, aborts, ext in [(True, 0, 1), (False, 1, 0)]:
        stm = TinySTM(extend=extend)
        run = Run(lambda: (Memory(stm.memory(data)), [atomically(stm, 0, put("a1", 15)),
                                                      atomically(stm, 1, audit(2))]))
        run.steps(1, 4)  # the audit: ub = 0, then a0 = 10 at version 0
        assert run.finish(0)  # the writer locks a1 at its write, commits with wv = 1
        assert run.mem.w[("lock", "a1")] == (1, None) and run.mem.w["clock"] == 1
        assert run.finish(1)  # the audit finds version 1 > ub = 0 on a1
        assert count(run.history, "abort") == aborts and stm.extensions == ext
        assert run.out[1] == 25
        assert opaque(run.history, data)


def test_exhaustive_two_transactions():
    for mode in MODES:
        make = lambda: TinySTM(**mode)
        for bodies, data, tries in [([skew("x", "y"), skew("y", "x")], XY, 2), ([inc("x"), inc("x")], XY, 2),
                                    ([transfer(0, 1, 3), audit(2)], bank(2, 10), 2),
                                    ([transfer(0, 1, 3), transfer(1, 0, 4)], bank(2, 10), 1)]:
            st = explore(setup_of(make, bodies, data, tries), opaque_check(data))
            assert st.failure is None and st.runs > 1, (mode, st.failure)


def test_exhaustive_three_transactions():
    # A reader of x and y against two writers: the case in which snapshot extension matters.
    def both(tx):
        a = yield from tx.read("x")
        b = yield from tx.read("y")
        return a, b
    for mode in MODES:
        st = explore(setup_of(lambda: TinySTM(**mode), [both, put("y", 4), put("x", 5)], XY, tries=1),
                     opaque_check(XY))
        assert st.failure is None and st.runs > 1000


def test_increments_are_not_lost():
    def check(run, truncated):
        return None if run.mem.w["x"] == count(run.history, "commit") else "lost update"
    for mode in MODES:
        assert explore(setup_of(lambda: TinySTM(**mode), [inc("x"), inc("x")], XY, tries=3), check).failure is None


def test_bank_random_schedules():
    m, data = 3, bank(3, 10)
    for mode in MODES:
        aborts = 0
        for seed in range(100):
            def setup():
                stm = TinySTM(**mode)
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
            assert opaque(run.history, data), (mode, seed)
            aborts += count(run.history, "abort")
        assert aborts > 20


def test_linked_list_random_schedules():
    data = sorted_list([2, 5], spare=3)
    for mode in MODES:
        for seed in range(60):
            def setup():
                stm = TinySTM(**mode)
                ops = [[list_insert(3, 4), list_contains(5)], [list_remove(2), list_insert(4, 5)],
                       [list_remove(5), list_insert(1, 6)]]
                def proc(p):
                    out = []
                    for body in ops[p]:
                        out.append((yield from atomically(stm, p, body)))
                    return out
                return Memory(stm.memory(data)), [proc(p) for p in range(3)]
            run = random_run(setup, seed)
            keys = list_keys(run.mem.w)
            assert set(keys) == {1, 3, 4} and keys == sorted(keys)
            assert opaque(run.history, data), (mode, seed)


def dirty(tx):
    yield from tx.write("x", 99)
    raise Abort  # the transaction aborts itself after its write reached memory


def reader(tx):
    v = yield from tx.read("x")
    return v


def test_write_through_abort_must_release_with_a_new_version():
    for bug, out, aborts in [(True, 99, 1), (False, 0, 2)]:
        stm = TinySTM(write_back=False, restore_version_on_abort=bug)
        run = Run(lambda: (Memory(stm.memory(XY)), [atomically(stm, 0, reader, tries=2),
                                                    atomically(stm, 1, dirty, tries=1)]))
        run.steps(0, 2)  # the reader: ub = 0, first lock sample (0, free)
        run.steps(1, 5)  # the writer: ub, lock read, CAS, undo log entry, x = 99 in place
        run.steps(0, 1)  # the reader loads x = 99
        assert run.finish(1)  # the writer aborts: x = 0 again, and the lock is released
        assert run.mem.w["x"] == 0
        assert run.mem.w[("lock", "x")] == ((0, None) if bug else (1, None))
        assert run.finish(0)  # the second lock sample equals the first only in the buggy variant
        assert run.out[0] == out and count(run.history, "abort") == aborts
        assert opaque(run.history, XY) == (not bug)
    st = explore(setup_of(lambda: TinySTM(write_back=False, restore_version_on_abort=True), [reader, dirty], XY,
                          tries=1), opaque_check(XY))
    assert st.failure is not None
    st = explore(setup_of(lambda: TinySTM(write_back=False), [reader, dirty], XY, tries=1), opaque_check(XY))
    assert st.failure is None


def test_encounter_time_locking_finds_a_write_write_conflict_at_the_write():
    stm = TinySTM()
    run = Run(lambda: (Memory(stm.memory(XY)), [atomically(stm, 0, put("x", 1)),
                                                 atomically(stm, 1, put("x", 2), tries=1)]))
    run.steps(0, 3)  # T1: ub, lock read, CAS: T1 owns the lock of x
    assert run.finish(1)  # T2 finds the lock owned at its first write and aborts there
    t2 = [ev for ev in run.history if ev[0][0] == 1]
    assert [ev[1] for ev in t2] == ["begin", "abort"]
    assert run.finish(0) and run.mem.w["x"] == 1


def test_read_only_transactions_do_not_touch_the_clock():
    for mode in MODES:
        stm = TinySTM(**mode)
        run = Run(lambda: (Memory(stm.memory(bank(3, 10))), [atomically(stm, 0, audit(3))]))
        assert run.finish(0) and run.out[0] == 30
        assert all(op[0] == "read" for _, op, _ in run.trace)
