# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sloppy-counter/. The authors are listed in prov/Y5EVC6.jsonl.

import random
import threading

from sloppy_counter import SPIN, SloppyCounter, run

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


def counter_spec(bound):
    """The relaxed counter: inc adds 1, exact is the count, approx is within bound below it."""

    def step(n, name, arg, result):
        if name == "inc":
            return n + 1
        if name == "exact":
            return n if result == n else None
        return n if n - bound <= result <= n else None

    return step


def make_ops(c, plan):
    ops = []
    for name, arg in plan:
        if name == "inc":
            ops.append((name, arg, lambda a=arg: c.increment_steps(a)))
        elif name == "approx":
            ops.append((name, None, c.approximate_steps))
        else:
            ops.append((name, None, c.exact_steps))
    return ops


def test_example() -> None:
    c = SloppyCounter(cores=2, threshold=3)
    for core in (0, 1, 0, 1):
        c.increment(core)
    assert c.local == [2, 2] and c.global_count == 0
    assert c.approximate() == 0  # the error is 4 = cores * (threshold - 1)
    g = c.increment_steps(0)
    next(g)  # L1, L2: local[0] = 3
    next(g)  # L3 to L5: global is 3, the global lock is held
    assert c.global_count == 3 and c.local == [3, 2]
    a = c.approximate_steps()
    assert next(a) == SPIN  # approximate waits for the global lock
    next(g)  # L6, L7: local[0] = 0, lock 0 still held
    assert c.local == [0, 2]
    assert run(a) == 3  # the true count is 5
    e = c.exact_steps()
    assert next(e) == SPIN  # lock 0 is held by the increment
    assert run(g) is None
    assert run(e) == 5
    assert c.approximate() == 3
    c.check_invariant()


def test_edges() -> None:
    c = SloppyCounter(cores=1, threshold=1)  # threshold 1: an exact counter
    for k in range(1, 6):
        c.increment(0)
        assert c.approximate() == k == c.exact()
    c = SloppyCounter(cores=3, threshold=4)
    assert c.approximate() == 0 == c.exact()
    c.increment(7)  # core 7 maps to stripe 1
    assert c.local == [0, 1, 0]
    try:
        SloppyCounter(cores=0, threshold=2)
    except ValueError:
        pass
    else:
        raise AssertionError("cores = 0 must be rejected")


def test_locks() -> None:
    c = SloppyCounter(cores=2, threshold=5)
    g = c.increment_steps(0)
    next(g)  # holds lock 0
    c.increment(1)  # another core does not wait
    h = c.increment_steps(2)  # the same stripe waits
    assert all(next(h) == SPIN for _ in range(5))
    assert c.approximate() == 0  # the global lock is free
    run(g)
    run(h)
    assert c.exact() == 3
    c.check_invariant()


def test_random_against_model() -> None:
    rng = random.Random(4711)
    for _ in range(500):
        cores, s = rng.randint(1, 4), rng.randint(1, 5)
        c = SloppyCounter(cores, s)
        n = 0
        last = 0
        for _ in range(rng.randint(0, 60)):
            c.increment(rng.randrange(cores))
            n += 1
            a = c.approximate()
            assert n - c.max_error() <= a <= n
            assert a >= last  # the global count never decreases
            last = a
            assert c.global_count + sum(c.local) == n
            c.check_invariant()
        assert c.exact() == n


def test_random_interleavings_are_linearizable() -> None:
    rng = random.Random(90210)
    names = ["inc", "inc", "inc", "approx", "exact"]
    for _ in range(500):
        cores, s = rng.randint(1, 3), rng.randint(1, 3)
        c = SloppyCounter(cores, s)
        start = rng.randint(0, 6)
        for k in range(start):
            c.increment(k)
        threads = []
        for t in range(3):
            plan = [(rng.choice(names), t) for _ in range(rng.randint(1, 4))]
            threads.append(make_ops(c, plan))
        schedule = [rng.randrange(3) for _ in range(rng.randint(0, 60))]
        h = interleave(threads, schedule)
        assert linearizable(h, start, counter_spec(c.max_error()))
        c.check_invariant()


def test_threads() -> None:
    c = SloppyCounter(cores=4, threshold=16)
    per = 2000
    seen: list[int] = []

    def work(core: int) -> None:
        for _ in range(per):
            c.increment(core)
        seen.append(c.approximate())

    ts = [threading.Thread(target=work, args=(i,)) for i in range(4)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    assert c.exact() == 4 * per
    assert 4 * per - c.max_error() <= c.approximate() <= 4 * per
    assert all(0 <= v <= 4 * per for v in seen)
    c.check_invariant()
