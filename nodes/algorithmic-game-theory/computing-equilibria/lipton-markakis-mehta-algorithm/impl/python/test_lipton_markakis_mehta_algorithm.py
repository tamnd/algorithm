# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lipton-markakis-mehta-algorithm/. The authors are listed in prov/JTYPN5.jsonl.

import math
import random
from fractions import Fraction

from agtgame import from_bimatrix, is_epsilon_nash, is_nash, max_gain
from lipton_markakis_mehta_algorithm import best_k_uniform, k_uniform_pairs, lmm, sample_size

F = Fraction
HALF = F(1, 2)

RPS = [[HALF, 0, 1], [1, HALF, 0], [0, 1, HALF]]  # rock-paper-scissors scaled to [0, 1]
RPS_T = [list(r) for r in zip(*RPS)]


def random_unit_matrix(rng, m, n, den):
    return [[F(rng.randint(0, den), den) for _ in range(n)] for _ in range(m)]


def is_k_uniform(p, k):
    return sum(p) == 1 and all(v >= 0 and (v * k).denominator == 1 for v in p)


def test_sample_size():
    for m, n, eps in [(2, 2, HALF), (3, 3, HALF), (2, 2, F(1, 4)), (10, 7, F(1, 10))]:
        k = sample_size(m, n, eps)
        bound = 2 * math.log(2 * (m + n)) / float(eps) ** 2
        assert k > bound >= k - 1
    assert sample_size(2, 2, HALF) == 17
    assert sample_size(3, 3, HALF) == 20


def test_small_k_on_check_games():
    mp_A, mp_B = [[1, 0], [0, 1]], [[0, 1], [1, 0]]
    assert best_k_uniform(mp_A, mp_B, 1)[0] == 1
    g, x, y = best_k_uniform(mp_A, mp_B, 2)
    assert g == 0 and x == [HALF, HALF] and y == [HALF, HALF]
    assert best_k_uniform(RPS, RPS_T, 1)[0] == HALF
    g, x, y = best_k_uniform(RPS, RPS_T, 3)
    assert g == 0 and x == [F(1, 3)] * 3 and y == [F(1, 3)] * 3


def test_exact_equilibria_on_the_grid_are_found_with_eps_zero():
    # Battle of the sexes: the mixed equilibrium (2/3, 1/3), (1/3, 2/3) is 3-uniform.
    A, B = [[2, 0], [0, 1]], [[1, 0], [0, 2]]
    x, y = lmm(A, B, 0, k=3)
    assert is_nash(from_bimatrix(A, B), [x, y])
    x, y = lmm(RPS, RPS_T, 0, k=3)
    assert x == [F(1, 3)] * 3 and y == [F(1, 3)] * 3
    assert lmm(RPS, RPS_T, 0, k=2) is None


def test_pair_gains_agree_with_the_helper():
    rng = random.Random(11)
    for _ in range(10):
        m, n, k = rng.randint(1, 3), rng.randint(1, 3), rng.randint(1, 3)
        A, B = random_unit_matrix(rng, m, n, 6), random_unit_matrix(rng, m, n, 6)
        g = from_bimatrix(A, B)
        count = 0
        for x, y, gr, gc in k_uniform_pairs(A, B, k):
            count += 1
            assert is_k_uniform(x, k) and is_k_uniform(y, k)
            assert max(gr, gc) == max_gain(g, [x, y])
        assert count == math.comb(m + k - 1, k) * math.comb(n + k - 1, k)


def test_lmm_with_given_k_matches_the_exhaustive_minimum():
    rng = random.Random(5)
    for _ in range(40):
        m, n, k = rng.randint(1, 3), rng.randint(1, 3), rng.randint(1, 3)
        A, B = random_unit_matrix(rng, m, n, 4), random_unit_matrix(rng, m, n, 4)
        best = best_k_uniform(A, B, k)[0]
        for eps in [0, F(1, 8), F(1, 4), HALF]:
            out = lmm(A, B, eps, k=k)
            assert (out is None) == (best > eps)
            if out is not None:
                assert is_epsilon_nash(from_bimatrix(A, B), list(out), eps)


def test_theorem_size_always_succeeds():
    rng = random.Random(20261120)
    cases = [(2, 2, HALF)] * 12 + [(2, 3, HALF)] * 6 + [(3, 3, HALF)] * 4 + [(2, 2, F(1, 4))] * 4
    for m, n, eps in cases:
        A, B = random_unit_matrix(rng, m, n, 10), random_unit_matrix(rng, m, n, 10)
        k = sample_size(m, n, eps)
        out = lmm(A, B, eps)
        assert out is not None
        x, y = out
        assert is_k_uniform(x, k) and is_k_uniform(y, k)
        assert is_epsilon_nash(from_bimatrix(A, B), [x, y], eps)
