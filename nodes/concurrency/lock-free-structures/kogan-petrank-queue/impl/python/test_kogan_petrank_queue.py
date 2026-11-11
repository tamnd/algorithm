# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kogan-petrank-queue/. The authors are listed in prov/MAZDKN.jsonl.

import random
from collections import deque

from explorer import Memory, Run, explore, program, random_run, replay
from kogan_petrank_queue import KPQueue, bound
from lincheck import EMPTY, QueueSpec, lin_check, linearize


class Spec(QueueSpec):
    def __init__(self, init=()):
        super().__init__()
        self.init = tuple(init)


def make(procs, init=(), objs=None):
    def setup():
        mem = Memory()
        q = KPQueue(mem, len(procs))
        q.enq_all(list(init))
        if objs is not None:
            objs[:] = [q]
        return mem, [program(q.handle(i), ops) for i, ops in enumerate(procs)]

    return setup


def results(run, p=None):
    return [ev[2] for ev in run.history if ev[1] == "res" and (p is None or ev[0] == p)]


def worst(run):
    return max((s for _, _, s in run.op_steps), default=0)


def bounded_explore(setup, check, switches):
    """Visit every schedule with at most `switches` preemptions (a switch away
    from a process that could still run), with a state cache. Return the
    number of complete runs, the largest step count of one operation, and the
    first failure."""
    runs, most = 0, 0
    seen = set()
    stack = [((), -1, switches)]
    while stack:
        prefix, cur, left = stack.pop()
        run = replay(setup, prefix)
        sched = list(prefix)
        while True:
            en = run.enabled()
            if not en:
                runs += 1
                most = max(most, worst(run))
                msg = check(run, False)
                if msg:
                    return runs, most, (msg, sched)
                break
            k = (run.key(), cur, left)
            if k in seen:
                break
            seen.add(k)
            nxt = cur if cur in en else en[0]
            cost = 1 if cur in en else 0
            for p in en:
                if p != nxt and left - cost >= 0:
                    stack.append((tuple(sched) + (p,), p, left - cost))
            run.step(nxt)
            sched.append(nxt)
            cur = nxt
    return runs, most, None


def test_example_sequential() -> None:
    run = Run(make([[("enq", 1), ("enq", 2), ("deq",), ("enq", 3), ("deq",), ("deq",), ("deq",)]]))
    assert run.finish(0)
    assert results(run) == [True, True, 1, True, 2, 3, EMPTY]


def test_random_sequential_against_deque() -> None:
    rng = random.Random(7)
    ops, model, want = [], deque(), []
    for i in range(300):
        if rng.random() < 0.55:
            ops.append(("enq", i))
            model.append(i)
            want.append(True)
        else:
            ops.append(("deq",))
            want.append(model.popleft() if model else EMPTY)
    run = Run(make([ops]))
    assert run.finish(0, limit=100000)
    assert results(run) == want


def test_solo_steps_are_bounded() -> None:
    # Alone, an operation does a fixed number of steps that grows with n
    # (the phase scan and the help scan read all n entries).
    # enq: 2n + 18; deq on an empty queue: 2n + 14; deq on a non-empty queue: 2n + 24.
    for n in (1, 2, 4, 8):
        for ops, init, extra in (([("enq", 1)], (), 18), ([("deq",)], (), 14), ([("deq",)], (5,), 24)):
            procs = [ops] + [[] for _ in range(n - 1)]
            run = Run(make(procs, init))
            steps = run.finish_op(0)
            assert steps == 2 * n + extra
            assert steps <= bound(n)


def test_bounded_preemption_exhaustive() -> None:
    cases = [
        ([[("enq", 1)], [("deq",)]], (), 3),
        ([[("enq", 1)], [("enq", 2)]], (), 3),
        ([[("deq",)], [("deq",)]], (1,), 3),
        ([[("deq",)], [("deq",)]], (), 3),
        ([[("enq", 1), ("deq",)], [("enq", 2), ("deq",)]], (), 2),
    ]
    for procs, init, sw in cases:
        runs, most, failure = bounded_explore(make(procs, init), lin_check(Spec(init)), sw)
        assert failure is None, failure
        assert runs > 0
        assert most <= bound(len(procs))


def test_exhaustive_prefixes() -> None:
    # Every interleaving of the first 26 steps; the partial histories must be linearizable.
    for procs, init in (([[("enq", 1)], [("deq",)]], ()), ([[("deq",)], [("deq",)]], (1,))):
        st = explore(make(procs, init), lin_check(Spec(init)), max_steps=26)
        assert st.failure is None, st.failure


def test_random_runs_linearizable_and_within_bound() -> None:
    for n in (2, 3, 4):
        for seed in range(40):
            procs = [[("enq", 10 * p + i) if (p + i + seed) % 2 else ("deq",) for i in range(3)] for p in range(n)]
            run = random_run(make(procs, (1,)), seed, max_steps=20000)
            assert all(op is None for op in run.pending)
            assert linearize(run.history, Spec((1,))) is not None
            assert worst(run) <= bound(n)


def test_crashed_processes_do_not_block() -> None:
    # Wait-freedom: the others stop for ever at random points, often in the
    # middle of an operation; process 0 still ends each operation within bound(n).
    n = 3
    for seed in range(40):
        rng = random.Random(seed)
        procs = [[("enq", 100), ("deq",), ("deq",)]] + [[("enq", 10 * p), ("deq",)] for p in range(1, n)]
        crash = {p: rng.randrange(1, 60) for p in range(1, n)}
        run = random_run(make(procs), seed, max_steps=20000, crash=crash)
        assert run.pending[0] is None
        assert all(s <= bound(n) for p, _, s in run.op_steps if p == 0)
        assert linearize(run.history, Spec()) is not None


def test_helping_finishes_a_crashed_enqueue() -> None:
    # Process 1 publishes enq(7) in state[1] and crashes. The next operation
    # of process 0 has a larger phase, so it helps: 7 is in the queue although
    # process 1 never takes another step.
    objs = []
    run = Run(make([[("deq",), ("deq",)], [("enq", 7)]], objs=objs))
    run.until(1, lambda op: op[0] == "write" and op[1] == ("state", 1))
    run.step(1)
    assert run.finish(0)
    assert 7 in results(run, 0)
    assert run.mem.peek(("state", 1))[2] is False
    assert linearize(run.history, Spec()) is not None


def test_no_starvation_under_a_hostile_schedule() -> None:
    # Process 1 runs many operations and process 0 gets one step for every
    # 25 steps of process 1. In a lock-free queue process 0 could lose every
    # race; here its operation ends within bound(2) of its own steps.
    procs = [[("deq",)], [("enq", i) if i % 2 == 0 else ("deq",) for i in range(200)]]
    run = Run(make(procs, (1,)))
    while run.pending[0] is not None:
        assert run.count[0] <= bound(2)
        for _ in range(25):
            if run.pending[1] is not None:
                run.step(1)
        run.step(0)
    assert worst(run) <= bound(2)
    assert linearize(run.history, Spec((1,))) is not None
