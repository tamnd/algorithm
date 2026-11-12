# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/contrastive-divergence/. The authors are listed in prov/ZQSFAJ.jsonl.

import random

from contrastive_divergence import (
    cd_gradient,
    cd_update,
    exact_gradient,
    expected_cd,
    flatten,
    log_likelihood,
    pcd_gradient,
    step,
    transition_matrix,
    unflatten,
    visible_marginal,
)

M, N = 3, 2
DATA = [(1, 0, 1), (0, 1, 1), (1, 1, 0)]


def random_params(seed, m=M, n=N, scale=1.0):
    rng = random.Random(seed)
    return unflatten([rng.gauss(0, scale) for _ in range(m * n + m + n)], m, n)


def jacobian(f, x, h=1e-5):
    cols = []
    for j in range(len(x)):
        up, dn = list(x), list(x)
        up[j] += h
        dn[j] -= h
        cols.append([(a - b) / (2 * h) for a, b in zip(f(up), f(dn))])
    return [[cols[j][i] for j in range(len(x))] for i in range(len(x))]


def test_worked_example():
    p = ([[2.0], [-1.0]], [0.0, 0.0], [0.0])
    _, marg = visible_marginal(p)
    assert [round(x, 4) for x in marg] == [0.1292, 0.0884, 0.5421, 0.2403]
    assert [round(x, 4) for x in flatten(exact_gradient(p, [(1, 0)]))] == [0.2277, -0.1994, 0.2176, -0.3287, 0.1393]
    assert [round(x, 4) for x in flatten(expected_cd(p, [(1, 0)], 1))] == [0.1807, -0.1899, 0.1646, -0.2965, 0.1118]


def test_exact_gradient_matches_finite_differences_of_the_log_likelihood():
    for seed in range(3):
        x = flatten(random_params(seed))
        g = flatten(exact_gradient(unflatten(x, M, N), DATA))
        h = 1e-6
        for j in range(len(x)):
            up, dn = list(x), list(x)
            up[j] += h
            dn[j] -= h
            num = (log_likelihood(unflatten(up, M, N), DATA) - log_likelihood(unflatten(dn, M, N), DATA)) / (2 * h)
            assert abs(num - g[j]) < 1e-7


def test_gibbs_kernel_is_stochastic_with_the_rbm_marginal_stationary():
    p = random_params(4)
    t = transition_matrix(p)
    _, marg = visible_marginal(p)
    for row in t:
        assert abs(sum(row) - 1) < 1e-12
        assert min(row) > 0
    moved = [sum(marg[r] * t[r][c] for r in range(len(t))) for c in range(len(t))]
    assert max(abs(a - b) for a, b in zip(moved, marg)) < 1e-12


def test_expected_cd_k_is_biased_for_small_k_and_converges_to_the_gradient():
    for seed in range(3):
        p = random_params(seed)
        g = flatten(exact_gradient(p, DATA))
        errs = [max(abs(a - b) for a, b in zip(flatten(expected_cd(p, DATA, k)), g)) for k in (1, 5, 20, 60)]
        assert errs[0] > 1e-3
        assert errs[1] < errs[0] and errs[2] < errs[1]
        assert errs[3] < 1e-8


def test_sampled_cd_matches_its_exact_expectation():
    p = random_params(5)
    rng = random.Random(6)
    for k, reps in ((1, 3000), (25, 1500)):
        acc = [0.0] * len(flatten(p))
        for _ in range(reps):
            acc = [a + b for a, b in zip(acc, flatten(cd_gradient(p, DATA, k, rng)))]
        mean = [a / reps for a in acc]
        target = flatten(expected_cd(p, DATA, k))
        assert max(abs(a - b) for a, b in zip(mean, target)) < 0.04
    # With k = 25 the target is the exact gradient up to 1e-6.
    assert max(abs(a - b) for a, b in zip(flatten(expected_cd(p, DATA, 25)), flatten(exact_gradient(p, DATA)))) < 1e-6


def test_cd1_update_is_not_a_gradient_field():
    x = flatten(random_params(3))
    cd = jacobian(lambda y: flatten(expected_cd(unflatten(y, M, N), DATA, 1)), x)
    ex = jacobian(lambda y: flatten(exact_gradient(unflatten(y, M, N), DATA)), x)
    n = len(x)
    assert max(abs(ex[i][j] - ex[j][i]) for i in range(n) for j in range(n)) < 1e-6
    assert max(abs(cd[i][j] - cd[j][i]) for i in range(n) for j in range(n)) > 1e-3


def test_cd1_and_pcd_training_raise_the_likelihood():
    rng = random.Random(1)
    data = [(1, 1, 0, 0), (0, 0, 1, 1), (1, 1, 0, 0), (0, 0, 1, 1), (1, 0, 0, 0), (0, 0, 0, 1)]
    p0 = ([[rng.gauss(0, 0.1) for _ in range(3)] for _ in range(4)], [0.0] * 4, [0.0] * 3)
    start = log_likelihood(p0, data)
    for persistent in (False, True):
        p, chains, r = p0, [list(v) for v in data], random.Random(2)
        for _ in range(300):
            if persistent:
                p = step(p, pcd_gradient(p, data, chains, 1, r), 0.1)
            else:
                p = cd_update(p, data, 1, 0.1, r)
        assert log_likelihood(p, data) > start + 0.15
