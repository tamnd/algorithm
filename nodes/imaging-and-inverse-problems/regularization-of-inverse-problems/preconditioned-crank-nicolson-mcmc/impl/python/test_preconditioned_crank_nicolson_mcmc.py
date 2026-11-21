# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/preconditioned-crank-nicolson-mcmc/. The authors are listed in prov/63HRT4.jsonl.

import math
import random

from imgla import matmul, matvec, solve, transpose
from preconditioned_crank_nicolson_mcmc import (
    diagonal_sampler,
    gaussian_sampler,
    linear_gaussian_misfit,
    mean_and_covariance,
    pcn,
    random_walk_metropolis,
)


def test_zero_misfit_accepts_every_proposal_and_keeps_the_prior():
    # Phi = 0: the acceptance probability is min(1, exp(0)) = 1, and the
    # chain is an AR(1) process whose stationary law is the prior N(3, 4).
    chain, acc = pcn(lambda u: 0.0, diagonal_sampler([4.0]), [3.0], 0.5, 10000, random.Random(5), m0=[3.0])
    assert acc == 1.0
    assert len(chain) == 10000
    mean, cov = mean_and_covariance(chain[500:])
    assert abs(mean[0] - 3.0) < 0.15
    assert abs(cov[0][0] - 4.0) < 0.3


def test_proposal_is_reversible_with_respect_to_the_prior():
    # For the prior N(0, c) and q(u, .) = N(rho u, beta^2 c), the product
    # pi_0(u) q(u, v) is symmetric in (u, v).
    c, beta = 2.5, 0.4
    rho = math.sqrt(1.0 - beta * beta)

    def log_joint(u, v):
        return -u * u / (2.0 * c) - (v - rho * u) ** 2 / (2.0 * beta * beta * c)

    rng = random.Random(3)
    for _ in range(50):
        u, v = rng.uniform(-4.0, 4.0), rng.uniform(-4.0, 4.0)
        assert abs(log_joint(u, v) - log_joint(v, u)) < 1e-12


def test_scalar_linear_gaussian_posterior():
    # y = a u + e, u ~ N(0, 1), e ~ N(0, sigma^2): the posterior is
    # N(0.96, 0.2) for a = 0.1, sigma = 0.05, y = 0.12.
    phi = linear_gaussian_misfit([[0.1]], [0.12], 0.05)
    chain, acc = pcn(phi, diagonal_sampler([1.0]), [0.0], 0.5, 12000, random.Random(1))
    mean, cov = mean_and_covariance(chain[1000:])
    assert 0.5 < acc < 0.9
    assert abs(mean[0] - 0.96) < 0.05
    assert abs(cov[0][0] - 0.2) < 0.03


def test_correlated_prior_two_dimensional_posterior():
    c0 = [[1.0, 0.5], [0.5, 1.0]]
    a = [[1.0, 1.0]]
    y = [1.0]
    sigma = 0.5
    prec = solve(c0, [[1.0, 0.0], [0.0, 1.0]])
    ata = matmul(transpose(a), a)
    post_prec = [[ata[i][j] / sigma ** 2 + prec[i][j] for j in range(2)] for i in range(2)]
    c_post = solve(post_prec, [[1.0, 0.0], [0.0, 1.0]])
    m_post = matvec(c_post, [v / sigma ** 2 for v in matvec(transpose(a), y)])
    chain, _ = pcn(linear_gaussian_misfit(a, y, sigma), gaussian_sampler(c0), [0.0, 0.0], 0.5, 12000, random.Random(7))
    mean, cov = mean_and_covariance(chain[1000:])
    for i in range(2):
        assert abs(mean[i] - m_post[i]) < 0.05
        for j in range(2):
            assert abs(cov[i][j] - c_post[i][j]) < 0.05


def test_acceptance_does_not_degrade_with_dimension():
    # Prior variances 1/k^2 and one observation of sum_k u_k / k. pCN keeps
    # its acceptance rate as n grows; random-walk Metropolis with the same
    # step does not.
    rates = {}
    for n in (10, 100):
        g = [1.0 / k for k in range(1, n + 1)]
        var = [1.0 / k ** 2 for k in range(1, n + 1)]

        def phi(u, g=g):
            return (sum(p * q for p, q in zip(g, u)) - 0.5) ** 2 / 0.02

        _, a_pcn = pcn(phi, diagonal_sampler(var), [0.0] * n, 0.3, 600, random.Random(2))
        _, a_rwm = random_walk_metropolis(phi, [1.0 / v for v in var], [0.0] * n, 0.3, 600, random.Random(2), diagonal_sampler(var))
        rates[n] = (a_pcn, a_rwm)
    assert abs(rates[10][0] - rates[100][0]) < 0.1
    assert rates[100][0] > 0.25
    assert rates[100][1] < 0.5 * rates[10][1]


def test_beta_must_be_in_the_unit_interval():
    for beta in (0.0, -0.1, 1.5):
        try:
            pcn(lambda u: 0.0, diagonal_sampler([1.0]), [0.0], beta, 10, random.Random(0))
        except ValueError:
            continue
        raise AssertionError("beta out of range was accepted")


def test_rejected_steps_repeat_the_state():
    # A huge misfit away from u = 0 makes almost every proposal fail, and a
    # failed step stores the previous state again.
    chain, acc = pcn(lambda u: 1e6 * u[0] * u[0], diagonal_sampler([1.0]), [0.0], 0.9, 200, random.Random(4))
    assert acc < 0.1
    repeats = sum(1 for p, q in zip(chain, chain[1:]) if p is q)
    assert repeats >= 200 * (1.0 - acc) - 2
