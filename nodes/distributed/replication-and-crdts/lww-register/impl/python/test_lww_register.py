# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lww-register/. The authors are listed in prov/TFCFZR.jsonl.

import random

from lww_register import LWWRegister, join


def test_page_example() -> None:
    a, b, c = LWWRegister(0), LWWRegister(1), LWWRegister(2)
    a.write("red")  # (1, 0)
    b.merge(a.state())
    b.write("green")  # (2, 1), causally after red
    c.write("blue")  # (1, 2), concurrent with both
    a.merge(c.state())
    assert a.read() == "blue"  # (1, 2) > (1, 0)
    a.merge(b.state())
    c.merge(b.state())
    c.merge(a.state())
    b.merge(c.state())
    assert a.read() == b.read() == c.read() == "green"
    assert a.state() == ((2, 1), "green")


def test_same_counter_tie_broken_by_replica_id() -> None:
    a, b = LWWRegister(0), LWWRegister(1)
    a.write("x")
    b.write("y")
    a.merge(b.state())
    b.merge(a.state())
    assert a.read() == b.read() == "y"


def test_semilattice_laws() -> None:
    states = [((0, -1), None)] + [((c, r), f"v{c}{r}") for c in range(1, 3) for r in range(3)]
    for x in states:
        assert join(x, x) == x
        for y in states:
            assert join(x, y) == join(y, x)
            for z in states:
                assert join(join(x, y), z) == join(x, join(y, z))


def simulate(seed: int, n: int, steps: int, dup: float) -> None:
    rng = random.Random(seed)
    reps = [LWWRegister(i) for i in range(n)]
    writes: list[tuple[tuple[int, int], int]] = []
    hist: list[set[int]] = [set() for _ in range(n)]
    net: list[tuple[int, tuple, frozenset]] = []
    for step in range(steps):
        if not net or rng.random() < 0.4:
            i = rng.randrange(n)
            reps[i].write(step)
            writes.append((reps[i].stamp, step))
            # a new write is ordered after everything this replica has seen
            assert all(writes[o][0] < reps[i].stamp for o in hist[i])
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
            if hist[i]:
                assert reps[i].read() == max(writes[o] for o in hist[i])[1]
    for _ in range(2):
        for i in range(n):
            for j in range(n):
                reps[j].merge(reps[i].state())
    stamps = [w[0] for w in writes]
    assert len(set(stamps)) == len(stamps)  # stamps are unique
    for i in range(n):
        assert reps[i].state() == max(writes)


def test_seeded_runs() -> None:
    for seed in range(300):
        simulate(seed, 2 + seed % 4, 60, 0.3)
