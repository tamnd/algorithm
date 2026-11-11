# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/norec/. The authors are listed in prov/4NBAVM.jsonl.

import random

from norec import NOrec
from stmsim import (Memory, Run, atomically, audit, bank, count, explore, list_contains, list_insert,
                    list_keys, list_remove, opaque, random_run, read_sums, serializable, sorted_list,
                    transfer)


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


def test_worked_example():
    data = bank(3, 10)
    # 1. A writer that touches a word outside the read log costs a validation, not an abort.
    stm = NOrec()
    run = Run(lambda: (Memory(stm.memory(data)), [atomically(stm, 0, put("a2", 15)), atomically(stm, 1, audit(2))]))
    run.steps(1, 3)  # the audit: snapshot = 0, a0 = 10, seqlock still 0
    assert run.finish(0)  # the writer: CAS 0 -> 1, a2 = 15, seqlock = 2
    assert run.mem.w["seqlock"] == 2
    assert run.finish(1)  # a1 = 10, seqlock 2 != 0, validate: a0 is still 10, snapshot = 2
    assert run.out[1] == 20 and count(run.history, "abort") == 0 and stm.validations == 1
    # 2. A writer that changes a logged value makes the validation fail.
    stm = NOrec()
    run = Run(lambda: (Memory(stm.memory(data)), [atomically(stm, 0, transfer(0, 1, 3)),
                                                  atomically(stm, 1, audit(2))]))
    run.steps(1, 3)
    assert run.finish(0)  # a0 = 7, a1 = 13
    assert run.finish(1)  # validation finds a0 = 7, not 10: abort, then retry and read 7 + 13
    assert run.out[1] == 20 and count(run.history, "abort") == 1
    assert opaque(run.history, data)


def test_exhaustive_two_transactions():
    for bodies, data, tries in [([skew("x", "y"), skew("y", "x")], XY, 2), ([inc("x"), inc("x")], XY, 2),
                                ([transfer(0, 1, 3), audit(2)], bank(2, 10), 2),
                                ([transfer(0, 1, 3), transfer(1, 0, 4)], bank(2, 10), 2)]:
        st = explore(setup_of(NOrec, bodies, data, tries), opaque_check(data))
        assert st.failure is None and st.runs > 1


def test_exhaustive_three_transactions():
    st = explore(setup_of(NOrec, [inc("x"), skew("x", "y"), skew("y", "x")], XY, tries=1), opaque_check(XY))
    assert st.failure is None and st.runs > 100


def test_increments_are_not_lost():
    def check(run, truncated):
        return None if run.mem.w["x"] == count(run.history, "commit") else "lost update"
    assert explore(setup_of(NOrec, [inc("x"), inc("x")], XY, tries=3), check).failure is None


def test_a_change_and_a_change_back_passes_value_validation():
    # x goes 0 -> 1 -> 0 while the reader runs. Value-based validation accepts it, and the
    # history is still opaque: the reader serializes after both writers.
    stm = NOrec()
    def reader(tx):
        a = yield from tx.read("x")
        b = yield from tx.read("y")
        return a, b
    procs = [atomically(stm, 0, reader), atomically(stm, 1, put("x", 1)), atomically(stm, 2, put("x", 0))]
    run = Run(lambda: (Memory(stm.memory(XY)), procs))
    run.steps(0, 3)  # x = 0
    assert run.finish(1) and run.finish(2)
    assert run.mem.w["seqlock"] == 4
    assert run.finish(0)
    assert run.out[0] == (0, 0) and count(run.history, "abort") == 0
    assert opaque(run.history, XY)


def test_commits_are_serialized():
    # In every state, at most one process is between its CAS and its release (its next
    # step is a write), and the sequence lock is odd exactly when one such process exists.
    def setup():
        stm = NOrec()
        return Memory(stm.memory(XY)), [atomically(stm, p, inc("xy"[p % 2])) for p in range(3)]

    for seed in range(100):
        rng = random.Random(seed)
        run = Run(setup)
        while run.enabled():
            in_writeback = [p for p, op in enumerate(run.pending) if op is not None and op[0] == "write"]
            assert len(in_writeback) <= 1
            assert (run.mem.w["seqlock"] % 2 == 1) == bool(in_writeback)
            run.step(rng.choice(run.enabled()))
        assert run.mem.w["x"] + run.mem.w["y"] == 3


def test_read_only_transactions_take_no_write_step():
    stm = NOrec()
    run = Run(lambda: (Memory(stm.memory(bank(3, 10))), [atomically(stm, 0, audit(3))]))
    assert run.finish(0) and run.out[0] == 30
    assert all(op[0] in ("read", "await") for _, op, _ in run.trace)


def test_bank_random_schedules():
    m, data = 3, bank(3, 10)
    aborts = 0
    for seed in range(150):
        def setup():
            stm = NOrec()
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
        assert opaque(run.history, data), seed
        aborts += count(run.history, "abort")
    assert aborts > 20


def test_linked_list_random_schedules():
    data = sorted_list([2, 5], spare=3)
    for seed in range(80):
        def setup():
            stm = NOrec()
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
        assert opaque(run.history, data), seed


def test_without_the_check_after_each_read_a_snapshot_is_inconsistent():
    data = bank(2, 10)
    make = lambda: NOrec(check_reads=False)
    st = explore(setup_of(make, [transfer(0, 1, 3), audit(2)], data),
                 lambda run, tr: None if serializable(run.history, data) else "not serializable")
    assert st.failure is not None
    run = Run(setup_of(make, [transfer(0, 1, 3), audit(2)], data))
    run.steps(1, 2)  # snapshot = 0, a0 = 10
    run.finish(0)  # a0 = 7, a1 = 13
    run.finish(1)  # a1 = 13 with no check; a read-only commit does not validate
    assert run.out[1] == 23 and not opaque(run.history, data)
