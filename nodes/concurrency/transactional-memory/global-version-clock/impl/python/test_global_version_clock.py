# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/global-version-clock/. The authors are listed in prov/VVC9F1.jsonl.

from stmsim import (Memory, Run, atomically, audit, bank, count, explore, list_contains, list_insert,
                    list_keys, list_remove, opaque, random_run, sorted_list, strictly_serializable,
                    transfer)
from global_version_clock import CLOCKS, ClockSTM


def setup_of(clock, bodies, data, tries=2, **kw):
    def setup():
        stm = ClockSTM(clock, **kw)
        procs = [atomically(stm, p, b, tries=tries) for p, b in enumerate(bodies)]
        return Memory(stm.memory(data)), procs
    return setup


def copy_plus_one(src, dst):
    def body(tx):
        v = yield from tx.read(src)
        yield from tx.write(dst, v + 1)
        return v
    return body


def put(a, v):
    def body(tx):
        yield from tx.write(a, v)
    return body


def get2(tx):
    u = yield from tx.read("x")
    v = yield from tx.read("y")
    return u, v


def test_solo_commit_writes_the_clock_once_or_never():
    data = bank(2, 10)
    for clock in CLOCKS:
        stm = ClockSTM(clock, n6=1)
        run = Run(lambda: (Memory(stm.memory(data)), [atomically(stm, 0, transfer(0, 1, 3), tries=1)]))
        assert run.finish(0)
        # begin 1, reads 3 + 3, locks 2 + 2, clock 1 or 2, write-back 2, release 2
        expect = {"gv1": 16, "gv4": 17, "gv5": 16, "gv6": 17}[clock]
        assert len(run.trace) == expect, clock
        assert run.mem.w["G"] == (0 if clock == "gv5" else 1)
        assert run.mem.w[("lock", "a0")] == (1, None)


def test_every_clock_is_opaque_on_all_schedules():
    data = bank(2, 10)
    xy = {"x": 0, "y": 0}
    for clock in CLOCKS:
        st = explore(setup_of(clock, [transfer(0, 1, 3), audit(2)], data, n6=2),
                     lambda run, tr: None if opaque(run.history, data) else "not opaque")
        assert st.failure is None and st.runs > 50, clock
        st = explore(setup_of(clock, [copy_plus_one("x", "y"), copy_plus_one("y", "x")], xy, n6=2),
                     lambda run, tr: None if opaque(run.history, xy) else "not opaque")
        assert st.failure is None and st.runs > 50, clock
        st = explore(setup_of(clock, [put("x", 1), put("y", 2), get2], xy, tries=1, n6=2),
                     lambda run, tr: None if opaque(run.history, xy) else "not opaque")
        assert st.failure is None and st.runs > 50, clock


def test_skipping_validation_on_a_shared_or_computed_wv_breaks_serializability():
    xy = {"x": 0, "y": 0}
    bodies = [copy_plus_one("x", "y"), copy_plus_one("y", "x")]
    for clock in ("gv4", "gv5"):
        st = explore(setup_of(clock, bodies, xy, unsafe_skip=True),
                     lambda run, tr: None if strictly_serializable(run.history, xy) else "not serializable")
        assert st.failure is not None, clock
    # GV5, two transactions with rv = 0: both compute wv = G + 1 = 1 = rv + 1
    setup = setup_of("gv5", bodies, xy, unsafe_skip=True)
    run = Run(setup)
    run.steps(0, 4)  # begin, read x = 0
    run.steps(1, 4)  # begin, read y = 0
    run.finish(0)  # locks y, wv = 1, skips the check, writes y = 1
    run.finish(1)  # locks x, wv = 1, skips the check, writes x = 1
    assert run.mem.w["x"] == 1 and run.mem.w["y"] == 1 and count(run.history, "commit") == 2
    assert not strictly_serializable(run.history, xy)  # write skew: a serial order gives 1 and 2
    # The safe rule validates, finds x locked by version 1 > rv, and aborts the second one
    run = Run(setup_of("gv5", bodies, xy, tries=1))
    run.steps(0, 4)
    run.steps(1, 4)
    run.finish(0)
    run.finish(1)
    assert count(run.history, "abort") == 1 and strictly_serializable(run.history, xy)
    # GV4: the second committer loses the CAS and borrows wv = 1
    run = Run(setup_of("gv4", bodies, xy, unsafe_skip=True))
    run.steps(0, 4)
    run.steps(1, 4)
    run.steps(0, 2 + 1)  # locks y, reads G = 0
    run.steps(1, 2 + 1)  # locks x, reads G = 0
    run.finish(0)  # CAS 0 -> 1 wins, wv = 1 = rv + 1: a true skip
    run.finish(1)  # CAS fails, reads G = 1, wv = 1 = rv + 1: an unsafe skip
    assert run.mem.w["x"] == 1 and run.mem.w["y"] == 1
    assert not strictly_serializable(run.history, xy)


def contended(clock, seed, **kw):
    data = bank(3, 10)
    bodies = [transfer(0, 1, 2), transfer(1, 2, 3), audit(3), transfer(2, 0, 1), audit(3)]
    stm = ClockSTM(clock, **kw)
    run = random_run(lambda: (Memory(stm.memory(data)),
                              [atomically(stm, p, b) for p, b in enumerate(bodies)]), seed)
    return stm, run, data


def test_bank_random_schedules():
    totals = {}
    for clock in CLOCKS:
        writes = aborts = commits = 0
        for seed in range(80):
            stm, run, data = contended(clock, seed)
            assert all(op is None for op in run.pending)
            assert sum(run.mem.w[f"a{i}"] for i in range(3)) == 30
            assert run.out[2] == 30 and run.out[4] == 30
            if seed < 15:
                assert opaque(run.history, data)
            writes += stm.clock_writes
            aborts += count(run.history, "abort")
            commits += count(run.history, "commit")
        assert commits == 80 * 5
        totals[clock] = (writes, aborts)
    # measured: gv1 (255, 731), gv4 (249, 797), gv5 (0, 1112), gv6 (22, 1111)
    assert totals["gv1"][0] >= 80 * 3  # one clock write per update commit, and some for failed commits
    assert totals["gv5"][0] == 0  # no clock write at commit at all
    assert totals["gv6"][0] < totals["gv4"][0] <= totals["gv1"][0]
    assert totals["gv5"][1] > 1.3 * totals["gv1"][1]  # but more aborts


def test_linked_list_random_schedules():
    data = sorted_list([2, 4, 6], spare=2)
    bodies = [list_insert(3, 5), list_remove(4), list_insert(5, 6), list_contains(6)]
    for clock in CLOCKS:
        for seed in range(30):
            run = random_run(setup_of(clock, bodies, data, tries=None), seed)
            assert all(op is None for op in run.pending)
            assert list_keys(run.mem.w) == [2, 3, 5, 6]
            assert run.out[3] is True
