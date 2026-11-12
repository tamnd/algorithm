# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/natural-policy-gradient/. The authors are listed in prov/DXW2GN.jsonl.

import math
import random
from fractions import Fraction as F

from natural_policy_gradient import (
    gradient_and_fisher,
    natural_gradient,
    npg,
    npg_exact,
    policy,
    score,
    solve,
    values,
    visitation,
)

P = [
    [[F(1, 2), F(1, 4)], [F(0), F(3, 4)]],
    [[F(1, 2), F(0)], [F(0), F(0)]],
]
R = [[F(1), F(0)], [F(0), F(3)]]
MU = [F(1), F(0)]
GAMMA = F(1, 2)
UNIFORM = [[F(1, 2), F(1, 2)], [F(1, 2), F(1, 2)]]


def tabular(n, k):
    return [[[1 if i == s * k + a else 0 for i in range(n * k)] for a in range(k)] for s in range(n)]


def random_mdp(rng, n, k, rewards01=False):
    Pm = []
    for _ in range(n):
        rows = []
        for _ in range(k):
            w = [rng.randint(0, 4) for _ in range(n + 1)]
            if sum(w) == 0:
                w[-1] = 1
            rows.append([F(x, sum(w)) for x in w[:n]])
        Pm.append(rows)
    Rm = [[F(rng.randint(0, 4), 4) if rewards01 else F(rng.randint(-3, 3)) for _ in range(k)] for _ in range(n)]
    return Pm, Rm


def random_policy(rng, n, k):
    out = []
    for _ in range(n):
        w = [rng.randint(1, 5) for _ in range(k)]
        out.append([F(x, sum(w)) for x in w])
    return out


def test_example():
    phi = tabular(2, 2)
    g, Fm = gradient_and_fisher(P, R, GAMMA, UNIFORM, MU, phi)
    assert g == [F(184, 729), F(-184, 729), F(-148, 729), F(148, 729)]
    # block s of F is d(s) (diag(pi) - pi pi^T) with d = (32/27, 8/27)
    assert Fm == [
        [F(8, 27), F(-8, 27), 0, 0],
        [F(-8, 27), F(8, 27), 0, 0],
        [0, 0, F(2, 27), F(-2, 27)],
        [0, 0, F(-2, 27), F(2, 27)],
    ]
    x = natural_gradient(P, R, GAMMA, UNIFORM, MU, phi)
    # the advantages are A(0, .) = (23/54, -23/54) and A(1, .) = (-37/27, 37/27)
    assert [x[0] - x[1], x[2] - x[3]] == [F(23, 27), F(-74, 27)]


def test_tabular_fisher_is_block_diagonal_and_natural_gradient_is_advantage():
    rng = random.Random(1)
    for _ in range(30):
        n, k = rng.randint(1, 3), rng.randint(2, 3)
        Pm, Rm = random_mdp(rng, n, k)
        pi = random_policy(rng, n, k)
        mu = random_policy(rng, 1, n)[0]
        phi = tabular(n, k)
        g, Fm = gradient_and_fisher(Pm, Rm, GAMMA, pi, mu, phi)
        d = visitation(Pm, GAMMA, pi, mu)
        V, Q = values(Pm, Rm, GAMMA, pi)
        for s in range(n):
            for a in range(k):
                for t in range(n):
                    for b in range(k):
                        want = d[s] * (pi[s][a] * (1 if a == b else 0) - pi[s][a] * pi[s][b]) if s == t else 0
                        assert Fm[s * k + a][t * k + b] == want
        x = natural_gradient(Pm, Rm, GAMMA, pi, mu, phi)
        assert [sum(Fm[i][j] * x[j] for j in range(n * k)) for i in range(n * k)] == g
        for s in range(n):
            c = x[s * k] - (Q[s][0] - V[s])
            assert all(x[s * k + a] - (Q[s][a] - V[s]) == c for a in range(k))


def error(Pm, Rm, gamma, pi, mu, phi, w):
    """epsilon(w) = sum_s d(s) sum_a pi(a|s) (w . psi(s,a) - Q(s,a))^2 (Kakade, Section 3.1)."""
    _, Q = values(Pm, Rm, gamma, pi)
    d = visitation(Pm, gamma, pi, mu)
    tot = 0
    for s in range(len(Pm)):
        for a in range(len(pi[s])):
            f = sum(wi * p for wi, p in zip(w, score(pi, phi, s, a)))
            tot += d[s] * pi[s][a] * (f - Q[s][a]) ** 2
    return tot


