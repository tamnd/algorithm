# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lcrq/. The authors are listed in prov/83B4J8.jsonl.

import random
import threading
from collections import deque

from lcrq import BOTTOM, CRQ, EMPTY, LCRQ

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


def queue_apply(state, name, arg):
    """The sequential FIFO queue on a tuple."""
    if name == "enq":
        return state + (arg,), None
    if not state:
        return state, EMPTY
    return state[1:], state[0]


def finish(gen):
    try:
        while True:
            next(gen)
    except StopIteration as stop:
        return stop.value


def until(gen, cond):
    while not cond():
        next(gen)


# ---- tests ----


def test_example_full_ring_moves_to_a_new_crq():
    q = LCRQ(r=2, patience=100)
    q.enqueue("a")
    q.enqueue("b")  # the ring of 2 cells is full
    q.enqueue("c")  # ticket 2 finds a in cell 0; 2 - 0 >= 2, so it closes the ring and links a new one
    assert q.rings() == 2
    first = q.head.read()
    assert first.tail.read() == (True, 3) and first.next.read().ring[0].read() == (1, 0, "c")
    assert [q.dequeue() for _ in range(4)] == ["a", "b", "c", EMPTY]
    assert q.rings() == 1  # the head moved to the second ring


def test_dequeue_overtakes_an_enqueue():
    q = LCRQ(r=2, patience=100)
    crq = q.head.read()
    e = q.enqueue_steps("x")
    until(e, lambda: crq.tail.read() == (False, 1))  # the enqueue has ticket 0 and waits
    assert finish(q.dequeue_steps()) == EMPTY  # dequeue 0 empties cell 0 for the next round: (1, 2, bottom)
    assert crq.ring[0].read() == (1, 2, BOTTOM)
    assert finish(e) is None  # ticket 0 is dead; the enqueue takes ticket 1 and succeeds
    assert crq.ring[1].read() == (1, 1, "x")
    assert q.dequeue() == "x"


def test_unsafe_cell_refuses_a_late_enqueue():
    crq = CRQ(2)
    finish(crq.enqueue_steps("a", 100))  # ticket 0, cell 0
    d0 = crq.dequeue_steps()
    next(d0)  # dequeue 0 has its ticket and waits
    finish(crq.enqueue_steps("b", 100))  # ticket 1, cell 1
    assert finish(crq.dequeue_steps()) == "b"  # dequeue 1
    e2 = crq.enqueue_steps("c", 100)
    next(e2)  # ticket 2, for cell 0, which still holds a
    assert finish(crq.dequeue_steps()) == EMPTY  # dequeue 2 finds a from round 0 and marks the cell unsafe
    assert crq.ring[0].read() == (0, 0, "a")
    assert finish(d0) == "a"  # dequeue 0 takes a; the cell stays unsafe: (0, 2, bottom)
    assert crq.ring[0].read() == (0, 2, BOTTOM)
    assert finish(e2) == "OK"  # ticket 2 is refused, since head > 2; c goes in with a later ticket
    assert crq.ring[0].read() == (0, 2, BOTTOM)
    assert finish(crq.dequeue_steps()) == "c"


def test_edges():
    q = LCRQ(r=1, patience=1)
    assert q.dequeue() == EMPTY and q.dequeue() == EMPTY
    for x in range(5):
        q.enqueue(x)
    assert [q.dequeue() for _ in range(6)] == [0, 1, 2, 3, 4, EMPTY]
    q.enqueue(7)
    assert q.dequeue() == 7


def test_random_sequential_against_deque():
    for seed in range(30):
        rng = random.Random(seed)
        q, model = LCRQ(r=rng.choice((1, 2, 4, 8)), patience=rng.randrange(1, 5)), deque()
        for i in range(400):
            if rng.random() < 0.55:
                q.enqueue(i)
                model.append(i)
            else:
                assert q.dequeue() == (model.popleft() if model else EMPTY)
        while model:
            assert q.dequeue() == model.popleft()
        assert q.dequeue() == EMPTY


def test_random_interleavings_are_linearizable():
    rings = 0
    for seed in range(500):
        rng = random.Random(seed)
        q = LCRQ(r=rng.choice((1, 2, 3)), patience=rng.randrange(1, 4))
        first = q.head.read()
        work, n = [], 0
        for t in range(3):
            ops = []
            for _ in range(rng.randrange(1, 4)):
                if rng.random() < 0.55:
                    ops.append(("enq", n, lambda n=n: q.enqueue_steps(n)))
                    n += 1
                else:
                    ops.append(("deq", None, q.dequeue_steps))
            work.append(ops)
        history = interleave(work, [rng.randrange(3) for _ in range(rng.randrange(200))])
        rest = []
        while (v := q.dequeue()) != EMPTY:
            rest.append(v)
        end = max(h[5] for h in history) + 1
        history.append((9, "rest", None, tuple(rest), end, end + 1))

        def apply(state, name, arg):
            if name == "rest":
                return (), state
            return queue_apply(state, name, arg)

        assert linearizable(history, (), apply), seed
        rings += first.next.read() is not None
    assert rings > 100  # many runs closed a ring and moved on to a new one


def test_threads():
    q = LCRQ(r=8, patience=4)
    out = [[] for _ in range(4)]

    def producer(p):
        for i in range(300):
            q.enqueue((p, i))

    def consumer(c):
        while len(out[c]) < 300:
            v = q.dequeue()
            if v != EMPTY:
                out[c].append(v)

    ts = [threading.Thread(target=producer, args=(p,)) for p in range(4)]
    ts += [threading.Thread(target=consumer, args=(c,)) for c in range(4)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    got = sum(out, [])
    assert sorted(got) == sorted((p, i) for p in range(4) for i in range(300))
    for c in range(4):  # each consumer sees each producer's items in order
        for p in range(4):
            seq = [i for (pp, i) in out[c] if pp == p]
            assert seq == sorted(seq)
    assert q.dequeue() == EMPTY
