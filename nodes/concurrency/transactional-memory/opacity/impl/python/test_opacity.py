# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/opacity/. The authors are listed in prov/7CW7RJ.jsonl.

import random

from opacity import (final_state_opaque, final_state_opaque_naive, opaque, serializable,
                     strictly_serializable, transactions)
from sched import explore, random_run
from stm import TL2, EagerSTM, History, Memory, NOrec

X, Y = 0, 1
T1, T2, T3 = ("T1",), ("T2",), ("T3",)


def doomed_history():
    # T1 reads x = 0, T2 writes x = y = 1 and commits, T1 reads y = 1 and aborts
    return [("B", T1, -1, None), ("R", T1, X, 0),
            ("B", T2, -1, None), ("W", T2, X, 1), ("W", T2, Y, 1), ("C", T2, -1, None),
            ("R", T1, Y, 1), ("A", T1, -1, None)]


def test_doomed_read_is_rejected():
    h = doomed_history()
    assert strictly_serializable(h)
    assert serializable(h)
    assert not final_state_opaque(h)
    assert not opaque(h)
    # without the second read of T1 the history is opaque
    h2 = h[:6] + [h[7]]
    assert opaque(h2)


def test_opaque_histories_are_accepted():
    seq = [("B", T1, -1, None), ("W", T1, X, 1), ("C", T1, -1, None),
           ("B", T2, -1, None), ("R", T2, X, 1), ("C", T2, -1, None)]
    assert opaque(seq)
    # T1 reads the old snapshot in full while T2 commits: T1 goes first
    snap = [("B", T1, -1, None), ("R", T1, X, 0), ("B", T2, -1, None), ("W", T2, X, 1),
            ("W", T2, Y, 1), ("C", T2, -1, None), ("R", T1, Y, 0), ("C", T1, -1, None)]
    assert opaque(snap)
    # but if T1 begins after T2 commits, real-time order forbids the old values
    late = [("B", T2, -1, None), ("W", T2, X, 1), ("C", T2, -1, None),
            ("B", T1, -1, None), ("R", T1, X, 0), ("A", T1, -1, None)]
    assert not opaque(late)
    assert strictly_serializable(late)


def test_reading_from_aborted_transaction_is_rejected():
    h = [("B", T1, -1, None), ("W", T1, X, 5), ("A", T1, -1, None),
         ("B", T2, -1, None), ("R", T2, X, 5), ("A", T2, -1, None)]
    assert not opaque(h)
    assert serializable(h)


def test_final_state_opacity_is_not_prefix_closed():
    # T1 reads the write of T2 before T2 commits; T2 commits later
    h = [("B", T2, -1, None), ("W", T2, X, 1), ("B", T1, -1, None), ("R", T1, X, 1),
         ("C", T2, -1, None), ("C", T1, -1, None)]
    assert final_state_opaque(h)
    assert not final_state_opaque(h[:4])
    assert not opaque(h)


def zombie_workload(cls, **kw):
    def make():
        mem = Memory(2)
        hist = History()
        stm = cls(mem, hist, **kw)

        def reader(tx):
            a = yield from tx.read(X)
            b = yield from tx.read(Y)
            return 10 // (1 + a - b)   # divides by zero when a = 0 and b = 1

        def writer(tx):
            yield from tx.write(X, 1)
            yield from tx.write(Y, 1)

        return hist, [stm.atomic(0, reader), stm.atomic(1, writer)]

    return make


def test_opaque_stms_never_show_the_zombie():
    for cls in (TL2, NOrec, EagerSTM):
        runs = 0
        for hist, sys in explore(zombie_workload(cls), max_steps=60):
            assert sys.finished()
            assert sys.error == [None, None]
            assert sys.result[0] == 10
            assert opaque(hist.events)
            runs += 1
        assert runs > 10


def test_non_validating_stm_has_a_zombie():
    crashes = 0
    for hist, sys in explore(zombie_workload(TL2, validate_reads=False), max_steps=60):
        assert sys.finished()
        if sys.error[0] is not None:
            assert isinstance(sys.error[0], ZeroDivisionError)
            assert not opaque(hist.events)
            assert strictly_serializable(hist.events)
            crashes += 1
    assert crashes > 0


def random_workload(rng, cls, **kw):
    progs = []
    for _ in range(3):
        progs.append([(rng.choice("RW"), rng.randrange(2), rng.randrange(1, 4))
                      for _ in range(rng.randint(1, 3))])

    def make():
        mem = Memory(2)
        hist = History()
        stm = cls(mem, hist, **kw)

        def body_of(ops):
            def body(tx):
                for kind, a, v in ops:
                    if kind == "R":
                        yield from tx.read(a)
                    else:
                        yield from tx.write(a, v)
            return body

        return hist, [stm.atomic(p, body_of(ops)) for p, ops in enumerate(progs)]

    return make


def test_random_histories_against_naive_checker():
    rng = random.Random(2008)
    checked = 0
    non_opaque = 0
    for i in range(600):
        validate = i % 2 == 0
        hist, sys = random_run(random_workload(rng, TL2, validate_reads=validate), rng, 400)
        assert sys.finished()
        h = hist.events
        if len(transactions(h)) <= 6:
            fast = final_state_opaque(h)
            assert fast == final_state_opaque_naive(h)
            checked += 1
        assert strictly_serializable(h)
        if validate:
            assert opaque(h)
        elif not opaque(h):
            non_opaque += 1
    assert checked >= 500
    assert non_opaque > 0
