# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/or-set/. The authors are listed in prov/DDH0TH.jsonl.

import random

from or_set import OptORSet, ORSet


def test_page_example_op_based() -> None:
    a, b = ORSet(0), ORSet(1)
    op1 = a.prepare_add("x")  # tag (0, 1)
    a.effect(op1)
    b.effect(op1)
    op2 = b.prepare_remove("x")  # b observed only (0, 1)
    b.effect(op2)
    op3 = a.prepare_add("x")  # tag (0, 2), concurrent with the remove
    a.effect(op3)
    a.effect(op2)
    b.effect(op3)
    assert a.s == b.s == {("x", (0, 2))}
    assert a.lookup("x") and b.lookup("x")  # the concurrent add wins
    op4 = a.prepare_remove("x")
    a.effect(op4)
    b.effect(op4)
    a.effect(a.prepare_add("x"))  # unlike a 2P-Set, x can come back
    assert a.lookup("x") and not b.lookup("x")


def test_page_example_optimized() -> None:
    a, b = OptORSet(2, 0), OptORSet(2, 1)
    a.add("x")
    b.merge(a.state())
    b.remove("x")
    a.add("x")
    assert a.state() == (frozenset({("x", 2, 0)}), (2, 0))
    assert b.state() == (frozenset(), (1, 0))
    a.merge(b.state())
    b.merge(a.state())
    assert a.state() == b.state() == (frozenset({("x", 2, 0)}), (2, 0))
    b.remove("x")
    a.merge(b.state())
    assert a.state() == (frozenset(), (2, 0))  # (x,2,0) covered by b's vector, so removed


def spec(ops: list[tuple[str, str, frozenset[int]]], hist: set[int]) -> frozenset:
    """Add-wins: x is present when some add(x) in the history has no remove(x) after it."""
    out = set()
    for a in hist:
        kind, x, _ = ops[a]
        if kind != "add":
            continue
        if not any(ops[r][0] == "rem" and ops[r][1] == x and a in ops[r][2] for r in hist):
            out.add(x)
    return frozenset(out)


def run_op_based(seed: int, n: int, steps: int, dup: float) -> None:
    rng = random.Random(seed)
    reps = [ORSet(i) for i in range(n)]
    ops: list[tuple[str, str, frozenset[int]]] = []  # kind, element, causal past
    payload: list[tuple] = []
    hist: list[set[int]] = [set() for _ in range(n)]
    net: list[tuple[int, int]] = []  # (destination, op id)
    for _ in range(steps):
        ready = [k for k, (d, o) in enumerate(net) if ops[o][2] <= hist[d]]
        if not ready or rng.random() < 0.4:
            i = rng.randrange(n)
            x = rng.choice("abc")
            if reps[i].lookup(x) and rng.random() < 0.5:
                op = reps[i].prepare_remove(x)
            else:
                op = reps[i].prepare_add(x)
            ops.append((op[0], x, frozenset(hist[i])))
            payload.append(op)
            o = len(ops) - 1
            reps[i].effect(op)
            hist[i].add(o)
            net.extend((j, o) for j in range(n) if j != i)
        else:
            k = rng.choice(ready)
            d, o = net[k]
            if rng.random() >= dup:
                net.pop(k)
            if o not in hist[d]:  # drop duplicates by op id
                reps[d].effect(payload[o])
                hist[d].add(o)
        for i in range(n):
            reps[i].check_invariant()
            assert reps[i].elements() == spec(ops, hist[i])
    while net:
        k = next(k for k, (d, o) in enumerate(net) if ops[o][2] <= hist[d])
        d, o = net.pop(k)
        if o not in hist[d]:
            reps[d].effect(payload[o])
            hist[d].add(o)
    for i in range(n):
        assert reps[i].s == reps[0].s
        assert reps[i].elements() == spec(ops, set(range(len(ops))))


def run_state_based(seed: int, n: int, steps: int, dup: float, keep: list | None = None) -> None:
    rng = random.Random(seed)
    reps = [OptORSet(n, i) for i in range(n)]
    ops: list[tuple[str, str, frozenset[int]]] = []
    hist: list[set[int]] = [set() for _ in range(n)]
    net: list[tuple[int, tuple, frozenset[int]]] = []
    for _ in range(steps):
        if not net or rng.random() < 0.45:
            i = rng.randrange(n)
            x = rng.choice("abc")
            kind = "rem" if reps[i].lookup(x) and rng.random() < 0.5 else "add"
            (reps[i].remove if kind == "rem" else reps[i].add)(x)
            ops.append((kind, x, frozenset(hist[i])))
            hist[i].add(len(ops) - 1)
            for j in range(n):
                if j != i and rng.random() < 0.5:
                    net.append((j, reps[i].state(), frozenset(hist[i])))
        else:
            k = rng.randrange(len(net))
            d, st, h = net[k]
            if rng.random() >= dup:
                net.pop(k)
            reps[d].merge(st)  # states can be stale, repeated or out of order
            hist[d] |= h
        for i in range(n):
            reps[i].check_invariant()
            assert reps[i].elements() == spec(ops, hist[i])
            if keep is not None:
                keep.append(reps[i].state())
    for _ in range(2):
        for i in range(n):
            for j in range(n):
                reps[j].merge(reps[i].state())
    for i in range(n):
        assert reps[i].state() == reps[0].state()
        assert reps[i].elements() == spec(ops, set(range(len(ops))))


def test_op_based_seeded_runs() -> None:
    for seed in range(200):
        run_op_based(seed, 2 + seed % 4, 50, 0.3)


def test_optimized_seeded_runs() -> None:
    for seed in range(200):
        run_state_based(seed, 2 + seed % 4, 50, 0.3)


def test_optimized_semilattice_laws() -> None:
    seen: list = []
    run_state_based(11, 3, 40, 0.2, seen)
    states = list(dict.fromkeys(seen))[:24]

    def join(x, y):
        r = OptORSet(3, 0)
        r.e, r.v = set(x[0]), list(x[1])
        r.merge(y)
        return r.state()

    for x in states:
        assert join(x, x) == x
        for y in states:
            assert join(x, y) == join(y, x)
            for z in states:
                assert join(join(x, y), z) == join(x, join(y, z))
