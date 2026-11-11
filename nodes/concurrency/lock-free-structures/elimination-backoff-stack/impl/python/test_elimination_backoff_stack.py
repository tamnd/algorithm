# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/elimination-backoff-stack/. The authors are listed in prov/BE3KEB.jsonl.

import random

from elimination_backoff_stack import BUSY, EliminationBackoffStack
from explorer import Memory, Run, explore, program, random_run
from lincheck import EMPTY, StackSpec, lin_check, linearize


class Spec(StackSpec):
    def __init__(self, init=()):
        self.init = tuple(init)


def make(procs, init=(), capacity=2, timeout=2, seed=0, handles=None):
    def setup():
        mem = Memory()
        s = EliminationBackoffStack(mem, capacity=capacity, timeout=timeout)
        s.push_all(list(init))
        hs = [s.handle(p, seed) for p in range(len(procs))]
        if handles is not None:
            handles[:] = hs
        return mem, [program(h, ops) for h, ops in zip(hs, procs)]

    return setup


def results(run):
    return [ev[2] for ev in run.history if ev[1] == "res"]


def test_example_sequential() -> None:
    run = Run(make([[("push", 1), ("push", 2), ("pop",), ("push", 3), ("pop",), ("pop",), ("pop",)]]))
    run.finish(0)
    assert results(run) == [None, None, 2, None, 3, 1, EMPTY]


def test_random_sequential_against_list() -> None:
    rng = random.Random(2004)
    for _ in range(500):
        ops = [("push", rng.randint(0, 9)) if rng.random() < 0.55 else ("pop",) for _ in range(rng.randint(0, 12))]
        run = Run(make([ops]))
        run.finish(0)
        model: list[int] = []
        expect = []
        for op in ops:
            if op[0] == "push":
                model.append(op[1])
                expect.append(None)
            else:
                expect.append(model.pop() if model else EMPTY)
        assert results(run) == expect


def test_solo_steps_are_bounded() -> None:
    run = Run(make([[("push", 1), ("pop",), ("pop",)]]))
    assert run.finish_op(0) == 4
    assert run.finish_op(0) == 4
    assert run.finish_op(0) == 1


def test_example_elimination_run() -> None:
    hs: list = []
    run = Run(make([[("push", 1)], [("pop",)], [("push", 2)]], init=(0,), capacity=1, handles=hs))
    run.until(0, lambda op: op[0] == "cas")  # p reads top = node of 0
    run.until(1, lambda op: op[0] == "cas")  # q reads top = node of 0
    run.finish_op(2)  # r pushes 2: top changes
    assert run.step(0) is False  # the CAS of p fails
    assert run.step(1) is False  # the CAS of q fails
    run.step(0)  # p reads slot 0: FREE
    assert run.step(0) is True  # p: FREE -> (1, WAITING)
    run.step(1)  # q reads slot 0: (1, WAITING)
    assert run.step(1) is True  # q: WAITING -> (POP, BUSY), q has the value 1
    run.finish(1)
    run.step(0)  # p reads (POP, BUSY)
    run.finish(0)
    assert results(run) == [None, 1, None]
    assert hs[0].eliminated == 1 and hs[1].eliminated == 1
    assert run.mem.peek(("slot", 0))[1] != BUSY
    order = linearize(run.history, Spec((0,)))
    assert order is not None
    assert [o.name for o in order] == ["push", "push", "pop"]  # push(2), push(1), then pop -> 1


def test_exhaustive_two_processes() -> None:
    cases = [
        ([[("push", 1), ("pop",)], [("push", 2), ("pop",)]], ()),
        ([[("pop",)], [("push", 3)]], (1,)),
    ]
    for procs, init in cases:
        st = explore(make(procs, init, capacity=1, timeout=1), lin_check(Spec(init)))
        assert st.failure is None, st.failure
        assert st.runs > 0


def test_exhaustive_three_processes_with_elimination() -> None:
    procs = [[("push", 1)], [("pop",)], [("push", 2)]]
    st = explore(make(procs, (0,), capacity=1, timeout=1), lin_check(Spec((0,))))
    assert st.failure is None, st.failure


def test_random_schedules_linearizable_and_eliminate() -> None:
    rng = random.Random(1007912)
    total = 0
    for seed in range(300):
        procs = [[("push", 10 * p + i) if (p + i) % 2 == 0 else ("pop",) for i in range(3)] for p in range(4)]
        hs: list = []
        run = random_run(make(procs, (1, 2), capacity=2, timeout=3, seed=seed, handles=hs), rng.randrange(10**6))
        assert all(q is None for q in run.pending)
        assert linearize(run.history, Spec((1, 2))) is not None
        total += sum(h.eliminated for h in hs)
    assert total > 0


def test_range_policy_adapts() -> None:
    s = EliminationBackoffStack(Memory(), capacity=4)
    h = s.handle(0)
    for _ in range(10):
        h.record_success()
    assert h.range == 4
    for _ in range(10):
        h.record_timeout()
    assert h.range == 1
