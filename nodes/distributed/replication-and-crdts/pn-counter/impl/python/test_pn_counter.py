# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pn-counter/. The authors are listed in prov/KN5BQ5.jsonl.

import itertools
import random

from pn_counter import BrokenSignedCounter, PNCounter, join


def test_page_example() -> None:
    a, b, c = PNCounter(3, 0), PNCounter(3, 1), PNCounter(3, 2)
    a.increment()
    a.increment()
    b.increment()
    b.decrement()
    c.decrement()
    assert (a.value(), b.value(), c.value()) == (2, 0, -1)
    b.merge(a.state())
    assert b.state() == ([2, 1, 0], [0, 1, 0]) and b.value() == 2
    c.merge(b.state())
    assert c.state() == ([2, 1, 0], [0, 1, 1]) and c.value() == 1
    old = a.state()
    a.merge(c.state())
    a.merge(c.state())
    a.merge(old)
    b.merge(c.state())
    assert a.value() == b.value() == c.value() == 1
    assert a.compare(b) and b.compare(a)


def test_broken_signed_vector() -> None:
    # A decrement that lowers the own entry is undone by a merge with an older copy.
    a, b = BrokenSignedCounter(2, 0), BrokenSignedCounter(2, 1)
    a.increment()
    b.merge(a.state())  # b holds [1, 0]
    a.decrement()  # a holds [0, 0], value 0
    a.merge(b.state())  # max brings back [1, 0]
    assert a.value() == 1  # one increment and one decrement were made
    p = PNCounter(2, 0)
    q = PNCounter(2, 1)
    p.increment()
    q.merge(p.state())
    p.decrement()
    p.merge(q.state())
    assert p.value() == 0


def states(n: int, top: int):
    vals = list(itertools.product(range(top), repeat=n))
    for pv in vals:
        for nv in vals:
            yield (list(pv), list(nv))


def test_semilattice_laws() -> None:
    all_states = list(states(2, 2))  # 16 states
    for x in all_states:
        assert join(x, x) == x
        for y in all_states:
            assert join(x, y) == join(y, x)
            for z in all_states:
                assert join(join(x, y), z) == join(x, join(y, z))


def test_operations_inflate() -> None:
    rng = random.Random(7)
    for _ in range(200):
        c = PNCounter(3, rng.randrange(3))
        for _ in range(rng.randrange(6)):
            before = c.state()
            (c.increment if rng.random() < 0.5 else c.decrement)()
            assert PNCounter(3, 0).compare(c)
            # the old state is below the new one
            assert join(before, c.state()) == c.state()


def simulate(seed: int, n: int, steps: int, dup: float) -> None:
    rng = random.Random(seed)
    reps = [PNCounter(n, i) for i in range(n)]
    origin: list[tuple[int, int]] = []  # op id -> (replica, +1 or -1)
    hist: list[set[int]] = [set() for _ in range(n)]
    net: list[tuple[int, tuple[list[int], list[int]], frozenset[int]]] = []

    def check(i: int) -> None:
        incs = [0] * n
        decs = [0] * n
        for o in hist[i]:
            r, s = origin[o]
            if s > 0:
                incs[r] += 1
            else:
                decs[r] += 1
        reps[i].check_invariant(incs, decs)
        assert reps[i].value() == sum(origin[o][1] for o in hist[i])

    for _ in range(steps):
        if not net or rng.random() < 0.4:
            i = rng.randrange(n)
            s = 1 if rng.random() < 0.55 else -1
            (reps[i].increment if s > 0 else reps[i].decrement)()
            origin.append((i, s))
            hist[i].add(len(origin) - 1)
            for j in range(n):
                if j != i and rng.random() < 0.5:
                    net.append((j, reps[i].state(), frozenset(hist[i])))
        else:
            k = rng.randrange(len(net))
            dest, st, h = net[k]
            if rng.random() >= dup:
                net.pop(k)
            reps[dest].merge(st)
            hist[dest] |= h
            check(dest)
    for i in range(n):
        for j in range(n):
            reps[j].merge(reps[i].state())
            hist[j] |= hist[i]
    for _ in range(2):
        for i in range(n):
            for j in range(n):
                reps[j].merge(reps[i].state())
                hist[j] |= hist[i]
    total = sum(s for _, s in origin)
    for i in range(n):
        check(i)
        assert reps[i].value() == total
        assert reps[i].state() == reps[0].state()


def test_seeded_runs() -> None:
    for seed in range(300):
        simulate(seed, 2 + seed % 4, 60, 0.3)
