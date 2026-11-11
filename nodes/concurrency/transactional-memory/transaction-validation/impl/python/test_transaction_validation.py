# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/transaction-validation/. The authors are listed in prov/HDPVHM.jsonl.

from stmsim import (Memory, Run, atomically, audit, bank, count, explore, list_contains, list_insert,
                    list_keys, list_remove, opaque, random_run, read_sums, sorted_list,
                    strictly_serializable, transfer)
from transaction_validation import MODES, ValidatingSTM

OPAQUE_MODES = ("incremental", "counter", "clock")


def setup_of(mode, bodies, data, tries=2, **kw):
    def setup():
        stm = ValidatingSTM(mode, **kw)
        procs = [atomically(stm, p, b, tries=tries) for p, b in enumerate(bodies)]
        return Memory(stm.memory(data)), procs
    return setup


def read_r_write_one(r):
    def body(tx):
        s = 0
        for i in range(r):
            s += yield from tx.read(f"a{i}")
        yield from tx.write(f"a{r}", s)
        return s
    return body


def solo(mode, body, data):
    stm = ValidatingSTM(mode)
    run = Run(lambda: (Memory(stm.memory(data)), [atomically(stm, 0, body, tries=1)]))
    assert run.finish(0)
    return stm, run


def test_incremental_validation_counts_r_r_plus_1_over_2():
    for r in range(1, 11):
        data = bank(r + 1, 1)
        got = {mode: solo(mode, read_r_write_one(r), data)[0].checks for mode in MODES}
        assert got["incremental"] == r * (r + 1) // 2
        assert got["clock"] == r and got["commit"] == r
        assert got["counter"] == r  # alone, the commit counter never moves before the commit


def test_shared_steps_of_a_solo_run():
    # incremental: 3r reads + r(r-1)/2 checks + commit (2 lock steps, r checks, 1 write, 1 release)
    # clock: 1 + 3r + 2 + 1 + r + 2
    for r in (1, 4, 8):
        data = bank(r + 1, 1)
        inc = len(solo("incremental", read_r_write_one(r), data)[1].trace)
        clk = len(solo("clock", read_r_write_one(r), data)[1].trace)
        assert inc == 3 * r + r * (r - 1) // 2 + 4 + r
        assert clk == 1 + 3 * r + 5 + r


def test_read_only_transactions_skip_the_commit_check_except_in_commit_mode():
    data = bank(5, 10)
    got = {mode: solo(mode, audit(5), data)[0].checks for mode in MODES}
    assert got == {"incremental": 10, "counter": 0, "clock": 0, "commit": 5}


def test_counter_heuristic_scans_only_after_a_commit():
    data = bank(4, 10)
    stm = ValidatingSTM("counter")
    run = Run(lambda: (Memory(stm.memory(data)), [atomically(stm, 0, audit(4)), atomically(stm, 1, transfer(2, 3, 1))]))
    run.steps(0, 1 + 4 + 4)  # begin and two reads, each followed by a counter read
    assert stm.checks == 0
    run.finish(1)  # the transfer commits and moves the counter
    run.finish(0)
    # the transfer's commit checks its 2 reads; then the audit's read of a2 sees the
    # counter at 1 and scans a0, a1, a2; its read of a3 sees no change and scans nothing
    assert run.out[0] == 40 and stm.scans == 2 and stm.checks == 2 + 3
    assert opaque(run.history, data)


def test_exhaustive_two_transactions_opaque_modes():
    data = bank(2, 10)
    for mode in OPAQUE_MODES:
        st = explore(setup_of(mode, [transfer(0, 1, 3), audit(2)], data),
                     lambda run, tr: None if opaque(run.history, data) else "not opaque")
        assert st.failure is None and st.runs > 50, mode


def test_exhaustive_three_transactions_opaque_modes():
    xy = {"x": 0, "y": 0}

    def put(a, v):
        def body(tx):
            yield from tx.write(a, v)
        return body

    def get2(tx):
        u = yield from tx.read("x")
        v = yield from tx.read("y")
        return u, v
    for mode in OPAQUE_MODES:
        st = explore(setup_of(mode, [put("x", 1), put("y", 2), get2], xy, tries=1),
                     lambda run, tr: None if opaque(run.history, xy) else "not opaque")
        assert st.failure is None and st.runs > 50, mode
    # The counter variant that scans only the earlier entries when the counter has moved:
    # the reader reads x = 0, the writer of x commits, the reader sees the counter move,
    # scans nothing, and then reads the new y = 2 with no further scan.
    st = explore(setup_of("counter", [put("x", 1), put("y", 2), get2], xy, tries=1, check_new=False),
                 lambda run, tr: None if opaque(run.history, xy) else "not opaque")
    assert st.failure is not None


def test_commit_only_validation_is_serializable_but_not_opaque():
    data = bank(2, 10)
    setup = setup_of("commit", [transfer(0, 1, 3), audit(2)], data)
    st = explore(setup, lambda run, tr: None if strictly_serializable(run.history, data) else "not serializable")
    assert st.failure is None
    st = explore(setup, lambda run, tr: None if opaque(run.history, data) else "not opaque")
    assert st.failure is not None
    run = Run(setup)
    run.steps(1, 3)  # the audit reads a0 = 10
    run.finish(0)  # the transfer commits a0 = 7, a1 = 13
    run.finish(1)  # the audit reads a1 = 13: it has seen a sum of 23, then aborts at commit
    assert read_sums(run.history, 2)[0] == 23 and count(run.history, "abort") == 1


def test_bank_random_schedules():
    data = bank(3, 10)
    bodies = [transfer(0, 1, 2), transfer(1, 2, 3), audit(3), transfer(2, 0, 1), audit(3)]
    for mode in MODES:
        zombies = 0
        for seed in range(60):
            run = random_run(setup_of(mode, bodies, data, tries=None), seed)
            assert all(op is None for op in run.pending)
            assert sum(run.mem.w[f"a{i}"] for i in range(3)) == 30
            assert run.out[2] == 30 and run.out[4] == 30
            zombies += sum(1 for s in read_sums(run.history, 3) if s != 30)
            if seed < 15:
                assert strictly_serializable(run.history, data)
                assert opaque(run.history, data) or mode == "commit"
        assert (zombies > 0) == (mode == "commit"), mode


def test_linked_list_random_schedules():
    data = sorted_list([2, 4, 6], spare=2)
    bodies = [list_insert(3, 5), list_remove(4), list_insert(5, 6), list_contains(6)]
    for mode in OPAQUE_MODES:
        for seed in range(30):
            run = random_run(setup_of(mode, bodies, data, tries=None), seed)
            assert all(op is None for op in run.pending)
            assert list_keys(run.mem.w) == [2, 3, 5, 6]
            assert run.out[3] is True
