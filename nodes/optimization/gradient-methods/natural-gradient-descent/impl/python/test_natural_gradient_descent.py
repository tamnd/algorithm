# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/natural-gradient-descent/. The authors are listed in prov/R1B2TS.jsonl.

import math
import random

from natural_gradient_descent import logistic_model, natural_gradient_descent, sigmoid, solve

TOL = 1e-9


def bernoulli_mean(ybar: float):
    """The mean negative log-likelihood of Bernoulli data in the mean parameter q."""

    def grad(q: list[float]) -> list[float]:
        return [(q[0] - ybar) / (q[0] * (1 - q[0]))]

    def fisher(q: list[float]) -> list[list[float]]:
        return [[1.0 / (q[0] * (1 - q[0]))]]

    return grad, fisher


def random_logistic(rng: random.Random, n_obs: int, d: int):
    xs = [[1.0] + [rng.gauss(0, 1) for _ in range(d - 1)] for _ in range(n_obs)]
    true = [rng.uniform(-1, 1) for _ in range(d)]
    ys = [1 if rng.random() < sigmoid(sum(a * b for a, b in zip(true, x))) else 0 for x in xs]
    return xs, ys


def test_bernoulli_mean_parameter_contracts_exactly() -> None:
    for ybar, q0, eta in [(0.8, 0.1, 0.5), (0.3, 0.95, 0.25), (0.5, 0.01, 0.9)]:
        grad, fisher = bernoulli_mean(ybar)
        qs = natural_gradient_descent(grad, fisher, [q0], eta, 30)
        for k, q in enumerate(qs):
            assert abs((q[0] - ybar) - (1 - eta) ** k * (q0 - ybar)) <= 1e-12
    grad, fisher = bernoulli_mean(0.8)
    assert abs(natural_gradient_descent(grad, fisher, [0.1], 1.0, 1)[1][0] - 0.8) <= 1e-15


def test_direction_is_invariant_under_a_nonlinear_change_of_parameter() -> None:
    # Mean parameter q against the logit theta: the natural directions satisfy d_theta = (dtheta/dq) d_q.
    rng = random.Random(51)
    for _ in range(100):
        ybar, theta = rng.uniform(0.05, 0.95), rng.uniform(-4, 4)
        q = sigmoid(theta)
        grad_q, fisher_q = bernoulli_mean(ybar)
        d_q = solve(fisher_q([q]), grad_q([q]))[0]
        d_theta = solve([[q * (1 - q)]], [q - ybar])[0]  # gradient and Fisher in the logit
        assert abs(d_theta - d_q / (q * (1 - q))) <= 1e-9 * (1 + abs(d_theta))


def test_iterates_are_invariant_under_a_linear_change_of_parameter() -> None:
    rng = random.Random(52)
    for _ in range(8):
        d = rng.randint(2, 4)
        xs, ys = random_logistic(rng, 200, d)  # enough data that the maximum likelihood estimate is finite
        loss, grad, fisher = logistic_model(xs, ys)
        b =[[rng.uniform(-1, 1) + (2.0 if i == j else 0.0) for j in range(d)] for i in range(d)]
        c = [rng.uniform(-1, 1) for _ in range(d)]

        def to_theta(xi: list[float], b=b, c=c) -> list[float]:
            return [sum(b[i][j] * xi[j] for j in range(d)) + c[i] for i in range(d)]

        def grad_xi(xi: list[float], b=b) -> list[float]:
            g = grad(to_theta(xi))
            return [sum(b[i][j] * g[i] for i in range(d)) for j in range(d)]

        def fisher_xi(xi: list[float], b=b) -> list[list[float]]:
            f = fisher(to_theta(xi))
            return [[sum(b[p][i] * f[p][q] * b[q][j] for p in range(d) for q in range(d)) for j in range(d)] for i in range(d)]

        xi0 = solve(b, [-a for a in c])  # theta_0 = 0
        run_xi = natural_gradient_descent(grad_xi, fisher_xi, xi0, 0.5, 8)
        run_theta = natural_gradient_descent(grad, fisher, to_theta(xi0), 0.5, 8)
        for xi, theta in zip(run_xi, run_theta):
            assert max(abs(p - q) for p, q in zip(to_theta(xi), theta)) <= 1e-8


def test_descent_lemma_with_damping() -> None:
    # With F + lam I between m I and M I, m = lam, M = lam + l, and the step m / l:
    # L(theta_(k+1)) <= L(theta_k) - (m / (2 l)) g^T (F + lam I)^(-1) g at every step.
    rng = random.Random(53)
    for _ in range(10):
        d = rng.randint(2, 4)
        xs, ys = random_logistic(rng, 30, d)
        loss, grad, fisher = logistic_model(xs, ys)
        ell = sum(sum(v * v for v in x) for x in xs) / (4 * len(xs))  # bounds the Hessian and F
        lam = rng.uniform(0.01, 0.5)
        m, big_m = lam, lam + ell
        eta = m / ell
        run = natural_gradient_descent(grad, fisher, [rng.uniform(-2, 2) for _ in range(d)], eta, 40, damping=lam)
        grads = []
        for k in range(len(run) - 1):
            g = grad(run[k])
            f = fisher(run[k])
            f = [[f[i][j] + (lam if i == j else 0.0) for j in range(d)] for i in range(d)]
            ginv_g = sum(a * b for a, b in zip(g, solve(f, g)))
            assert loss(run[k + 1]) <= loss(run[k]) - m / (2 * ell) * ginv_g + TOL
            grads.append(sum(a * a for a in g))
            kk = k + 1
            assert min(grads) <= 2 * ell * big_m * (loss(run[0]) - 0.0) / (m * kk) + TOL


def test_zero_iterations() -> None:
    grad, fisher = bernoulli_mean(0.5)
    assert natural_gradient_descent(grad, fisher, [0.2], 0.5, 0) == [[0.2]]
    assert math.isclose(sigmoid(0.0), 0.5)
