# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/loopy-belief-propagation/. The authors are listed in prov/BP1TB7.jsonl.

import itertools
import random

from loopy_belief_propagation import exact_marginals, ising_factors, loopy_bp, mooij_kappen_radius

K4 = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]


def random_table(rng, card, scope):
    return {a: rng.uniform(0.1, 2.0) for a in itertools.product(*[range(card[j]) for j in scope])}


def grid(rng, side, h_scale, j_scale):
    idx = lambda r, c: r * side + c
    edges = [(idx(r, c), idx(r, c + 1)) for r in range(side) for c in range(side - 1)]
    edges += [(idx(r, c), idx(r + 1, c)) for r in range(side - 1) for c in range(side)]
    fields = [rng.uniform(-h_scale, h_scale) for _ in range(side * side)]
    return fields, [(i, j, rng.uniform(-j_scale, j_scale)) for i, j in edges]


def max_err(beliefs, exact):
    return max(abs(x - y) for b, e in zip(beliefs, exact) for x, y in zip(b, e))


def test_exact_on_a_tree_factor_graph():
    # Variables 0..6, a ternary factor, pairwise and unary factors: a tree.
    rng = random.Random(1)
    for _ in range(10):
        card = [rng.randint(2, 3) for _ in range(7)]
        scopes = [(0, 1), (1, 2, 3), (3, 4), (2, 5), (5, 6), (0,), (4,), (6,)]
        factors = [(s, random_table(rng, card, s)) for s in scopes]
        out = loopy_bp(card, factors, tol=1e-13)
        exact, _ = exact_marginals(card, factors)
        assert out["converged"]
        assert max_err(out["beliefs"], exact) < 1e-10
        # Factor beliefs are the exact factor marginals on a tree too.
        scope, _ = factors[1]
        fb = out["factor_beliefs"][1]
        for a, prob in fb.items():
            total = 0.0
            z = 0.0
            for x in itertools.product(*[range(c) for c in card]):
                w = 1.0
                for s, t in factors:
                    w *= t[tuple(x[j] for j in s)]
                z += w
                if tuple(x[j] for j in scope) == a:
                    total += w
            assert abs(prob - total / z) < 1e-10


def test_tree_messages_settle_after_the_diameter():
    # A chain of 6 spins: the factor graph has diameter 10 (variable to variable
    # distance 5 factor hops), so the messages stop changing after a few rounds.
    rng = random.Random(2)
    card, factors = ising_factors(6, [rng.uniform(-1, 1) for _ in range(6)],
                                  [(i, i + 1, rng.uniform(-1, 1)) for i in range(5)])
    out = loopy_bp(card, factors, tol=1e-15)
    assert out["converged"] and out["iterations"] <= 7


def test_small_loop_converges_near_exact():
    card, factors = ising_factors(4, [0.3, -0.2, 0.1, 0.0], [(0, 1, 0.5), (1, 3, 0.5), (3, 2, 0.5), (2, 0, 0.5)])
    out = loopy_bp(card, factors)
    exact, _ = exact_marginals(card, factors)
    assert out["converged"]
    assert max_err(out["beliefs"], exact) < 0.015
    assert max_err(out["beliefs"], exact) > 1e-4  # approximate, not exact, on a loop


def test_seeded_grids_converge_near_exact():
    rng = random.Random(5)
    for _ in range(5):
        fields, couplings = grid(rng, 3, 0.5, 0.5)
        card, factors = ising_factors(9, fields, couplings)
        out = loopy_bp(card, factors)
        exact, _ = exact_marginals(card, factors)
        assert out["converged"]
        assert max_err(out["beliefs"], exact) < 0.02


def test_frustrated_k4_oscillates_without_damping():
    card, factors = ising_factors(4, [0.5, 0.0, 0.0, 0.0], [(i, j, -2.0) for i, j in K4])
    out = loopy_bp(card, factors, damping=0.0, max_iter=600, record=True)
    assert not out["converged"]
    # A period-two swing: every spin has belief near 0, then near 1.
    a, b, c = out["history"][-3], out["history"][-2], out["history"][-1]
    assert abs(a[1] - c[1]) < 1e-9 and abs(a[1] - b[1]) > 0.99
    damped = loopy_bp(card, factors, damping=0.5, max_iter=5000)
    assert damped["converged"]


def test_damping_keeps_the_fixed_points():
    card, factors = ising_factors(4, [0.3, -0.2, 0.1, 0.0], [(0, 1, 0.5), (1, 3, 0.5), (3, 2, 0.5), (2, 0, 0.5)])
    plain = loopy_bp(card, factors, tol=1e-13)
    damped = loopy_bp(card, factors, damping=0.6, tol=1e-13, max_iter=5000)
    assert max_err(plain["beliefs"], damped["beliefs"]) < 1e-10


def test_fixed_point_beliefs_are_locally_consistent():
    rng = random.Random(6)
    fields, couplings = grid(rng, 3, 0.5, 0.5)
    card, factors = ising_factors(9, fields, couplings)
    out = loopy_bp(card, factors, tol=1e-13)
    for (scope, _), fb in zip(factors, out["factor_beliefs"]):
        for pos, i in enumerate(scope):
            marg = [0.0, 0.0]
            for a, prob in fb.items():
                marg[a[pos]] += prob
            assert max(abs(x - y) for x, y in zip(marg, out["beliefs"][i])) < 1e-10


def test_mooij_kappen_condition():
    cycle = [(0, 1, 0.5), (1, 3, 0.5), (3, 2, 0.5), (2, 0, 0.5)]
    assert mooij_kappen_radius(4, cycle) < 1
    assert mooij_kappen_radius(4, [(i, j, -2.0) for i, j in K4]) > 1
    # Below 1: undamped BP from random messages ends at the same fixed point.
    rng = random.Random(7)
    for _ in range(5):
        fields, couplings = grid(rng, 3, 1.0, 0.6)
        if mooij_kappen_radius(9, couplings) >= 1:
            continue
        card, factors = ising_factors(9, fields, couplings)
        ref = loopy_bp(card, factors, tol=1e-13)
        assert ref["converged"]
        for _ in range(3):
            other = loopy_bp(card, factors, tol=1e-13, rng=rng)
            assert other["converged"]
            assert max_err(ref["beliefs"], other["beliefs"]) < 1e-9
        ex, _ = exact_marginals(card, factors)
        assert max_err(ref["beliefs"], ex) < 0.05
