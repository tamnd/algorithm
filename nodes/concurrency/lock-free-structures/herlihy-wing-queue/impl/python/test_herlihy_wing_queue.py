# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/herlihy-wing-queue/. The authors are listed in prov/FY15RG.jsonl.

import random

from explorer import Memory, Run, explore, program, random_run
from herlihy_wing_queue import HWQueue
from lincheck import QueueSpec, lin_check, linearize


def make(procs, capacity=8):
    def setup():
        mem = Memory()
        q = HWQueue(mem, capacity)
        return mem, [program(q, ops) for ops in procs]

    return setup


def results(run):
    return [ev[2] for ev in run.history if ev[1] == "res"]


def test_example_sequential() -> None:
    run = Run(make([[("enq", 1), ("enq", 2), ("deq",), ("enq", 3), ("deq",), ("deq",)]]))
    run.finish(0)
    assert results(run) == [True, True, 1, True, 2, 3]


def test_random_sequential_against_list() -> None:
    rng = random.Random(1990)
    for _ in range(500):
        ops, size = [], 0
        for _ in range(rng.randint(0, 12)):
            if size and rng.random() < 0.45:
                ops.append(("deq",))
                size -= 1
            else:
                ops.append(("enq", rng.randint(1, 9)))
                size += 1
        run = Run(make([ops], capacity=16))
        assert run.finish(0)
        model: list[int] = []
        expect = []
        for op in ops:
            if op[0] == "enq":
                model.append(op[1])
                expect.append(True)
            else:
                expect.append(model.pop(0))
        assert results(run) == expect


def test_enqueue_is_wait_free_two_steps() -> None:
    run = Run(make([[("enq", 1), ("enq", 2)], [("deq",)]]))
    assert run.finish_op(0) == 2
    assert run.finish_op(0) == 2


def test_dequeue_on_empty_queue_spins_forever() -> None:
    run = Run(make([[("deq",)]]))
    assert not run.finish(0, limit=1000)
    assert results(run) == []


def test_stalled_enqueuer_does_not_block_a_dequeue() -> None:
    run = Run(make([[("enq", "x")], [("enq", "y")], [("deq",)]]))
    run.step(0)  # x takes slot 0 with FAA and stops before its store
    run.finish(1)  # y takes slot 1 and stores
    assert run.finish(2, limit=50)
    assert results(run) == [True, "y"]


def no_fixed_point_runs():
    """The two extensions of one prefix that rule out a fixed linearization point."""
    procs = [[("enq", "x")], [("enq", "y")], [("deq",), ("deq",)]]
    prefix = [0, 1, 1]  # x: FAA (slot 0); y: FAA (slot 1), store y; enq(y) returns
    one = Run(make(procs))
    for p in prefix:
        one.step(p)
    one.finish_op(2)  # deq scans: slot 0 is empty, slot 1 has y
    one.finish(0)  # x stores in slot 0
    one.finish(2)  # deq returns x
    two = Run(make(procs))
    for p in prefix:
        two.step(p)
    two.finish(0)  # x stores in slot 0 first
    two.finish(2)  # deq returns x, then y
    return one, two


def deq_results(run):
    return [ev[2] for ev in run.history if ev[0] == 2 and ev[1] == "res"]


def test_no_fixed_linearization_point_for_enqueue() -> None:
    one, two = no_fixed_point_runs()
    assert deq_results(one) == ["y", "x"]  # enq(y) must come before enq(x)
    assert deq_results(two) == ["x", "y"]  # enq(x) must come before enq(y)
    for run in (one, two):
        assert linearize(run.history, QueueSpec()) is not None
        faa = [p for p, op, _ in run.trace if op[0] == "faa"]
        assert faa == [0, 1]  # the FAA of x comes first in both runs
    stores = [p for p, op, _ in two.trace if op[0] == "write"]
    assert stores == [1, 0]  # in run two the store of y also comes first
    # so in run one, neither step of enq(x) can be its point: both steps of
    # x come before the point of enq(y) or after it in a way that run two forbids


def test_exhaustive_linearizable() -> None:
    cases = [
        [[("enq", 1)], [("enq", 2)], [("deq",)]],
        [[("enq", 1), ("deq",)], [("enq", 2), ("deq",)]],
    ]
    for procs in cases:
        st = explore(make(procs), lin_check(QueueSpec()), max_steps=40)
        assert st.failure is None, st.failure


def test_random_schedules_linearizable() -> None:
    for seed in range(300):
        procs = [[("enq", 10 * p), ("deq",), ("enq", 10 * p + 1)] for p in range(4)]
        run = random_run(make(procs, capacity=16), seed)
        assert all(q is None for q in run.pending)
        assert linearize(run.history, QueueSpec()) is not None


def test_a_dequeue_can_starve_while_others_complete() -> None:
    k = 20
    run = Run(make([[("enq", i) for i in range(k)], [("deq",)], [("deq",)] * k], capacity=k))
    for _ in range(k):
        run.finish_op(0)  # one item is stored
        run.until(1, lambda op: op[0] == "swap")  # d1 has read back
        run.finish_op(2)  # d2 takes the item first
        run.until(1, lambda op: op[0] == "read")  # d1 scans and finds nothing
    assert len(deq_results_of(run, 2)) == k
    assert deq_results_of(run, 1) == []


def deq_results_of(run, pid):
    return [ev[2] for ev in run.history if ev[0] == pid and ev[1] == "res"]
