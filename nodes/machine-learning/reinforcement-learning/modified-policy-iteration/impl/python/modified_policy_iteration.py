# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/modified-policy-iteration/. The authors are listed in prov/1RG9V7.jsonl.

"""Modified policy iteration (Puterman and Shin 1978) for a discounted finite MDP.

P[s][a] is a list of pairs (p, t), the probability p of the next state t,
and R[s][a] is the expected reward. Numbers may be floats or Fractions.
The order m is the number of extra backups with the fixed policy in each
iteration: m = 0 gives value iteration, m = None (infinity) gives policy
iteration with an exact solve of the linear system.
"""


def _q(P, R, gamma, V, s, a):
    return R[s][a] + gamma * sum(p * V[t] for p, t in P[s][a])


def _greedy(P, R, gamma, V, pi):
    """Greedy policy for V. Keep pi[s] when it is a maximizer, else take the first maximizer."""
    out = []
    for s in range(len(P)):
        q = [_q(P, R, gamma, V, s, a) for a in range(len(P[s]))]
        best = max(q)
        out.append(pi[s] if q[pi[s]] == best else q.index(best))
    return out


def _backup(P, R, gamma, V, pi):
    """One backup with the fixed policy pi: return T^pi V."""
    return [_q(P, R, gamma, V, s, pi[s]) for s in range(len(P))]


def _solve(A, b):
    n = len(b)
    M = [list(A[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[p] = M[p], M[c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]
            for j in range(c, n + 1):
                M[r][j] -= f * M[c][j]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (M[i][n] - sum(M[i][j] * x[j] for j in range(i + 1, n))) / M[i][i]
    return x


def _evaluate(P, R, gamma, pi):
    n = len(P)
    A = [[(gamma ** 0) * (i == j) for j in range(n)] for i in range(n)]
    for s in range(n):
        for p, t in P[s][pi[s]]:
            A[s][t] -= gamma * p
    return _solve(A, [R[s][pi[s]] for s in range(n)])


def modified_policy_iteration(P, R, gamma, m, eps, v0=None, max_iter=None, history=None):
    """Return (V, pi, k): the last iterate, an eps-optimal policy and the number of iterations.

    Precondition: 0 < gamma < 1, eps > 0, m >= 0 or m is None (infinity).
    Iteration k: pi greedy for V, U = T V; stop if |U - V| < eps (1 - gamma) / (2 gamma)
    in the max norm and return U with a policy greedy for U; else V = (T^pi)^m U.
    If v0 satisfies T v0 >= v0, the iterates lie between T^k v0 and V*.
    Cost per iteration: O(S^2 A + m S^2), or O(S^3 + S^2 A) for m = None.
    If history is a list, the pair (pi, V) of each iteration is appended to it.
    """
    n = len(P)
    V = [0 * gamma] * n if v0 is None else list(v0)  # @line L1
    pi = [0] * n
    stop = eps * (1 - gamma) / (2 * gamma)
    k = 0
    while max_iter is None or k < max_iter:  # @line L2
        k += 1
        pi = _greedy(P, R, gamma, V, pi)  # @line L3
        U = _backup(P, R, gamma, V, pi)  # @line L4
        if max((abs(U[s] - V[s]) for s in range(n)), default=0) < stop:  # @line L5
            return U, _greedy(P, R, gamma, U, pi), k  # @line L6
        if m is None:  # @line L7
            U = _evaluate(P, R, gamma, pi)  # @line L8
        else:
            for _ in range(m):  # @line L9
                U = _backup(P, R, gamma, U, pi)  # @line L10
        V = U  # @line L11
        if history is not None:
            history.append((list(pi), list(V)))
    return V, _greedy(P, R, gamma, V, pi), k
