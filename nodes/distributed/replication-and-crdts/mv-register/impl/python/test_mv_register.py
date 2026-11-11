# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mv-register/. The authors are listed in prov/ZMJZQC.jsonl.

import itertools
import random

from mv_register import MVRegister, join, leq


def test_page_example() -> None:
    a, b, c = MVRegister(3, 0), MVRegister(3, 1), MVRegister(3, 2)
    a.write("milk")  # (1,0,0)
    b.merge(a.state())
    c.merge(a.state())
    b.write("eggs")  # (1,1,0)
    c.write("tea")  # (1,0,1)
    a.merge(b.state())
    a.merge(c.state())
    assert a.read() == {"eggs", "tea"}  # two siblings
    assert a.state() == {("eggs", (1, 1, 0)), ("tea", (1, 0, 1))}
    a.write("eggs, tea")  # (2,1,1) dominates both
    b.merge(a.state())
    c.merge(a.state())
    assert a.read() == b.read() == c.read() == {"eggs, tea"}
    assert a.state() == {("eggs, tea", (2, 1, 1))}


def test_semilattice_laws_on_reachable_states() -> None:
    # states built from a small pool of writes: antichains of vectors
    pool = [("p", (1, 0)), ("q", (0, 1)), ("r", (1, 1)), ("s", (2, 0)), ("t", (0, 2))]
    states = []
    for k in range(len(pool) + 1):
        for sub in itertools.combinations(pool, k):
            st = join(frozenset(), frozenset(sub))
            if st == frozenset(sub):
                states.append(st)
    for x in states:
        assert join(x, x) == x
        for y in states:
            assert join(x, y) == join(y, x)
            for z in states:
                assert join(join(x, y), z) == join(x, join(y, z))


def simulate(seed: int, n: int, steps: int, dup: float) -> None:
    rng = random.Random(seed)
    reps = [MVRegister(n, i) for i in range(n)]
    writes: list[tuple[int, tuple[int, ...]]] = []  # (value, vector)
    hist: list[set[int]] = [set() for _ in range(n)]
    net: list[tuple[int, frozenset, frozenset]] = []
    for step in range(steps):
        if not net or rng.random() < 0.4:
            i = rng.randrange(n)
            reps[i].write(step)
            (v,) = [w for _, w in reps[i].s]
            writes.append((step, v))
            hist[i].add(len(writes) - 1)
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
        for i in range(n):
            reps[i].check_invariant()
            seen = [writes[o] for o in hist[i]]
            # spec: the read returns the values of the writes that no other seen write follows
            want = {x for x, v in seen if not any(leq(v, w) and v != w for _, w in seen)}
            assert reps[i].read() == want
    for _ in range(2):
        for i in range(n):
            for j in range(n):
                reps[j].merge(reps[i].state())
    for i in range(n):
        assert reps[i].state() == reps[0].state()


def test_seeded_runs() -> None:
    for seed in range(300):
        simulate(seed, 2 + seed % 4, 50, 0.3)
