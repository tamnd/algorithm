# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/value-function-approximation/. The authors are listed in prov/0BFJGH.jsonl.

"""Linear value function approximation for a fixed policy on a finite Markov chain.

The chain has transition matrix P (the MDP under the policy), expected rewards r, discount gamma < 1
and features phi(s) in R^d (the rows of Phi). mu is the stationary distribution and D = diag(mu).
The TD fixed point solves A theta = b with A = Phi^T D (I - gamma P) Phi and b = Phi^T D r.
"""

import random
from fractions import Fraction
from typing import Sequence

Number = float | Fraction
Matrix = list[list[Number]]


def solve(a: Matrix, b: Sequence[Number]) -> list[Number]:
    """Solve a x = b by Gaussian elimination with partial pivoting. Exact for Fractions. O(d^3)."""
    n = len(b)
    m = [list(row) + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        p = max(range(c, n), key=lambda i: abs(m[i][c]))
        if m[p][c] == 0:
            raise ValueError("singular matrix")
        m[c], m[p] = m[p], m[c]
        for i in range(n):
            if i != c and m[i][c] != 0:
                f = m[i][c] / m[c][c]
                m[i] = [u - f * v for u, v in zip(m[i], m[c])]
    return [m[i][n] / m[i][i] for i in range(n)]


def true_values(p: Matrix, r: Sequence[Number], gamma: Number) -> list[Number]:
    """V = (I - gamma P)^(-1) r."""
    n = len(r)
    a = [[(1 if i == j else 0) - gamma * p[i][j] for j in range(n)] for i in range(n)]
    return solve(a, r)


def stationary_distribution(p: Matrix) -> list[Number]:
    """The mu with mu P = mu and sum mu = 1, for an irreducible chain."""
    n = len(p)
    a = [[p[j][i] - (1 if i == j else 0) for j in range(n)] for i in range(n - 1)]
    a.append([1] * n)
    return solve(a, [0] * (n - 1) + [1])


def td_matrices(p: Matrix, r: Sequence[Number], gamma: Number, phi: Matrix, mu: Sequence[Number]) -> tuple[Matrix, list[Number]]:
    """A = Phi^T D (I - gamma P) Phi and b = Phi^T D r."""
    n, d = len(phi), len(phi[0])
    pphi = [[sum(p[s][t] * phi[t][k] for t in range(n)) for k in range(d)] for s in range(n)]
    a = [[sum(mu[s] * phi[s][i] * (phi[s][j] - gamma * pphi[s][j]) for s in range(n)) for j in range(d)] for i in range(d)]
    b = [sum(mu[s] * phi[s][i] * r[s] for s in range(n)) for i in range(d)]
    return a, b


def td_fixed_point(p: Matrix, r: Sequence[Number], gamma: Number, phi: Matrix, mu: Sequence[Number]) -> list[Number]:
    """The theta with Phi theta = Pi T Phi theta, from A theta = b."""
    a, b = td_matrices(p, r, gamma, phi, mu)
    return solve(a, b)


def projection_weights(v: Sequence[Number], phi: Matrix, mu: Sequence[Number]) -> list[Number]:
    """The theta that minimizes ||Phi theta - v||_D, from the normal equations Phi^T D Phi theta = Phi^T D v."""
    n, d = len(phi), len(phi[0])
    c = [[sum(mu[s] * phi[s][i] * phi[s][j] for s in range(n)) for j in range(d)] for i in range(d)]
    rhs = [sum(mu[s] * phi[s][i] * v[s] for s in range(n)) for i in range(d)]
    return solve(c, rhs)


def d_norm2(v: Sequence[Number], mu: Sequence[Number]) -> Number:
    """||v||_D^2 = sum_s mu(s) v(s)^2."""
    return sum(m * x * x for m, x in zip(mu, v))


def semi_gradient_td0(
    p: Sequence[Sequence[float]],
    rewards: Sequence[float],
    gamma: float,
    phi: Sequence[Sequence[float]],
    steps: int,
    alpha0: float,
    rng: random.Random,
    s0: int = 0,
) -> list[float]:
    """Semi-gradient TD(0) with linear features along one trajectory of the chain (on-policy).

    theta <- theta + alpha_t (r(s) + gamma phi(s')^T theta - phi(s)^T theta) phi(s), with
    alpha_t = alpha0 / (1 + t / 1000), which meets the Robbins-Monro conditions. O(d) per step.
    """
    d = len(phi[0])
    theta = [0.0] * d  # @line L1
    s = s0  # @line L2
    n = len(p)
    for t in range(steps):  # @line L3
        s_next = rng.choices(range(n), weights=p[s])[0]  # @line L4
        v = sum(phi[s][k] * theta[k] for k in range(d))
        v_next = sum(phi[s_next][k] * theta[k] for k in range(d))
        delta = rewards[s] + gamma * v_next - v  # @line L5
        alpha = alpha0 / (1.0 + t / 1000.0)
        theta = [theta[k] + alpha * delta * phi[s][k] for k in range(d)]  # @line L6
        s = s_next  # @line L7
    return theta  # @line L8
