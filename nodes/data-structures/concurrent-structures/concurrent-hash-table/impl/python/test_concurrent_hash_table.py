# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/concurrent-hash-table/. The authors are listed in prov/HQKVBH.jsonl.

import random
import threading

import pytest

from concurrent_hash_table import MISSING, ConcurrentHashTable

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


def map_spec(state, name, arg):
    d = dict(state)
    if name == "put":
        k, v = arg
        old = d.get(k, MISSING)
        d[k] = v
    elif name == "get":
        return state, d.get(arg, MISSING)
    else:
        old = d.pop(arg, MISSING)
    return tuple(sorted(d.items())), old


def make_ops(t, plan):
    ops = []
    for name, arg in plan:
        if name == "put":
            ops.append((name, arg, lambda a=arg: t.put_steps(*a)))
        elif name == "get":
            ops.append((name, arg, lambda a=arg: t.get_steps(a)))
        else:
            ops.append((name, arg, lambda a=arg: t.remove_steps(a)))
    return ops


def test_example() -> None:
    t: ConcurrentHashTable[int, str] = ConcurrentHashTable(stripes=2, capacity=2, max_load=1.0)
    assert t.put(4, "a") is MISSING
    assert t.put(7, "b") is MISSING
    assert t.buckets == [[(4, "a")], [(7, "b")]]
    # keys 6 and 4 are in stripe 0, key 9 in stripe 1
    a = make_ops(t, [("put", (6, "c"))])
    b = make_ops(t, [("put", (9, "d"))])
    c = make_ops(t, [("get", 4)])
    h = interleave([a, b, c], [0, 1, 2, 0, 1, 2, 2, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1])
    res = {name: r for _, name, _, r, _, _ in h}
    assert res["get"] == "a"
    assert t.resizes == 1
    assert t.buckets == [[(4, "a")], [(9, "d")], [(6, "c")], [(7, "b")]]
    assert linearizable(h, ((4, "a"), (7, "b")), map_spec)
    t.check_invariant()


def test_edges() -> None:
    with pytest.raises(ValueError):
        ConcurrentHashTable(stripes=4, capacity=6)
    t: ConcurrentHashTable[str, int] = ConcurrentHashTable(stripes=1, capacity=1)
    assert t.get("x") is MISSING and t.remove("x") is MISSING
    assert t.put("x", 1) is MISSING
    assert t.put("x", 2) == 1
    assert t.get("x") == 2
    assert t.remove("x") == 2
    assert t.get("x") is MISSING
    t.check_invariant()


def test_same_stripe_waits_other_stripe_runs() -> None:
    t: ConcurrentHashTable[int, int] = ConcurrentHashTable(stripes=2, capacity=2, max_load=100)
    g = t.put_steps(0, 0)
    next(g)  # g holds lock 0
    assert t.put(1, 1) is MISSING  # stripe 1 is free
    w = t.get_steps(2)  # stripe 0: must wait
    assert all(next(w) == "spin" for _ in range(5))
    for _ in g:
        pass
    assert next(w) is None
    for _ in w:
        pass
    t.check_invariant()


def test_random_against_model() -> None:
    rng = random.Random(1234)
    for _ in range(500):
        stripes = rng.choice([1, 2, 4])
        t: ConcurrentHashTable[int, int] = ConcurrentHashTable(stripes, stripes * rng.randint(1, 2), rng.choice([0.5, 1.0, 3.0]))
        model: dict[int, int] = {}
        for _ in range(rng.randint(0, 60)):
            k, op = rng.randint(-10, 10), rng.random()
            if op < 0.5:
                v = rng.randint(0, 99)
                assert t.put(k, v) == model.get(k, MISSING)
                model[k] = v
            elif op < 0.75:
                assert t.get(k) == model.get(k, MISSING)
            else:
                assert t.remove(k) == model.pop(k, MISSING)
            t.check_invariant()
            assert t.to_dict() == model


def test_random_interleavings_are_linearizable() -> None:
    rng = random.Random(777)
    for _ in range(500):
        t: ConcurrentHashTable[int, int] = ConcurrentHashTable(2, 2, rng.choice([0.5, 1.0, 9.0]))
        for k in rng.sample(range(6), rng.randint(0, 3)):
            t.put(k, -1)
        init = tuple(sorted(t.to_dict().items()))
        threads = []
        for th in range(3):
            plan = []
            for i in range(rng.randint(1, 3)):
                k = rng.randrange(6)
                plan.append(rng.choice([("put", (k, 10 * th + i)), ("get", k), ("remove", k)]))
            threads.append(make_ops(t, plan))
        h = interleave(threads, [rng.randrange(3) for _ in range(rng.randint(0, 80))])
        assert linearizable(h, init, map_spec)
        t.check_invariant()


def test_threads() -> None:
    t: ConcurrentHashTable[int, int] = ConcurrentHashTable(stripes=4, capacity=4, max_load=1.0)

    def work(w: int) -> None:
        for i in range(300):
            assert t.put(4 * i + w, w) is MISSING
        for i in range(0, 300, 2):
            assert t.remove(4 * i + w) == w

    ts = [threading.Thread(target=work, args=(w,)) for w in range(4)]
    for x in ts:
        x.start()
    for x in ts:
        x.join()
    t.check_invariant()
    assert t.to_dict() == {4 * i + w: w for w in range(4) for i in range(1, 300, 2)}
    assert t.resizes >= 1
