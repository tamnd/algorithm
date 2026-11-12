# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-programming-for-mdps/. The authors are listed in prov/YX6WMJ.jsonl.

"""The linear program of a discounted finite MDP, solved by an exact simplex method.

P[s][a] is a list of pairs (p, t), the probability p of the next state t, and
R[s][a] is the expected reward. Use ints or Fractions: the arithmetic is exact.

Primal:  minimize   sum_s alpha(s) V(s)
         subject to V(s) - gamma sum_t P(t | s, a) V(t) >= R(s, a) for each (s, a).
Dual:    maximize   sum_(s,a) R(s, a) x(s, a)
         subject to sum_a x(t, a) - gamma sum_(s,a) P(t | s, a) x(s, a) = alpha(t) for each t,
                    x >= 0.
The simplex method runs on the dual. It starts from the basis of a policy pi0,
uses Dantzig's rule (largest reduced cost, the smallest column on ties), and
returns the occupancy measure x, the values V (the simplex multipliers) and the
optimal policy read from x.
"""

from fractions import Fraction


def _solve(M, b):
    """Solve M z = b exactly by Gauss-Jordan elimination. M is a nonsingular square matrix."""
    n = len(b)
    T = [[Fraction(v) for v in M[i]] + [Fraction(b[i])] for i in range(n)]
    for c in range(n):
        p = next(r for r in range(c, n) if T[r][c] != 0)
        T[c], T[p] = T[p], T[c]
        for r in range(n):
            if r != c and T[r][c] != 0:
                f = T[r][c] / T[c][c]
                T[r] = [x - f * y for x, y in zip(T[r], T[c])]
    return [T[i][n] / T[i][i] for i in range(n)]


def lp_mdp(P, R, gamma, alpha=None, pi0=None, history=None):
    """Return (V, x, pi, pivots).

    V[s] is the optimal value, x[(s, a)] the optimal occupancy measure, pi the
    optimal deterministic policy (pi[s] is the action with x[(s, a)] > 0), and
    pivots the number of simplex pivots. Preconditions: 0 <= gamma < 1, every
    alpha(s) > 0 (default 1). If history is a list, the policy of each basis is
    appended to it.
    """
    n = len(P)
    gamma = Fraction(gamma)
    alpha = [Fraction(1)] * n if alpha is None else [Fraction(v) for v in alpha]
    cols = [(s, a) for s in range(n) for a in range(len(P[s]))]
    A = []
    for s, a in cols:  # @line L1
        col = [Fraction(0)] * n
        col[s] += 1
        for p, t in P[s][a]:
            col[t] -= gamma * Fraction(p)
        A.append(col)
    c = [Fraction(R[s][a]) for s, a in cols]
    pi0 = [0] * n if pi0 is None else pi0
    basis = [cols.index((s, pi0[s])) for s in range(n)]  # @line L2
    pivots = 0
    while True:  # @line L3
        if history is not None:
            history.append([cols[j][1] for j in sorted(basis, key=lambda j: cols[j][0])])
        B = [[A[j][k] for j in basis] for k in range(n)]  # B[k][i] = A[basis[i]][k]
        y = _solve([A[j] for j in basis], [c[j] for j in basis])  # @line L4
        red = [c[j] - sum(A[j][k] * y[k] for k in range(n)) for j in range(len(cols))]  # @line L5
        xB = _solve(B, alpha)
        best = max(red)
        if best <= 0:  # @line L6
            x = {col: Fraction(0) for col in cols}
            for i, j in enumerate(basis):
                x[cols[j]] = xB[i]
            pi = [0] * n
            for (s, a), v in x.items():
                if v > 0:
                    pi[s] = a
            return y, x, pi, pivots
        e = red.index(best)  # @line L7
        u = _solve(B, A[e])  # @line L8
        rows = [i for i in range(n) if u[i] > 0]
        if not rows:
            raise ValueError("unbounded dual: check that 0 <= gamma < 1")
        r = min(rows, key=lambda i: (xB[i] / u[i], basis[i]))
        basis[r] = e  # @line L9
        pivots += 1
