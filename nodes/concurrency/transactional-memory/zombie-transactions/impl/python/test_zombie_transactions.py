# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zombie-transactions/. The authors are listed in prov/M45GVF.jsonl.

import pytest

from stmsim import (Memory, Run, atomically, bank, count, explore, opaque, random_run, read_sums,
                    strictly_serializable, transfer)
from zombie_transactions import MODES, ZombieSTM

XY = {"x": 0, "y": 0}  # invariant: x == y
XY1 = {"x": 0, "y": 1}  # invariant: y == x + 1


def setup_of(mode, bodies, data, tries=2, stms=None, **kw):
    def setup():
        stm = ZombieSTM(mode, **kw)
        if stms is not None:
            stms.append(stm)
        procs = [atomically(stm, p, b, tries=tries) for p, b in enumerate(bodies)]
        return Memory(stm.memory(data)), procs
    return setup


def bump_both(tx):
    u = yield from tx.read("x")
    v = yield from tx.read("y")
    yield from tx.write("x", u + 1)
    yield from tx.write("y", v + 1)


def spin_until_equal(tx):
    """Correct on every consistent state: x == y, so the loop never runs."""
    u = yield from tx.read("x")
    v = yield from tx.read("y")
    while u != v:
        yield from tx.stm.tick(tx)
    return u


def divide(tx):
    """Correct on every consistent state: y - x == 1, so it returns 10."""
    v = yield from tx.read("y")
    u = yield from tx.read("x")
    q = yield from tx.stm.guard(tx, lambda: 10 // (v - u))
    return q


def get2(tx):
    u = yield from tx.read("x")
    v = yield from tx.read("y")
    return u, v


def zombie_schedule(mode, body, data, **kw):
    """The reader begins and does its first read; the writer commits; the reader goes on."""
    stms = []
    run = Run(setup_of(mode, [bump_both, body], data, stms=stms, **kw))
    run.steps(1, 1 + 3)
    assert run.finish(0)
    return run, stms[0]


def test_a_zombie_loops_forever_without_opacity():
    run, stm = zombie_schedule("commit", spin_until_equal, XY)
    assert not run.finish(1, limit=500)  # still running after 500 steps
    assert run.pending[1] == ("local",) and stm.ticks > 490
    assert count(run.history, "commit") == 1  # only the writer
    assert strictly_serializable(run.history, XY)  # the committed part is fine
    assert not opaque(run.history, XY)  # but the reader saw x = 0 and y = 1


def test_a_zombie_divides_by_zero_without_opacity():
    run, stm = zombie_schedule("commit", divide, XY1)
    with pytest.raises(ZeroDivisionError):
        run.finish(1)  # the reader saw y = 1 (old) and x = 1 (new)
    assert stm.faults_raised == 1


def test_opacity_aborts_the_reader_at_the_read():
    for body, data, want in ((spin_until_equal, XY, 1), (divide, XY1, 10)):
        run, stm = zombie_schedule("opaque", body, data)
        assert run.finish(1)
        assert run.out[1] == want and count(run.history, "abort") == 1
        assert stm.ticks == 0 and stm.faults_raised == 0
        assert opaque(run.history, data)


def test_sandboxing_turns_the_zombie_into_an_abort():
    for period in (1, 4, 16):
        run, stm = zombie_schedule("sandbox", spin_until_equal, XY, period=period)
        assert run.finish(1) and run.out[1] == 1
        assert stm.ticks == period  # the zombie runs exactly one period before the check
        assert count(run.history, "abort") == 1
        assert strictly_serializable(run.history, XY) and not opaque(run.history, XY)
    run, stm = zombie_schedule("sandbox", divide, XY1)
    assert run.finish(1) and run.out[1] == 10
    assert stm.faults_hidden == 1 and stm.faults_raised == 0


def test_sandboxing_raises_a_real_fault():
    stms = []
    run = Run(setup_of("sandbox", [divide], {"x": 0, "y": 0}, stms=stms))
    with pytest.raises(ZeroDivisionError):
        run.finish(0)  # the state is consistent, so the fault is the program's own
    assert stms[0].faults_hidden == 0 and stms[0].faults_raised == 1


def test_all_schedules():
    # commit-only validation: the committed transactions are serializable, but some reader is a zombie
    setup = setup_of("commit", [bump_both, get2], XY)
    st = explore(setup, lambda run, tr: None if strictly_serializable(run.history, XY) else "not serializable")
    assert st.failure is None and st.runs > 20
    st = explore(setup, lambda run, tr: None if opaque(run.history, XY) else "not opaque")
    assert st.failure is not None
    # with the loop, some schedule has a zombie that spins on and on
    stms = []
    st = explore(setup_of("commit", [bump_both, spin_until_equal], XY, stms=stms),
                 lambda run, tr: "spins" if stms[-1].max_ticks > 50 else None, max_steps=80)
    assert st.failure is not None
    # opacity: no zombie at all; sandboxing: zombies, but each one is stopped within one
    # period, no fault escapes, and every run commits serializably. The reader has two
    # attempts; it may use both up against a writer that holds its locks.
    for mode, want_opaque in (("opaque", True), ("sandbox", False)):
        for body, data, want in ((spin_until_equal, XY, (0, 1)), (divide, XY1, (10,))):
            stms = []

            def check(run, tr, data=data, want=want, want_opaque=want_opaque, stms=stms):
                stm = stms[-1]
                if stm.max_ticks > (0 if want_opaque else stm.period) or stm.faults_raised:
                    return "a zombie ran on"
                if tr:
                    return "too long"
                if run.out[1] not in want + (None,) or not strictly_serializable(run.history, data):
                    return "wrong result"
                if want_opaque and not opaque(run.history, data):
                    return "not opaque"
                return None
            st = explore(setup_of(mode, [bump_both, body], data, tries=2, stms=stms), check, max_steps=80)
            assert st.failure is None and st.runs > 20, (mode, st.failure)


def audit_or_spin(m):
    def body(tx):
        s = 0
        for i in range(m):
            s += yield from tx.read(f"a{i}")
        while s != 10 * m:
            yield from tx.stm.tick(tx)
        return s
    return body


def test_bank_random_schedules():
    data = bank(3, 10)
    bodies = [transfer(0, 1, 2), transfer(1, 2, 3), audit_or_spin(3), transfer(2, 0, 1), audit_or_spin(3)]
    got = {}
    for mode in MODES:
        zombies = hung = 0
        for seed in range(60):
            run = random_run(setup_of(mode, bodies, data, tries=None), seed, max_steps=1500)
            stuck = [p for p, op in enumerate(run.pending) if op is not None]
            zombies += sum(1 for s in read_sums(run.history, 3) if s != 30)
            if stuck:
                hung += 1
                assert mode == "commit" and set(stuck) <= {2, 4}
                continue
            assert sum(run.mem.w[f"a{i}"] for i in range(3)) == 30
            assert run.out[2] == 30 and run.out[4] == 30
            if seed < 15:
                assert strictly_serializable(run.history, data)
                assert opaque(run.history, data) or mode != "opaque"
        got[mode] = (zombies, hung)
    # measured (zombie reads, runs that never end): commit (4, 4), opaque (0, 0), sandbox (4, 0)
    assert got["opaque"] == (0, 0)
    assert got["commit"][1] > 0 and got["sandbox"][0] > 0 and got["sandbox"][1] == 0
