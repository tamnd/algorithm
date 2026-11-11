# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/herlihy-moss-htm/. The authors are listed in prov/JTKCNV.jsonl.

import random

from herlihy_moss_htm import Machine, serial_replay_ok
from sched import explore, random_run, replay


def increment(m, p, tries):
    """The counter of Figure 1 of the paper, without the backoff."""
    for k in range(tries):
        v = m.ltx(p, "c")
        yield
        m.st(p, "c", v + 1)
        yield
        ok = m.commit(p)
        yield
        if ok:
            return k + 1
    return None


def transfer(m, p, src, dst, tries):
    """Move one unit from src to dst; validate before the stores."""
    for _ in range(tries):
        a = m.ltx(p, src)
        yield
        b = m.ltx(p, dst)
        yield
        ok = m.validate(p)
        yield
        if not ok:
            continue
        m.st(p, src, a - 1)
        yield
        m.st(p, dst, b + 1)
        yield
        if m.commit(p):
            yield
            return True
        yield
    return False


def audit(m, p, accounts, tries, seen):
    """Read-only: sum the accounts; record the sum only after VALIDATE."""
    for _ in range(tries):
        total = 0
        for acc in accounts:
            total += m.lt(p, acc)
            yield
        if m.validate(p):
            seen.append(total)
            m.commit(p)
            yield
            return True
        yield
    return False


def test_counter_all_interleavings():
    def make():
        m = Machine(2, {"c": 0}, capacity=2)
        return m, [increment(m, 0, 2), increment(m, 1, 2)]

    count = 0
    for m, sys in explore(make):
        count += 1
        assert sys.finished()
        commits = sum(1 for r in sys.result if r is not None)
        assert m.mem["c"] == commits
        assert serial_replay_ok({"c": 0}, m.history, m.mem)
        # requester-loses: two attempts cannot both fail in the same round
        assert commits >= 1
    assert count > 100


def test_transfer_and_audit_all_interleavings():
    init = {"x": 5, "y": 5}

    def make():
        seen = []
        m = Machine(2, init, capacity=2)
        return (m, seen), [transfer(m, 0, "x", "y", 2), audit(m, 1, ["x", "y"], 2, seen)]

    count = 0
    for (m, seen), sys in explore(make):
        count += 1
        assert sys.finished() and sys.error == [None, None]
        assert all(s == 10 for s in seen)        # values before a true VALIDATE are consistent
        assert m.mem["x"] + m.mem["y"] == 10
        assert serial_replay_ok(init, m.history, m.mem)
    assert count > 50


def test_busy_aborts_the_requester_not_the_holder():
    m = Machine(2, {"x": 1}, capacity=4)
    assert m.ltx(0, "x") == 1
    m.lt(1, "x")                 # T_READ meets an exclusive holder: BUSY
    assert m.abort_cause[1] == "busy" and m.tstatus[1] is False
    assert m.tstatus[0] is True
    m.st(0, "x", 2)
    assert m.commit(0) is True and m.mem["x"] == 2
    assert m.validate(1) is False  # ends the aborted transaction
    assert m.lt(1, "x") == 2 and m.commit(1) is True


def test_shared_readers_do_not_conflict():
    m = Machine(2, {"x": 1}, capacity=4)
    assert m.lt(0, "x") == 1 and m.lt(1, "x") == 1
    assert m.commit(0) and m.commit(1)


def test_overflow_aborts_even_when_alone():
    m = Machine(1, {i: 0 for i in range(5)}, capacity=4)
    for i in range(5):
        m.st(0, i, 7)
    assert m.abort_cause[0] == "overflow"
    assert m.commit(0) is False
    assert all(v == 0 for v in m.mem.values())
    m2 = Machine(1, {i: 0 for i in range(4)}, capacity=4)
    for i in range(4):
        m2.st(0, i, 7)
    assert m2.commit(0) is True and all(v == 7 for v in m2.mem.values())


def test_abort_discards_and_store_aborts_holders():
    m = Machine(2, {"x": 1, "y": 2}, capacity=4)
    m.st(0, "x", 9)
    m.abort(0)
    assert m.mem["x"] == 1 and m.tactive[0] is False
    m.lt(0, "y")
    m.store(1, "y", 3)           # footnote 1: a STORE aborts the holder
    assert m.abort_cause[0] == "store"
    assert m.commit(0) is False and m.mem["y"] == 3


def test_orphan_needs_validate():
    # The invariant is y = x + 1. An orphan reads arbitrary values (here 0).
    def reader(m, p, check):
        x = m.lt(p, "x")
        yield
        y = m.lt(p, "y")
        yield
        if check and not m.validate(p):
            return None
        return 100 // (y - x)    # safe only if the invariant holds

    def writer(m, p):
        m.ltx(p, "x")
        yield
        m.st(p, "x", 7)
        yield
        m.st(p, "y", 8)
        yield
        m.commit(p)
        yield

    for check in (False, True):
        def make():
            m = Machine(2, {"x": 1, "y": 2}, capacity=4)
            return m, [writer(m, 0), reader(m, 1, check)]

        m, sys = replay(make, [0, 1, 1, 1])  # the reader gets BUSY on x
        assert m.abort_cause[1] == "busy"
        if check:
            assert sys.error[1] is None and sys.result[1] is None
        else:
            assert isinstance(sys.error[1], ZeroDivisionError)


def test_requester_loses_can_livelock():
    # T0 takes x then y, T1 takes y then x; each loses the second request.
    def make():
        m = Machine(2, {"x": 0, "y": 0}, capacity=4)
        return m, [transfer(m, 0, "x", "y", 10), transfer(m, 1, "y", "x", 10)]

    # one round: 0 gets x, 1 gets y, 0 gets BUSY, 0 validates and restarts
    # and gets x again, 1 gets BUSY, 1 validates and restarts and gets y
    head = [0, 1]
    rnd = [0, 0, 0, 1, 1, 1]
    m, sys = replay(make, head + rnd * 4)
    assert m.history == []                      # no commit at all
    assert m.tcache[0] == {"x": ["X", 0]} and m.tcache[1] == {"y": ["X", 0]}
    assert sys.trace.count(0) == sys.trace.count(1)   # both take steps


def test_random_runs_are_serializable():
    rng = random.Random(1993)
    accounts = ["a", "b", "c", "d"]
    init = {a: 10 for a in accounts}
    for _ in range(600):
        seed = rng.random()

        def make():
            r = random.Random(seed)
            seen = []
            m = Machine(3, init, capacity=r.choice([3, 4]))
            procs = []
            for p in range(3):
                if r.random() < 0.3:
                    procs.append(audit(m, p, accounts, 3, seen))
                else:
                    s, d = r.sample(accounts, 2)
                    procs.append(transfer(m, p, s, d, 3))
            return (m, seen), procs

        (m, seen), sys = random_run(make, rng)
        assert sys.finished() and all(e is None for e in sys.error)
        assert all(s == 40 for s in seen)
        assert sum(m.mem.values()) == 40
        assert serial_replay_ok(init, m.history, m.mem)
        if m.capacity == 3:
            assert seen == []                        # four reads overflow a cache of 3
