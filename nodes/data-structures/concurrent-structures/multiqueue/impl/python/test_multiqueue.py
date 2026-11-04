# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multiqueue/. The authors are listed in prov/THZT7C.jsonl.

import random
import threading
from collections import Counter

import pytest
from multiqueue import EMPTY, SPIN, MultiQueue

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


def linearizable(history, init, step):
    """Wing and Gong search: is there a legal order that respects real time?

    step(state, name, arg, result) returns the new state if the call with this
    result is allowed in state, or None; states are hashable.
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
            s2 = step(state, history[i][1], history[i][2], history[i][3])
            if s2 is not None and dfs(done | 1 << i, s2):
                return True
        return False

    return dfs(0, init)


# ---- the relaxed sequential specification ----


def relaxed_step(state, name, arg, result):
    """state is the sorted multiset. Delete-min may return any item, and EMPTY only if empty."""
    if name == "insert":
        return tuple(sorted(state + (arg,)))
    if result == EMPTY:
        return state if not state else None
    if result not in state:
        return None
    s = list(state)
    s.remove(result)
    return tuple(s)


class Script:
    """A fake random source that returns scripted indices."""

    def __init__(self, picks):
        self.picks = list(picks)

    def randrange(self, n):
        return self.picks.pop(0)


def rank(items, x):
    return 1 + sum(y < x for y in items)


# ---- tests ----


def test_example():
    m = MultiQueue(4, rng=Script([0, 0, 1, 1, 2, 3, 0, 2, 1, 3, 2, 3]))
    for x in (3, 9, 1, 7, 5, 4):  # heaps [3, 9], [1, 7], [5], [4]
        m.insert(x)
    assert [q.top for q in m.heaps] == [3, 1, 5, 4]
    assert m.delete_min() == 3  # picks heaps 0 and 2: minima 3 and 5; rank 2
    assert m.delete_min() == 1  # picks heaps 1 and 3: minima 1 and 4
    assert m.delete_min() == 4  # picks heaps 2 and 3: minima 5 and 4
    m.check_invariant()
    assert m.items() == [5, 7, 9]


def test_try_lock_retry():
    m = MultiQueue(2, rng=Script([0, 1, 0, 0, 1, 1]))
    m.insert(1)
    m.insert(2)  # heaps [1], [2]
    m.heaps[0].lock.acquire()  # another thread holds heap 0
    g = m.delete_min_steps()  # picks heaps 0 and 0
    assert [next(g) for _ in range(3)] == [None, None, SPIN]  # the lock is taken, try again
    m.heaps[0].lock.release()
    try:
        while True:
            next(g)
    except StopIteration as stop:
        assert stop.value == 2  # second try picks heaps 1 and 1
    m.check_invariant()


def test_edges():
    with pytest.raises(ValueError):
        MultiQueue(0)
    m = MultiQueue(3, seed=1)
    assert m.delete_min() == EMPTY
    m.insert(5)
    assert m.delete_min() == 5  # found by the scan if the two picks are empty
    assert m.delete_min() == EMPTY
    one = MultiQueue(1, seed=2)  # one heap: an exact priority queue
    for x in (4, 2, 8, 6):
        one.insert(x)
    assert [one.delete_min() for _ in range(5)] == [2, 4, 6, 8, EMPTY]


def test_random_against_model():
    for seed in range(30):
        rng = random.Random(seed)
        m = MultiQueue(rng.randrange(1, 6), seed=seed)
        model = Counter()
        for _ in range(500):
            if rng.random() < 0.55:
                x = rng.randrange(100)
                m.insert(x)
                model[x] += 1
            else:
                x = m.delete_min()
                if x == EMPTY:
                    assert not +model
                else:
                    assert model[x] > 0
                    model[x] -= 1
            m.check_invariant()
        assert m.items() == sorted(model.elements())


def test_rank_quality():
    # the two-choice rule keeps the expected rank close to the number of heaps
    c = 8
    m = MultiQueue(c, seed=7)
    for x in random.Random(3).sample(range(100000), 4000):
        m.insert(x)
    ranks = []
    for _ in range(2000):
        items = m.items()
        x = m.delete_min()
        ranks.append(rank(items, x))
        m.insert(random.Random(len(ranks)).randrange(100000, 200000) + len(ranks))
    assert sum(ranks) / len(ranks) < 2 * c
    assert max(ranks) > 1  # it is not an exact queue


def test_random_interleavings_are_linearizable():
    for seed in range(400):
        rng = random.Random(seed)
        m = MultiQueue(rng.randrange(1, 4), seed=seed)
        init = []
        for _ in range(rng.randrange(0, 4)):
            x = rng.randrange(10)
            m.insert(x)
            init.append(x)
        threads = []
        for _ in range(3):
            ops = []
            for _ in range(rng.randrange(1, 4)):
                if rng.random() < 0.5:
                    x = rng.randrange(10)
                    ops.append(("insert", x, lambda x=x: m.insert_steps(x)))
                else:
                    ops.append(("delete_min", None, m.delete_min_steps))
            threads.append(ops)
        schedule = [rng.randrange(3) for _ in range(rng.randrange(10, 80))]
        history = interleave(threads, schedule)
        m.check_invariant()
        assert linearizable(history, tuple(sorted(init)), relaxed_step), (seed, history)


def test_threads():
    m = MultiQueue(8, seed=5)
    out = [[] for _ in range(4)]

    def worker(w):
        for i in range(500):
            m.insert(w * 1000 + i)
            if i % 2:
                out[w].append(m.delete_min())

    ts = [threading.Thread(target=worker, args=(w,)) for w in range(4)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    m.check_invariant()
    taken = [x for o in out for x in o]
    assert EMPTY not in taken
    assert sorted(taken + m.items()) == sorted(w * 1000 + i for w in range(4) for i in range(500))
