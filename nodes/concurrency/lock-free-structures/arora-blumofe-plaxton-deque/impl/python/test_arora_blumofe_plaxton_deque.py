# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/arora-blumofe-plaxton-deque/. The authors are listed in prov/YWVGPT.jsonl.

import random
from collections import Counter, deque

import pytest

from arora_blumofe_plaxton_deque import ABPDeque
from explorer import Memory, Run, explore, program, random_run
from lincheck import ABORT, EMPTY, WorkStealingDequeSpec, lin_check, linearize, operations

SPEC = WorkStealingDequeSpec()


def make(procs, **flags):
    def setup():
        mem = Memory()
        d = ABPDeque(mem, **flags)
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
    run = Run(make([[("push", 1), ("push", 2), ("push", 3), ("steal",), ("pop",), ("pop",), ("pop",), ("steal",), ("push", 4), ("steal",)]]))
    assert run.finish(0)
    assert results(run) == [None, None, None, 1, 3, 2, EMPTY, EMPTY, None, 4]
    assert run.mem.peek("age") == (1, 1) and run.mem.peek("bot") == 1


def test_random_sequential_against_deque() -> None:
    rng = random.Random(9)
    ops, model, want = [], deque(), []
    for i in range(400):
        r = rng.random()
        # The array has a fixed size, and the indices only go back to 0 when
        # the deque gets empty, so keep few items in it.
        if r < 0.4 and len(model) < 3:
            ops.append(("push", i))
            model.append(i)
            want.append(None)
        elif r < 0.75:
            ops.append(("pop",))
            want.append(model.pop() if model else EMPTY)
        else:
            ops.append(("steal",))
            want.append(model.popleft() if model else EMPTY)
    run = Run(make([ops], capacity=64))
    assert run.finish(0, limit=200000)
    assert results(run) == want


def test_fixed_size_overflow() -> None:
    run = Run(make([[("push", i) for i in range(5)]], capacity=4))
    with pytest.raises(OverflowError):
        run.finish(0)


def test_exhaustive_owner_and_thieves() -> None:
    cases = [
        [[("push", 1), ("pop",)], [("steal",)]],
        [[("push", 1), ("push", 2), ("pop",), ("pop",)], [("steal",), ("steal",)]],
        [[("push", 1), ("pop",)], [("steal",)], [("steal",)]],
        [[("push", 1), ("pop",), ("push", 2), ("pop",)], [("steal",), ("steal",)]],
    ]
    for procs in cases:
        st = explore(make(procs), lin_check(SPEC))
        assert st.failure is None, st.failure
        assert st.runs > 5


def test_aba_without_the_tag() -> None:
    # A thief reads age = (0, 0) and item 1, and stops. The owner pops 1
    # (top and bot go back to 0) and pushes 2 into the same slot. Without a
    # new tag, the thief's CAS succeeds and it returns 1 a second time.
    procs = [[("push", 1), ("pop",), ("push", 2)], [("steal",)]]
    st = explore(make(procs, tag=False), no_duplicates)
    assert st.failure is not None
    run = Run(make(procs, tag=False))
    run.finish_op(0)
    run.until(1, lambda op: op[0] == "cas")
    run.finish(0)
    run.finish(1)
    assert results(run, 0) == [None, 1, None] and results(run, 1) == [1]
    assert linearize(run.history, SPEC) is None
    # With the tag, the same schedule gives ABORT.
    run = Run(make(procs))
    run.finish_op(0)
    run.until(1, lambda op: op[0] == "cas")
    run.finish(0)
    run.finish(1)
    assert results(run, 1) == [ABORT]
    st = explore(make(procs), lin_check(SPEC))
    assert st.failure is None, st.failure


def test_operations_are_bounded() -> None:
    # push 3 steps, steal at most 4, pop at most 7, in every interleaving.
    limits = {"push": 3, "steal": 4, "pop": 7}

    def check_states(run):
        for p, name, s in run.op_steps:
            if s > limits[name]:
                return f"{name} took {s} steps"
        return None

    procs = [[("push", 1), ("push", 2), ("pop",), ("pop",)], [("steal",)], [("steal",)]]
    st = explore(make(procs), lin_check(SPEC), check_states=check_states)
    assert st.failure is None, st.failure


def test_seeded_runs() -> None:
    for seed in range(120):
        rng = random.Random(seed)
        owner, size = [], 0
        for i in range(8):
            if rng.random() < 0.6 and size < 3:
                owner.append(("push", i))
                size += 1
            else:
                owner.append(("pop",))
                size = max(0, size - 1)
        procs = [owner, [("steal",)] * 3, [("steal",)] * 3]
        run = random_run(make(procs, capacity=16), seed)
        assert all(op is None for op in run.pending)
        assert linearize(run.history, SPEC) is not None
        ops = operations(run.history)
        got = [o.result for o in ops if o.name in ("pop", "steal") and o.result not in (EMPTY, ABORT)]
        assert len(got) == len(set(got))
        assert Counter(got) <= Counter(o.arg[0] for o in ops if o.name == "push")
