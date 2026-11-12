# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tree-reweighted-belief-propagation/. The authors are listed in prov/638X2J.jsonl.

"""Tree-reweighted belief propagation (Wainwright, Jaakkola and Willsky 2005)
for an upper bound on log Z of a pairwise Markov random field.

A model is (card, theta, pair): card[s] is the number of states of x_s,
theta[s][x_s] is a unary log potential, and pair maps an edge (s, t) with s < t
to a table pair[(s, t)][x_s][x_t] of pairwise log potentials. The distribution is
    p(x) = exp(sum_s theta_s(x_s) + sum_(s,t) theta_st(x_s, x_t)) / Z.

rho maps each edge (s, t) with s < t to its edge appearance probability, the
probability that the edge lies in a random spanning tree. Messages are kept in
the log domain: logm[(t, s)] is the message from t to s, a list over x_s.
"""

import itertools
import math
from fractions import Fraction


def _lse(v):
    top = max(v)
    return top + math.log(sum(math.exp(x - top) for x in v))


def _log_normalize(v):
    z = _lse(v)
    return [x - z for x in v]


def neighbors(card, pair):
    nb = [[] for _ in card]
    for s, t in pair:
        nb[s].append(t)
        nb[t].append(s)
    return nb


def theta_pair(pair, s, t, xs, xt):
    return pair[(s, t)][xs][xt] if (s, t) in pair else pair[(t, s)][xt][xs]


def rho_of(rho, s, t):
    return rho[(s, t)] if (s, t) in rho else rho[(t, s)]


def uniform_spanning_tree_rho(n, edges):
    """Edge appearance probabilities under the uniform distribution over spanning
    trees. By Kirchhoff, P(e in T) is the effective resistance between the ends
    of e when every edge is a unit resistor. Exact, with fractions."""
    lap = [[Fraction(0)] * n for _ in range(n)]
    for s, t in edges:
        lap[s][s] += 1
        lap[t][t] += 1
        lap[s][t] -= 1
        lap[t][s] -= 1
    # Ground node 0 and invert the reduced Laplacian by Gauss-Jordan elimination.
    m = n - 1
    a = [row[1:] + [Fraction(int(i == j)) for j in range(m)] for i, row in enumerate(lap[1:])]
    for c in range(m):
        piv = next((r for r in range(c, m) if a[r][c] != 0), None)
        if piv is None:
            raise ValueError("the graph is not connected")
        a[c], a[piv] = a[piv], a[c]
        p = a[c][c]
        a[c] = [x / p for x in a[c]]
        for r in range(m):
            if r != c and a[r][c] != 0:
                f = a[r][c]
                a[r] = [x - f * y for x, y in zip(a[r], a[c])]
    inv = [[Fraction(0)] * n for _ in range(n)]
    for i in range(m):
        for j in range(m):
            inv[i + 1][j + 1] = a[i][m + j]
    return {(s, t): inv[s][s] + inv[t][t] - 2 * inv[s][t] for s, t in edges}


def message(card, theta, pair, rho, nb, logm, t, s):
    """log M_ts(x_s) = log sum_{x_t} exp(theta_st / rho_st + theta_t(x_t))
    prod_{v in N(t) minus s} M_vt(x_t)^rho_vt / M_st(x_t)^(1 - rho_st), normalized."""
    r = rho_of(rho, s, t)
    pre = []
    for xt in range(card[t]):
        w = theta[t][xt] - (1 - r) * logm[(s, t)][xt]
        for v in nb[t]:
            if v != s:
                w += rho_of(rho, v, t) * logm[(v, t)][xt]
        pre.append(w)
    return _log_normalize([_lse([theta_pair(pair, s, t, xs, xt) / r + pre[xt] for xt in range(card[t])])
                           for xs in range(card[s])])


def beliefs(card, theta, pair, rho, nb, logm):
    """The single and pairwise pseudomarginals tau_s and tau_st of the fixed point."""
    tau = []
    for s in range(len(card)):
        v = [theta[s][x] + sum(rho_of(rho, u, s) * logm[(u, s)][x] for u in nb[s]) for x in range(card[s])]
        tau.append([math.exp(x) for x in _log_normalize(v)])
    tau2 = {}
    for (s, t) in pair:
        r = rho[(s, t)]

        def side(a, b, xa):
            w = theta[a][xa] - (1 - r) * logm[(b, a)][xa]
            return w + sum(rho_of(rho, u, a) * logm[(u, a)][xa] for u in nb[a] if u != b)
        v = [[pair[(s, t)][xs][xt] / r + side(s, t, xs) + side(t, s, xt) for xt in range(card[t])]
             for xs in range(card[s])]
        z = _lse([x for row in v for x in row])
        tau2[(s, t)] = [[math.exp(x - z) for x in row] for row in v]
    return tau, tau2


