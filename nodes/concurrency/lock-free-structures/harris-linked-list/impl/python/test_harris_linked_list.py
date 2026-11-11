# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/harris-linked-list/. The authors are listed in prov/CQ32KC.jsonl.

import random

from explorer import Memory, Run, explore, program, random_run
from harris_linked_list import HarrisList
from lincheck import SetSpec, lin_check, linearize


class Spec(SetSpec):
    def __init__(self, keys=()):
        self.init = frozenset(keys)


def make(procs, keys=(), objs=None, **flags):
    def setup():
        mem = Memory()
        s = HarrisList(mem, keys, **flags)
        if objs is not None:
            objs[:] = [s]
        return mem, [program(s, ops) for ops in procs]

    return setup


def results(run, p=None):
    return [ev[2] for ev in run.history if ev[1] == "res" and (p is None or ev[0] == p)]


def test_example_sequential() -> None:
    objs = []
    ops = [("insert", 5), ("insert", 2), ("insert", 8), ("insert", 5), ("find", 2), ("delete", 2), ("find", 2), ("delete", 2), ("find", 8)]
    run = Run(make([ops], objs=objs))
    assert run.finish(0)
    assert results(run) == [True, True, True, False, True, True, False, False, True]
    assert objs[0].reachable() == [(5, False), (8, False)]


def test_random_sequential_against_set() -> None:
    rng = random.Random(3)
    ops, model, want = [], set(), []
    for _ in range(300):
        k = rng.randrange(10)
        name = rng.choice(["insert", "delete", "find"])
        ops.append((name, k))
        if name == "insert":
            want.append(k not in model)
            model.add(k)
        elif name == "delete":
            want.append(k in model)
            model.discard(k)
        else:
            want.append(k in model)
    objs = []
    run = Run(make([ops], objs=objs))
    assert run.finish(0, limit=100000)
    assert results(run) == want
    assert objs[0].reachable() == [(k, False) for k in sorted(model)]


CASES = [
    ((), [[("insert", 1), ("delete", 1)], [("insert", 1), ("find", 1)]]),
    ((1, 3), [[("delete", 1)], [("insert", 2), ("find", 2)]]),
    ((1, 2, 3), [[("delete", 1), ("find", 2)], [("delete", 2), ("find", 1)]]),
    ((), [[("insert", 2)], [("insert", 2)], [("delete", 2)]]),
    ((1, 2), [[("delete", 1)], [("delete", 2)], [("find", 2)]]),
    ((2,), [[("delete", 2), ("insert", 1)], [("insert", 3), ("delete", 1)]]),
]


def test_exhaustive_small_cases() -> None:
    for keys, procs in CASES:
        st = explore(make(procs, keys), lin_check(Spec(keys)))
        assert st.failure is None, (keys, st.failure)
        assert st.runs > 5


def test_naive_list_loses_an_insert() -> None:
    # pred -> 1 -> 3. delete(1) swings head.next from 1 to 3, while
    # insert(2) swings 1.next from 3 to 2. Both CAS steps succeed and 2 is lost.
    keys, procs = (1, 3), [[("delete", 1)], [("insert", 2), ("find", 2)]]
    st = explore(make(procs, keys, mark=False), lin_check(Spec(keys)))
    assert st.failure is not None
    objs = []
    run = Run(make(procs, keys, objs=objs, mark=False))
    run.until(0, lambda op: op[0] == "cas")  # delete(1) is about to unlink 1
    run.finish_op(1)  # insert(2) links 2 after 1
    run.finish(0)
    run.finish(1)
    assert results(run, 1) == [True, False]
    assert objs[0].reachable() == [(3, False)]
    assert linearize(run.history, Spec(keys)) is None


def test_naive_list_loses_a_delete() -> None:
    # head -> 1 -> 2 -> 3. delete(1) and delete(2) unlink neighbours at the
    # same time; 2 stays reachable after both return True.
    keys, procs = (1, 2, 3), [[("delete", 1), ("find", 2)], [("delete", 2), ("find", 1)]]
    st = explore(make(procs, keys, mark=False), lin_check(Spec(keys)))
    assert st.failure is not None


def test_one_cas_snips_a_chain_of_marked_nodes() -> None:
    objs = []
    run = Run(make([[("find", 3)]], keys=(1, 2, 3), marked=(1, 2), objs=objs))
    assert objs[0].reachable() == [(1, True), (2, True), (3, False)]
    run.finish(0)
    assert results(run) == [True]
    assert [op[0] for _, op, _ in run.trace].count("cas") == 1
    assert objs[0].reachable() == [(3, False)]


def test_solo_operations_are_bounded() -> None:
    # Alone, an operation on a list of n unmarked nodes reads each next field
    # on its way once: at most n + 4 steps for find and insert, n + 6 for delete.
    for n in (0, 1, 4, 16):
        keys = tuple(range(n))
        for name, k, bound in (("find", n, n + 4), ("insert", n, n + 4), ("delete", n - 1, n + 6)):
            if k < 0:
                continue
            run = Run(make([[(name, k)]], keys))
            steps = run.finish_op(0)
            assert steps is not None and steps <= bound, (name, n, steps)


def test_seeded_runs() -> None:
    for seed in range(100):
        rng = random.Random(seed)
        procs = [[(rng.choice(["insert", "delete", "find"]), rng.randrange(4)) for _ in range(4)] for _ in range(3)]
        keys = tuple(k for k in range(4) if rng.random() < 0.5)
        objs = []
        run = random_run(make(procs, keys, objs=objs), seed)
        assert all(op is None for op in run.pending)
        assert linearize(run.history, Spec(keys)) is not None, run.history
        assert [k for k, _ in objs[0].reachable()] == sorted(k for k, _ in objs[0].reachable())


def test_others_finish_when_a_deleter_stops_after_marking() -> None:
    # p0 marks 2 and stops before it unlinks it. The others unlink it in their
    # searches and finish (lock-freedom does not need p0).
    keys = (1, 2, 3)
    procs = [[("delete", 2)], [("insert", 4), ("find", 2), ("delete", 3)], [("find", 3), ("insert", 2)]]
    objs = []
    run = Run(make(procs, keys, objs=objs))
    run.until(0, lambda op: op[0] == "cas")
    run.step(0)  # the mark
    assert objs[0].reachable()[1] == (2, True)
    assert run.finish(1) and run.finish(2)
    assert results(run, 1) == [True, False, True]
    assert results(run, 2) == [False, True]  # p1 deleted 3 first
    assert linearize(run.history, Spec(keys)) is not None
    assert objs[0].reachable() == [(1, False), (2, False), (4, False)]
