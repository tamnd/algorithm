# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/alpha-expansion/. The authors are listed in prov/V82D4Y.jsonl.

import itertools
import random

import pytest

from alpha_expansion import (
    alpha_expansion,
    bound_factor,
    energy,
    expansion_move,
    grid_pairs,
    is_metric,
    minimize_regular_binary,
    potts,
    truncated_linear,
)


def brute_optimum(D, pairs, V):
    n, L = len(D), len(V)
    return min(energy(D, pairs, V, f) for f in itertools.product(range(L), repeat=n))


def brute_move(D, pairs, V, f, alpha):
    n = len(D)
    best = None
    for x in itertools.product((0, 1), repeat=n):
        g = [alpha if x[p] else f[p] for p in range(n)]
        e = energy(D, pairs, V, g)
        if best is None or e < best:
            best = e
    return best


def random_instance(rng, n_max=8):
    w = rng.randint(1, 4)
    h = rng.randint(1, max(1, n_max // w))
    L = rng.randint(2, 4)
    while L ** (w * h) > 4096:
        h -= 1
    n = w * h
    D = [[rng.randint(0, 9) for _ in range(L)] for _ in range(n)]
    pairs = [(p, q, rng.randint(1, 3)) for (p, q, _) in grid_pairs(w, h)]
    V = potts(L, rng.randint(1, 4)) if rng.random() < 0.5 else truncated_linear(L, rng.randint(1, 3))
    return D, pairs, V


def test_binary_cut_against_brute_force():
    rng = random.Random(1)
    for _ in range(200):
        n = rng.randint(2, 7)
        unary = [(rng.randint(-5, 5), rng.randint(-5, 5)) for _ in range(n)]
        terms = []
        for _ in range(rng.randint(0, 2 * n)):
            p, q = rng.sample(range(n), 2)
            A, B, C = rng.randint(-3, 3), rng.randint(-3, 3), rng.randint(-3, 3)
            Dd = B + C - A - rng.randint(0, 4)
            terms.append((p, q, A, B, C, Dd))

        def e(x):
            return (sum(unary[p][x[p]] for p in range(n))
                    + sum((A, B, C, Dd)[2 * x[p] + x[q]] for (p, q, A, B, C, Dd) in terms))
        x = minimize_regular_binary(n, unary, terms)
        assert e(x) == min(e(y) for y in itertools.product((0, 1), repeat=n))


def test_nonregular_term_is_rejected():
    with pytest.raises(ValueError):
        minimize_regular_binary(2, [(0, 0), (0, 0)], [(0, 1, 1, 0, 0, 1)])


def test_move_is_optimal_in_its_space():
    rng = random.Random(2)
    for _ in range(150):
        D, pairs, V = random_instance(rng)
        L = len(V)
        f = [rng.randrange(L) for _ in D]
        alpha = rng.randrange(L)
        g = expansion_move(D, pairs, V, f, alpha)
        assert all(g[p] in (f[p], alpha) for p in range(len(D)))
        assert energy(D, pairs, V, g) == brute_move(D, pairs, V, f, alpha)


def test_bound_and_local_minimum():
    rng = random.Random(3)
    for _ in range(120):
        D, pairs, V = random_instance(rng)
        assert is_metric(V)
        L = len(V)
        f0 = [rng.randrange(L) for _ in D]
        f, _ = alpha_expansion(D, pairs, V, f0)
        ef = energy(D, pairs, V, f)
        assert ef <= energy(D, pairs, V, f0)
        opt = brute_optimum(D, pairs, V)
        assert opt <= ef <= 2 * bound_factor(V) * opt
        for alpha in range(L):
            assert brute_move(D, pairs, V, f, alpha) == ef


def test_worked_example():
    # Four sites in a row, Potts with lambda = 4, labels 0, 1, 2.
    D = [[0, 5, 1], [2, 6, 0], [6, 0, 5], [0, 2, 5]]
    pairs = [(0, 1, 1), (1, 2, 1), (2, 3, 1)]
    V = potts(3, 4)
    f0 = [0, 2, 1, 0]
    assert energy(D, pairs, V, f0) == 12
    assert expansion_move(D, pairs, V, f0, 0) == [0, 0, 0, 0]
    f, cycles = alpha_expansion(D, pairs, V, f0)
    assert f == [0, 0, 0, 0] and energy(D, pairs, V, f) == 8 and cycles == 2
    assert brute_optimum(D, pairs, V) == 7
    assert energy(D, pairs, V, [2, 2, 1, 1]) == 7


def test_truncated_quadratic_is_not_metric():
    V = [[min((a - b) ** 2, 4) for b in range(3)] for a in range(3)]
    assert not is_metric(V)
    D = [[0, 9, 9], [9, 9, 0]]
    with pytest.raises(ValueError):
        expansion_move(D, [(0, 1, 1)], V, [0, 2], 1)