def _entropy(p):
    return -sum(x * math.log(x) for x in p if x > 0)


def trw_bound(card, theta, pair, rho, tau, tau2):
    """B(tau) = <theta, tau> + sum_s H(tau_s) - sum_st rho_st I_st(tau_st). For
    locally consistent tau this is at most its maximum, which is >= log Z."""
    val = sum(tau[s][x] * theta[s][x] for s in range(len(card)) for x in range(card[s]))
    val += sum(_entropy(p) for p in tau)
    for (s, t), tab in tau2.items():
        mi = 0.0
        for xs in range(card[s]):
            for xt in range(card[t]):
                q = tab[xs][xt]
                val += q * pair[(s, t)][xs][xt]
                if q > 0:
                    mi += q * math.log(q / (tau[s][xs] * tau[t][xt]))
        val -= float(rho[(s, t)]) * mi
    return val


def trw_bp(card, theta, pair, rho=None, damping=0.5, tol=1e-10, max_iter=10000, init=None):
    """Run damped synchronous TRW message passing. Return (bound, tau, tau2,
    iterations, converged). With rho = 1 on every edge this is ordinary BP."""
    if not 0.0 <= damping < 1.0:
        raise ValueError("damping must be in [0, 1)")
    if rho is None:
        rho = uniform_spanning_tree_rho(len(card), list(pair))  # @line L1
    rho = {e: float(r) for e, r in rho.items()}
    nb = neighbors(card, pair)
    logm = init or {(t, s): [0.0] * card[s] for s in range(len(card)) for t in nb[s]}  # @line L2
    logm = {e: list(v) for e, v in logm.items()}
    converged = False
    it = 0
    for it in range(1, max_iter + 1):  # @line L3
        new = {(t, s): message(card, theta, pair, rho, nb, logm, t, s) for (t, s) in logm}  # @line L4
        delta = 0.0
        for e, v in new.items():
            damped = _log_normalize([(1 - damping) * a + damping * b for a, b in zip(v, logm[e])])  # @line L5
            delta = max(delta, max(abs(math.exp(a) - math.exp(b)) for a, b in zip(damped, logm[e])))
            new[e] = damped
        logm = new
        if delta < tol:  # @line L6
            converged = True
            break
    tau, tau2 = beliefs(card, theta, pair, rho, nb, logm)  # @line L7
    return trw_bound(card, theta, pair, rho, tau, tau2), tau, tau2, it, converged  # @line L8


def exact(card, theta, pair):
    """log Z, the single marginals and the pairwise marginals, by enumeration."""
    states = list(itertools.product(*[range(c) for c in card]))
    logw = [sum(theta[s][x[s]] for s in range(len(card))) + sum(tab[x[s]][x[t]] for (s, t), tab in pair.items())
            for x in states]
    log_z = _lse(logw)
    tau = [[0.0] * c for c in card]
    tau2 = {e: [[0.0] * card[e[1]] for _ in range(card[e[0]])] for e in pair}
    for x, lw in zip(states, logw):
        p = math.exp(lw - log_z)
        for s in range(len(card)):
            tau[s][x[s]] += p
        for (s, t) in pair:
            tau2[(s, t)][x[s]][x[t]] += p
    return log_z, tau, tau2


def ising(n, fields, couplings):
    """Spins in {-1, +1} (state 0 is -1): theta_s = h_s s, theta_st = J_st s t."""
    spin = (-1, 1)
    theta = [[h * spin[a] for a in range(2)] for h in fields]
    pair = {(min(s, t), max(s, t)): [[j * spin[a] * spin[b] for b in range(2)] for a in range(2)]
            for s, t, j in couplings}
    return [2] * n, theta, pair


def grid_edges(rows, cols):
    idx = lambda r, c: r * cols + c
    edges = [(idx(r, c), idx(r, c + 1)) for r in range(rows) for c in range(cols - 1)]
    edges += [(idx(r, c), idx(r + 1, c)) for r in range(rows - 1) for c in range(cols)]
    return edges
