# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/combining-funnel/. The authors are listed in prov/3D757V.jsonl.

import random
import threading

from combining_funnel import SPIN, CombiningFunnel

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


def counter_apply(state, name, arg):
    """The sequential fetch-and-add counter."""
    return state + arg, state


def finish(gen):
    try:
        while True:
            next(gen)
    except StopIteration as stop:
        return stop.value


# ---- tests ----


def scripted(cells):
    """A chooser that gives each (thread, layer) the cell from the table."""
    return lambda me, d, w: cells[me, d]


def test_example():
    a, b, c, d = 0, 1, 2, 3
    cells = {(a, 0): 0, (b, 0): 0, (c, 0): 1, (d, 0): 1, (a, 1): 0, (b, 1): 0, (c, 1): 0, (d, 1): 0}
    f = CombiningFunnel([2, 1], 4, choose=scripted(cells), wait=0)
    gens = {t: f.fetch_and_add_steps(t, 1) for t in (a, b, c, d)}

    def until(t, cond):
        while not cond():
            assert next(gens[t]) != SPIN

    until(a, lambda: f.layers[0][0].read() == a)  # A swaps into layer 0, cell 0
    until(b, lambda: f.recs[b].sum == 2)  # B finds A there and captures it
    assert f.recs[a].loc.read() == "captured" and f.recs[b].kids == [(a, 1)]
    until(c, lambda: f.layers[0][1].read() == c)
    until(d, lambda: f.recs[d].sum == 2)  # D captures C
    until(b, lambda: f.recs[b].loc.read() == 1 and f.layers[1][0].read() == b)  # B moves on to layer 1
    until(d, lambda: f.recs[d].sum == 4)  # D meets B on layer 1 and captures it
    assert f.recs[b].loc.read() == "captured" and f.recs[d].kids == [(c, 1), (b, 2)]
    assert finish(gens[d]) == 0  # one fetch-and-add of 4 on the counter
    assert f.value() == 4
    assert finish(gens[c]) == 1
    assert finish(gens[b]) == 2  # B hands A its share
    assert finish(gens[a]) == 3


def test_no_layers_is_a_plain_counter():
    f = CombiningFunnel([], 1)
    assert [f.fetch_and_add(0, x) for x in (5, 1, 2)] == [0, 5, 6]
    assert f.value() == 8


def test_edges():
    f = CombiningFunnel([1, 1], 2, wait=0)
    assert f.fetch_and_add(0, 3) == 0  # alone: it finds itself or nothing, and applies its own sum
    assert f.fetch_and_add(0, 0) == 3
    assert f.fetch_and_add(1, -1) == 3  # it finds thread 0's stale id, but thread 0 is idle
    assert f.value() == 2


def test_random_sequential_against_model():
    rng = random.Random(1)
    f = CombiningFunnel([4, 2, 1], 3, seed=2)
    total = 0
    for _ in range(300):
        x = rng.randrange(-5, 10)
        assert f.fetch_and_add(rng.randrange(3), x) == total
        total += x
    assert f.value() == total


def random_run(seed, threads=3, ops=3):
    rng = random.Random(seed)
    f = CombiningFunnel([2, 1][: rng.randrange(3)], threads, seed=seed, wait=rng.randrange(3))
    work = [[("faa", x, lambda t=t, x=x: f.fetch_and_add_steps(t, x))
             for x in (rng.randrange(1, 6) for _ in range(rng.randrange(1, ops + 1)))]
            for t in range(threads)]
    schedule = [rng.randrange(threads) for _ in range(rng.randrange(0, 150))]
    history = interleave(work, schedule)
    return f, work, history


def test_random_interleavings_are_linearizable():
    combined = 0
    for seed in range(400):
        f, work, history = random_run(seed)
        assert len(history) == sum(len(w) for w in work)
        assert f.value() == sum(op[2] for op in history)
        assert linearizable(history, 0, counter_apply), seed
        combined += any(r.kids for r in f.recs)
    assert combined > 50  # many runs really combined operations


def test_threads():
    f = CombiningFunnel([4, 2, 1], 4, seed=3, wait=2)
    got = [[] for _ in range(4)]

    def worker(t):
        for _ in range(200):
            got[t].append(f.fetch_and_add(t, 1))

    ts = [threading.Thread(target=worker, args=(t,)) for t in range(4)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    assert f.value() == 800
    assert sorted(sum(got, [])) == list(range(800))
