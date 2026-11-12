# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/trpo/. The authors are listed in prov/TNPH8G.jsonl.

"""Trust region policy optimization (Schulman et al. 2015), single-path version, for a linear softmax policy.

An MDP is (P, R): P[s][a][t] is the probability of the next state t, the
missing mass of a row is the probability that the episode ends, and R[s][a] is
the reward. The policy is pi(a|s) proportional to exp(theta . phi[s][a]); its
score is psi(s, a) = phi[s][a] - sum_b pi(b|s) phi[s][b].

A sample is (w, s, a, adv): the state and action of one step, the weight
w = gamma^t / N of that step in a batch of N episodes, and the advantage
estimate. The functions that take probabilities pi directly also work with
Fractions.

Cost of one iteration: O(N T A k (c + l)) for N episodes of length at most T,
A actions, k features, c conjugate gradient iterations and l line search steps.
"""

import math
import random


def policy(theta, phi):
    """Softmax probabilities pi[s][a] from theta and features phi[s][a]."""
    out = []
    for rows in phi:
        z = [sum(t * f for t, f in zip(theta, row)) for row in rows]
        m = max(z)
        e = [math.exp(x - m) for x in z]
        out.append([x / sum(e) for x in e])
    return out


def score(pi, phi, s, a):
    return [phi[s][a][i] - sum(pi[s][b] * phi[s][b][i] for b in range(len(pi[s]))) for i in range(len(phi[s][a]))]


def surrogate(pi_new, pi_old, samples):
    """L(theta) - L(theta_old) = sum of w (pi_new(a|s) / pi_old(a|s) - 1) adv."""
    return sum(w * (pi_new[s][a] / pi_old[s][a] - 1) * adv for w, s, a, adv in samples)


def surrogate_gradient(pi_old, phi, samples):
    """Gradient of the surrogate at theta_old: sum of w adv psi(s, a)."""
    g = [0 * samples[0][0]] * len(phi[0][0]) if samples else [0.0] * len(phi[0][0])
    for w, s, a, adv in samples:
        g = [gi + w * adv * p for gi, p in zip(g, score(pi_old, phi, s, a))]
    return g


def kl(p, q):
    return sum(x * math.log(x / y) for x, y in zip(p, q) if x > 0)


def mean_kl(pi_old, pi_new, samples):
    """Average KL(pi_old(.|s) || pi_new(.|s)) over the sampled states, with the weights w."""
    tot = sum(w for w, _, _, _ in samples)
    return sum(w * kl(pi_old[s], pi_new[s]) for w, s, _, _ in samples) / tot


def fisher_vector_product(pi, phi, samples, v, damping=0.0):
    """F v for F = weighted mean over sampled states of sum_a pi(a|s) psi psi^T, the Hessian of the mean KL."""
    tot = sum(w for w, _, _, _ in samples)
    out = [damping * x for x in v]
    for w, s, _, _ in samples:
        for a in range(len(pi[s])):
            psi = score(pi, phi, s, a)
            c = w * pi[s][a] * sum(p * x for p, x in zip(psi, v)) / tot
            out = [o + c * p for o, p in zip(out, psi)]
    return out


def conjugate_gradient(Av, b, iterations, tol=1e-10):
    """Approximate solution of A x = b for a symmetric positive semidefinite A, given only x -> A x."""
    x = [0 * bi for bi in b]
    r = list(b)
    p = list(b)
    rr = sum(ri * ri for ri in r)
    for _ in range(iterations):
        if rr <= tol:
            break
        Ap = Av(p)
        alpha = rr / sum(pi * api for pi, api in zip(p, Ap))
        x = [xi + alpha * pi for xi, pi in zip(x, p)]
        r = [ri - alpha * api for ri, api in zip(r, Ap)]
        new = sum(ri * ri for ri in r)
        p = [ri + new / rr * pi for ri, pi in zip(r, p)]
        rr = new
    return x


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


