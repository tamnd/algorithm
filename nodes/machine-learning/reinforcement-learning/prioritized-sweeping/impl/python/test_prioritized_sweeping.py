# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/prioritized-sweeping/. The authors are listed in prov/NRKTQX.jsonl.

import itertools
import random
from fractions import Fraction as F

from prioritized_sweeping import OnlinePrioritizedSweeping, prioritized_sweeping


def exact_optimum(P, R, g):
    """Independent oracle: V* as the best of V^pi over all deterministic policies, in Fractions."""
    n = len(P)
    best = None
    for pi in itertools.product(*[range(len(P[s])) for s in range(n)]):
        M = [[F(int(i == j)) for j in range(n)] + [F(R[i][pi[i]])] for i in range(n)]
        for s in range(n):
            for p, t in P[s][pi[s]]:
                M[s][t] -= g * F(p)
        for c in range(n):
            r = next(r for r in range(c, n) if M[r][c] != 0)
            M[c], M[r] = M[r], M[c]
            for r in range(n):
                if r != c and M[r][c] != 0:
                    f = M[r][c] / M[c][c]
                    M[r] = [x - f * y for x, y in zip(M[r], M[c])]
        v = [M[i][n] / M[i][i] for i in range(n)]
        best = v if best is None else [max(x, y) for x, y in zip(best, v)]
    return best


def sync_value_iteration(P, R, g, theta):
    """Synchronous sweeps until every Bellman error is <= theta. Return (V, backups)."""
    V = [0.0] * len(P)
    backups = 0
    while True:
        W = [max(R[s][a] + g * sum(p * V[t] for p, t in P[s][a]) for a in range(len(P[s]))) for s in range(len(P))]
        backups += len(P)
        if max(abs(w - v) for w, v in zip(W, V)) <= theta:
            return V, backups
        V = W


def random_mdp(rng, n, k):
    P, R = [], []
    for _ in range(n):
        rows = []
        for _ in range(k):
            w = [rng.randrange(4) for _ in range(n)]
            w[rng.randrange(n)] += 1
            rows.append([(x / sum(w), t) for t, x in enumerate(w) if x])
        P.append(rows)
        R.append([float(rng.randint(-3, 3)) for _ in range(k)])
    return P, R


def chain(n):
    """States 0..n-1; action 0 moves left, action 1 moves right; the step into n-1 pays 1; n-1 absorbs."""
    P, R = [], []
    for s in range(n - 1):
        P.append([[(1.0, max(s - 1, 0))], [(1.0, s + 1)]])
        R.append([0.0, 1.0 if s == n - 2 else 0.0])
    P.append([[(1.0, n - 1)], [(1.0, n - 1)]])
    R.append([0.0, 0.0])
    return P, R


def test_chain_values_and_fewer_backups():
    for n in (10, 30, 60):
        P, R = chain(n)
        V, b = prioritized_sweeping(P, R, 0.9, 1e-6)
        want = [0.9 ** (n - 2 - s) for s in range(n - 1)] + [0.0]
        assert all(abs(v - w) < 1e-5 for v, w in zip(V, want))
        W, bv = sync_value_iteration(P, R, 0.9, 1e-6)
        assert all(abs(v - w) < 1e-5 for v, w in zip(V, W))
        assert b <= 2 * n and bv >= n * (n - 1)  # about n backups against about n^2


def test_against_exact_optimum():
    rng = random.Random(61)
    for _ in range(500):
        n, k = rng.randint(1, 4), rng.randint(1, 3)
        P, R = random_mdp(rng, n, k)
        g = rng.choice([0.5, 2 / 3, 0.9])
        theta = 1e-7
        V, _ = prioritized_sweeping(P, R, g, theta)
        for s in range(n):
            q = max(R[s][a] + g * sum(p * V[t] for p, t in P[s][a]) for a in range(k))
            assert abs(q - V[s]) <= theta + 1e-12
        Pf = [[[(F(p).limit_denominator(1000), t) for p, t in row] for row in st] for st in P]
        want = exact_optimum(Pf, R, F(g).limit_denominator(1000))
        assert all(abs(v - float(w)) <= theta / (1 - g) + 1e-9 for v, w in zip(V, want))


def test_edges():
    V, b = prioritized_sweeping([[[(1.0, 0)]]], [[0.0]], 0.9, 1e-9)
    assert V == [0.0] and b == 0
    V, b = prioritized_sweeping([[[(1.0, 0)]]], [[1.0]], 0.5, 1e-12)
    assert abs(V[0] - 2.0) < 1e-11


def test_online_count_model():
    rng = random.Random(62)
    for _ in range(20):
        n, k = 3, 2
        P, R = random_mdp(rng, n, k)
        g = 0.5
        agent = OnlinePrioritizedSweeping(n, k, g, 1e-6, backups_per_step=3)
        s = 0
        for _ in range(4000):
            a = rng.randrange(k)
            u, t = rng.random(), P[s][a][-1][1]
            for p, nxt in P[s][a]:
                u -= p
                if u < 0:
                    t = nxt
                    break
            agent.observe(s, a, R[s][a], t)
            s = t if rng.random() < 0.9 else rng.randrange(n)
        agent.flush()
        Vstar, _ = prioritized_sweeping(P, R, g, 1e-9)
        assert all(abs(v - w) < 0.25 for v, w in zip(agent.V, Vstar))
        assert agent.backups < 4000 * 3 + 100
