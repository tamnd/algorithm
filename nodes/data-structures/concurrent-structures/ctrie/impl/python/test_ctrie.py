# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ctrie/. The authors are listed in prov/3YJ33R.jsonl.

import random
import threading

from ctrie import NOTFOUND, CNode, Ctrie, INode, LNode, TNode

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


def map_apply(state, name, arg):
    """The sequential map on a frozenset of (key, value) pairs."""
    d = dict(state)
    if name == "lookup":
        return state, d.get(arg, NOTFOUND)
    if name == "insert":
        k, v = arg
        d[k] = v
        return frozenset(d.items()), None
    r = d.pop(arg, NOTFOUND)
    return frozenset(d.items()), r


def finish(gen):
    try:
        while True:
            next(gen)
    except StopIteration as stop:
        return stop.value


def small(**kw):
    """A trie with 4-way C-nodes and 4-bit hashes, so that paths and L-nodes are short."""
    return Ctrie(w=2, hbits=4, hash_fn=lambda k: k, **kw)


# ---- tests ----


def test_example():
    t = small()
    for k in (0, 4, 1):
        t.insert(k, str(k))
    root = t.root.read()
    assert root.bmp == 0b11 and isinstance(root.array[0], INode) and root.array[1].key == 1
    inner = root.array[0].read()  # 0 and 4 agree in the low 2 bits, and split on the next 2
    assert [sn.key for sn in inner.array] == [0, 4]
    assert t.lookup(4) == "4" and t.lookup(8) == NOTFOUND
    rem = t.remove_steps(4)
    while not isinstance(inner_main := root.array[0].read(), TNode):
        next(rem)  # the removal contracts the inner C-node to a tomb holding 0
    assert inner_main.sn.key == 0
    look = t.lookup_steps(0)
    next(look)  # the lookup has read the old root C-node and will meet the tomb
    assert finish(look) == "0"  # it cleans the root, which resurrects 0, and restarts
    assert finish(rem) == "4"
    root = t.root.read()
    assert [b.key for b in root.array] == [0, 1]  # the tomb is gone
    assert t.items() == {0: "0", 1: "1"}


def test_full_collisions_use_an_lnode():
    t = small()
    for k in (3, 19, 35):  # all equal to 3 in the low 4 bits
        t.insert(k, k)
    path = t.root.read().array[0].read().array[0].read()  # two C-nodes deep, the hash bits run out
    assert isinstance(path, LNode) and len(path.sns) == 3
    assert t.lookup(19) == 19 and t.lookup(51) == NOTFOUND
    assert t.remove(19) == 19 and t.remove(35) == 35
    assert t.lookup(3) == 3 and t.items() == {3: 3}


def test_edges():
    t = small()
    assert t.lookup(1) == NOTFOUND and t.remove(1) == NOTFOUND
    t.insert(1, "a")
    t.insert(1, "b")  # an update replaces the value
    assert t.lookup(1) == "b" and t.items() == {1: "b"}
    assert t.remove(1) == "b" and t.items() == {}
    assert isinstance(t.root.read(), CNode)  # the root is never a tomb
    d = Ctrie()
    for k in ("x", "y", 7):
        d.insert(k, k)
    assert d.lookup("y") == "y" and d.remove("x") == "x" and d.items() == {"y": "y", 7: 7}


def test_random_sequential_against_dict():
    for seed in range(20):
        rng = random.Random(seed)
        t, model = small(), {}
        for _ in range(400):
            k = rng.randrange(64)
            op = rng.random()
            if op < 0.4:
                t.insert(k, seed)
                model[k] = seed
            elif op < 0.75:
                assert t.remove(k) == model.pop(k, NOTFOUND)
            else:
                assert t.lookup(k) == model.get(k, NOTFOUND)
        assert t.items() == model


def test_random_interleavings_are_linearizable():
    for seed in range(400):
        rng = random.Random(seed)
        t = small()
        init = {}
        for _ in range(rng.randrange(6)):
            k = rng.choice((0, 4, 8, 1, 16, 32))
            t.insert(k, -1)
            init[k] = -1
        keys = (0, 4, 8, 1, 16, 32)
        work = []
        for th in range(3):
            ops = []
            for _ in range(rng.randrange(1, 4)):
                k, r = rng.choice(keys), rng.random()
                if r < 0.4:
                    ops.append(("insert", (k, th), lambda k=k, th=th: t.insert_steps(k, th)))
                elif r < 0.75:
                    ops.append(("remove", k, lambda k=k: t.remove_steps(k)))
                else:
                    ops.append(("lookup", k, lambda k=k: t.lookup_steps(k)))
            work.append(ops)
        history = interleave(work, [rng.randrange(3) for _ in range(rng.randrange(60))])
        final = t.items()  # also checks the shape
        history.append((9, "items", None, None, max(h[5] for h in history) + 1, 10 ** 9))

        def apply(state, name, arg):
            if name == "items":
                return state, None if dict(state) == final else "different"
            return map_apply(state, name, arg)

        assert linearizable(history, frozenset(init.items()), apply), seed


def test_threads():
    t = Ctrie(w=3, hbits=9, hash_fn=lambda k: k * 2654435761)
    def worker(w):
        for k in range(w, 2000, 4):
            t.insert(k, w)
        for k in range(w, 2000, 8):
            assert t.remove(k) == w

    ts = [threading.Thread(target=worker, args=(w,)) for w in range(4)]
    for th in ts:
        th.start()
    for th in ts:
        th.join()
    expect = {k: k % 4 for k in range(2000) if k % 8 >= 4}
    assert t.items() == expect
    assert all(t.lookup(k) == v for k, v in expect.items())
