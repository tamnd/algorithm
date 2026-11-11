# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dstm/. The authors are listed in prov/4KD1YP.jsonl.

from dstm import ABORTED, ACTIVE, COMMITTED, DSTM
from stmsim import (Memory, Run, atomically, audit, bank, count, explore, list_contains, list_insert, list_keys,
                    list_remove, opaque, random_run, read_sums, serializable, sorted_list, transfer)


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


def committed_value(words, o):
    """The current committed value of object o, read off the memory at once."""
    _, owner, old, new = words[("start", o)]
    if owner is None or words[("status",) + owner] == COMMITTED:
        return new[1]
    return old[1]


def check_opaque(data):
    def check(run, truncated):
        if truncated:
            return "too many steps"
        return None if opaque(run.history, data) else "not opaque"
    return check


XY = {"x": 0, "y": 0}


def test_worked_example_polite_reader_aborts_a_writer():
    stm = DSTM(nprocs=2, cm="polite", rounds=3, max_attempts=3)
    run = Run(lambda: (Memory(stm.memory(XY)), [atomically(stm, 0, put(("x", 1), ("y", 1))),
                                                 atomically(stm, 1, get("x", "y"))]))
    run.steps(0, 3)  # p: read start(x), CAS a new locator, validate (own status)
    assert run.mem.w[("start", "x")][1] == (0, 0)
    assert run.finish(1)  # q backs off 1 + 2 + 4 local steps, then aborts p and reads the old version
    assert run.out[1] == (0, 0) and stm.kills == 1
    assert run.mem.w[("status", 0, 0)] == ABORTED
    assert run.finish(0)  # p sees its abort at its next open and commits on the retry
    assert committed_value(run.mem.w, "x") == 1 and committed_value(run.mem.w, "y") == 1
    assert count(run.history, "abort") == 1 and opaque(run.history, XY)


def test_one_status_cas_commits_every_object():
    stm = DSTM(nprocs=1, max_attempts=1)
    run = Run(lambda: (Memory(stm.memory(XY)), [atomically(stm, 0, put(("x", 1), ("y", 1)))]))
    while run.pending[0][0] != "cas" or run.pending[0][1] != ("status", 0, 0):
        run.step(0)
    assert committed_value(run.mem.w, "x") == 0 and committed_value(run.mem.w, "y") == 0
    run.step(0)  # the CAS from ACTIVE to COMMITTED
    assert run.mem.w[("status", 0, 0)] == COMMITTED
    assert committed_value(run.mem.w, "x") == 1 and committed_value(run.mem.w, "y") == 1


def test_exhaustive_two_transactions():
    cases = [([skew("x", "y"), skew("y", "x")], XY), ([inc("x"), inc("x")], XY),
             ([put(("x", 1), ("y", 1)), put(("y", 2), ("x", 2))], XY), ([transfer(0, 1, 3), audit(2)], bank(2, 10))]
    # One attempt each: a second attempt makes the state space about a thousand times larger.
    for cm in ("aggressive", "polite"):
        for bodies, data in cases:
            make = lambda: DSTM(nprocs=2, cm=cm, rounds=1, max_attempts=1)
            st = explore(setup_of(make, bodies, data, tries=1), check_opaque(data))
            assert st.failure is None and st.runs > 100, (cm, st.failure)


def test_exhaustive_three_transactions():
    make = lambda: DSTM(nprocs=3, cm="aggressive", max_attempts=1)
    st = explore(setup_of(make, [get("x"), put(("x", 4)), put(("y", 5))], XY, tries=1), check_opaque(XY))
    assert st.failure is None and st.runs > 100


def test_increments_are_not_lost():
    def check(run, truncated):
        return None if committed_value(run.mem.w, "x") == count(run.history, "commit") else "lost update"
    for cm in ("aggressive", "polite"):
        st = explore(setup_of(lambda: DSTM(nprocs=2, cm=cm, rounds=1, max_attempts=1), [inc("x"), inc("x")], XY,
                              tries=1), check)
        assert st.failure is None


def test_validation_checks_grow_quadratically():
    # A transaction alone that reads r objects checks 1 + 2 + ... + r entries at its opens and r at commit.
    for r in range(1, 7):
        data = {f"o{i}": i for i in range(r)}
        stm = DSTM(nprocs=1, max_attempts=1)
        run = Run(lambda: (Memory(stm.memory(data)), [atomically(stm, 0, get(*data))]))
        assert run.finish(0)
        assert stm.checks == r * (r + 1) // 2 + r


def test_obstruction_freedom_a_solo_run_finishes():
    # p stops for ever after any number of steps of its transfer; q, running alone, still commits.
    data = bank(2, 10)
    p_steps = len(replay_alone(data))
    for k in range(p_steps):
        for cm in ("aggressive", "polite"):
            stm = DSTM(nprocs=2, cm=cm, max_attempts=2)
            run = Run(lambda: (Memory(stm.memory(data)), [atomically(stm, 0, transfer(0, 1, 3), tries=1),
                                                         atomically(stm, 1, transfer(1, 0, 5), tries=1)]))
            run.steps(0, k)
            assert run.finish(1, limit=200), (k, cm)
            assert count(run.history, "commit") >= 1 and opaque(run.history, data)


def replay_alone(data):
    stm = DSTM(nprocs=2, max_attempts=2)
    run = Run(lambda: (Memory(stm.memory(data)), [atomically(stm, 0, transfer(0, 1, 3), tries=1)]))
    run.finish(0)
    return run.trace