def trpo(P, R, gamma, mu, theta, phi, delta, iterations, episodes, rng,
         cg_iterations=10, damping=1e-3, backtracks=10, horizon=200):
    """Single-path TRPO with Monte Carlo advantages and a per-state mean return as the baseline."""
    theta = list(theta)
    b = [0.0] * len(P)
    for _ in range(iterations):  # @line L1
        pi = policy(theta, phi)
        batch = [sample_episode(P, R, pi, mu, rng, horizon) for _ in range(episodes)]  # @line L2
        samples, visits = [], [[0.0, 0] for _ in P]
        for ep in batch:
            G = 0.0
            for t in range(len(ep) - 1, -1, -1):
                s, a, r = ep[t]
                G = r + gamma * G
                samples.append((gamma ** t / episodes, s, a, G - b[s]))  # @line L3
                visits[s][0] += G
                visits[s][1] += 1
        b = [tot / cnt if cnt else old for (tot, cnt), old in zip(visits, b)]
        theta = update(theta, phi, samples, delta, cg_iterations, damping, backtracks)
    return theta


def update(theta, phi, samples, delta, cg_iterations=10, damping=1e-3, backtracks=10):
    """One TRPO step from theta on a batch of samples; returns theta unchanged if no step passes the checks."""
    pi = policy(theta, phi)
    g = surrogate_gradient(pi, phi, samples)  # @line L4
    x = conjugate_gradient(lambda v: fisher_vector_product(pi, phi, samples, v, damping), g, cg_iterations)  # @line L5
    xFx = sum(xi * fi for xi, fi in zip(x, fisher_vector_product(pi, phi, samples, x, damping)))
    if xFx <= 0:
        return list(theta)
    step = math.sqrt(2 * delta / xFx)  # @line L6
    for j in range(backtracks):  # @line L7
        cand = [t + step * 0.5 ** j * xi for t, xi in zip(theta, x)]
        pi_new = policy(cand, phi)
        if mean_kl(pi, pi_new, samples) <= delta and surrogate(pi_new, pi, samples) > 0:  # @line L8
            return cand  # @line L9
    return list(theta)


# Exact quantities with a known model, used for the theory of the page.

def _solve(M, b):
    n = len(M)
    A = [list(M[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda i: abs(A[i][c]))
        A[c], A[p] = A[p], A[c]
        for i in range(n):
            if i != c and A[i][c] != 0:
                f = A[i][c] / A[c][c]
                A[i] = [x - f * y for x, y in zip(A[i], A[c])]
    return [A[i][n] / A[i][i] for i in range(n)]


def values(P, R, gamma, pi):
    """V and Q of the policy pi."""
    n = len(P)
    M = [[(1 if s == t else 0) - gamma * sum(pi[s][a] * P[s][a][t] for a in range(len(pi[s]))) for t in range(n)] for s in range(n)]
    V = _solve(M, [sum(pi[s][a] * R[s][a] for a in range(len(pi[s]))) for s in range(n)])
    Q = [[R[s][a] + gamma * sum(P[s][a][t] * V[t] for t in range(n)) for a in range(len(pi[s]))] for s in range(n)]
    return V, Q


def visitation(P, gamma, pi, mu):
    """rho(s) = sum_t gamma^t Pr(S_t = s), not normalized."""
    n = len(P)
    MT = [[(1 if s == t else 0) - gamma * sum(pi[t][a] * P[t][a][s] for a in range(len(pi[t]))) for t in range(n)] for s in range(n)]
    return _solve(MT, list(mu))


def eta(P, R, gamma, mu, pi):
    V, _ = values(P, R, gamma, pi)
    return sum(m * v for m, v in zip(mu, V))


def local_approximation(P, R, gamma, mu, pi_old, pi_new):
    """L_old(pi_new) = eta(pi_old) + sum_s rho_old(s) sum_a pi_new(a|s) A_old(s, a) (Equation 3 of the paper)."""
    V, Q = values(P, R, gamma, pi_old)
    rho = visitation(P, gamma, pi_old, mu)
    return eta(P, R, gamma, mu, pi_old) + sum(
        rho[s] * sum(pi_new[s][a] * (Q[s][a] - V[s]) for a in range(len(pi_new[s]))) for s in range(len(P)))
