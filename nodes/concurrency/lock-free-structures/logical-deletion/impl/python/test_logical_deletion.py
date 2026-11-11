# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/logical-deletion/. The authors are listed in prov/5CC8PY.jsonl.

import random

from explorer import Memory, Run, explore, program, random_run
from lincheck import SetSpec, lin_check, linearize
from logical_deletion import LazyList, MarkedList


class Spec(SetSpec):
    def __init__(self, keys=()):
        self.init = frozenset(keys)


def make(cls, procs, keys=(), objs=None, **flags):
    def setup():
        mem = Memory()
        s = cls(mem, keys, **flags)
        if objs is not None:
            objs[:] = [s]
        return mem, [program(s, ops) for ops in procs]

    return setup


def results(run, p=None):
    return [ev[2] for ev in run.history if ev[1] == "res" and (p is None or ev[0] == p)]


def sequential_ops(seed, n):
    rng = random.Random(seed)
    ops, model, want = [], set(), []
    for _ in range(n):
        k = rng.randrange(8)
        name = rng.choice(["insert", "delete", "contains"])
        ops.append((name, k))
        if name == "insert":
            want.append(k not in model)
            model.add(k)
        elif name == "delete":
            want.append(k in model)
            model.discard(k)
        else:
            want.append(k in model)
    return ops, want, sorted(model)


def test_random_sequential_both_lists() -> None:
    ops, want, final = sequential_ops(5, 200)
    for cls in (MarkedList, LazyList):
        objs = []
        run = Run(make(cls, [ops], objs=objs))
        assert run.finish(0, limit=100000)
        assert results(run) == want
        assert objs[0].reachable() == final


CASES = [
    ((1, 3), [[("delete", 1)], [("insert", 2), ("contains", 2)]]),
    ((1, 2, 3), [[("delete", 1), ("contains", 2)], [("delete", 2), ("contains", 1)]]),
    ((), [[("insert", 1), ("delete", 1)], [("insert", 1), ("contains", 1)]]),
    ((2,), [[("delete", 2)], [("delete", 2)], [("contains", 2)]]),
]


def test_mark_in_the_pointer_word_is_linearizable() -> None:
    for keys, procs in CASES:
        st = explore(make(MarkedList, procs, keys), lin_check(Spec(keys)))
        assert st.failure is None, (keys, st.failure)
        assert st.runs > 5


def test_separate_mark_field_loses_an_insert() -> None:
    # head -> 1 -> 3. insert(2) finds pred = 1, reads 1.marked = False, and is
    # about to CAS 1.next. delete(1) marks 1 and unlinks it. The CAS on 1.next
    # still succeeds, because the mark is not in that word: 2 is linked after
    # a node that is no longer in the list.
    keys, procs = (1, 3), [[("delete", 1)], [("insert", 2), ("contains", 2)]]
    st = explore(make(MarkedList, procs, keys, mark_in_word=False), lin_check(Spec(keys)))
    assert st.failure is not None
    objs = []
    run = Run(make(MarkedList, procs, keys, objs=objs, mark_in_word=False))
    run.until(1, lambda op: op[0] == "cas")  # insert(2) has read 1.marked = False
    assert run.finish(0)  # delete(1) marks and unlinks 1
    assert run.finish(1)
    assert results(run, 0) == [True]
    assert results(run, 1) == [True, False]
    assert objs[0].reachable() == [3]
    assert linearize(run.history, Spec(keys)) is None
    # The same schedule on the list with the mark in the word: the CAS fails
    # and insert(2) tries again from the start.
    objs = []
    run = Run(make(MarkedList, procs, keys, objs=objs))
    run.until(1, lambda op: op[0] == "cas")
    assert run.finish(0)
    assert run.finish(1)
    assert results(run, 1) == [True, True]
    assert objs[0].reachable() == [2, 3]


def test_lazy_list_is_linearizable() -> None:
    for keys, procs in CASES[:2]:
        st = explore(make(LazyList, procs, keys), lin_check(Spec(keys)), max_steps=60)
        assert st.failure is None, (keys, st.failure)
        assert st.runs > 5


def test_seeded_runs_both_lists() -> None:
    for cls in (MarkedList, LazyList):
        for seed in range(60):
            rng = random.Random(seed)
            procs = [[(rng.choice(["insert", "delete", "contains"]), rng.randrange(4)) for _ in range(4)] for _ in range(3)]
            keys = tuple(k for k in range(4) if rng.random() < 0.5)
            objs = []
            run = random_run(make(cls, procs, keys, objs=objs), seed, max_steps=5000)
            assert all(op is None for op in run.pending), (cls, seed)
            assert linearize(run.history, Spec(keys)) is not None, (cls, seed)
            r = objs[0].reachable()
            assert r == sorted(set(r))


def test_contains_never_writes_and_is_bounded() -> None:
    # contains walks once and writes nothing, in both lists. Alone, on a list
    # of n nodes, it takes at most n + 2 steps.
    for cls in (MarkedList, LazyList):
        for n in (0, 1, 4, 16):
            run = Run(make(cls, [[("contains", n)]], tuple(range(n))))
            steps = run.finish_op(0)
            assert steps is not None and steps <= n + 2, (cls, n, steps)
            assert all(op[0] == "read" for _, op, _ in run.trace)


def test_marked_node_is_unlinked_by_others() -> None:
    # p0 marks 2 and stops before it unlinks it. p1 sees 2 as absent at once,
    # and its insert(4) unlinks 2 on the way.
    keys = (1, 2, 3)
    objs = []
    run = Run(make(MarkedList, [[("delete", 2)], [("contains", 2), ("insert", 4)]], keys, objs=objs))
    run.until(0, lambda op: op[0] == "cas")
    run.step(0)  # the mark: the logical deletion
    assert objs[0].reachable() == [1, 2, 3]
    assert run.finish(1)
    assert results(run, 1) == [False, True]
    assert objs[0].reachable() == [1, 3, 4]
    assert linearize(run.history, Spec(keys)) is not None
