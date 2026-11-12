# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/natural-policy-gradient/. The authors are listed in prov/DXW2GN.jsonl.

"""Natural policy gradient (Kakade 2001) for a linear softmax policy.

An MDP is (P, R): P[s][a][t] is the probability of the next state t, the
missing mass of a row is the probability that the episode ends, and R[s][a] is
the reward. The policy is pi(a|s) proportional to exp(theta . phi[s][a]); with
one-hot features phi it is the tabular softmax. Its score is
psi(s, a) = phi[s][a] - sum_b pi(b|s) phi[s][b].

The exact functions take the probabilities pi directly, so that rational
probabilities give exact Fraction results. d(s) = sum_t gamma^t Pr(S_t = s)
is the discounted visitation, not normalized, as in the policy gradient
theorem: grad J = sum_s d(s) sum_a pi(a|s) psi(s,a) Q(s,a) and
F = sum_s d(s) sum_a pi(a|s) psi(s,a) psi(s,a)^T.

Cost of one exact step: O(S^3 + S A k^2 + k^3) for S states, A actions and k
features. Cost of one sampled step: O(N T A k + N T k^2 + k^3) for N episodes
of length at most T.
"""

import math
import random


def solve(M, b):
    """Solve M x = b by Gauss-Jordan elimination; for a singular but consistent system, free variables are 0."""
    n, m = len(M), len(M[0])
    A = [list(M[i]) + [b[i]] for i in range(n)]
    pivots, r = [], 0
    for c in range(m):
        p = max(range(r, n), key=lambda i: abs(A[i][c]), default=None)
        if p is None or abs(A[p][c]) <= 1e-12 * (1 if isinstance(A[p][c], float) else 0):
            continue
        A[r], A[p] = A[p], A[r]
        for i in range(n):
            if i != r and A[i][c] != 0:
                f = A[i][c] / A[r][c]
                A[i] = [x - f * y for x, y in zip(A[i], A[r])]
        pivots.append(c)
        r += 1
        if r == n:
            break
    x = [0 * b[0]] * m
    for i, c in enumerate(pivots):
        x[c] = A[i][m] / A[i][c]
    return x


def policy(theta, phi):
    """Float softmax probabilities pi[s][a] from theta and features phi[s][a]."""
    out = []
    for rows in phi:
        z = [sum(t * f for t, f in zip(theta, row)) for row in rows]
        m = max(z)
        e = [math.exp(x - m) for x in z]
        out.append([x / sum(e) for x in e])
    return out


def values(P, R, gamma, pi):
    n = len(P)
    M = [[(1 if s == t else 0) - gamma * sum(pi[s][a] * P[s][a][t] for a in range(len(pi[s]))) for t in range(n)] for s in range(n)]
    V = solve(M, [sum(pi[s][a] * R[s][a] for a in range(len(pi[s]))) for s in range(n)])
    Q = [[R[s][a] + gamma * sum(P[s][a][t] * V[t] for t in range(n)) for a in range(len(pi[s]))] for s in range(n)]
    return V, Q


def visitation(P, gamma, pi, mu):
    n = len(P)
    MT = [[(1 if s == t else 0) - gamma * sum(pi[t][a] * P[t][a][s] for a in range(len(pi[t]))) for t in range(n)] for s in range(n)]
    return solve(MT, list(mu))


def score(pi, phi, s, a):
    k = len(phi[s][a])
    return [phi[s][a][i] - sum(pi[s][b] * phi[s][b][i] for b in range(len(pi[s]))) for i in range(k)]


def gradient_and_fisher(P, R, gamma, pi, mu, phi):
    """Exact (grad J, F) for the start-state objective J = sum_s mu(s) V(s)."""
    _, Q = values(P, R, gamma, pi)
    d = visitation(P, gamma, pi, mu)
    k = len(phi[0][0])
    zero = 0 * pi[0][0]
    g = [zero] * k
    F = [[zero] * k for _ in range(k)]
    for s in range(len(P)):
        for a in range(len(pi[s])):
            psi = score(pi, phi, s, a)
            w = d[s] * pi[s][a]
            for i in range(k):
                g[i] += w * psi[i] * Q[s][a]
                for j in range(k):
                    F[i][j] += w * psi[i] * psi[j]
    return g, F


def natural_gradient(P, R, gamma, pi, mu, phi):
    g, F = gradient_and_fisher(P, R, gamma, pi, mu, phi)
    return solve(F, g)


def npg_exact(P, R, gamma, mu, theta, phi, eta, iterations):
    """Exact natural gradient ascent with a known model; returns the list of thetas."""
    out = [list(theta)]
    for _ in range(iterations):
        x = natural_gradient(P, R, gamma, policy(theta, phi), mu, phi)
        theta = [t + eta * xi for t, xi in zip(theta, x)]
        out.append(theta)
    return out


def sample_episode(P, R, pi, mu, rng, horizon):
    n = len(P)
    s = rng.choices(range(n), weights=mu)[0]
    ep = []
    for _ in range(horizon):
        a = rng.choices(range(len(pi[s])), weights=pi[s])[0]
        ep.append((s, a, R[s][a]))
        u, acc, nxt = rng.random(), 0.0, None
        for t in range(n):
            acc += P[s][a][t]
            if u < acc:
                nxt = t
                break
        if nxt is None:
            break
        s = nxt
    return ep


def npg(P, R, gamma, mu, theta, phi, eta, iterations, episodes, rng, damping=1e-3, horizon=200):
    """Sample-based natural policy gradient with Monte Carlo advantages and a fitted tabular baseline."""
    k = len(theta)
    theta = list(theta)
    b = [0.0] * len(P)
    for _ in range(iterations):  # @line L1
        pi = policy(theta, phi)
        batch = [sample_episode(P, R, pi, mu, rng, horizon) for _ in range(episodes)]  # @line L2
        g = [0.0] * k
        F = [[0.0] * k for _ in range(k)]
        visits = [[0.0, 0] for _ in P]
        for ep in batch:
            G = 0.0
            for t in range(len(ep) - 1, -1, -1):
                s, a, r = ep[t]
                G = r + gamma * G
                adv = G - b[s]  # @line L3
                visits[s][0] += G
                visits[s][1] += 1
                psi = score(pi, phi, s, a)
                w = gamma ** t / episodes
                for i in range(k):
                    g[i] += w * adv * psi[i]  # @line L4
                    for j in range(k):
                        F[i][j] += w * psi[i] * psi[j]  # @line L5
        for i in range(k):
            F[i][i] += damping
        x = solve(F, g)  # @line L6
        theta = [t + eta * xi for t, xi in zip(theta, x)]  # @line L7
        b = [tot / cnt if cnt else old for (tot, cnt), old in zip(visits, b)]
    return theta
