# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/model-based-reinforcement-learning/. The authors are listed in prov/1JFJ2J.jsonl.

import itertools
import random

from model_based_reinforcement_learning import CountModel, certainty_equivalence, value_iteration


def evaluate(P, R, g, pi):
    """Independent oracle: V^pi by Gauss-Jordan elimination on (I - g P_pi) V = R_pi."""
    n = len(P)
    M = [[float(i == j) for j in range(n)] + [R[i][pi[i]]] for i in range(n)]
    for s in range(n):
        for p, t in P[s][pi[s]]:
            M[s][t] -= g * p
    for c in range(n):
        r = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[r] = M[r], M[c]
        for r in range(n):
            if r != c:
                f = M[r][c] / M[c][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]


def optimum(P, R, g):
    """Independent oracle: V* as the best V^pi over all deterministic policies."""
    best = None
    for pi in itertools.product(*[range(len(row)) for row in P]):
        v = evaluate(P, R, g, pi)
        best = v if best is None else [max(x, y) for x, y in zip(best, v)]
    return best


def random_mdp(rng, n, k, full=True):
    P, R = [], []
    for _ in range(n):
        rows = []
        for _ in range(k):
            w = [rng.randint(1 if full else 0, 4) for _ in range(n)]
            w[rng.randrange(n)] += 1
            rows.append([(x / sum(w), t) for t, x in enumerate(w) if x])
        P.append(rows)
        R.append([float(rng.randint(-3, 3)) for _ in range(k)])
    return P, R


class Env:
    def __init__(self, P, R, seed, noise=1.0):
        self.P, self.R, self.rng, self.noise, self.start = P, R, random.Random(seed), noise, 0

    def step(self, s, a):
        u, t = self.rng.random(), self.P[s][a][-1][1]
        for p, nxt in self.P[s][a]:
            u -= p
            if u < 0:
                t = nxt
                break
        return self.R[s][a] + self.rng.uniform(-self.noise, self.noise), t


def l1(row, row_hat, n):
    d, dh = {t: p for p, t in row}, {t: p for p, t in row_hat}
    return sum(abs(d.get(t, 0.0) - dh.get(t, 0.0)) for t in range(n))


def model_errors(model, P, R):
    """(largest L1 error of a row of P_hat, largest error of R_hat)."""
    Ph, Rh = model.estimate()
    eP = eR = 0.0
    for s in range(len(P)):
        for a in range(len(P[s])):
            eP = max(eP, l1(P[s][a], Ph[s][a], len(P)))
            eR = max(eR, abs(R[s][a] - Rh[s][a]))
    return eP, eR


def test_simulation_lemma_on_random_models():
    rng = random.Random(91)
    for _ in range(500):
        n, k = rng.randint(1, 4), rng.randint(1, 3)
        P, R = random_mdp(rng, n, k, full=rng.random() < 0.5)
        Ph, _ = random_mdp(rng, n, k, full=rng.random() < 0.5)
        Rh = [[r + rng.uniform(-0.5, 0.5) for r in row] for row in R]
        g = rng.choice([0.0, 0.5, 0.9])
        pi = [rng.randrange(k) for _ in range(n)]
        eP = max(l1(P[s][a], Ph[s][a], n) for s in range(n) for a in range(k))
        eR = max(abs(R[s][a] - Rh[s][a]) for s in range(n) for a in range(k))
        rmax = max(abs(r) for row in R for r in row)
        bound = (eR + g * eP * rmax / (1 - g)) / (1 - g)
        V, Vh = evaluate(P, R, g, pi), evaluate(Ph, Rh, g, pi)
        assert max(abs(x - y) for x, y in zip(V, Vh)) <= bound + 1e-9
        # planning on the wrong model loses at most twice the bound
        _, pih = value_iteration(Ph, Rh, g)
        Vs, Vpih = optimum(P, R, g), evaluate(P, R, g, pih)
        assert all(x >= y - 2 * bound - 1e-6 for x, y in zip(Vpih, Vs))


def test_model_converges_and_bound_holds():
    rng = random.Random(92)
    for case in range(500):
        n, k = rng.randint(1, 3), rng.randint(1, 3)
        P, R = random_mdp(rng, n, k)
        g = rng.choice([0.5, 0.8])
        model, pi, _ = certainty_equivalence(Env(P, R, case), n, k, g, 600, epsilon=1.0, plan_every=600, seed=case)
        eP, eR = model_errors(model, P, R)
        assert eP < 0.6 and eR < 0.6
        rmax = max(abs(r) for row in R for r in row)
        bound = (eR + g * eP * rmax / (1 - g)) / (1 - g)
        Vs, Vpi = optimum(P, R, g), evaluate(P, R, g, pi)
        assert all(x >= y - 2 * bound - 1e-6 for x, y in zip(Vpi, Vs))


def test_more_data_gives_exact_model_and_optimal_policy():
    rng = random.Random(93)
    for case in range(10):
        P, R = random_mdp(rng, 4, 2)
        g = 0.8
        Vs = optimum(P, R, g)
        errs = []
        for steps in (200, 2000, 40000):
            model, pi, Vh = certainty_equivalence(Env(P, R, case), 4, 2, g, steps, epsilon=0.5, plan_every=100, seed=case)
            errs.append(model_errors(model, P, R))
        assert errs[2][0] < errs[0][0] and errs[2][0] < 0.1 and errs[2][1] < 0.05
        Vpi = evaluate(P, R, g, pi)
        assert all(abs(x - y) < 1e-6 for x, y in zip(Vpi, Vs))  # the learned policy is optimal
        assert all(abs(x - y) < 1.0 for x, y in zip(Vh, Vs))


def test_unknown_pairs():
    m = CountModel(2, 2, r_unknown=1.0)
    m.observe(0, 0, 0.5, 1)
    m.observe(0, 0, 1.5, 1)
    P, R = m.estimate()
    assert P[0][0] == [(1.0, 1)] and R[0][0] == 1.0
    assert P[1][1] == [(1.0, 1)] and R[1][1] == 1.0
    V, pi = value_iteration(P, R, 0.5)
    assert abs(V[1] - 2.0) < 1e-9 and pi[0] in (0, 1)
