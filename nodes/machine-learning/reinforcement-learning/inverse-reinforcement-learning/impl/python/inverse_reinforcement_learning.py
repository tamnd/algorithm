# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/inverse-reinforcement-learning/. The authors are listed in prov/5XWNRJ.jsonl.

"""Two views of inverse reinforcement learning.

1. The characterization of Ng and Russell (2000, Theorem 3), in exact
   arithmetic: in a finite MDP with a state reward R, the deterministic policy
   pi is optimal if and only if
       (P_pi(s) - P_a(s)) (I - gamma P_pi)^{-1} R >= 0   for every s and a.
   The zero reward, and every constant reward, pass this test for every policy.

2. Maximum entropy IRL (Ziebart, Maas, Bagnell and Dey, 2008) on a
   deterministic MDP with horizon T: the action sequences have probabilities
   proportional to exp(sum_t theta . phi(s_t)). A soft backward pass gives the
   local action probabilities, a forward pass gives the expected state visits,
   and gradient ascent on theta makes the expected feature counts match the
   demonstrations.
"""

import math
from fractions import Fraction


# ---------------------------------------------------------------- Ng and Russell

def solve(a, b):
    """Solve a x = b exactly by Gauss-Jordan elimination over Fractions."""
    n = len(a)
    m = [list(map(Fraction, row)) + [Fraction(b[i])] for i, row in enumerate(a)]
    for c in range(n):
        p = next(r for r in range(c, n) if m[r][c] != 0)
        m[c], m[p] = m[p], m[c]
        piv = m[c][c]
        m[c] = [v / piv for v in m[c]]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c]
                m[r] = [vr - f * vc for vr, vc in zip(m[r], m[c])]
    return [m[r][n] for r in range(n)]


def policy_value(P, R, gamma, policy):
    """V^pi = (I - gamma P_pi)^{-1} R, exactly. P[a][s][s2]; policy[s] = action."""
    n = len(R)
    a = [[(1 if s == t else 0) - gamma * P[policy[s]][s][t] for t in range(n)] for s in range(n)]
    return solve(a, R)


def ng_russell_margins(P, R, gamma, policy):
    """margins[s][a] = (P_pi(s) - P_a(s)) . V^pi, which is (Q(s, pi(s)) - Q(s, a)) / gamma."""
    v = policy_value(P, R, gamma, policy)
    n = len(R)
    return [[sum((P[policy[s]][s][t] - P[a][s][t]) * v[t] for t in range(n))
             for a in range(len(P))] for s in range(n)]


def ng_russell_condition(P, R, gamma, policy) -> bool:
    """Theorem 3 of Ng and Russell: policy is optimal for R iff all margins are >= 0."""
    return all(m >= 0 for row in ng_russell_margins(P, R, gamma, policy) for m in row)


def optimal_policies(P, R, gamma):
    """All deterministic optimal policies, by enumeration (for testing)."""
    n, k = len(R), len(P)
    pols = [[]]
    for _ in range(n):
        pols = [p + [a] for p in pols for a in range(k)]
    values = {tuple(p): policy_value(P, R, gamma, p) for p in pols}
    best = [max(v[s] for v in values.values()) for s in range(n)]
    return {p for p, v in values.items() if v == best}


# ------------------------------------------------------------- maximum entropy IRL

def logsumexp(xs):
    m = max(xs)
    return m + math.log(sum(math.exp(x - m) for x in xs))


class DetMDP:
    """A deterministic MDP: nxt[s][a] is the next state, phi[s] the feature vector."""

    def __init__(self, nxt, phi, start, horizon):
        self.nxt, self.phi, self.start, self.T = nxt, phi, start, horizon
        self.n, self.k, self.d = len(nxt), len(nxt[0]), len(phi[0])

    def reward(self, theta):
        return [sum(t * f for t, f in zip(theta, self.phi[s])) for s in range(self.n)]


