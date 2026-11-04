# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/disruptor-ring-buffer/. The authors are listed in prov/1JS632.jsonl.

import random
import threading

from disruptor_ring_buffer import SPIN, Disruptor, run

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


def ring_spec(size, deps):
    """The sequential broadcast ring: state = (published entries, position of each consumer).

    deps[i] lists the consumers that consumer i waits for.
    """

    def step(state, name, arg, result):
        pub, pos = state
        if name == "pub":
            if pos and len(pub) - min(pos) >= size:
                return None  # full: the call could not have taken effect here
            return (pub + (arg,), pos) if result == len(pub) else None
        i = arg[0]
        limit = min([len(pub)] + [pos[d] for d in deps[i]])
        got = tuple(result)
        if name == "consume":
            end = pos[i] + len(got)
            ok = len(got) >= 1 and end <= limit and got == pub[pos[i] : end]
        else:  # consume up to arg[1] items in all: empty once they are done
            end = pos[i] + len(got)
            if pos[i] >= arg[1]:
                ok = got == ()
            else:
                ok = len(got) >= 1 and end <= limit and got == pub[pos[i] : end]
        if not ok:
            return None
        return pub, pos[:i] + (end,) + pos[i + 1 :]

    return step


def consume_upto(r, c, k):
    """A total consume for the tests: the next batch, or [] once k entries are done."""
    if c.seq.get() >= k - 1:
        return []
    return (yield from r.consume_steps(c))


def test_example() -> None:
    r: Disruptor[int] = Disruptor(4)
    a = r.add_consumer("A")
    b = r.add_consumer("B", [a])  # B handles an entry after A
    assert [r.publish(x) for x in (10, 11)] == [0, 1]
    assert r.consume(a) == [10, 11]
    assert [r.publish(x) for x in (12, 13)] == [2, 3]
    p = r.publish_steps(14)
    next(p)  # claims sequence 4, which reuses slot 0
    assert all(next(p) == SPIN for _ in range(5))  # B has not finished entry 0
    assert r.consume(b) == [10, 11]  # B may not pass A, which is at 1
    assert run(p) == 4
    assert r.entries == [14, 11, 12, 13]
    assert r.consume(a) == [12, 13, 14]
    assert r.consume(b) == [12, 13, 14]
    r.check_invariant()


def test_edges() -> None:
    r: Disruptor[str] = Disruptor(1)
    c = r.add_consumer("C")
    for x in "abc":
        r.publish(x)
        assert r.consume(c) == [x]
    g = r.consume_steps(c)
    assert all(next(g) == SPIN for _ in range(3))  # nothing to read: the consumer waits
    r.publish("d")
    assert run(g) == ["d"]
    lone: Disruptor[int] = Disruptor(2)  # no consumer: nothing gates the producer
    assert [lone.publish(i) for i in range(5)] == [0, 1, 2, 3, 4]
    for bad in (0, 3, 6):
        try:
            Disruptor(bad)
        except ValueError:
            continue
        raise AssertionError("bad size accepted")


def test_publish_in_order() -> None:
    r: Disruptor[int] = Disruptor(4)
    c = r.add_consumer("C")
    p1 = r.publish_steps(1)
    p2 = r.publish_steps(2)
    next(p1)  # claims 0
    next(p2)  # claims 1
    for _ in range(3):
        next(p2)  # p2 has written slot 1 and waits for the cursor to reach 0
    assert next(p2) == SPIN and r.cursor.get() == -1
    g = r.consume_steps(c)
    assert next(g) == SPIN  # entry 1 is written but not published
    assert run(p1) == 0
    assert run(p2) == 1
    assert run(g) == [1, 2]


def test_random_against_model() -> None:
    rng = random.Random(4711)
    for _ in range(500):
        size = rng.choice([1, 2, 4, 8])
        r: Disruptor[int] = Disruptor(size)
        a = r.add_consumer("A")
        b = r.add_consumer("B", [a])
        pub: list[int] = []
        pa = pb = 0
        for _ in range(rng.randint(0, 50)):
            op = rng.random()
            if op < 0.5 and len(pub) - min(pa, pb) < size:
                x = rng.randint(0, 99)
                assert r.publish(x) == len(pub)
                pub.append(x)
            elif op < 0.75 and pa < len(pub):
                assert r.consume(a) == pub[pa:]
                pa = len(pub)
            elif pb < pa:
                assert r.consume(b) == pub[pb:pa]
                pb = pa
            r.check_invariant()


def test_random_interleavings_are_linearizable() -> None:
    rng = random.Random(90210)
    for _ in range(500):
        size = rng.choice([1, 2, 4])
        r: Disruptor[int] = Disruptor(size)
        a = r.add_consumer("A")
        b = r.add_consumer("B", [a] if rng.random() < 0.5 else [])
        deps = [[], [0] if b.deps else []]
        k = rng.randint(1, 5)
        producers = rng.choice([1, 2])
        items = list(range(100, 100 + k))
        threads = [[] for _ in range(producers)]
        for i, x in enumerate(items):
            threads[i % producers].append(("pub", x, lambda x=x: r.publish_steps(x)))
        for ci, c in enumerate((a, b)):
            threads.append([("upto", (ci, k), lambda c=c: consume_upto(r, c, k)) for _ in range(k)])
        n = len(threads)
        schedule = [rng.randrange(n) for _ in range(rng.randint(0, 80))]
        h = interleave(threads, schedule)
        assert linearizable(h, ((), (0, 0)), ring_spec(size, deps))
        r.check_invariant()


def test_threads() -> None:
    r: Disruptor[int] = Disruptor(8)
    a = r.add_consumer("A")
    b = r.add_consumer("B", [a])
    total = 3000
    seen: dict[str, list[int]] = {"A": [], "B": []}
    behind: list[bool] = []

    def produce() -> None:
        for i in range(total):
            r.publish(i)

    def consume(c, name: str) -> None:
        while len(seen[name]) < total:
            batch = r.consume(c)
            if name == "B":
                behind.append(a.seq.get() >= len(seen["B"]) + len(batch) - 1)
            seen[name] += batch

    ts = [threading.Thread(target=produce), threading.Thread(target=consume, args=(a, "A")), threading.Thread(target=consume, args=(b, "B"))]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    assert seen["A"] == list(range(total)) == seen["B"]
    assert all(behind)  # B never handled an entry before A had finished it
    r.check_invariant()
