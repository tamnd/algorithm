# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/policy-gradient-theorem/. The authors are listed in prov/57DPX1.jsonl.

"""The policy gradient theorem as exact computations on a small finite MDP.

An MDP is (P, R): P[s][a][t] is the probability of the next state t after
action a in state s, and R[s][a] is the expected reward. A row of P may sum to
less than 1; the missing mass is the probability that the episode ends. The
policy is a tabular softmax, pi[s][a] = exp(theta[s][a]) / sum_b exp(theta[s][b]),
given here by its probabilities, so that rational probabilities give exact
Fraction results. For this policy d pi(a|s) / d theta[s][b] = pi(a|s) (1[a = b] - pi(b|s)).

Cost: one linear solve of size S, O(S^3), plus O(S^2 A) to build the system.
"""

import math


def solve(M, b):
    """Solve M x = b by Gaussian elimination with pivoting (M square, nonsingular)."""
    n = len(M)
    A = [list(M[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(A[r][c]))
        if A[p][c] == 0:
            raise ValueError("singular system")
        A[c], A[p] = A[p], A[c]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c] / A[c][c]
                A[r] = [x - f * y for x, y in zip(A[r], A[c])]
    return [A[i][n] / A[i][i] for i in range(n)]


def softmax(theta):
    """Tabular softmax probabilities (floats) from preferences theta[s][a]."""
    out = []
    for row in theta:
        m = max(row)
        e = [math.exp(x - m) for x in row]
        z = sum(e)
        out.append([x / z for x in e])
    return out


def state_transitions(P, pi):
    """P_pi[s][t] = sum_a pi(a|s) P(t|s,a)."""
    n = len(P)
    return [[sum(pi[s][a] * P[s][a][t] for a in range(len(pi[s]))) for t in range(n)] for s in range(n)]


def values(P, R, gamma, pi):
    """V^pi and Q^pi from the linear Bellman system (I - gamma P_pi) V = r_pi."""
    n = len(P)
    Ppi = state_transitions(P, pi)
    M = [[(1 if s == t else 0) - gamma * Ppi[s][t] for t in range(n)] for s in range(n)]
    r = [sum(pi[s][a] * R[s][a] for a in range(len(pi[s]))) for s in range(n)]
    V = solve(M, r)
    Q = [[R[s][a] + gamma * sum(P[s][a][t] * V[t] for t in range(n)) for a in range(len(P[s]))] for s in range(n)]
    return V, Q


def objective(P, R, gamma, pi, mu):
    """J = sum_s mu(s) V^pi(s), the expected discounted return from the start distribution mu."""
    V, _ = values(P, R, gamma, pi)
    return sum(m * v for m, v in zip(mu, V))


def visitation(P, gamma, pi, mu):
    """d(s) = sum_t gamma^t Pr(S_t = s): solve d (I - gamma P_pi) = mu. Not normalized."""
    n = len(P)
    Ppi = state_transitions(P, pi)
    MT = [[(1 if s == t else 0) - gamma * Ppi[t][s] for t in range(n)] for s in range(n)]
    return solve(MT, list(mu))


def dpi(pi, s, a, b):
    """d pi(a|s) / d theta[s][b] for the tabular softmax policy."""
    return pi[s][a] * ((1 if a == b else 0) - pi[s][b])


def theorem_gradient(P, R, gamma, pi, mu, baseline=None, weights=None, Q=None):
    """grad J[s][b] = sum_a weights(s) d pi(a|s)/d theta[s][b] (Q(s,a) - baseline(s)).

    With the default weights, the discounted visitation d, this is the policy
    gradient theorem. Any baseline gives the same result. Other weights (for
    example the undiscounted visitation) give the common biased estimate.
    """
    if Q is None:
        _, Q = values(P, R, gamma, pi)
    d = visitation(P, gamma, pi, mu) if weights is None else weights
    n, k = len(P), len(pi[0])
    b = baseline if baseline is not None else [0] * n
    return [[d[s] * sum(dpi(pi, s, a, j) * (Q[s][a] - b[s]) for a in range(k)) for j in range(k)] for s in range(n)]


def score(pi, s, a):
    """psi(s, a) = grad log pi(a|s), flattened over (state, action) parameters."""
    n, k = len(pi), len(pi[0])
    out = [0 * pi[0][0]] * (n * k)
    for j in range(k):
        out[s * k + j] = (1 if a == j else 0) - pi[s][j]
    return out


def compatible_weights(P, R, gamma, pi, mu):
    """w that minimizes sum_s d(s) sum_a pi(a|s) (w . psi(s,a) - Q(s,a))^2.

    The normal equations are singular for the tabular softmax (adding a
    constant to theta[s] changes nothing), so we add the constraint
    sum_a w[s][a] = 0 in each state, which picks one minimizer.
    """
    _, Q = values(P, R, gamma, pi)
    d = visitation(P, gamma, pi, mu)
    n, k = len(P), len(pi[0])
    m = n * k
    G = [[0 * pi[0][0]] * m for _ in range(m)]
    h = [0 * pi[0][0]] * m
    for s in range(n):
        for a in range(k):
            f = score(pi, s, a)
            wgt = d[s] * pi[s][a]
            for i in range(m):
                h[i] += wgt * f[i] * Q[s][a]
                for j in range(m):
                    G[i][j] += wgt * f[i] * f[j]
    for s in range(n):  # the normal equations plus the constraint, in a bordered system
        for a in range(k):
            G[s * k + a] = G[s * k + a] + [1 if t == s else 0 for t in range(n)]
    for s in range(n):
        G.append([1 if i // k == s else 0 for i in range(m)] + [0] * n)
        h.append(0)
    w = solve(G, h)[:m]
    return [w[s * k:(s + 1) * k] for s in range(n)]


def stationary(P, pi):
    """The stationary distribution of P_pi for a recurrent chain (rows of P sum to 1)."""
    n = len(P)
    Ppi = state_transitions(P, pi)
    M = [[(1 if s == t else 0) - Ppi[t][s] for t in range(n)] for s in range(n)]
    M[-1] = [1] * n
    return solve(M, [0] * (n - 1) + [1])


def average_reward_gradient(P, R, pi):
    """The theorem in the average reward setting: sum_s d(s) sum_a grad pi(a|s) Q(s,a).

    d is the stationary distribution and Q the differential action values,
    Q(s,a) = R(s,a) - rho + sum_t P(t|s,a) h(t) with h solving the Poisson equation.
    """
    n, k = len(P), len(pi[0])
    d = stationary(P, pi)
    r = [sum(pi[s][a] * R[s][a] for a in range(k)) for s in range(n)]
    rho = sum(x * y for x, y in zip(d, r))
    Ppi = state_transitions(P, pi)
    M = [[(1 if s == t else 0) - Ppi[s][t] for t in range(n)] for s in range(n)]
    M[-1] = [1 if t == n - 1 else 0 for t in range(n)]  # fix h(last) = 0
    h = solve(M, [r[s] - rho for s in range(n - 1)] + [0])
    Q = [[R[s][a] - rho + sum(P[s][a][t] * h[t] for t in range(n)) for a in range(k)] for s in range(n)]
    return [[d[s] * sum(dpi(pi, s, a, j) * Q[s][a] for a in range(k)) for j in range(k)] for s in range(n)], rho
