# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deterministic-policy-gradient/. The authors are listed in prov/KFKT3Y.jsonl.

import random
from fractions import Fraction as F

from deterministic_policy_gradient import (
    deterministic_gradient_one_step,
    deterministic_policy_gradient,
    expected_return,
    q_action_derivative,
    stochastic_gradient_one_step,
    values,
)


def random_model(rng, gamma):
    while True:
        alpha, beta = F(rng.randint(-4, 4), 4), F(rng.randint(1, 4), 4)
        k, c = F(rng.randint(-4, 4), 4), F(rng.randint(-4, 4), 4)
        if gamma * (alpha + beta * k) ** 2 < F(9, 10):
            break
    q, rho, u = F(rng.randint(0, 3)), F(rng.randint(1, 3)), F(rng.randint(-3, 3))
    start = [(F(1, 3), F(rng.randint(-3, 3))), (F(2, 3), F(rng.randint(-3, 3)))]
    noise = [(F(1, 2), F(rng.randint(-2, 2), 2)), (F(1, 2), F(rng.randint(-2, 2), 2))]
    return (alpha, beta, q, rho, u, gamma, start, noise), (k, c)


def test_one_step_problem_is_exact():
    # gamma = 0: J(theta) = E r(S, k S + c) is a quadratic in theta, so the central difference is exact for any h
    rng = random.Random(1)
    for _ in range(30):
        model, theta = random_model(rng, F(0))
        k, c = theta
        g = deterministic_policy_gradient(model, theta)
        for i, h in [(0, F(1)), (1, F(3, 7))]:
            up = (k + h, c) if i == 0 else (k, c + h)
            dn = (k - h, c) if i == 0 else (k, c - h)
            assert (expected_return(model, up) - expected_return(model, dn)) / (2 * h) == g[i]
        # and it is the chain rule: E[(S, 1) d_a r(S, mu(S))] with d_a r = -2 rho a + u
        _, _, _, rho, u, _, start, _ = model
        want = (sum(p * s * (-2 * rho * (k * s + c) + u) for p, s in start),
                sum(p * (-2 * rho * (k * s + c) + u) for p, s in start))
        assert g == want


def test_one_step_optimum():
    model = (F(1), F(1), F(1), F(2), F(3), F(0), [(F(1), F(5))], [(F(1), F(0))])
    # r(s, a) = -(s^2 + 2 a^2) + 3 a is largest at a = 3/4 for every s
    assert deterministic_policy_gradient(model, (F(0), F(3, 4))) == (0, 0)
    assert deterministic_policy_gradient(model, (F(0), F(0))) == (15, 3)


def test_multi_step_matches_the_derivative_of_the_return():
    rng = random.Random(2)
    h = F(1, 10 ** 6)
    for _ in range(30):
        model, theta = random_model(rng, F(rng.randint(1, 3), 4))
        k, c = theta
        g = deterministic_policy_gradient(model, theta)
        fd = ((expected_return(model, (k + h, c)) - expected_return(model, (k - h, c))) / (2 * h),
              (expected_return(model, (k, c + h)) - expected_return(model, (k, c - h))) / (2 * h))
        for a, b in zip(g, fd):
            assert abs(a - b) <= F(1, 10 ** 6) * (1 + abs(a))


def test_values_solve_the_bellman_equation():
    rng = random.Random(3)
    for _ in range(20):
        model, theta = random_model(rng, F(rng.randint(1, 3), 4))
        alpha, beta, q, rho, u, gamma, start, noise = model
        k, c = theta
        p, l, c0 = values(model, theta)

        def V(s):
            return p * s * s + l * s + c0

        for s in [F(-2), F(0), F(1, 3), F(5)]:
            a = k * s + c
            assert V(s) == -(q * s * s + rho * a * a) + u * a + gamma * sum(w * V(alpha * s + beta * a + x) for w, x in noise)
            # d_a Q by a central difference, exact because Q is quadratic in a
            def Q(b):
                return -(q * s * s + rho * b * b) + u * b + gamma * sum(w * V(alpha * s + beta * b + x) for w, x in noise)
            assert (Q(a + 1) - Q(a - 1)) / 2 == q_action_derivative(model, theta, s, a)
        assert sum(w * V(s) for w, s in start) == expected_return(model, theta)


def test_stochastic_gradient_tends_to_deterministic_gradient():
    # r(a) = -(a - 2)^4 = -a^4 + 8 a^3 - 24 a^2 + 32 a - 16
    coeffs = [F(-16), F(32), F(-24), F(8), F(-1)]
    for theta in [F(0), F(1, 2), F(3), F(7, 3)]:
        x = theta - 2
        det = deterministic_gradient_one_step(coeffs, theta)
        assert det == -4 * x ** 3
        for e in range(0, 8):
            sigma2 = F(1, 10 ** e)
            sto = stochastic_gradient_one_step(coeffs, theta, sigma2)
            # E[r(theta + sigma Z)] = -(x^4 + 6 x^2 sigma2 + 3 sigma2^2), whose derivative is -(4 x^3 + 12 x sigma2)
            assert sto == -(4 * x ** 3 + 12 * x * sigma2)
            assert abs(sto - det) == abs(12 * x) * sigma2


def test_quadratic_reward_has_no_gap():
    # for a reward quadratic in a, the Gaussian smoothing only adds a constant, so the two gradients agree for every sigma
    coeffs = [F(1), F(-3), F(-2)]
    for theta in [F(-1), F(0), F(5, 2)]:
        for sigma2 in [F(1), F(4), F(1, 9)]:
            assert stochastic_gradient_one_step(coeffs, theta, sigma2) == deterministic_gradient_one_step(coeffs, theta)
