# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/equivalence-checking/. The authors are listed in prov/N16FPV.jsonl.

import random

from equivalence_checking import (
    bisim_naive,
    bisim_partition,
    same_blocks,
    simulation_naive,
    simulators,
    stutter_naive,
    stutter_partition,
    trace_equivalent,
    traces,
)

# Two vending machines. P (state 0): coin, then a choice of tea or coffee.
# Q (state 4): coin, then a machine that already chose tea or coffee.
VENDING = [
    (0, "coin", 1), (1, "tea", 2), (1, "coffee", 3),
    (4, "coin", 5), (4, "coin", 6), (5, "tea", 7), (6, "coffee", 8),
]


def test_vending_machines():
    n = 9
    assert trace_equivalent(n, VENDING, 0, 4) is None
    block = bisim_partition(n, VENDING)
    assert block[0] != block[4]
    sim = simulators(n, VENDING)
    assert 0 in sim[4] and 4 not in sim[0]
    assert traces(n, VENDING, 0, 2) == {(), ("coin",), ("coin", "tea"), ("coin", "coffee")}


def test_trace_witness():
    trans = [(0, "a", 1), (1, "b", 2), (3, "a", 4)]
    assert trace_equivalent(5, trans, 0, 3) == ("a", "b")


def rand_lts(rng, acts="ab"):
    n = rng.randint(1, 7)
    trans = sorted({(rng.randrange(n), rng.choice(acts), rng.randrange(n)) for _ in range(rng.randint(0, 2 * n))})
    labels = [rng.randrange(2) for _ in range(n)] if rng.random() < 0.5 else None
    return n, trans, labels


def test_bisimulation_against_gfp():
    rng = random.Random(1987)
    for _ in range(300):
        n, trans, labels = rand_lts(rng)
        assert same_blocks(bisim_partition(n, trans, labels)) == bisim_naive(n, trans, labels)


def test_simulation_against_gfp():
    rng = random.Random(1995)
    for _ in range(300):
        n, trans, labels = rand_lts(rng)
        sim = simulators(n, trans, labels)
        assert {(v, u) for v in range(n) for u in sim[v]} == simulation_naive(n, trans, labels)


def test_order_of_equivalences():
    """Bisimilar implies similar both ways, which implies trace equivalent."""
    rng = random.Random(1990)
    for _ in range(300):
        n, trans, labels = rand_lts(rng)
        bis = bisim_naive(n, trans, None)
        sim = simulation_naive(n, trans, None)
        for s in range(n):
            for t in range(n):
                both = (s, t) in sim and (t, s) in sim
                if (s, t) in bis:
                    assert both
                if both:
                    assert trace_equivalent(n, trans, s, t) is None


def test_trace_equivalence_against_enumeration():
    rng = random.Random(1992)
    for _ in range(300):
        n, trans, _ = rand_lts(rng)
        s, t = rng.randrange(n), rng.randrange(n)
        # Compare all traces up to length 9 by direct enumeration.
        same = traces(n, trans, s, 9) == traces(n, trans, t, 9)
        w = trace_equivalent(n, trans, s, t)
        if w is None:
            assert same
        else:
            assert (w in traces(n, trans, s, len(w))) != (w in traces(n, trans, t, len(w)))
            if len(w) <= 9:
                assert not same


def test_stuttering_against_gfp():
    rng = random.Random(1990)
    for _ in range(300):
        n = rng.randint(1, 7)
        succ = [sorted(set(rng.randrange(n) for _ in range(rng.randint(1, 2)))) for _ in range(n)]
        labels = [rng.randrange(2) for _ in range(n)]
        part = same_blocks(stutter_partition(n, succ, labels))
        assert part == stutter_naive(n, succ, labels)
        trans = [(s, "t", t) for s in range(n) for t in succ[s]]
        assert same_blocks(bisim_partition(n, trans, labels)) <= part
