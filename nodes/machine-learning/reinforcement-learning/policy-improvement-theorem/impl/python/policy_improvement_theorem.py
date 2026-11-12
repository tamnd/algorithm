# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/policy-improvement-theorem/. The authors are listed in prov/ZMPCA4.jsonl.

"""The policy improvement theorem, as exact computations on a finite discounted MDP.

P[s][a] is a list of pairs (p, t), the probability p of the next state t, and
R[s][a] is the expected reward. Policies are deterministic: pi[s] is an action.
Use Fractions for exact results; floats also work but ties become unreliable.
"""


def evaluate(P, R, gamma, pi):
    """V^pi, the solution of (I - gamma P_pi) V = r_pi, by Gauss-Jordan elimination."""
    n = len(P)
    M = [[(gamma ** 0) * (i == j) for j in range(n)] + [R[i][pi[i]]] for i in range(n)]
    for s in range(n):
        for p, t in P[s][pi[s]]:
            M[s][t] -= gamma * p
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[piv] = M[piv], M[c]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c] / M[c][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]


def q_value(P, R, gamma, V, s, a):
    """Q(s, a) = R(s, a) + gamma * sum_t P(t | s, a) V(t)."""
    return R[s][a] + gamma * sum(p * V[t] for p, t in P[s][a])


def gain(P, R, gamma, pi, pi2):
    """g(s) = Q^pi(s, pi2(s)) - V^pi(s). The theorem's premise is g >= 0."""
    V = evaluate(P, R, gamma, pi)
    return [q_value(P, R, gamma, V, s, pi2[s]) - V[s] for s in range(len(P))]


def improve(P, R, gamma, pi):
    """Return the greedy policy for V^pi, keeping pi[s] when it is a maximizer.

    By the theorem, V^improve(pi) >= V^pi in every state, with strict
    inequality in every state where the action changed.
    """
    V = evaluate(P, R, gamma, pi)  # @line L1
    out = []
    for s in range(len(P)):  # @line L2
        q = [q_value(P, R, gamma, V, s, a) for a in range(len(P[s]))]  # @line L3
        best = max(q)
        out.append(pi[s] if q[pi[s]] == best else q.index(best))  # @line L4
    return out  # @line L5
