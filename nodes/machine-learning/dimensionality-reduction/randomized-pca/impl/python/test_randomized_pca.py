# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/randomized-pca/. The authors are listed in prov/A8T6DS.jsonl.

import math
import random

from randomized_pca import orth_columns, randomized_pca, range_error

EXAMPLE = [(13, 11, 9), (9, 15, 7), (5, 7, 17), (1, 11, 15), (7, -1, -3), (3, 3, -5), (-1, -5, 5), (-5, -1, 3)]


def planted(rng, n, d, sing, shift):
    """Rows mu + sum_j s_j u_j[i] v_j with orthonormal u_j orthogonal to the ones vector,
    so the centered matrix has exactly the singular values sing and right vectors v_j."""
    ones = [1.0 / math.sqrt(n)] * n
    us = orth_columns([ones] + [[rng.gauss(0, 1) for _ in range(n)] for _ in sing])[1:]
    vs = orth_columns([[rng.gauss(0, 1) for _ in range(d)] for _ in sing])
    x = [[shift * j + sum(s * u[i] * v[j] for s, u, v in zip(sing, us, vs)) for j in range(d)] for i in range(n)]
    return x, vs


def aligned(a, b, tol):
    return abs(abs(sum(s * t for s, t in zip(a, b))) - 1.0) < tol


def test_worked_example():
    mu, comps, values, qb = randomized_pca(EXAMPLE, 2, random.Random(1), p=1, q=0)
    assert all(abs(a - b) < 1e-12 for a, b in zip(mu, [4, 5, 6]))
    assert all(abs(a - b) < 1e-9 for a, b in zip(values, [81, 36]))
    for c, want in zip(comps, [(1, 2, 2), (2, 1, -2)]):
        assert aligned(c, [t / 3 for t in want], 1e-9)


def test_exact_when_rank_at_most_k_plus_p():
    sing = [9.0, 4.0, 2.0, 1.0]
    x, vs = planted(random.Random(2), 30, 12, sing, 1.0)
    for seed in range(3):
        mu, comps, values, qb = randomized_pca(x, 2, random.Random(seed), p=3, q=0)
        assert range_error(x, mu, qb, random.Random(7)) < 1e-9
        assert all(abs(math.sqrt(v * 30) - s) < 1e-9 for v, s in zip(values, sing))
        for c, v in zip(comps, vs):
            assert aligned(c, v, 1e-9)


def test_fast_decay_error_close_to_sigma_k_plus_1():
    n, d, k, p = 60, 20, 3, 5
    sing = [10 * 0.5 ** j for j in range(d - 1)]
    x, vs = planted(random.Random(3), n, d, sing, 2.0)
    tail = math.sqrt(sum(s * s for s in sing[k:]))
    bound = (1 + math.sqrt(k / (p - 1))) * sing[k] + math.e * math.sqrt(k + p) / p * tail  # Halko et al., Theorem 10.6
    errors = []
    for seed in range(4):
        mu, comps, values, qb = randomized_pca(x, k, random.Random(seed), p=p, q=1)
        err = range_error(x, mu, qb, random.Random(11))
        errors.append(err)
        # never better than the best rank k + p approximation, by Eckart-Young
        assert err >= sing[k + p] * (1 - 1e-6)
        assert err <= sing[k]
        for v, s in zip(values, sing):
            assert abs(math.sqrt(v * n) - s) < 1e-6 * s
        for c, v in zip(comps, vs):
            assert aligned(c, v, 1e-6)
    q0 = [range_error(x, *randomized_pca(x, k, random.Random(seed), p=p, q=0)[::3], random.Random(11)) for seed in range(4)]
    assert sum(q0) / len(q0) <= bound
    assert max(errors) <= min(q0)


def test_power_iterations_help_on_slow_decay():
    n, d, k = 60, 20, 3
    sing = [10 / math.sqrt(1 + j) for j in range(d - 1)]
    x, _ = planted(random.Random(4), n, d, sing, 0.5)
    mean_err = []
    for q in (0, 2):
        errs = [range_error(x, *randomized_pca(x, k, random.Random(s), p=2, q=q)[::3], random.Random(5)) for s in range(4)]
        mean_err.append(sum(errs) / len(errs))
    assert mean_err[1] < mean_err[0]
    assert mean_err[1] < 1.3 * sing[k]
