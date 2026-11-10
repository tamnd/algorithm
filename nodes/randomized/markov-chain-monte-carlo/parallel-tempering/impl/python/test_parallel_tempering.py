# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-tempering/. The authors are listed in prov/381BFJ.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from parallel_tempering import joint_transition_matrix, metropolis_local_step, parallel_tempering


def ess(xs):
    """Effective sample size by Geyer's initial positive sequence."""
    n = len(xs)
    m = sum(xs) / n
    c = [x - m for x in xs]
    var = sum(v * v for v in c) / n
    if var == 0:
        return 1.0

    def rho(k):
        return sum(c[i] * c[i + k] for i in range(n - k)) / (n * var)

    tau, k = -1.0, 0
    while k + 1 < n:
        g = rho(k) + rho(k + 1)
        if g <= 0:
            break
        tau += 2 * g
        k += 2
    return n / max(tau, 1e-9)


def check_mean(xs, mu, sd):
    # the sample mean has standard error about sd / sqrt(ESS)
    assert abs(sum(xs) / len(xs) - mu) < 5 * sd / math.sqrt(ess(xs))


ENERGY = [0, 3, 3, 0]
BASES = [F(1, 8), F(1, 2), F(4, 5)]  # level k has weights BASES[k] ** energy, that is pi^beta_k with pi = 8^(-E)


def walk_kernel(w):
    n = len(w)
    p = [[F(0)] * n for _ in range(n)]
    for x in range(n):
        for y in (x - 1, x + 1):
            if 0 <= y < n:
                p[x][y] = F(1, 2) * min(F(1), w[y] / w[x])
        p[x][x] = 1 - sum(p[x])
    return p


def example():
    weights = [[b**e for e in ENERGY] for b in BASES]
    return weights, joint_transition_matrix(weights, [walk_kernel(w) for w in weights])


def product_law(weights, states):
    z = [sum(w) for w in weights]
    return [math.prod(weights[k][s[k]] / z[k] for k in range(len(s))) for s in states]


def test_product_law_is_stationary_exactly() -> None:
    weights, (states, local, swap) = example()
    pi = product_law(weights, states)
    m = len(states)
    for kern in (local, swap):
        assert all(sum(row) == 1 for row in kern)
        assert [sum(pi[i] * kern[i][j] for i in range(m)) for j in range(m)] == pi
    # the swap move is reversible with respect to the product law
    assert all(pi[i] * swap[i][j] == pi[j] * swap[j][i] for i in range(m) for j in range(m))


def test_swap_ratio_has_no_normalizing_constants() -> None:
    weights, _ = example()
    # cold level at x = 1, hot level at x = 0: ratio (pi(0) / pi(1))^(beta_1 - beta_2) = 512^(2/3) = 64
    r = weights[0][0] * weights[1][1] / (weights[0][1] * weights[1][0])
    assert r == 64


def test_tempering_speeds_up_crossing() -> None:
    weights, (states, local, swap) = example()
    m = len(states)
    lf = [[float(v) for v in r] for r in local]
    sf = [[float(v) for v in r] for r in swap]
    cold = [[float(v) for v in r] for r in walk_kernel(weights[0])]
    v = [0.0] * m
    v[states.index((0, 0, 0))] = 1.0
    w = [1.0, 0.0, 0.0, 0.0]
    for _ in range(50):
        v = [sum(v[i] * lf[i][j] for i in range(m)) for j in range(m)]
        v = [sum(v[i] * sf[i][j] for i in range(m)) for j in range(m)]
        w = [sum(w[i] * cold[i][j] for i in range(4)) for j in range(4)]
    right_pt = sum(v[i] for i, s in enumerate(states) if s[0] >= 2)
    assert abs(right_pt - 0.4608) < 1e-4
    assert abs(w[2] + w[3] - 0.0158) < 1e-4


C = 6.0  # the modes are at -C and +C, and the density at 0 is e^(-18) times the peak


def mixture(weight_right):
    def log_t(x):
        a = math.log(1 - weight_right) - (x + C) ** 2 / 2
        b = math.log(weight_right) - (x - C) ** 2 / 2
        top = max(a, b)
        return top + math.log(math.exp(a - top) + math.exp(b - top))

    return log_t


def test_bimodal_mixture_weights_recovered() -> None:
    rng = random.Random(1)
    log_t = mixture(0.7)
    betas = [1.0, 0.3, 0.1, 0.03]
    chains, prop, acc = parallel_tempering(log_t, betas, [-C] * 4, metropolis_local_step(1.5), 20000, rng)
    cold = chains[0]
    right = [1.0 if x > 0 else 0.0 for x in cold]
    check_mean(right, 0.7, math.sqrt(0.21))
    sd = math.sqrt(1 + C * C - (0.4 * C) ** 2)
    check_mean(cold, 0.4 * C, sd)
    assert all(a > 0.2 * p for a, p in zip(acc, prop))


def test_cold_chain_alone_is_stuck() -> None:
    rng = random.Random(2)
    log_t = mixture(0.5)
    step = metropolis_local_step(1.5)
    x, right = -C, 0
    for _ in range(20000):
        x = step(log_t, 1.0, x, rng)
        right += x > 0
    assert right == 0


def test_bad_inputs() -> None:
    rng = random.Random(3)
    step = metropolis_local_step(1.0)
    with pytest.raises(ValueError):
        parallel_tempering(mixture(0.5), [1.0, 1.0], [0.0, 0.0], step, 10, rng)
    with pytest.raises(ValueError):
        parallel_tempering(mixture(0.5), [0.5, 0.2], [0.0, 0.0], step, 10, rng)
    with pytest.raises(ValueError):
        parallel_tempering(mixture(0.5), [1.0, 0.5], [0.0], step, 10, rng)
