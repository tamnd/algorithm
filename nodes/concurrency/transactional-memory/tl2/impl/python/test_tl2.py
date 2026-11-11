# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tl2/. The authors are listed in prov/V7T1AZ.jsonl.

from stmsim import (Memory, Run, atomically, audit, bank, count, explore, list_contains, list_insert,
                    list_keys, list_remove, opaque, random_run, read_sums, serializable, sorted_list,
                    strictly_serializable, transfer)
from tl2 import TL2


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


def opaque_check(data):
    return lambda run, truncated: None if opaque(run.history, data) else "not opaque"


XY = {"x": 0, "y": 0}


def test_worked_example():
    data = bank(2, 10)
    stm = TL2()
    procs = [atomically(stm, 0, transfer(0, 1, 3)), atomically(stm, 1, audit(2))]
    run = Run(lambda: (Memory(stm.memory(data)), procs))
    run.steps(1, 4)  # T2: rv = 0, then a0 = 10 with its two lock samples
    assert run.finish(0)  # T1 commits alone: wv = 1 = rv + 1, so no validation
    assert stm.skipped == 1 and run.mem.w["gv"] == 1
    assert run.mem.w[("lock", "a0")] == (1, None) and run.mem.w["a0"] == 7
    assert run.finish(1)  # T2 sees version 1 > rv = 0 on a1, aborts, retries with rv = 1
    assert run.out[1] == 20
    assert count(run.history, "abort") == 1
    assert [ev for ev in run.history if ev[0] == (1, 0)] == [((1, 0), "begin"), ((1, 0), "read", "a0", 10),
                                                         ((1, 0), "abort")]
    assert opaque(run.history, data)


def test_exhaustive_two_transactions():
    for bodies, data in [([skew("x", "y"), skew("y", "x")], XY), ([inc("x"), inc("x")], XY),
                         ([transfer(0, 1, 3), audit(2)], bank(2, 10))]:
        st = explore(setup_of(TL2, bodies, data), opaque_check(data))
        assert st.failure is None and st.runs > 1
    data = bank(2, 10)
    st = explore(setup_of(TL2, [transfer(0, 1, 3), transfer(1, 0, 4)], data, tries=1), opaque_check(data))
    assert st.failure is None


def test_exhaustive_three_transactions():
    data = {"x": 0, "y": 0}
    st = explore(setup_of(TL2, [inc("x"), skew("x", "y"), skew("y", "x")], data, tries=1), opaque_check(data))
    assert st.failure is None and st.runs > 1000


def test_increments_are_not_lost():
    def check(run, truncated):
        commits = count(run.history, "commit")
        return None if run.mem.w["x"] == commits else "lost update"
    assert explore(setup_of(TL2, [inc("x"), inc("x")], XY, tries=3), check).failure is None


def test_bank_random_schedules():
    m, data = 3, bank(3, 10)
    aborts = 0
    for seed in range(150):
        def setup():
            stm = TL2()
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
    assert aborts > 50


def test_linked_list_random_schedules():
    data = sorted_list([2, 5], spare=3)
    for seed in range(80):
        def setup():
            stm = TL2()
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
        assert keys == sorted(set(keys))
        assert set(keys) == {1, 3, 4}
        assert opaque(run.history, data), seed


def test_without_post_validation_a_read_only_transaction_commits_an_inconsistent_snapshot():
    data = bank(2, 10)
    st = explore(setup_of(lambda: TL2(post_validate=False), [transfer(0, 1, 3), audit(2)], data),
                 lambda run, tr: None if serializable(run.history, data) else "not serializable")
    assert st.failure is not None
    run = Run(setup_of(lambda: TL2(post_validate=False), [transfer(0, 1, 3), audit(2)], data))
    run.steps(1, 2)  # the audit reads a0 = 10
    run.finish(0)  # the transfer commits a0 = 7, a1 = 13
    run.finish(1)
    assert run.out[1] == 23 and count(run.history, "abort") == 0
    assert not opaque(run.history, data)


def test_without_write_locks_an_update_is_lost():
    st = explore(setup_of(lambda: TL2(write_locks=False), [inc("x"), inc("x")], XY),
                 lambda run, tr: None if strictly_serializable(run.history, XY) else "lost update")
    assert st.failure is not None
    run = Run(setup_of(lambda: TL2(write_locks=False), [inc("x"), inc("x")], XY))
    run.steps(0, 5)  # T1: rv, read x = 0 with two samples, faa gives wv = 1
    run.steps(1, 5)  # T2: rv = 0, read x = 0, wv = 2
    run.finish(1)  # T2 validates (x still has version 0) and writes x = 1
    run.finish(0)  # T1 has wv = rv + 1, skips validation and writes x = 1 again
    assert count(run.history, "commit") == 2 and run.mem.w["x"] == 1


def test_lock_striping_gives_a_false_conflict():
    data = XY

    def reader(tx):
        v = yield from tx.read("x")
        return v

    def writer(tx):
        yield from tx.write("y", 1)

    for stripe, aborts in [(None, 0), (lambda a: 0, 1)]:
        run = Run(setup_of(lambda: TL2(stripe=stripe), [reader, writer], data))
        run.steps(0, 1)  # the reader takes rv = 0
        run.finish(1)  # the writer commits y = 1; it releases its lock with version 1
        run.finish(0)  # the reader reads x; with one stripe it sees version 1 > rv
        assert count(run.history, "abort") == aborts
        assert opaque(run.history, data)


def test_validation_is_skipped_only_when_wv_is_rv_plus_one():
    stm = TL2()
    run = Run(lambda: (Memory(stm.memory(XY)), [atomically(stm, 0, inc("x")), atomically(stm, 1, inc("y"))]))
    run.steps(0, 4)  # T1: rv = 0 and read x
    run.finish(1)  # T2 commits with wv = 1 = rv + 1
    run.finish(0)  # T1 gets wv = 2 and must validate; x is still at version 0, so T1 commits
    assert (stm.skipped, stm.validated) == (1, 1)
    assert count(run.history, "commit") == 2 and run.mem.w["gv"] == 2


def test_a_crashed_committer_blocks_others():
    data = XY
    for k in range(1, 12):
        run = random_run(setup_of(TL2, [inc("x"), inc("x")], data, tries=3), seed=k, crash={0: k})
        assert opaque(run.history, data)
    run = Run(setup_of(TL2, [inc("x"), inc("x")], data, tries=3))
    run.steps(0, 6)  # T1 has locked x and stops forever
    assert run.mem.w[("lock", "x")][1] == (0, 0)
    run.finish(1)
    assert count(run.history, "commit") == 0 and count(run.history, "abort") == 3
