# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/combining-tree/. The authors are listed in prov/9G1178.jsonl.

import random
import threading

from combining_tree import FIRST, IDLE, RESULT, SECOND, SPIN, CombiningTree, run

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


def make_ops(tree, tid, count):
    return [("inc", tid, lambda: tree.get_and_increment_steps(tid)) for _ in range(count)]


def drive(gen, k):
    """Advance a step generator by k steps."""
    for _ in range(k):
        next(gen)


def test_example() -> None:
    tree = CombiningTree(4)  # leaf 0 for threads 0 and 1, leaf 1 for 2 and 3
    leaf0, leaf1 = tree.leaves
    a = tree.get_and_increment_steps(0)
    b = tree.get_and_increment_steps(1)
    c = tree.get_and_increment_steps(2)
    drive(a, 2)  # precombine: leaf 0 becomes FIRST, the root stops A
    assert leaf0.status == FIRST
    drive(b, 1)  # precombine at leaf 0: SECOND and locked, B stops here
    assert leaf0.status == SECOND and leaf0.locked
    drive(c, 2)  # C is FIRST at leaf 1 and stops at the root
    drive(b, 1)  # op at leaf 0: B deposits 1 and unlocks
    assert leaf0.second == 1 and not leaf0.locked
    assert next(b) == SPIN  # B waits for RESULT
    drive(a, 1)  # combine at leaf 0: A carries 2
    drive(c, 1)  # combine at leaf 1: C carries 1
    assert run(c) == 0  # op at the root gives C the value 0, distribute frees leaf 1
    assert leaf1.status == IDLE and tree.value() == 1
    drive(a, 1)  # op at the root: prior 1, result 3
    assert tree.value() == 3
    assert next(b) == SPIN
    assert run(a) == 1  # distribute: leaf 0 gets RESULT 2
    assert leaf0.status == RESULT and leaf0.result == 2
    assert run(b) == 2
    tree.check_invariant()


def test_edges() -> None:
    tree = CombiningTree(2)  # the root is the only leaf
    assert [tree.get_and_increment(t) for t in (0, 1, 1, 0)] == [0, 1, 2, 3]
    tree.check_invariant()
    tree = CombiningTree(8)
    assert [tree.get_and_increment(7) for _ in range(5)] == [0, 1, 2, 3, 4]
    tree.check_invariant()
    for bad in (1, 3, 6):
        try:
            CombiningTree(bad)
        except ValueError:
            continue
        raise AssertionError("bad width accepted")


def test_waits() -> None:
    tree = CombiningTree(4)
    leaf0 = tree.leaves[0]
    a = tree.get_and_increment_steps(0)
    drive(a, 2)  # A is FIRST at leaf 0, stop is the root
    drive(a, 1)  # A combines at leaf 0 alone and locks it
    assert leaf0.locked and leaf0.status == FIRST
    b = tree.get_and_increment_steps(1)
    assert all(next(b) == SPIN for _ in range(5))  # B waits until A distributes
    assert run(a) == 0
    assert run(b) == 1
    tree.check_invariant()


def test_random_against_model() -> None:
    rng = random.Random(4711)
    for _ in range(500):
        width = rng.choice([2, 4, 8, 16])
        tree = CombiningTree(width)
        k = rng.randint(0, 40)
        got = [tree.get_and_increment(rng.randrange(width)) for _ in range(k)]
        assert got == list(range(k))
        tree.check_invariant()
        assert tree.value() == k


def test_random_interleavings_are_linearizable() -> None:
    rng = random.Random(90210)
    for _ in range(500):
        width = rng.choice([4, 8])
        tree = CombiningTree(width)
        start = rng.randint(0, 3)
        for _ in range(start):
            tree.get_and_increment(0)
        tids = rng.sample(range(width), 3)
        threads = [make_ops(tree, tid, rng.randint(1, 3)) for tid in tids]
        schedule = [rng.randrange(3) for _ in range(rng.randint(0, 120))]
        h = interleave(threads, schedule)
        results = sorted(r for _, _, _, r, _, _ in h)
        assert results == list(range(start, start + len(h)))
        assert linearizable(h, start, counter_spec)
        tree.check_invariant()


def test_threads() -> None:
    width, per = 8, 200
    tree = CombiningTree(width)
    got: list[list[int]] = [[] for _ in range(width)]

    def work(t: int) -> None:
        for _ in range(per):
            got[t].append(tree.get_and_increment(t))

    ts = [threading.Thread(target=work, args=(t,)) for t in range(width)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    assert sorted(x for g in got for x in g) == list(range(width * per))
    for g in got:
        assert g == sorted(g)  # one thread gets increasing values
    tree.check_invariant()
