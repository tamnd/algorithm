# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/flow-based-transcript-assembly/. The authors are listed in prov/9XQGWM.jsonl.

import random
from itertools import product

from flow_based_transcript_assembly import assemble, compatible, edmonds_karp, path_flow


def brute_min_cut(n, cap, s, t):
    best = float("inf")
    others = [v for v in range(n) if v not in (s, t)]
    for side in product([0, 1], repeat=len(others)):
        S = {s} | {v for v, b in zip(others, side) if b}
        best = min(best, sum(c for (u, v), c in cap.items() if u in S and v not in S))
    return best


def test_edmonds_karp_against_min_cut():
    rng = random.Random(1)
    for _ in range(500):
        n = rng.randint(2, 6)
        cap = {(u, v): rng.randint(0, 9) for u in range(n) for v in range(u + 1, n) if rng.random() < 0.6}
        value, flow = edmonds_karp(n, cap, 0, n - 1)
        assert value == brute_min_cut(n, cap, 0, n - 1)
        for e, c in cap.items():
            assert 0 <= flow[e] <= c
        for v in range(1, n - 1):
            inflow = sum(f for (a, b), f in flow.items() if b == v)
            outflow = sum(f for (a, b), f in flow.items() if a == v)
            assert inflow == outflow


def test_worked_example():
    # A = 0, B = 1, C = 2. Fragments AB 30, BC 30 and AC 10.
    edges = [(0, 1), (1, 2), (0, 2)]
    out = assemble(3, edges, {(0, 1): 30, (1, 2): 30, (0, 2): 10})
    assert out == [([0, 1, 2], 30), ([0, 2], 10)]
    value, g = path_flow((0, 1, 2), {(0, 1): 30, (1, 2): 30, (0, 2): 10})
    assert value == 30 and g == {(0, 1): 30, (1, 2): 30}


def test_two_isoforms_are_recovered():
    # T1 = 0 1 2 3 with 50 reads per junction and T2 = 0 2 3 with 20; the junction 2 3 is shared.
    edges = [(0, 1), (1, 2), (2, 3), (0, 2)]
    frags = {(0, 1): 50, (1, 2): 50, (2, 3): 70, (0, 2): 20}
    assert assemble(4, edges, frags) == [([0, 1, 2, 3], 50), ([0, 2, 3], 20)]


def test_unphased_junctions_give_false_transcripts():
    # T1 = 0 1 2 3 4 with 10 reads per junction and T2 = 0 2 4 with 20. Junction reads alone
    # do not link the choice before node 2 to the choice after it.
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 2), (2, 4)]
    frags = {(0, 1): 10, (1, 2): 10, (2, 3): 10, (3, 4): 10, (0, 2): 20, (2, 4): 20}
    assert assemble(5, edges, frags) == [([0, 2, 3, 4], 10), ([0, 1, 2, 4], 10), ([0, 2, 4], 10)]
    # One read that spans 1 2 3 links the two choices, and the true pair comes out.
    frags = {(0, 1): 10, (1, 2, 3): 10, (3, 4): 10, (0, 2): 20, (2, 4): 20}
    assert assemble(5, edges, frags) == [([0, 2, 4], 20), ([0, 1, 2, 3, 4], 10)]


def test_compatibility():
    assert compatible((0, 1), (0, 1, 2))
    assert compatible((1, 2, 3), (0, 1, 2))
    assert not compatible((0, 2), (0, 1, 2))
    assert not compatible((3, 4), (0, 1, 2))
    assert compatible((2, 5), (0, 1, 2))


def random_instance(rng):
    n = rng.randint(2, 7)
    edges = sorted({(u, u + 1) for u in range(n - 1)} |
                   {(u, v) for u in range(n) for v in range(u + 2, n) if rng.random() < 0.3})
    succ = {u: [v for a, v in edges if a == u] for u in range(n)}
    frags = {}
    for _ in range(rng.randint(1, 8)):
        f = [rng.randrange(n - 1)]
        for _ in range(rng.randint(1, 3)):
            if not succ[f[-1]]:
                break
            f.append(rng.choice(succ[f[-1]]))
        if len(f) >= 2:
            frags[tuple(f)] = frags.get(tuple(f), 0) + rng.randint(1, 40)
    return n, edges, frags


def test_random_graphs_terminate_with_valid_output():
    rng = random.Random(2)
    for _ in range(300):
        n, edges, frags = random_instance(rng)
        out = assemble(n, edges, frags, c_min=1)
        eset = set(edges)
        total = sum(frags.values())
        for p, a in out:
            assert len(p) >= 2 and all((u, v) in eset for u, v in zip(p, p[1:]))
            assert 1 <= a <= total
        assert len(out) <= sum(frags.values())


def test_single_isoform():
    rng = random.Random(3)
    for _ in range(100):
        n = rng.randint(3, 8)
        path = list(range(n))
        edges = [(u, u + 1) for u in range(n - 1)]
        frags = {}
        for _ in range(30):
            a = rng.randrange(n - 1)
            b = rng.randint(a + 1, min(n - 1, a + 3))
            frags[tuple(path[a:b + 1])] = frags.get(tuple(path[a:b + 1]), 0) + 1
        out = assemble(n, edges, frags)
        assert out
        # The first transcript is the whole path whenever the fragments chain from end to end.
        value, _ = path_flow(tuple(path), frags)
        if value >= 1:
            assert out[0] == (path, value)
