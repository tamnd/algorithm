# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vyukov-bounded-mpmc-queue/. The authors are listed in prov/8Z65SA.jsonl.

import random
from collections import Counter, deque

from explorer import Memory, Run, explore, program, random_run
from lincheck import EMPTY, FULL, QueueSpec, lin_check, linearize, operations
from vyukov_bounded_mpmc_queue import VyukovQueue


def make(procs, capacity=2, objs=None):
    def setup():
        mem = Memory()
        q = VyukovQueue(mem, capacity)
        if objs is not None:
            objs[:] = [q]
        return mem, [program(q, ops) for ops in procs]

    return setup


def results(run, p=None):
    return [ev[2] for ev in run.history if ev[1] == "res" and (p is None or ev[0] == p)]


TRY = QueueSpec(capacity=2, spurious=True)
STRICT = QueueSpec(capacity=2)


def test_example_sequential() -> None:
    run = Run(make([[("enq", 1), ("enq", 2), ("enq", 3), ("deq",), ("enq", 4), ("deq",), ("deq",), ("deq",)]]))
    assert run.finish(0)
    assert results(run) == [True, True, FULL, 1, True, 2, 4, EMPTY]


def test_random_sequential_is_strict() -> None:
    # With one process there are no spurious results.
    rng = random.Random(11)
    ops, model, want = [], deque(), []
    for i in range(500):
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
    run = Run(make([ops], capacity=4))
    assert run.finish(0, limit=100000)
    assert results(run) == want


def test_solo_steps() -> None:
    # Alone, enq and deq take 5 steps (read pos, read seq, CAS, data, seq),
    # or 2 when they return FULL or EMPTY.
    run = Run(make([[("deq",), ("enq", 1), ("enq", 2), ("enq", 3), ("deq",)]]))
    assert [run.finish_op(0) for _ in range(5)] == [2, 5, 5, 2, 5]


def test_exhaustive_try_semantics() -> None:
    # Linearizable if enq may fail with FULL and deq with EMPTY at any time.
    cases = [
        [[("enq", 1)], [("enq", 2)], [("deq",), ("deq",)]],
        [[("enq", 1), ("deq",)], [("enq", 2), ("deq",)]],
        [[("enq", 1), ("enq", 2), ("enq", 3)], [("deq",), ("deq",)]],
        [[("deq",)], [("deq",)], [("enq", 1), ("enq", 2)]],
    ]
    for procs in cases:
        st = explore(make(procs), lin_check(TRY))
        assert st.failure is None, st.failure


def test_not_linearizable_as_a_strict_queue() -> None:
    # p claims position 0 and stops before it sets seq; q's item 2 is in the
    # queue, but a later deq returns EMPTY.
    run = Run(make([[("enq", 1)], [("enq", 2)], [("deq",)]]))
    run.until(0, lambda op: op[0] == "write" and op[1] == ("data", 0))
    assert run.finish(1)
    assert run.finish(2)
    assert results(run) == [True, EMPTY]
    assert linearize(run.history, STRICT) is None
    assert linearize(run.history, TRY) is not None
    # The explorer finds such a run by itself.
    st = explore(make([[("enq", 1)], [("enq", 2)], [("deq",)]]), lin_check(STRICT))
    assert st.failure is not None


def test_a_stalled_producer_blocks_the_queue() -> None:
    # After the stall, at most N - 1 more items go in, every later enq returns
    # FULL and every deq returns EMPTY, for ever. A blocking deq never returns.
    n = 4
    procs = [[("enq", 100)], [("enq", i) for i in range(10)], [("deq",)] * 10, [("deq_wait",)]]
    run = Run(make(procs, capacity=n))
    run.until(0, lambda op: op[0] == "write" and op[1] == ("data", 0))
    assert run.finish(1)
    assert run.finish(2)
    assert results(run, 1) == [True] * (n - 1) + [FULL] * (10 - (n - 1))
    assert results(run, 2) == [EMPTY] * 10
    for _ in range(2000):
        run.step(3)
    assert results(run, 3) == []
    # When p runs again, everything flows.
    assert run.finish(0)
    assert run.finish(3)
    assert results(run, 3) == [100]


def test_seeded_runs() -> None:
    for seed in range(150):
        rng = random.Random(seed)
        cap = rng.choice([2, 3, 4])
        procs = [[("enq", 10 * p + i) if rng.random() < 0.5 else ("deq",) for i in range(4)] for p in range(3)]
        run = random_run(make(procs, capacity=cap), seed)
        assert all(op is None for op in run.pending)
        assert linearize(run.history, QueueSpec(capacity=cap, spurious=True)) is not None
        # No item is lost or taken twice: what went in is what came out plus
        # what is still in the cells from deq_pos to enq_pos.
        ops = operations(run.history)
        put = [o.arg[0] for o in ops if o.name == "enq" and o.result is True]
        got = [o.result for o in ops if o.name == "deq" and o.result != EMPTY]
        lo, hi = run.mem.peek("deq_pos"), run.mem.peek("enq_pos")
        left = [run.mem.peek(("data", i % cap)) for i in range(lo, hi)]
        assert Counter(got + left) == Counter(put)
