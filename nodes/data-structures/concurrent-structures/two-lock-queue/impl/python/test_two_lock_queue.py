# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-lock-queue/. The authors are listed in prov/PMYQM4.jsonl.

import random
import threading

from two_lock_queue import EMPTY, TwoLockQueue, run

# ---- deterministic interleaving driver and linearizability check ----

Op = tuple  # (thread, name, arg, result, invoke time, response time)


def interleave(threads, schedule, limit=100000):
    """Run the operations of each thread, one atomic step at a time.

    threads[t] is a list of (name, arg, make) where make() returns the step
    generator of the operation. schedule is a sequence of thread numbers; a
    pick of a thread with no work left is skipped. After the schedule, the
    remaining steps run round robin. Returns the history as a list of Op.
    """
    todo = [list(reversed(ops)) for ops in threads]
    cur: list = [None] * len(threads)
    history: list = []
    clock = 0

    def step(t):
        nonlocal clock
        if cur[t] is None:
            if not todo[t]:
                return False
            name, arg, make = todo[t].pop()
            cur[t] = (name, arg, make(), clock)
        name, arg, gen, inv = cur[t]
        clock += 1
        try:
            next(gen)
        except StopIteration as stop:
            history.append((t, name, arg, stop.value, inv, clock))
            cur[t] = None
        return True

    for t in schedule:
        step(t)
    steps = 0
    while any(cur) or any(todo):
        for t in range(len(threads)):
            step(t)
        steps += 1
        assert steps < limit, "no progress"
    return history


def linearizable(history, init, apply):
    """Wing and Gong search: is there a legal order that respects real time?

    apply(state, name, arg) returns (new state, result); states are hashable.
    """
    n = len(history)
    full = (1 << n) - 1
    seen = set()

    def dfs(done, state):
        if done == full:
            return True
        if (done, state) in seen:
            return False
        seen.add((done, state))
        for i in range(n):
            if done >> i & 1:
                continue
            inv_i = history[i][4]
            if any(not done >> j & 1 and history[j][5] < inv_i for j in range(n)):
                continue
            s2, r = apply(state, history[i][1], history[i][2])
            if r == history[i][3] and dfs(done | 1 << i, s2):
                return True
        return False

    return dfs(0, init)


def queue_spec(state, name, arg):
    if name == "enq":
        return state + (arg,), None
    if not state:
        return state, EMPTY
    return state[1:], state[0]


def make_ops(q, plan):
    ops = []
    for name, arg in plan:
        if name == "enq":
            ops.append((name, arg, lambda a=arg: q.enqueue_steps(a)))
        else:
            ops.append((name, None, q.dequeue_steps))
    return ops


def test_example() -> None:
    q: TwoLockQueue[int] = TwoLockQueue()
    q.enqueue(7)
    a = make_ops(q, [("enq", 8)])
    b = make_ops(q, [("deq", None)])
    c = make_ops(q, [("deq", None)])
    # A links node 8 and stops before it moves tail; B and C then dequeue 7 and 8.
    h = interleave([a, b, c], [0, 1, 1, 1, 1, 2, 2, 2, 2, 0, 0])
    assert [(t, r) for t, _, _, r, _, _ in h] == [(1, 7), (2, 8), (0, None)]
    assert h[1][5] < h[2][5]  # C returned 8 before enq(8) returned
    assert linearizable(h, (7,), queue_spec)
    q.check_invariant()
    assert q.items() == []


def test_head_passes_tail() -> None:
    q: TwoLockQueue[int] = TwoLockQueue()
    g = q.enqueue_steps(1)
    next(g)  # node 1 is linked, tail still at the sentinel
    assert q.dequeue() == 1
    assert q.head is not q.tail and q.tail.next is q.head
    for _ in g:
        pass
    q.check_invariant()
    assert q.dequeue() is EMPTY


def test_edges() -> None:
    q: TwoLockQueue[str] = TwoLockQueue()
    assert q.dequeue() is EMPTY
    q.enqueue("a")
    q.check_invariant()
    assert q.items() == ["a"]
    assert q.dequeue() == "a"
    assert q.dequeue() is EMPTY
    q.check_invariant()
    q.enqueue(None)  # type: ignore[arg-type]
    assert q.dequeue() is None


def test_locks() -> None:
    q: TwoLockQueue[int] = TwoLockQueue()
    q.enqueue(5)
    g = q.enqueue_steps(6)
    next(g)  # g holds tail_lock
    assert q.dequeue() == 5  # a dequeue does not wait for an enqueuer
    e = q.enqueue_steps(7)
    assert all(next(e) == "spin" for _ in range(10))  # a second enqueuer waits
    d = q.dequeue_steps()
    next(d)  # d holds head_lock
    d2 = q.dequeue_steps()
    assert all(next(d2) == "spin" for _ in range(10))  # a second dequeuer waits
    assert [run(gen) for gen in (g, e, d, d2)] == [None, None, 6, 7]
    q.check_invariant()
    assert q.items() == []


def test_random_against_model() -> None:
    rng = random.Random(4711)
    for _ in range(500):
        q: TwoLockQueue[int] = TwoLockQueue()
        model: list[int] = []
        for _ in range(rng.randint(0, 40)):
            if rng.random() < 0.55:
                x = rng.randint(-5, 5)
                q.enqueue(x)
                model.append(x)
            else:
                want = model.pop(0) if model else EMPTY
                assert q.dequeue() == want
            q.check_invariant()
            assert q.items() == model


def test_random_interleavings_are_linearizable() -> None:
    rng = random.Random(90210)
    for _ in range(500):
        q: TwoLockQueue[int] = TwoLockQueue()
        start = [rng.randint(0, 9) for _ in range(rng.randint(0, 2))]
        for x in start:
            q.enqueue(x)
        threads = []
        for t in range(3):
            plan = [("enq", 10 * t + i) if rng.random() < 0.5 else ("deq", None) for i in range(rng.randint(1, 3))]
            threads.append(make_ops(q, plan))
        schedule = [rng.randrange(3) for _ in range(rng.randint(0, 60))]
        h = interleave(threads, schedule)
        assert linearizable(h, tuple(start), queue_spec)
        q.check_invariant()


def test_threads() -> None:
    q: TwoLockQueue[tuple[int, int]] = TwoLockQueue()
    per, producers = 300, 3
    got: list[list[tuple[int, int]]] = [[] for _ in range(3)]

    def produce(p: int) -> None:
        for i in range(per):
            q.enqueue((p, i))

    def consume(c: int) -> None:
        while len(got[c]) < per:
            x = q.dequeue()
            if x is not EMPTY:
                got[c].append(x)  # type: ignore[arg-type]

    ts = [threading.Thread(target=produce, args=(p,)) for p in range(producers)]
    ts += [threading.Thread(target=consume, args=(c,)) for c in range(3)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    allgot = [x for g in got for x in g]
    assert sorted(allgot) == sorted((p, i) for p in range(producers) for i in range(per))
    for g in got:  # one consumer sees the items of one producer in order
        for p in range(producers):
            seq = [i for (pp, i) in g if pp == p]
            assert seq == sorted(seq)
    assert q.dequeue() is EMPTY
