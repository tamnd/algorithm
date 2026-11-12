# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stochastic-variational-inference/. The authors are listed in prov/MB3DWW.jsonl.

import random

from stochastic_variational_inference import cavi, elbo, fisher, intermediate, local_step, mean_var, svi

S0 = 10.0
LAM0 = [[-1.0, 1.0], [0.0, 1.0], [1.0, 1.0]]


def data():
    rng = random.Random(1)
    centers = [-4.0, 0.0, 3.0]
    return [rng.gauss(centers[rng.randrange(3)], 1.0) for _ in range(500)]


def solve2(a, b):
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    return [(a[1][1] * b[0] - a[0][1] * b[1]) / det, (a[0][0] * b[1] - a[1][0] * b[0]) / det]


def test_natural_gradient_is_lam_hat_minus_lam():
    xs = data()[:40]
    lam = [[-2.0, 3.0], [0.5, 2.0], [4.0, 1.5]]
    phis = [local_step(x, lam) for x in xs]
    lam_hat = intermediate(xs, range(len(xs)), lam, S0, 1.0)
    h = 1e-6
    for k in range(3):
        grad = []
        for d in range(2):
            up = [list(l) for l in lam]
            dn = [list(l) for l in lam]
            up[k][d] += h
            dn[k][d] -= h
            grad.append((elbo(xs, up, phis, S0) - elbo(xs, dn, phis, S0)) / (2 * h))
        nat = solve2(fisher(lam[k]), grad)
        assert all(abs(a - (b - c)) < 1e-4 for a, b, c in zip(nat, lam_hat[k], lam[k]))


def test_full_batch_with_step_one_is_a_cavi_sweep():
    xs = data()
    lam = [list(l) for l in LAM0]
    for _ in range(5):
        full = intermediate(xs, range(len(xs)), lam, S0, 1.0)
        step = svi(xs, 3, S0, lam, len(xs), 1, random.Random(0), tau=0.0, kappa=0.7)  # rho_1 = 1
        assert all(abs(a - b) < 1e-9 for l1, l2 in zip(full, step) for a, b in zip(l1, l2))
        lam = full


def test_minibatch_estimate_is_unbiased():
    xs = data()[:60]
    N = len(xs)
    full = intermediate(xs, range(N), LAM0, S0, 1.0)
    avg = [[0.0, 0.0] for _ in range(3)]
    for n in range(N):  # all singleton minibatches, each with probability 1 / N
        one = intermediate(xs, [n], LAM0, S0, float(N))
        for k in range(3):
            for d in range(2):
                avg[k][d] += one[k][d] / N
    assert all(abs(a - b) < 1e-9 for l1, l2 in zip(avg, full) for a, b in zip(l1, l2))


def test_svi_reaches_the_cavi_fixed_point():
    xs = data()
    lam_c, sweeps = cavi(xs, 3, S0, LAM0)
    assert sweeps == 50
    means_c = [mean_var(l)[0] for l in lam_c]
    assert [round(m, 4) for m in means_c] == [-3.8483, 0.1549, 3.0676]
    errors = []
    for steps in (100, 10000):
        lam_s = svi(xs, 3, S0, LAM0, 50, steps, random.Random(3), kappa=0.9)
        errors.append(max(abs(mean_var(a)[0] - c) for a, c in zip(lam_s, means_c)))
        variances = [mean_var(l)[1] for l in lam_s]
    assert errors[1] < 0.005 < errors[0]
    assert all(abs(v - mean_var(l)[1]) < 2e-4 for v, l in zip(variances, lam_c))
