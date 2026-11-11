# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/michael-scott-queue/. The authors are listed in prov/N8QFHV.jsonl.

import random

from explorer import Memory, Run, explore, program, random_run
from lincheck import EMPTY, QueueSpec, lin_check, linearize
from michael_scott_queue import MSQueue, TwoLockQueue


class Spec(QueueSpec):
    def __init__(self, init=()):
        super().__init__()
        self.init = tuple(init)


def make(procs, init=(), cls=MSQueue, objs=None, **flags):
    def setup():
        mem = Memory()
        q = cls(mem, **flags)
        if init:
            if cls is MSQueue:
                q.enq_all(list(init))
            else:
                raise ValueError("init only for MSQueue")
        if objs is not None:
            objs[:] = [q]
        return mem, [program(q, ops) for ops in procs]

    return setup


def results(run):
    return [ev[2] for ev in run.history if ev[1] == "res"]


def test_example_sequential() -> None:
    for cls in (MSQueue, TwoLockQueue):
        run = Run(make([[("enq", 1), ("enq", 2), ("deq",), ("enq", 3), ("deq",), ("deq",), ("deq",)]], cls=cls))
        run.finish(0)
        assert results(run) == [True, True, 1, True, 2, 3, EMPTY]


def test_random_sequential_against_deque() -> None:
    rng = random.Random(1996)
    for t in range(500):
        ops = [("enq", rng.randint(0, 9)) if rng.random() < 0.55 else ("deq",) for _ in range(rng.randint(0, 12))]
        run = Run(make([ops], cls=MSQueue if t % 2 else TwoLockQueue))
        run.finish(0)
        model: list[int] = []
        expect = []
        for op in ops:
            if op[0] == "enq":
                model.append(op[1])
                expect.append(True)
            else:
                expect.append(model.pop(0) if model else EMPTY)
        assert results(run) == expect


def test_solo_steps_are_bounded() -> None:
    run = Run(make([[("enq", 1), ("deq",), ("deq",)]]))
    assert run.finish_op(0) == 6
    assert run.finish_op(0) == 6
    assert run.finish_op(0) == 4


def test_exhaustive_linearizable() -> None:
    cases = [
        ([[("enq", 1), ("deq",)], [("enq", 2), ("deq",)]], ()),
        ([[("deq",), ("deq",)], [("enq", 3)]], (1,)),
        ([[("enq", 1)], [("enq", 2)], [("deq",)]], ()),
    ]
    for procs, init in cases:
        st = explore(make(procs, init), lin_check(Spec(init)))
        assert st.failure is None, st.failure


def test_exhaustive_two_lock_queue() -> None:
    procs = [[("enq", 1), ("deq",)], [("enq", 2)]]
    st = explore(make(procs, cls=TwoLockQueue), lin_check(Spec()), max_steps=40)
    assert st.failure is None, st.failure


def test_random_schedules_linearizable() -> None:
    rng = random.Random(248052)
    for seed in range(300):
        procs = [[("enq", 10 * p + i) if rng.random() < 0.5 else ("deq",) for i in range(3)] for p in range(4)]
        run = random_run(make(procs, (1, 2)), seed)
        assert all(q is None for q in run.pending)
        assert linearize(run.history, Spec((1, 2))) is not None


def stalled_enqueuer(help_on):
    """p links its node and stops before it swings Tail; then q runs alone."""
    run = Run(make([[("enq", 1)], [("enq", 2), ("deq",), ("deq",)]], help=help_on))
    run.until(0, lambda op: op[0] == "cas" and op[1] == "Tail")  # p is past its CAS on next
    return run


def test_helping_lets_others_pass_a_stalled_enqueuer() -> None:
    run = stalled_enqueuer(True)
    assert run.finish(1, limit=200)
    assert results(run) == [True, 1, 2]


def test_without_helping_a_stalled_enqueuer_blocks_the_others() -> None:
    run = stalled_enqueuer(False)
    assert not run.finish(1, limit=2000)
    assert results(run) == []  # q took 2000 steps and completed nothing


def test_without_the_head_tail_check_head_passes_tail() -> None:
    objs: list = []
    run = Run(make([[("enq", 1)], [("deq",)]], objs=objs, head_tail_check=False))
    run.until(0, lambda op: op[0] == "cas" and op[1] == "Tail")  # 1 is linked, Tail lags
    run.finish(1)  # the dequeue swings Head to the node of 1, past Tail
    assert results(run) == [1]
    assert not objs[0].tail_reachable_from_head()


def test_explorer_finds_head_past_tail_and_not_with_the_check() -> None:
    procs = [[("enq", 1)], [("deq",)]]

    def holder():
        box: list = []
        return box

    for flag, bad in ((False, True), (True, False)):
        box = holder()
        st = explore(make(procs, objs=box, head_tail_check=flag), lin_check(Spec()),
                     check_states=lambda run: None if box[0].tail_reachable_from_head() else "Head passed Tail")
        assert (st.failure is not None) == bad