def test_aggressive_managers_can_livelock():
    # Two writers of x and y in opposite order, scheduled in lockstep: each aborts the other at its second open.
    stm = DSTM(nprocs=2, cm="aggressive", max_attempts=40)
    run = Run(lambda: (Memory(stm.memory(XY)), [atomically(stm, 0, put(("x", 1), ("y", 1)), tries=30),
                                                 atomically(stm, 1, put(("y", 2), ("x", 2)), tries=30)]))
    for _ in range(300):
        for p in (0, 1):
            if run.pending[p] is not None:
                run.step(p)
    assert count(run.history, "commit") == 0 and count(run.history, "abort") >= 20
    assert stm.kills >= 20


def test_early_release():
    def reader(release):
        def body(tx):
            x = yield from tx.read("x")
            if release:
                yield from tx.stm.release(tx, "x")
            y = yield from tx.read("y")
            return x, y
        return body
    for release, aborts in ((True, 0), (False, 1)):
        stm = DSTM(nprocs=2, max_attempts=2)
        run = Run(lambda: (Memory(stm.memory(XY)), [atomically(stm, 0, reader(release)),
                                                     atomically(stm, 1, put(("x", 7)))]))
        while not any(ev[0] == (0, 0) and ev[1] == "read" for ev in run.history):
            run.step(0)
        assert run.finish(1)  # the writer does not see the invisible reader and commits x = 7
        assert run.finish(0)
        assert count(run.history, "abort") == aborts
        assert run.out[0] == ((0, 0) if release else (7, 0))
        assert opaque(run.history, XY)  # here the reader is serialized before the writer


def test_bank_random_schedules():
    m, data = 3, bank(3, 10)
    for cm in ("aggressive", "polite"):
        for seed in range(80):
            def setup():
                stm = DSTM(nprocs=3, cm=cm, max_attempts=60)
                def proc(p):
                    for k in range(3):
                        yield from atomically(stm, p, transfer((p + k) % m, (p + k + 1) % m, k + 1))
                    return (yield from atomically(stm, p, audit(m)))
                return Memory(stm.memory(data)), [proc(p) for p in range(3)]
            run = random_run(setup, seed, max_steps=20000)
            assert all(r is None for r in run.pending), (cm, seed)
            assert sum(committed_value(run.mem.w, f"a{i}") for i in range(m)) == 30
            assert run.out == [30, 30, 30]
            assert all(s == 30 for s in read_sums(run.history, m))
            assert opaque(run.history, data), (cm, seed)


def test_linked_list_random_schedules():
    data = sorted_list([2, 5], spare=3)
    for seed in range(60):
        def setup():
            stm = DSTM(nprocs=3, cm="polite", max_attempts=60)
            ops = [[list_insert(3, 4), list_contains(5)], [list_remove(2), list_insert(4, 5)],
                   [list_remove(5), list_insert(1, 6)]]
            def proc(p):
                out = []
                for body in ops[p]:
                    out.append((yield from atomically(stm, p, body)))
                return out
            return Memory(stm.memory(data)), [proc(p) for p in range(3)]
        run = random_run(setup, seed, max_steps=20000)
        assert all(r is None for r in run.pending)
        words = {o: committed_value(run.mem.w, o) for o in data}
        keys = list_keys(words)
        assert set(keys) == {1, 3, 4} and keys == sorted(keys)
        assert opaque(run.history, data), seed


def test_version_only_validation_allows_write_skew():
    # T1 reads x and writes y; T2 reads y and writes x. Each opens its write while the other is active, so
    # each read version is still the last committed one when the other validates. Both commit.
    for strict, commits in ((False, 2), (True, 1)):
        stm = DSTM(nprocs=2, max_attempts=1, strict=strict)
        run = Run(lambda: (Memory(stm.memory(XY)), [atomically(stm, 0, skew("x", "y"), tries=1),
                                                     atomically(stm, 1, skew("y", "x"), tries=1)]))

        def until(p, pred):
            while run.pending[p] is not None and not pred():
                run.step(p)

        def did(tid, kind):
            return lambda: any(ev[0] == tid and ev[1] == kind for ev in run.history)

        def at_commit(p):
            return lambda: run.pending[p][0] == "cas" and run.pending[p][1][0] == "status"

        until(0, did((0, 0), "read"))
        until(1, did((1, 0), "read"))
        until(0, did((0, 0), "write"))
        until(1, did((1, 0), "write"))
        until(0, at_commit(0))
        until(1, at_commit(1))
        assert run.finish(0) and run.finish(1)
        assert count(run.history, "commit") == commits
        assert serializable(run.history, XY) == (not commits == 2)
        if strict:
            assert opaque(run.history, XY)


def test_without_validation_at_each_open_a_zombie_sees_x_ne_y():
    # Validation only at commit: the reader sees x = 0 and y = 1, which no serial run shows; it aborts at commit.
    stm = DSTM(nprocs=2, max_attempts=3, validate_reads=False)
    run = Run(lambda: (Memory(stm.memory(XY)), [atomically(stm, 0, get("x", "y")),
                                                 atomically(stm, 1, put(("x", 1), ("y", 1)))]))
    while not any(ev[0] == (0, 0) and ev[1] == "read" for ev in run.history):
        run.step(0)
    assert run.finish(1)
    assert run.finish(0) and run.out[0] == (1, 1)
    seen = [ev[3] for ev in run.history if ev[0] == (0, 0) and ev[1] == "read"]
    assert seen == [0, 1] and count(run.history, "abort") == 1
    assert serializable(run.history, XY) and not opaque(run.history, XY)
