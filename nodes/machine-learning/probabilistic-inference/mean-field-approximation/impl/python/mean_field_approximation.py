# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mean-field-approximation/. The authors are listed in prov/0P6CAT.jsonl.

"""Naive mean field for an Ising model.

The model on spins s_i in {-1, +1}, i = 0..n-1, is
    p(s) = exp(sum_i h[i] s_i + sum_(i,j) J s_i s_j) / Z
with the couplings given as a list of edges (i, j, J). The family is the
fully factorized q(s) = prod_i q_i(s_i), written by the means m_i = E_q[s_i].
The objective is the lower bound on log Z
    L(m) = sum_i h_i m_i + sum_(i,j) J m_i m_j + sum_i H_b(m_i),
where H_b is the entropy of a spin with mean m. Coordinate ascent sets
m_i = tanh(h_i + sum_j J_ij m_j), one spin at a time.
"""

import itertools
import math


def neighbors(n, edges):
    nb = [[] for _ in range(n)]
    for i, j, w in edges:
        nb[i].append((j, w))
        nb[j].append((i, w))
    return nb


def spin_entropy(m):
    """Entropy (in nats) of a +-1 spin with mean m."""
    h = 0.0
    for p in ((1 + m) / 2, (1 - m) / 2):
        if p > 0:
            h -= p * math.log(p)
    return h


def bound(h, edges, m):
    """L(m) = E_q[log p~(s)] + H(q) for the factorized q with means m."""
    val = sum(hi * mi for hi, mi in zip(h, m))
    val += sum(w * m[i] * m[j] for i, j, w in edges)
    return val + sum(spin_entropy(mi) for mi in m)


def mean_field(h, edges, m0=None, tol=1e-10, max_sweeps=10000, trace=False):
    """Sequential coordinate ascent. Return (m, L(m), sweeps[, trace]).

    With trace=True the value of L after each single update is recorded."""
    n = len(h)
    nb = neighbors(n, edges)
    m = list(m0) if m0 is not None else [0.0] * n
    values = [bound(h, edges, m)] if trace else None
    sweeps = 0
    for sweeps in range(1, max_sweeps + 1):  # @line L1
        delta = 0.0  # @line L2
        for i in range(n):  # @line L3
            new = math.tanh(h[i] + sum(w * m[j] for j, w in nb[i]))  # @line L4
            delta = max(delta, abs(new - m[i]))  # @line L5
            m[i] = new
            if trace:
                values.append(bound(h, edges, m))
        if delta < tol:  # @line L6
            break
    out = (m, bound(h, edges, m), sweeps)  # @line L7
    return out + (values,) if trace else out


def exact(h, edges):
    """log Z and the exact means E_p[s_i] by enumeration of all 2^n states."""
    n = len(h)
    weights = []
    states = list(itertools.product((-1, 1), repeat=n))
    for s in states:
        e = sum(hi * si for hi, si in zip(h, s)) + sum(w * s[i] * s[j] for i, j, w in edges)
        weights.append(e)
    top = max(weights)
    ws = [math.exp(e - top) for e in weights]
    z = sum(ws)
    means = [sum(wk * s[i] for wk, s in zip(ws, states)) / z for i in range(n)]
    return top + math.log(z), means


def kl_q_p(h, edges, m):
    """KL(q || p) = log Z - L(m), by enumeration."""
    return exact(h, edges)[0] - bound(h, edges, m)
