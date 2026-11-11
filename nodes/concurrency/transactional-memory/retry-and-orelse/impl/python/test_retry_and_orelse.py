# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/retry-and-orelse/. The authors are listed in prov/E1CEZX.jsonl.

import random

from retry_and_orelse import BlockingTL2, or_else, put, retry, take
from sched import explore, random_run
from stm import Memory

Q, Z = 0, 1
Q1, Q2, M = 0, 1, 2


def write_z(tx):
    yield from tx.write(Z, 1)


def consumer_producer(write_q: bool):
    def make():
        mem = Memory(2)
        stm = BlockingTL2(mem)

        def consumer():
            return (yield from stm.atomic(0, take(Q)))

        def producer():
            yield from stm.atomic(1, write_z)
            if write_q:
                yield from stm.atomic(1, put(Q, 1))

        return (mem, stm), [consumer(), producer()]

    return make


def wake_ups(log, pid):
    """Pairs (versions at a retry of pid, versions at the next begin of pid)."""
    out, pending = [], None
    for kind, tid, ver in log:
        if tid[0] != pid:
            continue
        if kind == "retry":
            pending = ver
        elif pending is not None:
            out.append((pending, ver))
            pending = None
    return out


def test_retry_wakes_only_after_a_write_to_the_read_set():
    runs = slept_through_z = 0
    for (mem, stm), sys in explore(consumer_producer(True), 120):
        runs += 1
        assert sys.finished() and sys.error == [None, None]
        assert sys.result[0] == Q and mem.val[Q] == 0 and mem.val[Z] == 1
        for before, after in wake_ups(stm.log, 0):
            assert after[Q] != before[Q]          # Q changed: the reason to wake
            if after[Z] != before[Z]:
                slept_through_z += 1               # Z changed too, but did not wake it
    assert runs > 10 and slept_through_z > 0


def test_unrelated_write_does_not_wake():
    for (mem, stm), sys in explore(consumer_producer(False), 120):
        assert sys.done == [False, True]           # the consumer stays blocked
        assert sys.runnable() == []
        begins = [e for e in stm.log if e[0] == "begin" and e[1][0] == 0]
        assert len(begins) == 1                    # it never ran again


def or_else_program(target: int, initial: dict):
    def make():
        mem = Memory(3, dict(initial))
        stm = BlockingTL2(mem)

        def first(tx):
            yield from tx.write(M, 7)              # must vanish when first retries
            return (yield from take(Q1)(tx))

        def body(tx):
            return (yield from or_else(tx, first, take(Q2)))

        def consumer():
            return (yield from stm.atomic(0, body))

        def producer():
            if target >= 0:
                yield from stm.atomic(1, put(target, 9))

        return (mem, stm), [consumer(), producer()]

    return make


def test_or_else_runs_second_branch_and_discards_first():
    for (mem, stm), sys in explore(or_else_program(Q2, {}), 120):
        assert sys.finished()
        assert sys.result[0] == Q2
        assert mem.val[M] == 0 and mem.val[Q1] == 0 and mem.val[Q2] == 0


def test_or_else_waits_on_the_union_of_read_sets():
    for target in (Q1, Q2):
        for (mem, stm), sys in explore(or_else_program(target, {}), 120):
            assert sys.finished()
            assert sys.result[0] == target
            expected_m = 7 if target == Q1 else 0
            assert mem.val[M] == expected_m


def test_or_else_prefers_first_branch():
    for (mem, stm), sys in explore(or_else_program(-1, {Q1: 1, Q2: 1}), 120):
        assert sys.finished()
        assert sys.result[0] == Q1 and mem.val[M] == 7 and mem.val[Q2] == 1


def test_retry_with_both_branches_empty_blocks_forever():
    for (mem, stm), sys in explore(or_else_program(-1, {}), 120):
        assert sys.done == [False, True] and sys.runnable() == []


def buffers(n_proc: int, items: int, cap: int, two: bool):
    def make():
        mem = Memory(2)
        stm = BlockingTL2(mem)

        def take_any(tx):
            return (yield from or_else(tx, take(0), take(1)))

        def put_any(tx):
            return (yield from or_else(tx, put(0, cap), put(1, cap)))

        def producer(pid):
            for _ in range(items):
                yield from stm.atomic(pid, put_any if two else put(0, cap))

        def consumer(pid):
            got = []
            for _ in range(items):
                got.append((yield from stm.atomic(pid, take_any if two else take(0))))
            return got

        procs = [producer(i) for i in range(n_proc)]
        procs += [consumer(n_proc + i) for i in range(n_proc)]
        return mem, procs

    return make


def test_random_bounded_buffers():
    rng = random.Random(2005)
    for i in range(600):
        n_proc = 1 + i % 2
        items = 1 + (i // 2) % 3
        cap = 1 + (i // 6) % 2
        two = i % 3 == 0
        mem, sys = random_run(buffers(n_proc, items, cap, two), rng, 20_000)
        # every put is matched by a take, so a lost wake-up would leave a
        # process blocked forever
        assert sys.finished(), (i, sys.done)
        assert all(e is None for e in sys.error)
        assert mem.val == [0, 0]
        assert sum(len(sys.result[n_proc + k]) for k in range(n_proc)) == n_proc * items


def test_retry_is_an_exception_outside_or_else():
    try:
        retry()
    except Exception as exc:
        assert type(exc).__name__ == "Retry"
    else:
        raise AssertionError("retry returned")
