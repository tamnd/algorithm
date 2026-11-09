# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimum-cut-count-bound/. The authors are listed in prov/7P1NFC.jsonl.

import random
from fractions import Fraction
from math import comb

from minimum_cut_count_bound import (
    all_cuts,
    all_simple_graphs,
    contract,
    contraction_distribution,
    cut_size,
    cycle,
    is_connected,
    minimum_cuts,
)


def is_cycle(n: int, edges) -> bool:
    deg = [0] * n
    for u, v in edges:
        deg[u] += 1
        deg[v] += 1
    return len(edges) == n and all(d == 2 for d in deg) and is_connected(n, edges)


def test_all_simple_graphs_up_to_five_vertices() -> None:
    for n in range(2, 6):
        best = 0
        reaching = []
        for edges in all_simple_graphs(n):
            if not is_connected(n, edges):
                continue
            _, cuts = minimum_cuts(n, edges)
            assert len(cuts) <= comb(n, 2)
            if len(cuts) > best:
                best, reaching = len(cuts), [edges]
            elif len(cuts) == best:
                reaching.append(edges)
        assert best == comb(n, 2)
        if n >= 3:
            # Only the labeled cycles reach the bound: 1, 3, 12 of them.
            assert all(is_cycle(n, e) for e in reaching)
            assert len(reaching) == {3: 1, 4: 3, 5: 12}[n]


def test_cycles_reach_the_bound() -> None:
    for n in range(3, 11):
        lam, cuts = minimum_cuts(n, cycle(n))
        assert lam == 2 and len(cuts) == comb(n, 2)


def test_contraction_probability_bound_exact() -> None:
    # Each minimum cut is output with probability at least 2/(n(n-1)).
    for n in range(2, 6):
        for edges in all_simple_graphs(n):
            if not is_connected(n, edges):
                continue
            dist = contraction_distribution(n, edges)
            assert sum(dist.values()) == 1
            _, cuts = minimum_cuts(n, edges)
            for c in cuts:
                assert dist.get(c, Fraction(0)) >= Fraction(2, n * (n - 1))


def test_contraction_on_multigraphs() -> None:
    rng = random.Random(8)
    for _ in range(60):
        n = rng.randint(3, 6)
        edges = [(i, i + 1) for i in range(n - 1)]  # a path keeps the graph connected
        for _ in range(rng.randint(0, 8)):
            u, v = rng.sample(range(n), 2)
            edges.append((u, v))
        dist = contraction_distribution(n, edges)
        _, cuts = minimum_cuts(n, edges)
        assert len(cuts) <= comb(n, 2)
        for c in cuts:
            assert dist[c] >= Fraction(2, n * (n - 1))


def test_cycle_output_is_uniform_over_minimum_cuts() -> None:
    for n in range(3, 7):
        dist = contraction_distribution(n, cycle(n))
        assert len(dist) == comb(n, 2)
        assert all(p == Fraction(2, n * (n - 1)) for p in dist.values())


def test_random_contraction_frequencies() -> None:
    rng = random.Random(1)
    n = 5
    edges = cycle(n)
    counts: dict = {}
    trials = 20000
    for _ in range(trials):
        c = contract(n, edges, rng)
        assert cut_size(edges, c) == 2
        counts[c] = counts.get(c, 0) + 1
    assert len(counts) == 10
    assert all(abs(k / trials - 0.1) < 0.015 for k in counts.values())


def test_disconnected_graphs_break_the_bound() -> None:
    # Six isolated vertices: every one of the 31 cuts has size 0.
    lam, cuts = minimum_cuts(6, [])
    assert lam == 0 and len(cuts) == 2**5 - 1 > comb(6, 2)


def test_minimum_st_cuts_can_be_exponential() -> None:
    # s = 0 and t = 1 joined by n - 2 paths of length 2: 2^(n-2) minimum s-t cuts.
    n = 7
    edges = [e for m in range(2, n) for e in ((0, m), (m, 1))]
    st_cuts = [s for s in all_cuts(n) if 1 not in s]
    lam = min(cut_size(edges, s) for s in st_cuts)
    count = sum(1 for s in st_cuts if cut_size(edges, s) == lam)
    assert lam == n - 2 and count == 2 ** (n - 2) > comb(n, 2)