def grid(width=3, height=3, horizon=5):
    """A small grid with moves up, down, left, right and stay; a move into the
    border stays. Features: [at the goal (2, 2)], [in the water (1, 1) or
    (1, 2)], [the column divided by 2]. The start is (0, 0)."""
    cells = [(r, c) for r in range(height) for c in range(width)]
    index = {cell: i for i, cell in enumerate(cells)}
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]
    nxt = []
    for r, c in cells:
        row = []
        for dr, dc in moves:
            cell = (r + dr, c + dc)
            row.append(index.get(cell, index[(r, c)]))
        nxt.append(row)
    water = {(1, 1), (1, 2)}
    phi = [[1.0 if (r, c) == (2, 2) else 0.0, 1.0 if (r, c) in water else 0.0, c / 2]
           for r, c in cells]
    return DetMDP(nxt, phi, index[(0, 0)], horizon)


def soft_backward(env: DetMDP, theta):
    """Line L4 and L5: V[t][s] = log of the sum over continuations from s at step t
    of exp(total reward), and the local policies pi[t][s][a] for t = 0..T-2."""
    r = env.reward(theta)
    v = [None] * env.T
    v[env.T - 1] = list(r)
    pi = [None] * (env.T - 1)
    for t in range(env.T - 2, -1, -1):
        v[t], pi[t] = [], []
        for s in range(env.n):
            q = [v[t + 1][env.nxt[s][a]] for a in range(env.k)]
            z = logsumexp(q)
            v[t].append(r[s] + z)
            pi[t].append([math.exp(x - z) for x in q])
    return v, pi


def forward(env: DetMDP, pi):
    """Line L6: D[t][s], the probability of being in s at step t."""
    d = [0.0] * env.n
    d[env.start] = 1.0
    out = [d]
    for t in range(env.T - 1):
        nd = [0.0] * env.n
        for s in range(env.n):
            if d[s]:
                for a in range(env.k):
                    nd[env.nxt[s][a]] += d[s] * pi[t][s][a]
        d = nd
        out.append(d)
    return out


def expected_features(env: DetMDP, theta):
    """E[sum_t phi(s_t)] under the maximum entropy distribution for theta."""
    _, pi = soft_backward(env, theta)
    visits = forward(env, pi)
    return [sum(d[s] * env.phi[s][j] for d in visits for s in range(env.n)) for j in range(env.d)]


def path_features(env: DetMDP, actions):
    s, f = env.start, list(env.phi[env.start])
    for a in actions:
        s = env.nxt[s][a]
        f = [x + y for x, y in zip(f, env.phi[s])]
    return f


def log_likelihood(env: DetMDP, theta, demos):
    """Average log probability of the demonstrated action sequences."""
    v, _ = soft_backward(env, theta)
    log_z = v[0][env.start]
    return sum(sum(t * f for t, f in zip(theta, path_features(env, d))) - log_z
               for d in demos) / len(demos)


def maxent_irl(env: DetMDP, target, lr=0.5, iters=5000, tol=1e-10):
    """Gradient ascent on the log likelihood; target is the average feature count
    of the demonstrations. Returns theta."""
    theta = [0.0] * env.d  # @line L2
    for _ in range(iters):  # @line L3
        _, pi = soft_backward(env, theta)  # @line L4
        visits = forward(env, pi)  # @line L6
        mu = [sum(d[s] * env.phi[s][j] for d in visits for s in range(env.n)) for j in range(env.d)]
        grad = [f - m for f, m in zip(target, mu)]
        theta = [t + lr * g for t, g in zip(theta, grad)]  # @line L7
        if max(abs(g) for g in grad) < tol:  # @line L8
            break
    return theta  # @line L9


def feature_counts(env: DetMDP, demos):
    """Line L1: the average feature count of action sequences."""
    fs = [path_features(env, d) for d in demos]  # @line L1
    return [sum(f[j] for f in fs) / len(fs) for j in range(env.d)]


def sample_paths(env: DetMDP, theta, n, rng):
    """Draw n action sequences from the maximum entropy distribution for theta.
    The policy pi[t][s][a] of line L5 gives the step probabilities."""
    _, pi = soft_backward(env, theta)  # @line L5
    out = []
    for _ in range(n):
        s, acts = env.start, []
        for t in range(env.T - 1):
            u, acc = rng.random(), 0.0
            for a in range(env.k):
                acc += pi[t][s][a]
                if u < acc:
                    break
            acts.append(a)
            s = env.nxt[s][a]
        out.append(acts)
    return out
