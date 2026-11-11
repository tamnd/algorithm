# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/g-set/. The authors are listed in prov/PZZKRZ.jsonl.

import itertools
import random

from g_set import GSet


def test_page_example() -> None:
    a, b, c = GSet(), GSet(), GSet()
    a.add("x")
    b.add("y")
    b.add("x")
    c.add("z")
    b.merge(a.state())
    assert b.elements() == {"x", "y"}
    c.merge(b.state())
    old = a.state()
    a.merge(c.state())
    a.merge(c.state())
    a.merge(old)
    b.merge(c.state())
    assert a.elements() == b.elements() == c.elements() == {"x", "y", "z"}
    assert a.compare(b) and GSet().compare(a) and not a.compare({"x"})
    assert a.lookup("z") and not a.lookup("w")


def test_semilattice_laws() -> None:
    universe = ["a", "b", "c"]
    subsets = [frozenset(s) for k in range(4) for s in itertools.combinations(universe, k)]
    for x in subsets:
        assert x | x == x
        for y in subsets:
            assert x | y == y | x
            g = GSet()
            g.merge(x)
            g.merge(y)
            assert g.state() == x | y
            assert g.compare(x | y) and GSet().compare(g)
            for z in subsets:
                assert (x | y) | z == x | (y | z)


def simulate(seed: int, n: int, steps: int, dup: float) -> None:
    rng = random.Random(seed)
    reps = [GSet() for _ in range(n)]
    hist: list[set[str]] = [set() for _ in range(n)]  # elements added in the causal history
    net: list[tuple[int, frozenset, frozenset]] = []
    added: set[str] = set()
    for _ in range(steps):
        if not net or rng.random() < 0.4:
            i = rng.randrange(n)
            e = rng.choice("abcdefgh")
            reps[i].add(e)
            hist[i].add(e)
            added.add(e)
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
            reps[dest].check_invariant(hist[dest])
    for _ in range(2):
        for i in range(n):
            for j in range(n):
                reps[j].merge(reps[i].state())
    for i in range(n):
        assert reps[i].elements() == added


def test_seeded_runs() -> None:
    for seed in range(400):
        simulate(seed, 2 + seed % 4, 50, 0.3)
