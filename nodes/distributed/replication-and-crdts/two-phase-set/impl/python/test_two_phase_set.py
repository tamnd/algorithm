# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-phase-set/. The authors are listed in prov/0YDBGZ.jsonl.

import itertools
import random

import pytest

from two_phase_set import TwoPhaseSet


def test_page_example() -> None:
    a, b = TwoPhaseSet(), TwoPhaseSet()
    a.add("x")
    a.add("y")
    b.merge(a.state())
    b.remove("x")  # b saw x, so the precondition holds
    a.add("z")
    a.merge(b.state())
    assert a.elements() == {"y", "z"}
    a.add("x")  # re-add after the remove has no effect
    assert not a.lookup("x")
    b.merge(a.state())
    assert a.state() == b.state() and b.elements() == {"y", "z"}


def test_remove_precondition() -> None:
    s = TwoPhaseSet()
    with pytest.raises(ValueError):
        s.remove("q")  # never added here
    s.add("q")
    s.remove("q")
    with pytest.raises(ValueError):
        s.remove("q")  # already removed


def test_concurrent_add_and_remove_remove_wins() -> None:
    a, b = TwoPhaseSet(), TwoPhaseSet()
    a.add("x")
    b.merge(a.state())
    a.add("x")  # a concurrent add of the same element
    b.remove("x")
    a.merge(b.state())
    b.merge(a.state())
    assert not a.lookup("x") and not b.lookup("x")


def test_semilattice_laws() -> None:
    universe = ["a", "b"]
    subsets = [frozenset(s) for k in range(3) for s in itertools.combinations(universe, k)]
    states = [(x, y) for x in subsets for y in subsets if y <= x]  # reachable: R within A

    def join(s, t):
        return (s[0] | t[0], s[1] | t[1])

    for x in states:
        assert join(x, x) == x
        for y in states:
            assert join(x, y) == join(y, x)
            assert join(x, y)[1] <= join(x, y)[0]
            for z in states:
                assert join(join(x, y), z) == join(x, join(y, z))


def simulate(seed: int, n: int, steps: int, dup: float) -> None:
    rng = random.Random(seed)
    reps = [TwoPhaseSet() for _ in range(n)]
    adds: list[set[str]] = [set() for _ in range(n)]  # elements added in the causal history
    rems: list[set[str]] = [set() for _ in range(n)]
    net: list[tuple[int, tuple, frozenset, frozenset]] = []
    for _ in range(steps):
        if not net or rng.random() < 0.45:
            i = rng.randrange(n)
            e = rng.choice("abcde")
            if reps[i].lookup(e) and rng.random() < 0.5:
                reps[i].remove(e)
                rems[i].add(e)
            else:
                reps[i].add(e)
                adds[i].add(e)
            for j in range(n):
                if j != i and rng.random() < 0.5:
                    net.append((j, reps[i].state(), frozenset(adds[i]), frozenset(rems[i])))
        else:
            k = rng.randrange(len(net))
            dest, st, ha, hr = net[k]
            if rng.random() >= dup:
                net.pop(k)
            reps[dest].merge(st)
            adds[dest] |= ha
            rems[dest] |= hr
        for i in range(n):
            reps[i].check_invariant()
            # sequential specification of the 2P-Set: added and never removed
            assert reps[i].elements() == adds[i] - rems[i]
    for _ in range(2):
        for i in range(n):
            for j in range(n):
                reps[j].merge(reps[i].state())
    for i in range(n):
        assert reps[i].state() == reps[0].state()
    allr = set().union(*rems)
    for e in allr:  # no re-add: a removed element stays out
        reps[0].add(e)
        assert not reps[0].lookup(e)


def test_seeded_runs() -> None:
    for seed in range(400):
        simulate(seed, 2 + seed % 4, 50, 0.3)
