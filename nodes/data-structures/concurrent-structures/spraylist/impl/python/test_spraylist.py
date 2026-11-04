# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spraylist/. The authors are listed in prov/GA0P2G.jsonl.

import random
import threading
from collections import Counter

from spraylist import EMPTY, SprayList

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
    """A fake random source: scripted coin flips for node heights and scripted jumps."""

    def __init__(self, coins, jumps):
        self.coins, self.jumps = list(coins), list(jumps)

    def random(self):
        return self.coins.pop(0)

    def randint(self, a, b):
        return self.jumps.pop(0)


def heights(tops):
    coins = []
    for t in tops:
        coins += [0.0] * t + [0.9]
    return coins


def finish(gen):
    try:
        while True:
            next(gen)
    except StopIteration as stop:
        return stop.value


# ---- tests ----


def test_example():
    s = SprayList(threads=4)  # sprays start at level 2 and go down one level at a time
    s.rng = Script(heights([0, 1, 0, 2, 0, 1, 0, 0]), [1, 0, 1, 1, 0, 1, 0, 0, 0])
    for x in (10, 20, 30, 40, 50, 60, 70, 80):
        s.insert(x)
    # level 2: 40; level 1: 20, 40, 60; level 0: all
    assert s.delete_min() == 50  # level 2 jumps to 40, level 1 stays, level 0 moves to 50
    assert s.delete_min() == 60  # the same path lands on 50, which is gone; 60 is next
    assert s.delete_min() == 10  # no jumps: the spray lands on the first node
    s.check_invariant()
    assert s.items() == [20, 30, 40, 70, 80]


def test_spray_skips_a_claimed_node():
    s = SprayList(threads=4)
    s.rng = Script(heights([0, 0, 0]), [0, 0, 0, 0, 0, 0])
    for x in (1, 2, 3):
        s.insert(x)
    a, b = s.delete_min_steps(), s.delete_min_steps()
    for _ in range(4):
        next(a)  # a has claimed node 1 but not yet unlinked it
    assert s.head.next[0].ref().claimed.get()
    assert finish(b) == 2  # b lands on node 1, sees the claim, and takes 2
    assert finish(a) == 1
    s.check_invariant()


def test_edges():
    s = SprayList(threads=8, seed=1)
    assert s.delete_min() == EMPTY
    s.insert(5)
    assert s.delete_min() == 5  # the spray falls off the end; the scan finds it
    assert s.delete_min() == EMPTY
    exact = SprayList(threads=8, seed=2, jump=0)  # jump 0: an exact priority queue
    for x in (4, 2, 8, 6, 2):
        exact.insert(x)
    assert [exact.delete_min() for _ in range(6)] == [2, 2, 4, 6, 8, EMPTY]
    s.check_invariant()
    exact.check_invariant()


def test_random_against_model():
    for seed in range(30):
        rng = random.Random(seed)
        s = SprayList(threads=rng.choice([1, 2, 4, 8, 16]), seed=seed)
        model = Counter()
        for _ in range(500):
            if rng.random() < 0.55:
                x = rng.randrange(100)
                s.insert(x)
                model[x] += 1
            else:
                x = s.delete_min()
                if x == EMPTY:
                    assert not +model
                else:
                    assert model[x] > 0
                    model[x] -= 1
        s.check_invariant()
        assert s.items() == sorted(model.elements())


def test_rank_quality():
    # the spray stays within the first O(p log^3 p) items or so
    s = SprayList(threads=4, seed=3)
    for x in random.Random(4).sample(range(100000), 3000):
        s.insert(x)
    ranks = []
    for i in range(1000):
        items = s.items()
        x = s.delete_min()
        ranks.append(1 + sum(y < x for y in items))
        s.insert(100000 + i)
    assert 1 < sum(ranks) / len(ranks) < 4 * 2**3 * 2
    assert max(ranks) <= (2**3 + 1) * 3 * 4


def test_random_interleavings_are_linearizable():
    for seed in range(400):
        rng = random.Random(seed)
        s = SprayList(threads=rng.choice([1, 2, 4]), seed=seed, jump=rng.choice([0, 1, 3]))
        init = []
        for _ in range(rng.randrange(0, 4)):
            x = rng.randrange(10)
            s.insert(x)
            init.append(x)
        threads = []
        for _ in range(3):
            ops = []
            for _ in range(rng.randrange(1, 4)):
                if rng.random() < 0.5:
                    x = rng.randrange(10)
                    ops.append(("insert", x, lambda x=x: s.insert_steps(x)))
                else:
                    ops.append(("delete_min", None, s.delete_min_steps))
            threads.append(ops)
        schedule = [rng.randrange(3) for _ in range(rng.randrange(10, 150))]
        history = interleave(threads, schedule)
        s.check_invariant()
        assert linearizable(history, tuple(sorted(init)), relaxed_step), (seed, history)


def test_threads():
    s = SprayList(threads=4, seed=5)
    out = [[] for _ in range(4)]

    def worker(w):
        for i in range(300):
            s.insert(w * 1000 + i)
            if i % 2:
                out[w].append(s.delete_min())

    ts = [threading.Thread(target=worker, args=(w,)) for w in range(4)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    s.check_invariant()
    taken = [x for o in out for x in o]
    assert EMPTY not in taken
    assert sorted(taken + s.items()) == sorted(w * 1000 + i for w in range(4) for i in range(300))