def test_compatible_function_approximation():
    rng = random.Random(2)
    for _ in range(20):
        n, k, m = rng.randint(1, 3), rng.randint(2, 3), rng.randint(1, 4)
        Pm, Rm = random_mdp(rng, n, k)
        pi = random_policy(rng, n, k)
        mu = random_policy(rng, 1, n)[0]
        phi = [[[F(rng.randint(-2, 2)) for _ in range(m)] for _ in range(k)] for _ in range(n)]
        x = natural_gradient(Pm, Rm, GAMMA, pi, mu, phi)
        best = error(Pm, Rm, GAMMA, pi, mu, phi, x)
        for _ in range(5):
            v = [F(rng.randint(-3, 3), rng.randint(1, 3)) for _ in range(m)]
            assert error(Pm, Rm, GAMMA, pi, mu, phi, [a + b for a, b in zip(x, v)]) >= best


def test_invariance_under_reparameterization():
    rng = random.Random(3)
    phi = [[[F(1), F(0), F(2)], [F(0), F(1), F(-1)]], [[F(1), F(1), F(0)], [F(-1), F(2), F(1)]]]
    pi = [[F(1, 3), F(2, 3)], [F(3, 5), F(2, 5)]]
    x = natural_gradient(P, R, GAMMA, pi, MU, phi)
    for _ in range(5):
        while True:
            B = [[F(rng.randint(-3, 3)) for _ in range(3)] for _ in range(3)]
            det = (B[0][0] * (B[1][1] * B[2][2] - B[1][2] * B[2][1]) - B[0][1] * (B[1][0] * B[2][2] - B[1][2] * B[2][0])
                   + B[0][2] * (B[1][0] * B[2][1] - B[1][1] * B[2][0]))
            if det != 0:
                break
        # theta = B xi, so theta . phi = xi . (B^T phi)
        phi2 = [[[sum(B[i][j] * f[i] for i in range(3)) for j in range(3)] for f in rows] for rows in phi]
        y = natural_gradient(P, R, GAMMA, pi, MU, phi2)
        By = [sum(B[i][j] * y[j] for j in range(3)) for i in range(3)]
        # F is singular here (rank 2), so compare the first-order change of log pi, psi . step, for every (s, a)
        for s in range(2):
            for a in range(2):
                psi = score(pi, phi, s, a)
                assert sum(p * u for p, u in zip(psi, By)) == sum(p * u for p, u in zip(psi, x))
        # the plain gradient is not invariant: the step B h in theta changes log pi differently from g
        g, _ = gradient_and_fisher(P, R, GAMMA, pi, MU, phi)
        h, _ = gradient_and_fisher(P, R, GAMMA, pi, MU, phi2)
        Bh = [sum(B[i][j] * h[j] for j in range(3)) for i in range(3)]
        changes = [(sum(p * u for p, u in zip(score(pi, phi, s, a), Bh)), sum(p * u for p, u in zip(score(pi, phi, s, a), g))) for s in range(2) for a in range(2)]
        assert any(c1 != c2 for c1, c2 in changes)


def test_monotone_improvement_and_rate():
    rng = random.Random(4)
    for _ in range(5):
        n, k, gamma = 3, 3, 0.9
        Pm, Rm = random_mdp(rng, n, k, rewards01=True)
        Pf = [[[float(x) for x in r] for r in rows] for rows in Pm]
        Rf = [[float(x) for x in r] for r in Rm]
        mu = [1 / 3] * 3
        phi = tabular(n, k)
        V = [0.0] * n
        for _ in range(2000):  # value iteration for V*
            V = [max(Rf[s][a] + gamma * sum(Pf[s][a][t] * V[t] for t in range(n)) for a in range(k)) for s in range(n)]
        eta = 1.0  # theta <- theta + eta / (1 - gamma) A, the step of Agarwal et al.
        thetas = npg_exact(Pf, Rf, gamma, mu, [0.0] * (n * k), phi, eta / (1 - gamma), 60)
        prev = None
        for T, th in enumerate(thetas):
            Vt, _ = values(Pf, Rf, gamma, policy(th, phi))
            if prev is not None:
                assert all(v >= p - 1e-9 for v, p in zip(Vt, prev))  # every state improves
            prev = Vt
            if T >= 1:
                gap = max(V[s] - Vt[s] for s in range(n))
                assert gap <= math.log(k) / (eta * T) + 1 / ((1 - gamma) ** 2 * T) + 1e-9


def test_solve_consistent_singular():
    M = [[F(1), F(-1)], [F(-1), F(1)]]
    x = solve(M, [F(2), F(-2)])
    assert x[0] - x[1] == 2


def test_sampled_npg_learns():
    Pf = [[[float(x) for x in r] for r in rows] for rows in P]
    Rf = [[float(x) for x in r] for r in R]
    phi = tabular(2, 2)
    theta = npg(Pf, Rf, 0.5, [1.0, 0.0], [0.0] * 4, phi, 0.5, 15, 100, random.Random(0))
    pi = policy(theta, phi)
    assert pi[0][0] > 0.9 and pi[1][1] > 0.9
