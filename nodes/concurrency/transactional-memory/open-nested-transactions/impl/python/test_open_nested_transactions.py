# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/open-nested-transactions/. The authors are listed in prov/R3QGVQ.jsonl.

import random

from open_nested_transactions import (
    SIZE, OpenNestingTL2, compensate_insert, contains, insert, parent,
    physical_undo, unconditional_remove,
)
from sched import explore, random_run
from stm import Memory

K1, K2, WORK = 1, 2, 3


def consistent(mem, keys):
    return mem.val[SIZE] == sum(mem.val[k] for k in keys)


def scenario_size(comp_factory):
    """Parent inserts K1 and cancels; process 1 inserts K2 (closed)."""

    def make():
        mem = Memory(4)
        stm = OpenNestingTL2(mem, coarse=True)

        def p1():
            return (yield from stm.run_op(1, insert(K2)))

        return mem, [parent(stm, 0, K1, comp_factory(K1), True, WORK), p1()]

    return make


def test_semantic_compensation_keeps_the_size_right():
    runs = 0
    for mem, sys in explore(scenario_size(compensate_insert), 150):
        runs += 1
        assert sys.finished() and all(e is None for e in sys.error)
        assert mem.val[K1] == 0 and mem.val[K2] == 1 and mem.val[SIZE] == 1
    assert runs > 10


def test_physical_undo_loses_a_concurrent_update():
    bad = [mem.val[SIZE] for mem, sys in explore(scenario_size(physical_undo), 150)
           if not consistent(mem, (K1, K2))]
    assert bad and set(bad) == {0}       # K2 is in the set but SIZE says 0


def scenario_visibility(use_locks):
    """Parent inserts K1 and cancels; process 1 asks whether K1 is in the set."""

    def make():
        mem = Memory(4)
        stm = OpenNestingTL2(mem, use_locks=use_locks, coarse=True)

        def body(tx):
            return (yield from stm.open_atomic(tx, K1, contains(K1), None))

        def p1():
            return (yield from stm.atomic_top(1, body))

        return mem, [parent(stm, 0, K1, compensate_insert(K1), True, WORK), p1()]

    return make


def test_abstract_lock_hides_the_effect_of_an_open_child():
    for mem, sys in explore(scenario_visibility(True), 150):
        assert sys.finished()
        assert sys.result[1] is False      # K1 was never in a committed state


def test_without_abstract_lock_the_effect_leaks():
    seen = [sys.result[1] for mem, sys in explore(scenario_visibility(False), 150)]
    assert True in seen                    # some run saw K1, which no commit added


def scenario_existing_key(comp_factory):
    """Process 1 inserts K1 and commits; the parent also inserts K1 and cancels."""

    def make():
        mem = Memory(4)
        stm = OpenNestingTL2(mem, coarse=True)

        def body(tx):
            return (yield from stm.open_atomic(tx, K1, insert(K1), compensate_insert(K1)))

        def p1():
            return (yield from stm.atomic_top(1, body))

        return mem, [parent(stm, 0, K1, comp_factory(K1), True, WORK), p1()]

    return make


def test_unconditional_compensation_removes_another_insert():
    finals = {mem.val[K1] for mem, sys in explore(scenario_existing_key(unconditional_remove), 150)}
    assert 0 in finals


def test_conditional_compensation_keeps_another_insert():
    for mem, sys in explore(scenario_existing_key(compensate_insert), 150):
        assert mem.val[K1] == 1 and mem.val[SIZE] == 1


def test_random_parents_with_compensation_and_locks():
    rng = random.Random(2007)
    for i in range(600):
        n = 2 + i % 3
        keys = list(range(1, 4))
        mem = None
        plan = [(rng.choice(keys), rng.random() < 0.5) for _ in range(n)]
        use_writer = i % 2 == 0

        def make(plan=plan, use_writer=use_writer):
            m = Memory(5)
            stm = OpenNestingTL2(m)
            procs = [parent(stm, p, k, compensate_insert(k), c, 4) for p, (k, c) in enumerate(plan)]
            if use_writer:
                def writer():
                    def w(tx):
                        yield from tx.write(4, 1)
                    yield from stm.atomic(len(plan), w)
                procs.append(writer())
            return m, procs

        mem, sys = random_run(make, rng, 20_000)
        assert sys.finished() and all(e is None for e in sys.error)
        expected = {k for k, c in plan if not c}
        assert {k for k in keys if mem.val[k]} == expected
        assert mem.val[SIZE] == len(expected)
