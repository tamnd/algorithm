# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/diffracting-tree/. The authors are listed in prov/8G5PTB.jsonl.

import random
import threading

from diffracting_tree import EMPTY, TIMEOUT, WAITING, Atomic, DiffractingTree, exchange_steps, run

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


def counter_spec(n, name, arg):
    return n + 1, n


def quiescently_consistent(history, start):
    """For a counter: at each quiescent point the finished calls hold exactly start .. start + m - 1."""
    values = [r for _, _, _, r, _, _ in history]
    if len(set(values)) != len(values):
        return False
    times = sorted({h[5] for h in history} | {h[4] for h in history})
    for t in times:
        if any(h[4] < t < h[5] for h in history):
            continue  # some call is pending at t
        done = sorted(h[3] for h in history if h[5] <= t)
        if done != list(range(start, start + len(done))):
            return False
    return True


def make_ops(tree, me, count):
    return [("inc", me, lambda: tree.get_and_increment_steps(me)) for _ in range(count)]


def test_example() -> None:
    # Width 2, one balancer. B passes the toggle and stalls; A then calls twice.
    tree = DiffractingTree(2, prism_size=1, patience=1)
    b = tree.get_and_increment_steps(1)
    while tree.balancers[0].toggle.get() == 0:
        next(b)  # B times out in the prism and takes side 0 of the toggle
    a1 = tree.get_and_increment(0)
    a2 = tree.get_and_increment(0)
    vb = run(b)
    assert (a1, a2, vb) == (1, 0, 2)  # A got 1 and then 0: not linearizable
    h = [(0, "inc", 0, 1, 10, 20), (0, "inc", 0, 0, 30, 40), (1, "inc", 1, 2, 0, 50)]
    assert not linearizable(h, 0, counter_spec)
    assert quiescently_consistent(h, 0)
    tree.check_step_property()


def test_diffraction() -> None:
    tree = DiffractingTree(2, prism_size=1, patience=4)
    a = tree.get_and_increment_steps(5)
    b = tree.get_and_increment_steps(9)
    next(a)  # A reads the slot: EMPTY
    next(a)  # A installs itself: WAITING
    assert tree.balancers[0].prism[0].get() == (5, WAITING)
    next(b)  # B reads the slot
    next(b)  # B swaps in: BUSY, B leaves with partner 5 on side 1
    assert run(b) == 1  # side 1, wire 1, first value of the wire
    assert run(a) == 0  # A sees BUSY, takes 9, leaves on side 0
    assert tree.balancers[0].toggle.get() == 0  # the toggle was not touched
    assert tree.balancers[0].diffracted == 1
    tree.check_step_property()


def test_exchanger_alone_times_out() -> None:
    slot = Atomic((None, EMPTY))
    assert run(exchange_steps(slot, 3, 2)) is TIMEOUT
    assert slot.get() == (None, EMPTY)


def test_edges() -> None:
    tree = DiffractingTree(2)
    assert [tree.get_and_increment(0) for _ in range(5)] == [0, 1, 2, 3, 4]
    for bad in (1, 3, 12):
        try:
            DiffractingTree(bad)
        except ValueError:
            continue
        raise AssertionError("bad width accepted")


def test_random_against_model() -> None:
    rng = random.Random(4711)
    for _ in range(500):
        width = rng.choice([2, 4, 8, 16])
        tree = DiffractingTree(width, prism_size=rng.randint(1, 4), patience=1, seed=rng.randrange(99))
        k = rng.randint(0, 40)
        assert [tree.get_and_increment(rng.randrange(8)) for _ in range(k)] == list(range(k))
        tree.check_step_property()


def test_random_interleavings_are_quiescently_consistent() -> None:
    rng = random.Random(90210)
    not_linearizable = 0
    for _ in range(500):
        width = rng.choice([2, 4, 8])
        tree = DiffractingTree(width, prism_size=rng.randint(1, 3), patience=rng.randint(1, 3), seed=rng.randrange(99))
        start = rng.randint(0, 3)
        for _ in range(start):
            tree.get_and_increment(0)
        threads = [make_ops(tree, t, rng.randint(1, 3)) for t in range(3)]
        schedule = [rng.randrange(3) for _ in range(rng.randint(0, 80))]
        h = interleave(threads, schedule)
        assert quiescently_consistent(h, start)
        if not linearizable(h, start, counter_spec):
            not_linearizable += 1
        tree.check_step_property()
    assert not_linearizable > 0  # the counter is really weaker than linearizable


def test_threads() -> None:
    width, per, n = 8, 200, 6
    tree = DiffractingTree(width, prism_size=4, patience=8, seed=7)
    got: list[list[int]] = [[] for _ in range(n)]

    def work(t: int) -> None:
        for _ in range(per):
            got[t].append(tree.get_and_increment(t))

    ts = [threading.Thread(target=work, args=(t,)) for t in range(n)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    assert sorted(x for g in got for x in g) == list(range(n * per))
    tree.check_step_property()
