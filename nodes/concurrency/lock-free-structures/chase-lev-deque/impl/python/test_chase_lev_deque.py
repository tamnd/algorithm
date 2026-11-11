# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chase-lev-deque/. The authors are listed in prov/HJCFRC.jsonl.

import random
from collections import Counter, deque

from chase_lev_deque import ChaseLevDeque
from explorer import Memory, Run, explore, program, random_run
from lincheck import ABORT, EMPTY, WorkStealingDequeSpec, lin_check, linearize, operations

SPEC = WorkStealingDequeSpec()


def make(procs, objs=None, **flags):
    def setup():
        mem = Memory()
        d = ChaseLevDeque(mem, **flags)
        if objs is not None:
            objs[:] = [d]
        return mem, [program(d, ops) for ops in procs]

    return setup


def results(run, p=None):
    return [ev[2] for ev in run.history if ev[1] == "res" and (p is None or ev[0] == p)]


def no_duplicates(run, truncated=False):
    got = [o.result for o in operations(run.history) if o.name in ("pop", "steal") and o.result not in (None, EMPTY, ABORT)]
    if len(got) != len(set(got)):
        return "an item was taken twice: " + repr(operations(run.history))
    return None


def test_example_sequential() -> None:
    run = Run(make([[("push", 1), ("push", 2), ("push", 3), ("steal",), ("pop",), ("pop",), ("pop",), ("steal",)]]))
    assert run.finish(0)
    assert results(run) == [None, None, None, 1, 3, 2, EMPTY, EMPTY]


def test_random_sequential_against_deque_with_growth() -> None:
    rng = random.Random(5)
    ops, model, want = [], deque(), []
    for i in range(400):
        r = rng.random()
        if r < 0.5:
            ops.append(("push", i))
            model.append(i)
            want.append(None)
        elif r < 0.75:
            ops.append(("pop",))
            want.append(model.pop() if model else EMPTY)
        else:
            ops.append(("steal",))
            want.append(model.popleft() if model else EMPTY)
    run = Run(make([ops]))
    assert run.finish(0, limit=200000)
    assert results(run) == want


def test_growth_keeps_order() -> None:
    objs = []
    run = Run(make([[("push", i) for i in range(100)] + [("steal",)] * 50 + [("pop",)] * 50], objs=objs))
    assert run.finish(0, limit=200000)
    assert results(run)[100:] == list(range(50)) + list(range(99, 49, -1))
    assert run.mem.peek((run.mem.peek("array"), "size")) == 128


def test_exhaustive_owner_and_thieves() -> None:
    cases = [
        [[("push", 1), ("pop",)], [("steal",)]],
        [[("push", 1), ("push", 2), ("pop",), ("pop",)], [("steal",), ("steal",)]],
        [[("push", 1), ("pop",)], [("steal",)], [("steal",)]],
        [[("push", 1), ("push", 2), ("push", 3), ("pop",)], [("steal",), ("steal",)]],  # grows from size 2
    ]
    for procs in cases:
        st = explore(make(procs), lin_check(SPEC))
        assert st.failure is None, st.failure
        assert st.runs > 5


def test_last_item_race_needs_the_cas() -> None:
    # One item, the owner pops it and a thief steals it. Without the CAS on
    # top, both can return it.
    procs = [[("push", 1), ("pop",)], [("steal",)]]
    st = explore(make(procs, last_cas=False), no_duplicates)
    assert st.failure is not None
    st = explore(make(procs), no_duplicates)
    assert st.failure is None


def test_store_load_reordering_breaks_pop() -> None:
    # If the owner reads top before its write of bottom is visible (x86
    # without the fence), a thief can steal twice while the owner takes the
    # second item without a CAS: the same item twice.
    procs = [[("push", 1), ("push", 2), ("pop",)], [("steal",), ("steal",)]]
    st = explore(make(procs, reorder_pop=True), no_duplicates)
    assert st.failure is not None
    run = Run(make(procs, reorder_pop=True))
    run.finish_op(0)
    run.finish_op(0)
    run.until(0, lambda op: op == ("write", "bottom", 1))  # owner has read top = 0
    run.finish(1)  # the thief steals 1 and then 2, since bottom is still 2
    run.finish(0)
    assert results(run, 1) == [1, 2]
    assert results(run, 0)[-1] == 2


def test_owner_operations_are_wait_free() -> None:
    # Without growth, push takes 6 steps and pop at most 8, in every state.
    def check_states(run):
        for p, name, s in run.op_steps:
            if p == 0 and s > 8:
                return f"{name} took {s} steps"
        return None

    procs = [[("push", 1), ("pop",), ("pop",)], [("steal",)], [("steal",)]]
    st = explore(make(procs, size=4), lin_check(SPEC), check_states=check_states)
    assert st.failure is None, st.failure


def test_seeded_runs() -> None:
    for seed in range(120):
        rng = random.Random(seed)
        owner = []
        for i in range(8):
            owner.append(("push", i) if rng.random() < 0.6 else ("pop",))
        procs = [owner, [("steal",)] * 3, [("steal",)] * 3]
        run = random_run(make(procs), seed)
        assert all(op is None for op in run.pending)
        assert linearize(run.history, SPEC) is not None
        ops = operations(run.history)
        got = [o.result for o in ops if o.name in ("pop", "steal") and o.result not in (EMPTY, ABORT)]
        assert len(got) == len(set(got))
        assert Counter(got) <= Counter(o.arg[0] for o in ops if o.name == "push")
