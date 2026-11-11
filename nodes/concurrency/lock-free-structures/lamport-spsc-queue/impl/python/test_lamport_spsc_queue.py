# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lamport-spsc-queue/. The authors are listed in prov/63WNND.jsonl.

import random
from collections import deque

from explorer import Memory, Run, explore, program, random_run
from lamport_spsc_queue import FastForwardQueue, LamportQueue
from lincheck import EMPTY, FULL, QueueSpec, lin_check, linearize


def make(procs, cls=LamportQueue, capacity=2, **flags):
    def setup():
        mem = Memory()
        q = cls(mem, capacity, **flags)
        return mem, [program(q, ops) for ops in procs]

    return setup


def results(run):
    return [ev[2] for ev in run.history if ev[1] == "res"]


PRODUCER = [("enq", 1), ("enq", 2), ("enq", 3)]
CONSUMER = [("deq",), ("deq",), ("deq",)]


def test_example_sequential() -> None:
    for cls in (LamportQueue, FastForwardQueue):
        run = Run(make([[("enq", 1), ("enq", 2), ("enq", 3), ("deq",), ("enq", 4), ("deq",), ("deq",), ("deq",)]], cls))
        assert run.finish(0)
        assert results(run) == [True, True, FULL, 1, True, 2, 4, EMPTY]


def test_random_sequential_against_deque() -> None:
    for cls in (LamportQueue, FastForwardQueue):
        rng = random.Random(3)
        ops, model, want = [], deque(), []
        for i in range(400):
            if rng.random() < 0.5:
                ops.append(("enq", i))
                if len(model) < 4:
                    model.append(i)
                    want.append(True)
                else:
                    want.append(FULL)
            else:
                ops.append(("deq",))
                want.append(model.popleft() if model else EMPTY)
        run = Run(make([ops], cls, capacity=4))
        assert run.finish(0, limit=100000)
        assert results(run) == want


def test_exhaustive_one_producer_one_consumer() -> None:
    for cls in (LamportQueue, FastForwardQueue):
        for cap in (1, 2):
            st = explore(make([PRODUCER, CONSUMER], cls, capacity=cap), lin_check(QueueSpec(capacity=cap)))
            assert st.failure is None, st.failure
            assert st.runs > 10


def test_every_operation_is_bounded_and_uses_no_rmw() -> None:
    # Wait-free: in every state of every interleaving, no operation has taken
    # more than 4 steps (Lamport) or 2 steps (FastForward), and every step is
    # a plain read or write.
    for cls, most in ((LamportQueue, 4), (FastForwardQueue, 2)):
        def check_states(run, most=most):
            if max(run.count) > most:
                return "too many steps"
            if any(op[0] not in ("read", "write") for _, op, _ in run.trace):
                return "a step that is not a read or a write"
            return None

        st = explore(make([PRODUCER, CONSUMER], cls), lin_check(QueueSpec(capacity=2)), check_states=check_states)
        assert st.failure is None, st.failure


def test_seeded_runs_linearizable() -> None:
    for seed in range(100):
        rng = random.Random(seed)
        cap = rng.randrange(1, 4)
        k = rng.randrange(3, 8)
        prod = [("enq", i) for i in range(k)]
        cons = [("deq",)] * k
        for cls in (LamportQueue, FastForwardQueue):
            run = random_run(make([prod, cons], cls, capacity=cap), seed)
            assert linearize(run.history, QueueSpec(capacity=cap)) is not None


def test_store_reorder_breaks_it() -> None:
    # Without release order, the write of tail can become visible before the
    # write of the item. The consumer then sees a non-empty queue, reads the
    # slot too early, and returns a value that was never enqueued.
    st = explore(make([[("enq", 7)], [("deq",)]], store_reorder=True), lin_check(QueueSpec(capacity=2)))
    assert st.failure is not None
    assert "None" in st.failure[0]


def test_two_producers_break_it() -> None:
    # The queue is for one producer only: two producers read the same tail
    # and write the same slot, and one item is lost.
    for cls in (LamportQueue, FastForwardQueue):
        st = explore(make([[("enq", 1)], [("enq", 2)], [("deq",), ("deq",)]], cls), lin_check(QueueSpec(capacity=2)))
        assert st.failure is not None
