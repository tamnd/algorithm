# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/policy-improvement-theorem/. The authors are listed in prov/ZMPCA4.jsonl.

import itertools
import random
from fractions import Fraction as F

from policy_improvement_theorem import evaluate, gain, improve


def solve(P, R, g, pi):
    """Independent oracle: V^pi by Gaussian elimination with back substitution, over Fractions."""
    n = len(P)
    A = [[F(int(i == j)) for j in range(n)] for i in range(n)]
    b = [F(R[s][pi[s]]) for s in range(n)]
    for s in range(n):
        for p, t in P[s][pi[s]]:
            A[s][t] -= g * p
    for c in range(n):
        r = next(r for r in range(c, n) if A[r][c] != 0)
        A[c], A[r], b[c], b[r] = A[r], A[c], b[r], b[c]
        for r in range(c + 1, n):
            f = A[r][c] / A[c][c]
            A[r] = [x - f * y for x, y in zip(A[r], A[c])]
            b[r] -= f * b[c]
    x = [F(0)] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x


def random_mdp(rng, n, k):
    P, R = [], []
    for _ in range(n):
        rows = []
        for _ in range(k):
            w = [rng.randrange(4) for _ in range(n)]
            w[rng.randrange(n)] += 1
            rows.append([(F(x, sum(w)), t) for t, x in enumerate(w) if x])
        P.append(rows)
        R.append([F(rng.randint(-3, 3)) for _ in range(k)])
    return P, R


def example():
    P = [[[(1, 0)], [(F(1, 2), 1), (F(1, 2), 0)]], [[(1, 1)], [(1, 0)]]]
    R = [[1, 0], [2, 0]]
    return P, R, F(9, 10)


def test_example():
    P, R, g = example()
    assert evaluate(P, R, g, [0, 0]) == [10, 20]
    assert gain(P, R, g, [0, 0], [1, 0]) == [F(7, 2), 0]
    assert improve(P, R, g, [0, 0]) == [1, 0]
    assert evaluate(P, R, g, [1, 0]) == [F(180, 11), 20]
    assert improve(P, R, g, [1, 0]) == [1, 0]


def test_theorem_on_random_mdps():
    rng = random.Random(41)
    strict = 0
    for _ in range(600):
        n, k = rng.randint(1, 4), rng.randint(1, 3)
        P, R = random_mdp(rng, n, k)
        g = rng.choice([F(1, 2), F(2, 3), F(9, 10)])
        pi = [rng.randrange(k) for _ in range(n)]
        V = solve(P, R, g, pi)
        assert evaluate(P, R, g, pi) == V
        # Any pi2 that satisfies the premise in every state.
        allg = [[gain(P, R, g, pi, [a] * n)[s] for a in range(k)] for s in range(n)]
        ok = [[a for a in range(k) if allg[s][a] >= 0] for s in range(n)]
        pi2 = [rng.choice(ok[s]) for s in range(n)]
        gs = gain(P, R, g, pi, pi2)
        W = solve(P, R, g, pi2)
        d = [w - v for w, v in zip(W, V)]
        assert all(x >= 0 for x in gs)
        assert all(ds >= x for ds, x in zip(d, gs))  # d >= g >= 0
        # The exact identity (I - g P_pi2) d = gain.
        for s in range(n):
            assert d[s] - g * sum(p * d[t] for p, t in P[s][pi2[s]]) == gs[s]
        if any(x > 0 for x in gs):
            strict += 1
            assert W != V
    assert strict > 100


def test_premise_reversed():
    """If the gain is <= 0 in every state, the new policy is no better anywhere."""
    rng = random.Random(42)
    for _ in range(500):
        n, k = rng.randint(1, 4), rng.randint(1, 3)
        P, R = random_mdp(rng, n, k)
        g = rng.choice([F(1, 2), F(9, 10)])
        pi = [rng.randrange(k) for _ in range(n)]
        allg = [[gain(P, R, g, pi, [a] * n)[s] for a in range(k)] for s in range(n)]
        pi2 = [rng.choice([a for a in range(k) if allg[s][a] <= 0]) for s in range(n)]
        V, W = solve(P, R, g, pi), solve(P, R, g, pi2)
        assert all(w <= v for w, v in zip(W, V))


def test_greedy_fixed_point_iff_optimal():
    rng = random.Random(43)
    for _ in range(500):
        n, k = rng.randint(1, 3), rng.randint(1, 3)
        P, R = random_mdp(rng, n, k)
        g = rng.choice([F(1, 2), F(2, 3), F(9, 10)])
        values = {pi: solve(P, R, g, pi) for pi in itertools.product(range(k), repeat=n)}
        best = [max(v[s] for v in values.values()) for s in range(n)]
        pi = tuple(rng.randrange(k) for _ in range(n))
        new = tuple(improve(P, R, g, list(pi)))
        assert (new == pi) == (values[pi] == best)
        assert all(w >= v for w, v in zip(values[new], values[pi]))
        if new != pi:
            changed = [s for s in range(n) if new[s] != pi[s]]
            assert all(values[new][s] > values[pi][s] for s in changed)


def test_undiscounted_counterexample():
    """With gamma = 1 and a policy that never ends, the premise holds but the value drops."""
    P = [[[(1, 1)], [(1, 0)]], [[(1, 1)], [(1, 1)]]]  # state 1 is terminal
    R = [[1, 0], [0, 0]]
    pi, pi2 = [0, 0], [1, 0]  # exit at once, or stay forever

    def total(policy, horizon):
        """Expected total reward over the first horizon steps from state 0."""
        dist, out = {0: F(1)}, F(0)
        for _ in range(horizon):
            nxt = {}
            for s, w in dist.items():
                out += w * R[s][policy[s]]
                for p, t in P[s][policy[s]]:
                    nxt[t] = nxt.get(t, 0) + w * p
            dist = nxt
        return out

    V = [total(pi, 100), 0]
    assert V[0] == 1
    q_stay = R[0][1] + sum(p * V[t] for p, t in P[0][1])
    assert q_stay >= V[0]  # the premise holds with gamma = 1
    assert all(total(pi2, h) == 0 for h in range(1, 60))  # but pi2 collects 0 < 1
