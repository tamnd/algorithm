# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/g-counter/. The authors are listed in prov/MQEY7J.jsonl.

import random

from g_counter import GCounter, MaxIntCounter, OpGCounter, SumMergeCounter


def test_page_example() -> None:
    a, b, c = GCounter(3, 0), GCounter(3, 1), GCounter(3, 2)
    a.increment()
    a.increment()
    b.increment()
    c.increment()
    assert (a.state(), b.state(), c.state()) == ([2, 0, 0], [0, 1, 0], [0, 0, 1])
    b.merge(a.state())
    assert b.state() == [2, 1, 0] and b.value() == 3
    c.merge(b.state())
    assert c.state() == [2, 1, 1] and c.value() == 4
    old = b.state()  # a stale copy of b that arrives late
    a.merge(c.state())
    a.merge(c.state())  # a duplicate changes nothing
    a.merge(old)  # an old state changes nothing
    assert a.state() == [2, 1, 1] and a.value() == 4
    b.merge(c.state())
    assert a.value() == b.value() == c.value() == 4
    assert GCounter(3, 0).compare(a) and not a.compare([2, 1, 0])


def test_not_crdts() -> None:
    # A single integer merged with max loses one of two concurrent increments.
    x, y = MaxIntCounter(), MaxIntCounter()
    x.increment()
    y.increment()
    x.merge(y.value())
    y.merge(x.value())
    assert x.value() == y.value() == 1  # two increments were made
    # Merging by addition counts a duplicate twice.
    s, t = SumMergeCounter(), SumMergeCounter()
    t.increment()
    s.merge(t.value())
    s.merge(t.value())
    assert s.value() == 2  # one increment was made at t, none at s


def test_op_based_needs_exactly_once() -> None:
    rng = random.Random(9)
    for _ in range(50):
        reps = [OpGCounter() for _ in range(3)]
        msgs: list[tuple[int, str]] = []
        for _ in range(rng.randint(1, 8)):
            src = rng.randrange(3)
            msgs.append((src, reps[src].increment()))
        for dst in range(3):
            mine = [m for s, m in msgs if s != dst]
            rng.shuffle(mine)
            for m in mine:
                reps[dst].deliver(m)
        assert len({r.value() for r in reps}) == 1 and reps[0].value() == len(msgs)
    # one duplicated message makes the replicas differ
    a, b = OpGCounter(), OpGCounter()
    m = a.increment()
    b.deliver(m)
    b.deliver(m)
    assert (a.value(), b.value()) == (1, 2)


def run_random(rng: random.Random) -> None:
    n = rng.randint(1, 5)
    reps = [GCounter(n, i) for i in range(n)]
    known: list[set[tuple[int, int]]] = [set() for _ in range(n)]  # model: ids (j, k) known at i
    issued = [0] * n
    net: list[tuple[int, list[int], frozenset]] = []  # (destination, state, model of the sender)
    last_value = [0] * n
    for _ in range(rng.randint(0, 40)):
        act = rng.random()
        i = rng.randrange(n)
        if act < 0.35:
            reps[i].increment()
            issued[i] += 1
            known[i].add((i, issued[i]))
        elif act < 0.7:
            dst = rng.randrange(n)
            net.append((dst, reps[i].state(), frozenset(known[i])))
        elif net:
            k = rng.randrange(len(net))  # any message, so delivery is reordered
            dst, st, kn = net[k]
            r = rng.random()
            if r < 0.2:
                net.pop(k)  # lost
                continue
            if r > 0.6:
                net.pop(k)  # delivered once more is possible only if kept
            reps[dst].merge(st)
            known[dst] |= kn
        for j in range(n):
            reps[j].check_invariant([sum(1 for (a, _) in known[j] if a == q) for q in range(n)])
            assert reps[j].value() >= last_value[j]
            assert reps[j].value() <= sum(issued)
            last_value[j] = reps[j].value()
    # anti-entropy: every replica sends its state to every other one, twice
    for _ in range(2):
        for i in range(n):
            for j in range(n):
                reps[j].merge(reps[i].state())
    assert all(r.state() == issued for r in reps)
    assert all(r.value() == sum(issued) for r in reps)


def test_random_runs_with_loss_duplication_and_reordering() -> None:
    rng = random.Random(20111010)
    for _ in range(600):
        run_random(rng)


def test_merge_is_order_independent() -> None:
    rng = random.Random(3)
    for _ in range(500):
        n = rng.randint(1, 4)
        states = [[rng.randint(0, 5) for _ in range(n)] for _ in range(rng.randint(1, 5))]
        seq = states + rng.choices(states, k=rng.randint(0, 3))
        rng.shuffle(seq)
        c = GCounter(n, 0)
        for s in seq:
            c.merge(s)
        assert c.state() == [max(s[j] for s in states) for j in range(n)]
