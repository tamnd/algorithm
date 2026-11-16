# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/alpha-beta-swap/. The authors are listed in prov/Y9ZT41.jsonl.

import itertools
import random

from alpha_beta_swap import (
    alpha_beta_swap,
    energy,
    grid_pairs,
    is_semimetric,
    potts,
    swap_move,
    truncated_quadratic,
)


def brute_swap(D, pairs, V, f, alpha, beta):
    sites = [p for p in range(len(D)) if f[p] in (alpha, beta)]
    best = None
    for bits in itertools.product((alpha, beta), repeat=len(sites)):
        g = list(f)
        for p, l in zip(sites, bits):
            g[p] = l
        e = energy(D, pairs, V, g)
        if best is None or e < best:
            best = e
    return best


def random_instance(rng):
    w = rng.randint(1, 4)
    h = rng.randint(1, 3)
    L = rng.randint(2, 4)
    while L ** (w * h) > 4096:
        h -= 1
    n = w * h
    D = [[rng.randint(0, 9) for _ in range(L)] for _ in range(n)]
    pairs = [(p, q, rng.randint(1, 3)) for (p, q, _) in grid_pairs(w, h)]
    if rng.random() < 0.5:
        V = potts(L, rng.randint(1, 4))
    else:
        V = truncated_quadratic(L, rng.randint(1, 9))
    return D, pairs, V


def test_move_is_optimal_in_its_space():
    rng = random.Random(1)
    for _ in range(200):
        D, pairs, V = random_instance(rng)
        L = len(V)
        f = [rng.randrange(L) for _ in D]
        alpha, beta = rng.sample(range(L), 2)
        g = swap_move(D, pairs, V, f, alpha, beta)
        for p in range(len(D)):
            if f[p] in (alpha, beta):
                assert g[p] in (alpha, beta)
            else:
                assert g[p] == f[p]
        assert energy(D, pairs, V, g) == brute_swap(D, pairs, V, f, alpha, beta)


def test_local_minimum_and_monotone():
    rng = random.Random(2)
    for _ in range(100):
        D, pairs, V = random_instance(rng)
        assert is_semimetric(V)
        L = len(V)
        f0 = [rng.randrange(L) for _ in D]
        f, _ = alpha_beta_swap(D, pairs, V, f0)
        ef = energy(D, pairs, V, f)
        assert ef <= energy(D, pairs, V, f0)
        opt = min(energy(D, pairs, V, g) for g in itertools.product(range(L), repeat=len(D)))
        assert ef >= opt
        for alpha, beta in itertools.combinations(range(L), 2):
            assert brute_swap(D, pairs, V, f, alpha, beta) == ef


def test_unbounded_ratio_example():
    # Two neighbors p, q, labels a = 0, b = 1, c = 2, Potts with lambda.
    for lam, M, delta in ((10, 10, 1), (100, 100, 1), (1000, 1000, 1)):
        D = [[0, M, delta], [M, 0, delta]]
        pairs = [(0, 1, 1)]
        V = potts(3, lam)
        f, _ = alpha_beta_swap(D, pairs, V, [0, 1])
        assert f == [0, 1] and energy(D, pairs, V, f) == lam
        assert energy(D, pairs, V, [2, 2]) == 2 * delta
    # The ratio lam / (2 delta) grows without bound.


def test_worked_example():
    D = [[0, 9, 1], [9, 0, 1]]
    V = potts(3, 6)
    pairs = [(0, 1, 1)]
    assert swap_move(D, pairs, V, [0, 1], 0, 1) == [0, 1]
    assert swap_move(D, pairs, V, [0, 1], 0, 2) == [0, 1]
    assert swap_move(D, pairs, V, [0, 1], 1, 2) == [0, 1]
    assert energy(D, pairs, V, [0, 1]) == 6
    assert energy(D, pairs, V, [2, 2]) == 2
