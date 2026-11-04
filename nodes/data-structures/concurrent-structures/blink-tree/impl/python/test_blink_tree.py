# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blink-tree/. The authors are listed in prov/DQ5FW8.jsonl.

import random
import threading

import pytest
from blink_tree import BLinkTree

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


# ---- the sequential map ----


def map_apply(state, name, arg):
    d = dict(state)
    if name == "search":
        return state, d.get(arg)
    if name == "insert":
        k, v = arg
        old = d.get(k)
        d[k] = v
        return tuple(sorted(d.items())), old
    if name == "delete":
        old = d.pop(arg, None)
        return tuple(sorted(d.items())), old
    assert name == "items"
    return state, state


def op(t, name, arg):
    if name == "search":
        return (name, arg, lambda: t.search_steps(arg))
    if name == "insert":
        return (name, arg, lambda: t.insert_steps(*arg))
    return (name, arg, lambda: t.delete_steps(arg))


# ---- tests ----


def test_example():
    t = BLinkTree(3)
    for k in (10, 20, 30, 40, 50):
        t.insert(k, k * 10)
    # leaves [10, 20] and [30, 40, 50] under the root (20, +inf)
    right = t._read(t.root).vals[1]
    assert t._read(right).keys == (30, 40, 50)
    s = t.search_steps(50)
    next(s)  # L1: the root
    next(s)  # L2: reads the root page and will go to the right leaf
    assert t.insert(45, 450) is None  # splits that leaf and updates the root
    assert t._read(right).keys == (30, 40) and t._read(right).high == 40
    assert t._read(t.root).keys == (20, 40, None)
    try:
        while True:
            next(s)
    except StopIteration as stop:
        assert stop.value == 500  # found by the right link of the old leaf
    t.check_invariant()


def test_search_takes_no_lock():
    t = BLinkTree(3)
    for k in range(20):
        t.insert(k, -k)
    for node in t.nodes:
        node.lock.acquire()
    assert [t.search(k) for k in range(21)] == [-k for k in range(20)] + [None]
    for node in t.nodes:
        node.lock.release()


def test_edges():
    with pytest.raises(ValueError):
        BLinkTree(2)
    t = BLinkTree(3)
    assert t.search(5) is None and t.delete(5) is None and t.items() == []
    assert t.insert(5, "a") is None
    assert t.insert(5, "b") == "a"
    assert t.search(5) == "b" and t.delete(5) == "b" and t.search(5) is None
    for k in range(100):
        t.insert(k, k)
    assert t.height >= 3
    for k in range(100):
        assert t.delete(k) == k
    assert t.items() == []
    t.check_invariant()
    t.insert(7, 7)
    assert t.items() == [(7, 7)]


def test_random_against_model():
    for seed in range(40):
        rng = random.Random(seed)
        t = BLinkTree(rng.choice([3, 4, 5]))
        d = {}
        for i in range(400):
            k = rng.randrange(80)
            r = rng.random()
            if r < 0.5:
                assert t.insert(k, i) == d.get(k)
                d[k] = i
            elif r < 0.7:
                assert t.delete(k) == d.pop(k, None)
            else:
                assert t.search(k) == d.get(k)
        t.check_invariant()
        assert t.items() == sorted(d.items())


def test_random_interleavings_are_linearizable():
    for seed in range(300):
        rng = random.Random(seed)
        t = BLinkTree(3)
        init = {}
        for k in rng.sample(range(0, 40, 2), rng.randrange(0, 9)):
            t.insert(k, -k)
            init[k] = -k
        threads = []
        for th in range(3):
            ops = []
            for i in range(rng.randrange(2, 5)):
                k = rng.randrange(40)
                r = rng.random()
                if r < 0.6:
                    ops.append(op(t, "insert", (k, 100 * th + i)))
                elif r < 0.75:
                    ops.append(op(t, "delete", k))
                else:
                    ops.append(op(t, "search", k))
            threads.append(ops)
        schedule = [rng.randrange(3) for _ in range(rng.randrange(20, 200))]
        history = interleave(threads, schedule)
        t.check_invariant()
        end = max(h[5] for h in history) + 1
        history.append((3, "items", None, tuple(t.items()), end, end + 1))
        assert linearizable(history, tuple(sorted(init.items())), map_apply), (seed, history)


def test_threads():
    t = BLinkTree(4)
    errors = []

    def worker(w):
        try:
            for k in range(w, 2000, 4):
                assert t.insert(k, w) is None
                assert t.search(k) == w
            for k in range(w, 2000, 8):
                assert t.delete(k) == w
        except AssertionError as e:  # pragma: no cover
            errors.append(e)

    ts = [threading.Thread(target=worker, args=(w,)) for w in range(4)]
    for x in ts:
        x.start()
    for x in ts:
        x.join()
    assert not errors
    t.check_invariant()
    expect = [(k, k % 4) for k in range(2000) if not (k % 8 < 4 and k % 4 == k % 8)]
    assert t.items() == expect
