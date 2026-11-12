# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/markov-random-field/. The authors are listed in prov/KQP2ZG.jsonl.

import random
from fractions import Fraction as F
from itertools import combinations, product

from markov_random_field import (
    MarkovRandomField,
    edge_support_closure_violations,
    global_markov,
    hammersley_clifford_potentials,
    is_ci,
    is_clique,
    local_markov,
    pairwise_markov,
)


def grid_edges(rows: int, cols: int):
    idx = lambda r, c: r * cols + c
    edges = []
    for r in range(rows):
        for c in range(cols):
            if c + 1 < cols:
                edges.append((idx(r, c), idx(r, c + 1)))
            if r + 1 < rows:
                edges.append((idx(r, c), idx(r + 1, c)))
    return edges


def random_grid_mrf(rng: random.Random, rows: int = 2, cols: int = 3) -> MarkovRandomField:
    pots = []
    for e in grid_edges(rows, cols):
        pots.append((e, {xy: F(rng.randint(1, 9)) for xy in product((0, 1), repeat=2)}))
    for i in range(rows * cols):
        pots.append(((i,), {(0,): F(1), (1,): F(rng.randint(1, 5))}))
    return MarkovRandomField([2] * (rows * cols), pots)


def test_chain_example_numbers() -> None:
    agree = {(0, 0): F(3), (0, 1): F(1), (1, 0): F(1), (1, 1): F(3)}
    m = MarkovRandomField([2, 2, 2], [((0, 1), agree), ((1, 2), agree)])
    assert m.partition_function() == 32
    p = m.joint()
    assert p[(0, 0, 0)] + p[(1, 0, 1)] + p[(0, 1, 0)] + p[(1, 1, 1)] == F(5, 8)  # P(A = C)
    assert is_ci(p, [0], [2], [1]) and not is_ci(p, [0], [2], [])


def test_grid_has_pairwise_local_and_global_markov_properties() -> None:
    rng = random.Random(1974)
    for _ in range(3):
        m = random_grid_mrf(rng)
        p = m.joint()
        assert sum(p.values()) == 1
        assert pairwise_markov(p, m.adj)
        assert local_markov(p, m.adj)
    assert global_markov(p, m.adj)


def test_hammersley_clifford_inversion_gives_clique_potentials() -> None:
    rng = random.Random(1971)
    m = random_grid_mrf(rng, 2, 2)
    p = m.joint()
    phis = hammersley_clifford_potentials(p, 4)
    for x in p:
        prod = F(1)
        for A, phi in phis.items():
            v = phi(x)
            if not is_clique(m.adj, sorted(A)):
                assert v == 1  # only cliques carry a nontrivial potential
            prod *= v
        assert prod == p[x]


def moussouris():
    support = [(0, 0, 0, 0), (1, 0, 0, 0), (1, 1, 0, 0), (1, 1, 1, 0),
               (0, 0, 0, 1), (0, 0, 1, 1), (0, 1, 1, 1), (1, 1, 1, 1)]
    return {x: (F(1, 8) if x in support else F(0)) for x in product((0, 1), repeat=4)}


def test_moussouris_counterexample() -> None:
    p = moussouris()
    cycle = {0: {1, 3}, 1: {0, 2}, 2: {1, 3}, 3: {0, 2}}
    # Markov with respect to the 4-cycle, in the global (hence local and pairwise) sense
    assert global_markov(p, cycle) and local_markov(p, cycle) and pairwise_markov(p, cycle)
    # but no product of edge potentials gives it: (0,1,0,1) would have to be positive
    bad = edge_support_closure_violations(p, [(0, 1), (1, 2), (2, 3), (3, 0)])
    assert (0, 1, 0, 1) in bad and (1, 0, 1, 0) in bad
    # the Mobius construction needs positivity: p(0,1,0,0) = 0
    assert p[(0, 1, 0, 0)] == 0


def test_positive_pairwise_markov_implies_factorization_on_random_cycle() -> None:
    rng = random.Random(3)
    edges = [(0, 1), (1, 2), (2, 3), (3, 0)]
    m = MarkovRandomField([2] * 4, [(e, {xy: F(rng.randint(1, 9)) for xy in product((0, 1), repeat=2)}) for e in edges])
    p = m.joint()
    phis = hammersley_clifford_potentials(p, 4)
    for A, phi in phis.items():
        if len(A) >= 3 or (len(A) == 2 and tuple(sorted(A)) not in {tuple(sorted(e)) for e in edges}):
            assert all(phi(x) == 1 for x in p)
