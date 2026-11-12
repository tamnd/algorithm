# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/trpo/. The authors are listed in prov/TNPH8G.jsonl.

import math
import random
from fractions import Fraction as F

from trpo import (
    conjugate_gradient,
    eta,
    fisher_vector_product,
    kl,
    local_approximation,
    mean_kl,
    policy,
    sample_episode,
    score,
    surrogate,
    surrogate_gradient,
    trpo,
    update,
    values,
    visitation,
)

P = [
    [[F(1, 2), F(1, 4)], [F(0), F(3, 4)]],
    [[F(1, 2), F(0)], [F(0), F(0)]],
]
R = [[F(1), F(0)], [F(0), F(3)]]
GAMMA = F(1, 2)


def random_mdp(rng, n, k, acyclic=False):
    Pm = []
    for s in range(n):
        rows = []
        for _ in range(k):
            w = [rng.randint(0, 4) if (t > s or not acyclic) else 0 for t in range(n)] + [rng.randint(1, 4)]
            rows.append([F(x, sum(w)) for x in w[:n]])
        Pm.append(rows)
    Rm = [[F(rng.randint(-3, 3)) for _ in range(k)] for _ in range(n)]
    return Pm, Rm


def random_policy(rng, n, k):
    out = []
    for _ in range(n):
        w = [rng.randint(1, 5) for _ in range(k)]
        out.append([F(x, sum(w)) for x in w])
    return out


def episodes(Pm, pi, mu):
    """All episodes of an acyclic MDP as (probability, [(s, a), ...])."""
    out = []

    def go(s, prob, hist):
        for a in range(len(pi[s])):
            pa = prob * pi[s][a]
            h = hist + [(s, a)]
            end = 1 - sum(Pm[s][a])
            if end:
                out.append((pa * end, h))
            for t, p in enumerate(Pm[s][a]):
                if p:
                    go(t, pa * p, h)

    for s, m in enumerate(mu):
        if m:
            go(s, m, [])
    return out


def test_surrogate_gradient_equals_policy_gradient():
    rng = random.Random(1)
    for _ in range(20):
        n, k, m = rng.randint(1, 3), rng.randint(2, 3), rng.randint(1, 3)
        Pm, Rm = random_mdp(rng, n, k, acyclic=True)
        pi = random_policy(rng, n, k)
        mu = random_policy(rng, 1, n)[0]
        phi = [[[F(rng.randint(-2, 2)) for _ in range(m)] for _ in range(k)] for _ in range(n)]
        V, Q = values(Pm, Rm, GAMMA, pi)
        samples = [(prob * GAMMA ** t, s, a, Q[s][a] - V[s])
                   for prob, h in episodes(Pm, pi, mu) for t, (s, a) in enumerate(h)]
        rho = visitation(Pm, GAMMA, pi, mu)
        grad = [sum(rho[s] * pi[s][a] * score(pi, phi, s, a)[i] * Q[s][a] for s in range(n) for a in range(k))
                for i in range(m)]
        assert surrogate_gradient(pi, phi, samples) == grad


def test_local_approximation_matches_to_first_order():
    rng = random.Random(2)
    for _ in range(20):
        n, k = rng.randint(1, 3), rng.randint(2, 3)
        Pm, Rm = random_mdp(rng, n, k)
        old, new = random_policy(rng, n, k), random_policy(rng, n, k)
        mu = random_policy(rng, 1, n)[0]
        # Kakade and Langford: eta(new) - eta(old) = sum_s rho_new(s) sum_a new(a|s) A_old(s, a)
        V, Q = values(Pm, Rm, GAMMA, old)
        rho_new = visitation(Pm, GAMMA, new, mu)
        gain = sum(rho_new[s] * sum(new[s][a] * (Q[s][a] - V[s]) for a in range(k)) for s in range(n))
        assert eta(Pm, Rm, GAMMA, mu, new) - eta(Pm, Rm, GAMMA, mu, old) == gain
        assert local_approximation(Pm, Rm, GAMMA, mu, old, old) == eta(Pm, Rm, GAMMA, mu, old)
        t = F(1, 10 ** 6)
        mid = [[o + t * (w - o) for o, w in zip(ro, rw)] for ro, rw in zip(old, new)]
        diff = eta(Pm, Rm, GAMMA, mu, mid) - local_approximation(Pm, Rm, GAMMA, mu, old, mid)
        assert abs(diff) < t * F(1, 10 ** 4)


