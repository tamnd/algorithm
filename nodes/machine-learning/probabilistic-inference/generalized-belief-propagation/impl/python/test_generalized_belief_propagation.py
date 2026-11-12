# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-belief-propagation/. The authors are listed in prov/7XZC5Z.jsonl.

import math
import random

from generalized_belief_propagation import (RegionGraph, exact_marginals, gbp, grid_edges, ising_factors,
                                            kikuchi_free_energy, plaquettes, variable_marginals)

E33 = grid_edges(3, 3)


def seeded_grid(rng, j_scale=1.0):
    fields = [rng.uniform(-0.5, 0.5) for _ in range(9)]
    couplings = [(i, j, rng.uniform(-j_scale, j_scale)) for i, j in E33]
    return ising_factors(9, fields, couplings), fields, couplings


def max_err(a, b):
    return max(abs(x - y) for u, v in zip(a, b) for x, y in zip(u, v))


def loopy_bp_pairwise(n, fields, couplings, iters=3000):
    """An independent synchronous loopy BP on the Ising model, for comparison."""
    nb = [[] for _ in range(n)]
    w = {}
    for i, j, c in couplings:
        nb[i].append(j)
        nb[j].append(i)
        w[(i, j)] = w[(j, i)] = c
    phi = [[math.exp(-h), math.exp(h)] for h in fields]
    m = {(i, j): [0.5, 0.5] for i in range(n) for j in nb[i]}
    for _ in range(iters):
        new = {}
        for (i, j) in m:
            pre = list(phi[i])
            for k in nb[i]:
                if k != j:
                    pre = [p * x for p, x in zip(pre, m[(k, i)])]
            out = [sum(pre[a] * math.exp(w[(i, j)] * (2 * a - 1) * (2 * b - 1)) for a in range(2)) for b in range(2)]
            new[(i, j)] = [x / sum(out) for x in out]
        m = new
    out = []
    for i in range(n):
        b = list(phi[i])
        for k in nb[i]:
            b = [p * x for p, x in zip(b, m[(k, i)])]
        out.append([x / sum(b) for x in b])
    return out


def test_counting_numbers_of_the_plaquette_region_graph():
    card, factors = ising_factors(9, [0.0] * 9, [(i, j, 1.0) for i, j in E33])
    g = RegionGraph(card, factors, plaquettes(3, 3))
    counts = {g.vars[k]: g.counting[k] for k in range(len(g.regions))}
    assert counts == {(0, 1, 3, 4): 1, (1, 2, 4, 5): 1, (3, 4, 6, 7): 1, (4, 5, 7, 8): 1,
                      (1, 4): -1, (3, 4): -1, (4, 5): -1, (4, 7): -1, (4,): 1}
    assert len(g.edges) == 12
    # Every variable and every factor is counted once in total.
    for v in range(9):
        assert sum(c for r, c in zip(g.regions, g.counting) if v in r) == 1
    for scope, _ in factors:
        assert sum(c for r, c in zip(g.regions, g.counting) if set(scope) <= r) == 1


def test_exact_when_the_regions_form_a_junction_tree():
    rng = random.Random(5)
    for _ in range(3):
        (card, factors), _, _ = seeded_grid(rng)
        exact, log_z = exact_marginals(card, factors)
        g, beliefs, _, ok = gbp(card, factors, [set(range(6)), set(range(3, 9))], tol=1e-13)
        assert ok
        assert max_err(variable_marginals(g, beliefs), exact) < 1e-10
        assert abs(-kikuchi_free_energy(g, beliefs) - log_z) < 1e-9
    # A 2 x 3 grid as two squares that share the edge {1, 4}.
    card, factors = ising_factors(6, [0.3, -0.1, 0.2, 0.0, 0.4, -0.5],
                                  [(i, j, rng.uniform(-1, 1)) for i, j in grid_edges(2, 3)])
    exact, log_z = exact_marginals(card, factors)
    g, beliefs, _, ok = gbp(card, factors, plaquettes(2, 3), tol=1e-13)
    assert ok and max_err(variable_marginals(g, beliefs), exact) < 1e-10
    assert abs(-kikuchi_free_energy(g, beliefs) - log_z) < 1e-9


def test_edge_and_node_regions_give_loopy_bp():
    rng = random.Random(8)
    for _ in range(3):
        (card, factors), fields, couplings = seeded_grid(rng, 0.5)
        g, beliefs, _, ok = gbp(card, factors, [set(e) for e in E33], tol=1e-12)
        assert ok
        assert max_err(variable_marginals(g, beliefs), loopy_bp_pairwise(9, fields, couplings)) < 1e-8


def test_plaquettes_closer_than_loopy_bp_on_seeded_grids():
    # An observed result on these seeds, not a theorem.
    rng = random.Random(5)
    for _ in range(5):
        (card, factors), fields, couplings = seeded_grid(rng)
        exact, log_z = exact_marginals(card, factors)
        g, beliefs, _, ok = gbp(card, factors, plaquettes(3, 3))
        assert ok
        err_gbp = max_err(variable_marginals(g, beliefs), exact)
        err_bp = max_err(loopy_bp_pairwise(9, fields, couplings), exact)
        assert err_gbp < 2e-4 and err_bp > 5e-3 and err_gbp < err_bp / 10
        gb, bb, _, _ = gbp(card, factors, [set(e) for e in E33])
        assert abs(-kikuchi_free_energy(g, beliefs) - log_z) < abs(-kikuchi_free_energy(gb, bb) - log_z)


def test_beliefs_are_consistent_at_convergence():
    rng = random.Random(9)
    (card, factors), _, _ = seeded_grid(rng)
    g, beliefs, _, ok = gbp(card, factors, plaquettes(3, 3), tol=1e-12)
    assert ok
    for p, r in g.edges:
        marg = {}
        for x, prob in beliefs[p].items():
            y = g.restrict(p, r, x)
            marg[y] = marg.get(y, 0.0) + prob
        assert max(abs(marg[y] - beliefs[r][y]) for y in beliefs[r]) < 1e-9


def test_page_example():
    rng = random.Random(5)
    (card, factors), _, _ = seeded_grid(rng)
    exact, log_z = exact_marginals(card, factors)
    g, beliefs, sweeps, ok = gbp(card, factors, plaquettes(3, 3))
    assert ok and sweeps == 70
    assert abs(log_z - 8.50493) < 1e-5
    assert abs(-kikuchi_free_energy(g, beliefs) - 8.50494) < 1e-5
    assert max_err(variable_marginals(g, beliefs), exact) < 1e-5
