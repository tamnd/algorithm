# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/annealed-importance-sampling/. The authors are listed in prov/R9W3YJ.jsonl.

import itertools
import math
import random
from fractions import Fraction

from annealed_importance_sampling import (ais, effective_sample_size, exact_mean_weight, ising_ais,
                                          ising_log_f, ising_log_z, linear_path_exact,
                                          log_mean_exp, metropolis_matrix, weighted_expectation)


def random_model(rng, m):
    f0 = [Fraction(rng.randint(1, 9)) for _ in range(m)]
    fT = [Fraction(rng.randint(1, 50), rng.randint(1, 7)) for _ in range(m)]
    t = rng.randint(1, 5)
    inner = sorted({Fraction(rng.randint(1, 99), 100) for _ in range(t - 1)})
    return f0, fT, [Fraction(0)] + inner + [Fraction(1)]


def test_metropolis_matrix_leaves_f_invariant():
    rng = random.Random(1)
    for _ in range(20):
        f = [Fraction(rng.randint(1, 20), rng.randint(1, 5)) for _ in range(rng.randint(2, 6))]
        mat = metropolis_matrix(f)
        for row in mat:
            assert sum(row) == 1 and min(row) >= 0
        for y in range(len(f)):
            assert sum(f[x] * mat[x][y] for x in range(len(f))) == f[y]


def test_exact_unbiasedness_on_the_linear_path():
    rng = random.Random(2)
    for _ in range(40):
        f0, fT, betas = random_model(rng, rng.randint(2, 5))
        fs = linear_path_exact(f0, fT, betas)
        mats = [None] + [metropolis_matrix(f) for f in fs[1:]]
        mean, v = exact_mean_weight(fs, mats)
        assert mean == sum(fT) / sum(f0)
        assert v == [c / sum(f0) for c in fT]


def test_identity_kernels_give_plain_importance_sampling_and_stay_unbiased():
    rng = random.Random(3)
    for _ in range(20):
        f0, fT, betas = random_model(rng, 4)
        fs = linear_path_exact(f0, fT, betas)
        eye = [[Fraction(int(i == j)) for j in range(4)] for i in range(4)]
        mean, _ = exact_mean_weight(fs, [None] + [eye] * (len(fs) - 1))
        assert mean == sum(fT) / sum(f0)


def test_kernels_with_the_wrong_invariant_distribution_give_bias():
    # Kernels that leave f_0 invariant instead of f_j: the mean weight is no longer Z_T / Z_0.
    f0 = [Fraction(1), Fraction(1), Fraction(1)]
    fT = [Fraction(8), Fraction(1), Fraction(1)]
    betas = [Fraction(0), Fraction(1, 2), Fraction(1)]
    fs = linear_path_exact(f0, fT, betas)
    wrong = [None] + [metropolis_matrix(f0)] * 2
    mean, _ = exact_mean_weight(fs, wrong)
    assert mean != Fraction(10, 3)


def test_monte_carlo_mean_matches_the_exact_value_on_a_small_model():
    f0 = [1.0, 2.0, 3.0, 4.0]
    fT = [10.0, 0.5, 0.5, 20.0]
    betas = [0.0, 0.25, 0.5, 0.75, 1.0]
    fs = [[(1 - b) * a + b * c for a, c in zip(f0, fT)] for b in betas]

    def sample_p0(r):
        return r.choices(range(4), weights=f0)[0]

    def metropolis(j, x, r):
        y = r.choice([z for z in range(4) if z != x])
        return y if r.random() < min(1.0, fs[j][y] / fs[j][x]) else x

    rng = random.Random(4)
    log_ws, xs = ais(lambda j, x: math.log(fs[j][x]), sample_p0, metropolis, 4, 40000, rng)
    est = math.exp(log_mean_exp(log_ws)) * sum(f0)
    assert abs(est - sum(fT)) / sum(fT) < 0.02
    p3 = weighted_expectation(log_ws, xs, lambda x: x == 3)
    assert abs(p3 - 20.0 / 31.0) < 0.02


def test_transfer_matrix_matches_enumeration():
    for n, j, h in [(1, 0.7, 0.3), (5, 1.0, -0.2), (8, -0.5, 0.4)]:
        z = sum(math.exp(ising_log_f(s, j, h)) for s in itertools.product((-1, 1), repeat=n))
        assert abs(ising_log_z(n, j, h) - math.log(z)) < 1e-12


def test_ising_estimate_within_tolerance():
    rng = random.Random(1)
    n, j, h = 8, 1.0, 0.2
    est, log_ws, xs = ising_ais(n, j, h, 50, 1000, rng)
    assert abs(math.exp(est - ising_log_z(n, j, h)) - 1) < 0.05
    assert effective_sample_size(log_ws) > 500


def test_example_of_the_page():
    lz = ising_log_z(16, 2.0, 0.0)
    assert abs(lz - 30.9654) < 1e-4
    est, log_ws, _ = ising_ais(16, 2.0, 0.0, 10, 1000, random.Random(1))
    assert abs(math.exp(est - lz) - 1.7435) < 1e-3
    assert abs(effective_sample_size(log_ws) - 6.1) < 0.1
