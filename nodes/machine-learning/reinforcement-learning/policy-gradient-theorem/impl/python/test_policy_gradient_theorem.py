# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/policy-gradient-theorem/. The authors are listed in prov/57DPX1.jsonl.

import math
import random
from fractions import Fraction as F

from policy_gradient_theorem import (
    average_reward_gradient,
    compatible_weights,
    objective,
    softmax,
    solve,
    theorem_gradient,
    values,
    visitation,
)

# The example of the page: two states, two actions, episodes end with the missing mass.
P = [
    [[F(1, 2), F(1, 4)], [F(0), F(3, 4)]],
    [[F(1, 2), F(0)], [F(0), F(0)]],
]
R = [[F(1), F(0)], [F(0), F(3)]]
MU = [F(1), F(0)]
GAMMA = F(1, 2)
UNIFORM = [[F(1, 2), F(1, 2)], [F(1, 2), F(1, 2)]]


def exact_derivative(P, R, gamma, pi, mu):
    """Oracle: differentiate (I - gamma P_pi) V = r_pi, so dV = (I - gamma P_pi)^-1 (dr + gamma dP V)."""
    n, k = len(P), len(pi[0])
    V, _ = values(P, R, gamma, pi)
    M = [[(1 if s == t else 0) - gamma * sum(pi[s][a] * P[s][a][t] for a in range(k)) for t in range(n)] for s in range(n)]
    out = []
    for s0 in range(n):
        row = []
        for b in range(k):
            rhs = [F(0)] * n
            for a in range(k):
                dp = pi[s0][a] * ((1 if a == b else 0) - pi[s0][b])
                rhs[s0] += dp * (R[s0][a] + gamma * sum(P[s0][a][t] * V[t] for t in range(n)))
            dV = solve(M, rhs)
            row.append(sum(m * x for m, x in zip(mu, dV)))
        out.append(row)
    return out


def random_mdp(rng, n, k, terminal=True):
    P = []
    for _ in range(n):
        rows = []
        for _ in range(k):
            w = [rng.randint(0, 4) for _ in range(n + (1 if terminal else 0))]
            if sum(w) == 0:
                w[-1] = 1
            rows.append([F(x, sum(w)) for x in w[:n]])
        P.append(rows)
    R = [[F(rng.randint(-3, 3)) for _ in range(k)] for _ in range(n)]
    return P, R


def random_policy(rng, n, k):
    pi = []
    for _ in range(n):
        w = [rng.randint(1, 5) for _ in range(k)]
        pi.append([F(x, sum(w)) for x in w])
    return pi


def test_solve():
    M = [[F(2), F(1)], [F(1), F(3)]]
    x = solve(M, [F(3), F(5)])
    assert [M[0][0] * x[0] + M[0][1] * x[1], M[1][0] * x[0] + M[1][1] * x[1]] == [3, 5]


def test_example_values():
    V, Q = values(P, R, GAMMA, UNIFORM)
    assert V == [F(28, 27), F(44, 27)]
    assert Q == [[F(79, 54), F(11, 18)], [F(7, 27), F(3)]]
    d = visitation(P, GAMMA, UNIFORM, MU)
    assert d == [F(32, 27), F(8, 27)]
    g = theorem_gradient(P, R, GAMMA, UNIFORM, MU)
    assert g == [[F(184, 729), F(-184, 729)], [F(-148, 729), F(148, 729)]]
    assert g == exact_derivative(P, R, GAMMA, UNIFORM, MU)


def test_theorem_exact_on_random_mdps():
    rng = random.Random(7)
    for _ in range(40):
        n, k = rng.randint(1, 3), rng.randint(2, 3)
        P2, R2 = random_mdp(rng, n, k)
        pi = random_policy(rng, n, k)
        mu = random_policy(rng, 1, n)[0]
        gamma = F(rng.randint(1, 9), 10)
        assert theorem_gradient(P2, R2, gamma, pi, mu) == exact_derivative(P2, R2, gamma, pi, mu)


def test_theorem_against_finite_differences():
    theta = [[0.3, -0.2], [0.5, 0.1]]
    Pf = [[[float(x) for x in row] for row in rows] for rows in P]
    Rf = [[float(x) for x in row] for row in R]
    g = theorem_gradient(Pf, Rf, 0.9, softmax(theta), [1.0, 0.0])
    h = 1e-5
    for s in range(2):
        for a in range(2):
            tp = [row[:] for row in theta]
            tm = [row[:] for row in theta]
            tp[s][a] += h
            tm[s][a] -= h
            fd = (objective(Pf, Rf, 0.9, softmax(tp), [1.0, 0.0]) - objective(Pf, Rf, 0.9, softmax(tm), [1.0, 0.0])) / (2 * h)
            assert abs(fd - g[s][a]) < 1e-7


def test_baseline_leaves_gradient_unchanged():
    rng = random.Random(3)
    for _ in range(20):
        b = [F(rng.randint(-9, 9), rng.randint(1, 5)) for _ in range(2)]
        pi = random_policy(rng, 2, 2)
        assert theorem_gradient(P, R, GAMMA, pi, MU, baseline=b) == theorem_gradient(P, R, GAMMA, pi, MU)


def test_compatible_function_approximation():
    rng = random.Random(11)
    for _ in range(15):
        n, k = rng.randint(1, 3), rng.randint(2, 3)
        P2, R2 = random_mdp(rng, n, k)
        pi = random_policy(rng, n, k)
        mu = random_policy(rng, 1, n)[0]
        w = compatible_weights(P2, R2, GAMMA, pi, mu)
        f = [[sum(((1 if a == j else 0) - pi[s][j]) * w[s][j] for j in range(k)) for a in range(k)] for s in range(n)]
        assert theorem_gradient(P2, R2, GAMMA, pi, mu, Q=f) == theorem_gradient(P2, R2, GAMMA, pi, mu)


def test_dropping_gamma_t_is_biased():
    n = len(P)
    d1 = visitation(P, F(1), UNIFORM, MU)  # undiscounted visits, finite because episodes end
    assert d1 == [F(8, 5), F(4, 5)]
    biased = theorem_gradient(P, R, GAMMA, UNIFORM, MU, weights=d1)
    true = theorem_gradient(P, R, GAMMA, UNIFORM, MU)
    assert biased != true
    # one parameter w shared by both states (theta[s][0] = w, theta[s][1] = 0): the sign flips
    assert true[0][0] + true[1][0] == F(4, 81)
    assert biased[0][0] + biased[1][0] == F(-28, 135)
    # with gamma = 1 the two weightings agree
    assert theorem_gradient(P, R, F(1), UNIFORM, MU, weights=d1) == exact_derivative(P, R, F(1), UNIFORM, MU)
    assert n == 2


def test_average_reward_setting():
    Pc = [[[0.7, 0.3], [0.1, 0.9]], [[0.6, 0.4], [0.2, 0.8]]]
    Rc = [[1.0, 0.0], [0.0, 2.0]]
    theta = [[0.2, -0.4], [0.1, 0.3]]

    def rho(th):
        return average_reward_gradient(Pc, Rc, softmax(th))[1]

    g, _ = average_reward_gradient(Pc, Rc, softmax(theta))
    h = 1e-6
    for s in range(2):
        for a in range(2):
            tp = [row[:] for row in theta]
            tm = [row[:] for row in theta]
            tp[s][a] += h
            tm[s][a] -= h
            assert abs((rho(tp) - rho(tm)) / (2 * h) - g[s][a]) < 1e-7
    assert math.isfinite(rho(theta))
