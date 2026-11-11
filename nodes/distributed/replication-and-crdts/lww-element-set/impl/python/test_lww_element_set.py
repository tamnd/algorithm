# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lww-element-set/. The authors are listed in prov/3D6HMS.jsonl.

import itertools
import random

from lww_element_set import LWWElementSet


def test_page_example() -> None:
    a, b = LWWElementSet(), LWWElementSet()
    a.add("x", 1)
    b.merge(a.state())
    b.remove("x", 3)
    a.add("x", 2)
    a.merge(b.state())
    b.merge(a.state())
    assert not a.lookup("x") and not b.lookup("x")  # 3 > 2, the remove is later
    a.add("x", 4)
    b.merge(a.state())
    assert b.lookup("x")  # unlike a 2P-Set, an element can come back


def test_bias_on_equal_timestamps() -> None:
    for bias, expect in (("add", True), ("remove", False)):
        a, b = LWWElementSet(bias), LWWElementSet(bias)
        a.add("x", 5)
        b.remove("x", 5)
        a.merge(b.state())
        b.merge(a.state())
        assert a.lookup("x") == b.lookup("x") == expect


def test_clock_skew_loses_a_later_add() -> None:
    # Replica b runs 10 units behind. Its add happens after a's remove in real
    # time, but it carries the smaller timestamp, so the merged set drops it.
    a, b = LWWElementSet(), LWWElementSet()
    a.add("x", 100)
    b.merge(a.state())
    a.remove("x", 105)  # real time 105
    b.add("x", 98)  # real time 108, b's clock reads 98
    a.merge(b.state())
    b.merge(a.state())
    assert not a.lookup("x") and not b.lookup("x")


def test_semilattice_laws() -> None:
    ts = [None, 0, 1]
    states = []
    for a, r in itertools.product(ts, ts):
        s = LWWElementSet()
        if a is not None:
            s.add("x", a)
        if r is not None:
            s.remove("x", r)
        states.append(s.state())

    def join(x, y):
        s = LWWElementSet()
        s.merge(x)
        s.merge(y)
        return s.state()

    for x in states:
        assert join(x, x) == x
        for y in states:
            assert join(x, y) == join(y, x)
            for z in states:
                assert join(join(x, y), z) == join(x, join(y, z))


def simulate(seed: int, n: int, steps: int, dup: float, bias: str) -> None:
    rng = random.Random(seed)
    reps = [LWWElementSet(bias) for _ in range(n)]
    clock = 0
    ops: list[tuple[str, str, int]] = []  # (kind, element, ts)
    hist: list[set[int]] = [set() for _ in range(n)]
    net: list[tuple[int, object, frozenset]] = []
    for _ in range(steps):
        if not net or rng.random() < 0.45:
            i = rng.randrange(n)
            e = rng.choice("abcd")
            clock += rng.choice((0, 1))  # equal stamps happen on purpose
            kind = "add" if rng.random() < 0.6 else "rem"
            (reps[i].add if kind == "add" else reps[i].remove)(e, clock)
            ops.append((kind, e, clock))
            hist[i].add(len(ops) - 1)
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
            assert reps[i].elements() == oracle([ops[o] for o in hist[i]], bias)
    for _ in range(2):
        for i in range(n):
            for j in range(n):
                reps[j].merge(reps[i].state())
    for i in range(n):
        assert reps[i].state() == reps[0].state()
    assert reps[0].elements() == oracle(ops, bias)


def oracle(ops: list[tuple[str, str, int]], bias: str) -> frozenset:
    out = set()
    for e in {o[1] for o in ops}:
        adds = [t for k, x, t in ops if x == e and k == "add"]
        rems = [t for k, x, t in ops if x == e and k == "rem"]
        if not adds:
            continue
        a, r = max(adds), max(rems, default=-1)
        if a > r or (a == r and bias == "add"):
            out.add(e)
    return frozenset(out)


def test_seeded_runs() -> None:
    for seed in range(300):
        simulate(seed, 2 + seed % 4, 50, 0.3, "add" if seed % 2 else "remove")
