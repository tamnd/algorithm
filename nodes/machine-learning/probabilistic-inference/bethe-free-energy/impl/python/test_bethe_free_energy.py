# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bethe-free-energy/. The authors are listed in prov/QK8KM6.jsonl.

import itertools
import math
import random

from bethe_free_energy import (bethe_free_energy, exact_beliefs, gibbs_free_energy, in_local_polytope,
                               ising_factors, symmetric_ising_beliefs)


def random_tree_model(rng):
    card = [rng.randint(2, 3) for _ in range(6)]
    scopes = [(0, 1), (1, 2, 3), (3, 4), (2, 5), (0,), (4,)]
    factors = [(s, {x: rng.uniform(0.1, 3.0) for x in itertools.product(*[range(card[j]) for j in s])})
               for s in scopes]
    return card, factors


def marginals_of(card, factors, q):
    var_b = [[0.0] * c for c in card]
    fac_b = [{x: 0.0 for x in table} for _, table in factors]
    for x, prob in q.items():
        for i, xi in enumerate(x):
            var_b[i][xi] += prob
        for a, (scope, _) in enumerate(factors):
            fac_b[a][tuple(x[j] for j in scope)] += prob
    return var_b, fac_b


def test_tree_exact_marginals_give_minus_log_z():
    rng = random.Random(1)
    for _ in range(10):
        card, factors = random_tree_model(rng)
        vb, fb, log_z = exact_beliefs(card, factors)
        assert in_local_polytope(card, factors, vb, fb)
        assert abs(bethe_free_energy(card, factors, vb, fb) + log_z) < 1e-10


def test_page_tree_example():
    card, factors = ising_factors(3, [0.5, 0.0, -0.3], [(0, 1, 1.0), (1, 2, -0.5)])
    vb, fb, log_z = exact_beliefs(card, factors)
    assert abs(log_z - 2.8441) < 1e-4
    assert abs(bethe_free_energy(card, factors, vb, fb) + log_z) < 1e-12


def test_tree_bethe_is_at_least_minus_log_z():
    # On a tree the local polytope is the marginal polytope, and F_Bethe(b) is the
    # Gibbs free energy of the tree distribution built from b, so F >= -log Z.
    rng = random.Random(2)
    for _ in range(10):
        card, factors = random_tree_model(rng)
        _, _, log_z = exact_beliefs(card, factors)
        states = list(itertools.product(*[range(c) for c in card]))
        weights = [rng.random() ** 3 for _ in states]
        total = sum(weights)
        q = {x: w / total for x, w in zip(states, weights)}
        vb, fb = marginals_of(card, factors, q)
        f = bethe_free_energy(card, factors, vb, fb)
        assert f >= -log_z - 1e-12
        # The tree projection of q has a Gibbs free energy equal to F_Bethe.
        d = [0] * len(card)
        for scope, _ in factors:
            for i in scope:
                d[i] += 1
        tree_q = {}
        for x in states:
            v = 1.0
            for a, (scope, _) in enumerate(factors):
                v *= fb[a][tuple(x[j] for j in scope)]
            for i, xi in enumerate(x):
                v /= vb[i][xi] ** (d[i] - 1)
            tree_q[x] = v
        assert abs(sum(tree_q.values()) - 1) < 1e-10
        assert abs(gibbs_free_energy(card, factors, tree_q) - f) < 1e-9


def test_not_exact_on_a_loop():
    card, factors = ising_factors(4, [0.3, -0.2, 0.1, 0.0], [(0, 1, 0.5), (1, 3, 0.5), (3, 2, 0.5), (2, 0, 0.5)])
    vb, fb, log_z = exact_beliefs(card, factors)
    f = bethe_free_energy(card, factors, vb, fb)
    assert abs(f - (-3.2901)) < 1e-4 and abs(log_z - 3.3433) < 1e-4


def test_pseudomarginal_below_minus_log_z_on_a_frustrated_triangle():
    # b_ij puts mass 1/2 on each disagreeing pair: in the local polytope, but no
    # distribution on three spins has these pair marginals.
    card, factors = ising_factors(3, [0.0] * 3, [(0, 1, -1.0), (1, 2, -1.0), (0, 2, -1.0)])
    vb = [[0.5, 0.5] for _ in range(3)]
    fb = [{(0,): 0.5, (1,): 0.5} for _ in range(3)]
    fb += [{(0, 0): 0.0, (0, 1): 0.5, (1, 0): 0.5, (1, 1): 0.0} for _ in range(3)]
    assert in_local_polytope(card, factors, vb, fb)
    _, _, log_z = exact_beliefs(card, factors)
    assert abs(log_z - math.log(2 * math.exp(-3) + 6 * math.e)) < 1e-12
    f = bethe_free_energy(card, factors, vb, fb)
    assert abs(f + 3.0) < 1e-12
    assert f < -log_z


def test_not_convex_on_a_loop():
    # K4, J = 1, no fields: the points (m, c) and (-m, c) of the symmetric family
    # have the same value, and their midpoint (0, c) has a larger one.
    card, factors = ising_factors(4, [0.0] * 4, [(i, j, 1.0) for i in range(4) for j in range(i + 1, 4)])
    m, c = 0.9, 0.913
    plus = symmetric_ising_beliefs(4, factors, m, c)
    minus = symmetric_ising_beliefs(4, factors, -m, c)
    mid = symmetric_ising_beliefs(4, factors, 0.0, c)
    for b in (plus, minus, mid):
        assert in_local_polytope(card, factors, *b)
    fp = bethe_free_energy(card, factors, *plus)
    fm = bethe_free_energy(card, factors, *minus)
    fmid = bethe_free_energy(card, factors, *mid)
    assert abs(fp - fm) < 1e-12
    assert fmid > (fp + fm) / 2 + 0.5


def test_local_polytope_check_rejects_inconsistent_beliefs():
    card, factors = ising_factors(2, [0.0, 0.0], [(0, 1, 1.0)])
    vb = [[0.5, 0.5], [0.5, 0.5]]
    fb = [{(0,): 0.5, (1,): 0.5}, {(0,): 0.5, (1,): 0.5},
          {(0, 0): 0.7, (0, 1): 0.1, (1, 0): 0.1, (1, 1): 0.1}]
    assert not in_local_polytope(card, factors, vb, fb)