def test_lower_bound_of_theorem_1():
    rng = random.Random(3)
    for _ in range(40):
        n, k = rng.randint(1, 3), rng.randint(2, 3)
        Pm, Rm = random_mdp(rng, n, k)
        old, new = random_policy(rng, n, k), random_policy(rng, n, k)
        mu = random_policy(rng, 1, n)[0]
        V, Q = values(Pm, Rm, GAMMA, old)
        eps = max(abs(Q[s][a] - V[s]) for s in range(n) for a in range(k))
        alpha = max(sum(abs(p - q) for p, q in zip(old[s], new[s])) / 2 for s in range(n))
        C = 4 * eps * GAMMA / (1 - GAMMA) ** 2
        lower = local_approximation(Pm, Rm, GAMMA, mu, old, new) - C * alpha ** 2
        assert eta(Pm, Rm, GAMMA, mu, new) >= lower
        # the KL form: D_TV^2 <= D_KL, so the KL penalty is also a lower bound
        kl_max = max(kl([float(x) for x in old[s]], [float(x) for x in new[s]]) for s in range(n))
        assert float(alpha) ** 2 <= kl_max + 1e-12
        assert float(eta(Pm, Rm, GAMMA, mu, new)) >= float(local_approximation(Pm, Rm, GAMMA, mu, old, new)) - float(C) * kl_max - 1e-9


def test_conjugate_gradient_is_exact_in_n_steps():
    rng = random.Random(4)
    for n in range(1, 6):
        B = [[F(rng.randint(-3, 3)) for _ in range(n)] for _ in range(n)]
        A = [[sum(B[i][l] * B[j][l] for l in range(n)) + (1 if i == j else 0) for j in range(n)] for i in range(n)]
        b = [F(rng.randint(-5, 5)) for _ in range(n)]
        x = conjugate_gradient(lambda v: [sum(A[i][j] * v[j] for j in range(n)) for i in range(n)], b, n, tol=0)
        assert [sum(A[i][j] * x[j] for j in range(n)) for i in range(n)] == b


def test_fisher_vector_product_is_hessian_of_mean_kl():
    rng = random.Random(5)
    n, k, m = 3, 3, 4
    phi = [[[rng.uniform(-1, 1) for _ in range(m)] for _ in range(k)] for _ in range(n)]
    theta = [rng.uniform(-1, 1) for _ in range(m)]
    samples = [(rng.uniform(0.1, 1), rng.randrange(n), 0, 0.0) for _ in range(10)]
    pi = policy(theta, phi)
    for _ in range(5):
        v = [rng.uniform(-1, 1) for _ in range(m)]
        vFv = sum(a * b for a, b in zip(v, fisher_vector_product(pi, phi, samples, v)))
        h = 1e-4
        moved = policy([t + h * x for t, x in zip(theta, v)], phi)
        assert abs(mean_kl(pi, moved, samples) / (h * h / 2) - vFv) <= 1e-3 * max(vFv, 1e-6)


def batch_samples(theta, phi, n_episodes, rng):
    Pf = [[[float(x) for x in r] for r in rows] for rows in P]
    Rf = [[float(x) for x in r] for r in R]
    pi = policy(theta, phi)
    samples = []
    for _ in range(n_episodes):
        ep = sample_episode(Pf, Rf, pi, [1.0, 0.0], rng, 200)
        G = 0.0
        for t in range(len(ep) - 1, -1, -1):
            s, a, r = ep[t]
            G = r + 0.5 * G
            samples.append((0.5 ** t / n_episodes, s, a, G - 1.0))
    return samples


def tabular(n, k):
    return [[[1.0 if i == s * k + a else 0.0 for i in range(n * k)] for a in range(k)] for s in range(n)]


def test_update_respects_trust_region():
    rng = random.Random(6)
    phi = tabular(2, 2)
    for delta in [0.001, 0.01, 0.1, 1.0]:
        theta = [rng.uniform(-1, 1) for _ in range(4)]
        samples = batch_samples(theta, phi, 50, rng)
        new = update(theta, phi, samples, delta)
        pi, pi_new = policy(theta, phi), policy(new, phi)
        assert mean_kl(pi, pi_new, samples) <= delta
        assert new == theta or surrogate(pi_new, pi, samples) > 0


def test_trpo_learns():
    Pf = [[[float(x) for x in r] for r in rows] for rows in P]
    Rf = [[float(x) for x in r] for r in R]
    theta = trpo(Pf, Rf, 0.5, [1.0, 0.0], [0.0] * 4, tabular(2, 2), 0.05, 30, 50, random.Random(0))
    pi = policy(theta, tabular(2, 2))
    assert pi[0][0] > 0.9 and pi[1][1] > 0.9
    assert math.isfinite(sum(theta))
