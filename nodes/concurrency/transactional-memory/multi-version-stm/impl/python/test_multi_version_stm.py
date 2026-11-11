# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multi-version-stm/. The authors are listed in prov/0DZJAM.jsonl.

from stmsim import (Memory, Run, atomically, audit, bank, count, explore, list_contains, list_insert,
                    list_keys, list_remove, opaque, random_run, sorted_list, transactions, transfer)
from multi_version_stm import MultiVersionSTM

KEEPS = (None, "active", 2, 1)


def setup_of(keep, bodies, data, tries=2, stms=None):
    def setup():
        stm = MultiVersionSTM(keep)
        if stms is not None:
            stms.append(stm)
        procs = [atomically(stm, p, b, tries=tries) for p, b in enumerate(bodies)]
        return Memory(stm.memory(data, nprocs=len(bodies))), procs
    return setup


def current(words, data):
    """The newest committed value of each data word."""
    return {a: words[a][0][1] for a in data}


def aborts_of(history, p):
    return sum(1 for (q, _), t in transactions(history).items() if q == p and t["status"] == "abort")


def put(a, v):
    def body(tx):
        yield from tx.write(a, v)
    return body


def get2(tx):
    u = yield from tx.read("x")
    v = yield from tx.read("y")
    return u, v


def put_xy(tx):
    yield from tx.write("x", 1)
    yield from tx.write("y", 2)


def test_read_only_transactions_never_abort_on_all_schedules():
    data = bank(2, 10)
    xy = {"x": 0, "y": 0}
    cases = {
        None: [([transfer(0, 1, 3), audit(2)], data, 1), ([put_xy, get2], xy, 1),
               ([put("x", 1), put("y", 2), get2], xy, 2)],
        "active": [([transfer(0, 1, 3), audit(2)], data, 1), ([put_xy, get2], xy, 1)],
    }
    for keep in cases:
        for bodies, init, reader in cases[keep]:
            def check(run, truncated, init=init, reader=reader):
                if truncated:
                    return "too long"
                if aborts_of(run.history, reader):
                    return "a read-only transaction aborted"
                if not opaque(run.history, init):
                    return "not opaque"
                return None
            st = explore(setup_of(keep, bodies, init, tries=1), check)
            assert st.failure is None and st.runs > 20, (keep, st.failure)


def test_bounded_versions_are_opaque_but_readers_can_abort():
    data = bank(2, 10)
    xy = {"x": 0, "y": 0}
    for keep in (2, 1):
        st = explore(setup_of(keep, [put("x", 1), put("y", 2), get2], xy, tries=1),
                     lambda run, tr: None if opaque(run.history, xy) else "not opaque")
        assert st.failure is None and st.runs > 500, keep
    st = explore(setup_of(1, [transfer(0, 1, 3), audit(2)], data, tries=1),
                 lambda run, tr: "a reader aborted" if aborts_of(run.history, 1) else None)
    assert st.failure is not None


def test_the_old_version_saves_the_reader():
    data = bank(2, 10)
    out = {}
    for keep in (None, 1):
        run = Run(setup_of(keep, [transfer(0, 1, 3), audit(2)], data, tries=1))
        run.steps(1, 2)  # the audit reads G = 0 and the box of a0: 10
        run.finish(0)  # the transfer commits version 1: a0 = 7, a1 = 13
        run.finish(1)  # the audit reads the box of a1
        out[keep] = (run.out[1], count(run.history, "abort"), run.mem.w["a1"])
        assert opaque(run.history, data)
    assert out[None] == (20, 0, ((1, 13), (0, 10)))  # version 0 of a1 is still there
    assert out[1] == (None, 1, ((1, 13),))  # single version: the snapshot is gone


def test_steps_of_a_read_only_transaction():
    for r in (1, 4, 8):
        data = bank(r, 1)
        for keep, extra in ((None, 0), (1, 0), ("active", 2 + 1)):
            stm = MultiVersionSTM(keep)
            run = Run(lambda: (Memory(stm.memory(data, nprocs=1)), [atomically(stm, 0, audit(r))]))
            assert run.finish(0) and run.out[0] == r
            assert len(run.trace) == 1 + r + extra  # clock, one read per box, (announce, check, retire)


def contended(keep, seed, stms):
    data = bank(3, 10)
    bodies = [transfer(0, 1, 2), transfer(1, 2, 3), audit(3), transfer(2, 0, 1), audit(3)]
    return random_run(setup_of(keep, bodies, data, tries=None, stms=stms), seed), data


def test_bank_random_schedules_and_space():
    got = {}
    for keep in KEEPS:
        ro_aborts = space = box = 0
        for seed in range(80):
            stms = []
            run, data = contended(keep, seed, stms)
            stm = stms[0]
            assert all(op is None for op in run.pending)
            now = current(run.mem.w, data)
            assert sum(now.values()) == 30
            assert run.out[2] == 30 and run.out[4] == 30
            if seed < 15:
                assert opaque(run.history, data)
            ro_aborts += aborts_of(run.history, 2) + aborts_of(run.history, 4)
            space = max(space, stm.max_space)
            box = max(box, stm.max_box)
            if keep is None:  # every committed write stays: 3 initial versions + 3 transfers of 2 words
                assert stm.max_space == 3 + 3 * 2
        got[keep] = (ro_aborts, space, box)
    # measured: None (0, 9, 3), "active" (0, 7, 3), 2 (0, 6, 2), 1 (19, 3, 1)
    assert got[None][0] == 0 and got["active"][0] == 0
    assert got[2][0] <= got[1][0] and got[1][0] > 0
    assert got["active"][1] <= got[None][1]
    assert got[1][1:] == (3, 1) and got[2][2] == 2


def test_a_long_reader_holds_versions_until_it_ends():
    # The audit announces rv = 0 and reads a0. Five transfers commit, one after the other.
    # The audit then reads version 0 of a1, and ends. A sixth transfer commits.
    data = bank(2, 10)
    bodies = [audit(2)] + [transfer(0, 1, 1)] * 6
    got = {}
    for keep in (None, "active", 1):
        stms = []
        run = Run(setup_of(keep, bodies, data, tries=1, stms=stms))
        run.steps(0, 2 if keep != "active" else 4)
        for p in range(1, 6):
            assert run.finish(p)
        middle = len(run.mem.w["a1"])
        run.finish(0)
        run.finish(6)
        got[keep] = (run.out[0], middle, len(run.mem.w["a1"]), stms[0].max_space)
        assert opaque(run.history, data)
    assert got[None] == (20, 6, 7, 14)  # every version stays
    assert got["active"] == (20, 6, 2, 12)  # versions 0 to 5 kept for the reader, then trimmed
    assert got[1] == (None, 1, 1, 2)  # the reader lost version 0 and aborted


def test_linked_list_random_schedules():
    data = sorted_list([2, 4, 6], spare=2)
    bodies = [list_insert(3, 5), list_remove(4), list_insert(5, 6), list_contains(6)]
    for keep in KEEPS:
        for seed in range(30):
            run = random_run(setup_of(keep, bodies, data, tries=None), seed)
            assert all(op is None for op in run.pending)
            assert list_keys(current(run.mem.w, data)) == [2, 3, 5, 6]
            assert run.out[3] is True
            if keep in (None, "active"):
                assert aborts_of(run.history, 3) == 0
