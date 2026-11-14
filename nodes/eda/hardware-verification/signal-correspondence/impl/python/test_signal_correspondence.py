# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/signal-correspondence/. The authors are listed in prov/EMBMJW.jsonl.

import itertools
import random

from netlist import Netlist, initial_state, mutate, next_state, product, random_netlist, rewrite, simulate
from signal_correspondence import ONE, ZERO, signal_correspondence, simulation_classes

# The page example: a one-hot ring of three latches; the output h0 AND h1 is always 0.
RING = Netlist(
    (),
    (("o", "AND", ("h0", "h1")),),
    ("o",),
    (("h0", "h2", 1), ("h1", "h0", 0), ("h2", "h1", 0)),
)
ZERO_CIRCUIT = Netlist((), (("z", "CONST0", ()),), ("z",))
# The same ring with the other two pairwise ANDs as extra gates.
RING3 = Netlist(
    (),
    (("o", "AND", ("h0", "h1")), ("u", "AND", ("h1", "h2")), ("w", "AND", ("h0", "h2"))),
    ("o",),
    RING.latches,
)


def explicit_equivalent(p: Netlist, pairs) -> bool:
    """Oracle: explicit-state reachability of the product machine; every output pair agrees in every reachable state."""
    names = [n for n, _, _ in p.latches]
    start = tuple(initial_state(p, 1)[n] for n in names)
    seen = {start}
    todo = [start]
    while todo:
        st = todo.pop()
        for xs in itertools.product((0, 1), repeat=len(p.inputs)):
            val = simulate(p, {**dict(zip(p.inputs, xs)), **dict(zip(names, st))}, 1)
            if any(val[o] != val[o2] for o, o2 in pairs):
                return False
            nxt = next_state(p, val)
            t = tuple(nxt[n] for n in names)
            if t not in seen:
                seen.add(t)
                todo.append(t)
    return True


def explicit_gfp(p: Netlist, classes):
    """Oracle: the greatest inductive refinement of classes, by enumeration of all (s, x0, x1) at once."""
    names = [n for n, _, _ in p.latches]
    nl, ni = len(names), len(p.inputs)
    npts = 1 << (nl + 2 * ni)
    mask = (1 << npts) - 1

    def bit_word(b: int) -> int:
        return sum(1 << i for i in range(npts) if (i >> b) & 1)

    s = {n: bit_word(j) for j, n in enumerate(names)}
    x0 = {x: bit_word(nl + i) for i, x in enumerate(p.inputs)}
    x1 = {x: bit_word(nl + ni + i) for i, x in enumerate(p.inputs)}
    v0 = simulate(p, {**s, **x0}, mask)
    v1 = simulate(p, {**next_state(p, v0), **x1}, mask)
    vb = simulate(p, {**initial_state(p, mask), **x0}, mask)
    for v in (v0, v1, vb):
        v[ZERO], v[ONE] = 0, mask

    def refine(cls, key):
        out = []
        for k in cls:
            parts = {}
            for n in k:
                parts.setdefault(key(n), []).append(n)
            out.extend(parts.values())
        return out

    cls = refine(classes, lambda n: vb[n])
    while True:
        q = mask
        for k in cls:
            for n in k[1:]:
                q &= ~(v0[n] ^ v0[k[0]])
        new = refine(cls, lambda n: v1[n] & q)
        if len(new) == len(cls):
            return cls
        cls = new


def as_sets(classes):
    return {frozenset(k) for k in classes}


def test_page_example_is_a_miss():
    p, pairs = product(RING, ZERO_CIRCUIT)
    init = simulation_classes(p)
    assert ["a.o", "b.z"] == [n for k in init if ZERO in k for n in k if n != ZERO]
    res = signal_correspondence(p, pairs)
    assert not res.proved
    assert res.splits == 1
    assert explicit_equivalent(p, pairs)
    assert as_sets(res.classes) == as_sets(explicit_gfp(p, init))


def test_extra_signals_make_the_page_example_provable():
    p, pairs = product(RING3, ZERO_CIRCUIT)
    res = signal_correspondence(p, pairs)
    assert res.proved and res.splits == 0
    assert explicit_equivalent(p, pairs)


def test_a_real_difference_is_never_proved():
    # The ring against a circuit whose output is h0 (not always 0).
    other = Netlist((), (("o", "BUF", ("h0",)),), ("o",), RING.latches)
    p, pairs = product(RING, other)
    assert not explicit_equivalent(p, pairs)
    assert not signal_correspondence(p, pairs).proved


def test_given_classes_and_trivial_classes():
    p, pairs = product(RING, RING)
    res = signal_correspondence(p, pairs)
    assert res.proved
    alone = [[n] for k in simulation_classes(p) for n in k]
    res2 = signal_correspondence(p, pairs, classes=alone)
    assert not res2.proved and res2.splits == 0


def test_random_sound_and_greatest_fixed_point():
    rng = random.Random(4242)
    proved_rewrites = 0
    for case in range(500):
        a = random_netlist(rng, rng.randint(0, 2), rng.randint(1, 2), rng.randint(2, 6), rng.randint(1, 2))
        b = rewrite(a, rng)
        kind = case % 3
        if kind == 1:
            b = mutate(b, rng)
        p, pairs = product(a, b)
        init = simulation_classes(p, cycles=rng.randint(1, 6), width=rng.choice([1, 8, 32]), seed=case)
        res = signal_correspondence(p, pairs, classes=init)
        if res.proved:
            assert explicit_equivalent(p, pairs)
        assert as_sets(res.classes) == as_sets(explicit_gfp(p, init))
        if kind != 1:
            # A pure rewrite keeps every signal of a, so the correspondence by name is inductive.
            full = signal_correspondence(p, pairs, cycles=8, width=64, seed=case)
            assert full.proved
            proved_rewrites += 1
    assert proved_rewrites > 300
