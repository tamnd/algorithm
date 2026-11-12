# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deterministic-policy-gradient/. The authors are listed in prov/KFKT3Y.jsonl.

"""The deterministic policy gradient theorem as exact computations.

Model: a scalar linear system with a linear deterministic policy.
State s, action a = mu(s) = k s + c with theta = (k, c).
Next state s' = alpha s + beta a + w, with w drawn from a finite noise law.
Reward r(s, a) = -(q s^2 + rho a^2) + u a, discount gamma.
Start state from a finite law.
A model is the tuple (alpha, beta, q, rho, u, gamma, start, noise); start and
noise are lists of (probability, value). Everything is quadratic, so the value
functions, the discounted state moments and the return are exact with
Fractions. The closed loop must satisfy gamma (alpha + beta k)^2 < 1.

Cost: O(|start| + |noise|) arithmetic operations per call.
"""

from math import comb


def _mean(law, f):
    return sum(p * f(x) for p, x in law)


def values(model, theta):
    """V(s) = p s^2 + l s + c0 for the policy theta, from the Bellman equation."""
    alpha, beta, q, rho, u, gamma, _, noise = model
    k, c = theta
    lam = alpha + beta * k
    drift = _mean(noise, lambda w: beta * c + w)  # E[beta c + w]
    second = _mean(noise, lambda w: (beta * c + w) ** 2)
    p = -(q + rho * k * k) / (1 - gamma * lam * lam)
    l = (-2 * rho * k * c + u * k + gamma * 2 * p * lam * drift) / (1 - gamma * lam)
    c0 = (-rho * c * c + u * c + gamma * (p * second + l * drift)) / (1 - gamma)
    return p, l, c0


def q_action_derivative(model, theta, s, a):
    """d Q(s, a) / d a, where Q(s, a) = r(s, a) + gamma E V(alpha s + beta a + w)."""
    alpha, beta, q, rho, u, gamma, _, noise = model
    p, l, _ = values(model, theta)
    mean_next = _mean(noise, lambda w: alpha * s + beta * a + w)
    return -2 * rho * a + u + gamma * beta * (2 * p * mean_next + l)


def moments(model, theta):
    """(Z, M, S2) = sum_t gamma^t (1, E s_t, E s_t^2) under the policy theta."""
    alpha, beta, q, rho, u, gamma, start, noise = model
    k, c = theta
    lam = alpha + beta * k
    drift = _mean(noise, lambda w: beta * c + w)
    second = _mean(noise, lambda w: (beta * c + w) ** 2)
    m0 = _mean(start, lambda s: s)
    v0 = _mean(start, lambda s: s * s)
    Z = 1 / (1 - gamma)
    M = (m0 + gamma * drift * Z) / (1 - gamma * lam)
    S2 = (v0 + gamma * (2 * lam * drift * M + second * Z)) / (1 - gamma * lam * lam)
    return Z, M, S2


def expected_return(model, theta):
    """J(theta) = E[sum_t gamma^t r(S_t, mu(S_t))]."""
    alpha, beta, q, rho, u, gamma, start, noise = model
    k, c = theta
    Z, M, S2 = moments(model, theta)
    # r(s, k s + c) = -(q + rho k^2) s^2 + (u k - 2 rho k c) s + (u c - rho c^2)
    return -(q + rho * k * k) * S2 + (u * k - 2 * rho * k * c) * M + (u * c - rho * c * c) * Z


def deterministic_policy_gradient(model, theta):
    """sum_t gamma^t E[grad_theta mu(S_t) d_a Q(S_t, a) at a = mu(S_t)], with grad_theta mu(s) = (s, 1)."""
    k, c = theta
    Z, M, S2 = moments(model, theta)
    # d_a Q(s, mu(s)) is linear in s: g1 s + g0
    g0 = q_action_derivative(model, theta, 0 * k, c)
    g1 = q_action_derivative(model, theta, 1 + 0 * k, k + c) - g0
    return (g1 * S2 + g0 * M, g1 * M + g0 * Z)


def gaussian_moment(n):
    """E[Z^n] for a standard normal Z."""
    if n % 2:
        return 0
    out = 1
    for j in range(1, n, 2):
        out *= j
    return out


def stochastic_gradient_one_step(coeffs, theta, sigma2):
    """d/d theta E[r(A)] for A ~ N(theta, sigma2) and r(a) = sum_j coeffs[j] a^j, by the score function formula.

    E[(A - theta) / sigma2 r(A)] = E[Z r(theta + sigma Z)] / sigma; only odd powers of sigma Z survive,
    so the result is a polynomial in sigma2 and stays exact for rational inputs.
    """
    out = 0 * theta
    for j, cj in enumerate(coeffs):
        for i in range(1, j + 1, 2):  # sigma^(i - 1) = sigma2^((i - 1) / 2)
            out += cj * comb(j, i) * theta ** (j - i) * sigma2 ** ((i - 1) // 2) * gaussian_moment(i + 1)
    return out


def deterministic_gradient_one_step(coeffs, theta):
    """d/d theta r(theta) for a deterministic policy that plays theta."""
    return sum(j * cj * theta ** (j - 1) for j, cj in enumerate(coeffs) if j)
