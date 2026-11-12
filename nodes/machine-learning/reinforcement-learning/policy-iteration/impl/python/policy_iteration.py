# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/policy-iteration/. The authors are listed in prov/BW714H.jsonl.

"""Howard's policy iteration for a finite MDP with the discounted criterion.

P[s][a] is a list of pairs (p, t), the probability p of the next state t,
and R[s][a] is the expected reward. Numbers may be floats or Fractions;
with Fractions every step is exact.
"""


def solve_linear(A, b):
    """Solve A x = b by Gaussian elimination with partial pivoting. O(n^3)."""
    n = len(b)
    M = [list(A[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[p] = M[p], M[c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]
            if f:
                for j in range(c, n + 1):
                    M[r][j] -= f * M[c][j]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (M[i][n] - sum(M[i][j] * x[j] for j in range(i + 1, n))) / M[i][i]
    return x


def evaluate_policy(P, R, gamma, pi):
    """Return V^pi, the solution of (I - gamma P_pi) V = r_pi."""
    n = len(P)
    A = [[(1 if i == j else 0) * (gamma ** 0) for j in range(n)] for i in range(n)]
    for s in range(n):
        for p, t in P[s][pi[s]]:
            A[s][t] -= gamma * p
    return solve_linear(A, [R[s][pi[s]] for s in range(n)])


def policy_iteration(P, R, gamma, pi0=None, tol=0, history=None):
    """Return (pi, V, k): an optimal deterministic policy, its values, and the number of evaluations.

    Precondition: 0 <= gamma < 1 and each state has at least one action.
    The greedy step keeps pi(s) when pi(s) is a maximizer (up to tol), so the
    loop ends on the first repeated policy. Use tol > 0 with floats, so that
    rounding cannot switch between two equally good actions. Each iteration
    costs O(S^3 + S^2 A) for S states and A actions; at most A^S iterations
    are possible. If history is a list, each pair (pi, V^pi) is appended to it.
    """
    n = len(P)
    pi = [0] * n if pi0 is None else list(pi0)  # @line L1
    k = 0
    while True:  # @line L2
        V = evaluate_policy(P, R, gamma, pi)  # @line L3
        k += 1
        if history is not None:
            history.append((list(pi), V))
        stable = True  # @line L4
        for s in range(n):  # @line L5
            q = [R[s][a] + gamma * sum(p * V[t] for p, t in P[s][a]) for a in range(len(P[s]))]
            best = max(q)
            b = pi[s] if q[pi[s]] >= best - tol else q.index(best)  # @line L6
            if b != pi[s]:  # @line L7
                pi[s], stable = b, False
        if stable:  # @line L8
            return pi, V, k  # @line L9
