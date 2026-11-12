# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bethe-free-energy/. The authors are listed in prov/QK8KM6.jsonl.

"""The Bethe free energy of a factor graph at a point of the local polytope.

A model is a list card of variable cardinalities and a list of factors. Each
factor is a pair (scope, table): scope is a tuple of distinct variables and
table maps each assignment tuple of the scope to a positive number. The
distribution is p(x) = prod_a f_a(x_a) / Z.

Beliefs are var_beliefs[i][x_i] and factor_beliefs[a][x_a] (a dict keyed like
the table). The Bethe free energy is

    F(b) = sum_a sum_{x_a} b_a log(b_a / f_a) - sum_i (d_i - 1) sum_{x_i} b_i log b_i
         = U(b) - H_Bethe(b),

with U(b) = -sum_a sum b_a log f_a (the average energy) and
H_Bethe(b) = sum_a H(b_a) - sum_i (d_i - 1) H(b_i), where d_i is the number
of factors that contain x_i. The convention 0 log 0 = 0 is used.
"""

import itertools
import math


def _plogp(p):
    return p * math.log(p) if p > 0 else 0.0


def degrees(card, factors):
    d = [0] * len(card)
    for scope, _ in factors:
        for i in scope:
            d[i] += 1
    return d


def average_energy(factors, factor_beliefs):
    return -sum(prob * math.log(table[x]) for (_, table), b in zip(factors, factor_beliefs) for x, prob in b.items())


def bethe_entropy(card, factors, var_beliefs, factor_beliefs):
    d = degrees(card, factors)
    h_factors = -sum(_plogp(prob) for b in factor_beliefs for prob in b.values())
    h_vars = -sum((d[i] - 1) * sum(_plogp(p) for p in var_beliefs[i]) for i in range(len(card)))
    return h_factors - h_vars


def bethe_free_energy(card, factors, var_beliefs, factor_beliefs):
    """F_Bethe(b) = U(b) - H_Bethe(b)."""
    return average_energy(factors, factor_beliefs) - bethe_entropy(card, factors, var_beliefs, factor_beliefs)


def in_local_polytope(card, factors, var_beliefs, factor_beliefs, tol=1e-9):
    """Nonnegative, normalized, and each factor belief sums to each variable belief."""
    for i, b in enumerate(var_beliefs):
        if len(b) != card[i] or min(b) < -tol or abs(sum(b) - 1) > tol:
            return False
    for (scope, _), b in zip(factors, factor_beliefs):
        if min(b.values()) < -tol or abs(sum(b.values()) - 1) > tol:
            return False
        for pos, i in enumerate(scope):
            marg = [0.0] * card[i]
            for x, prob in b.items():
                marg[x[pos]] += prob
            if max(abs(u - v) for u, v in zip(marg, var_beliefs[i])) > tol:
                return False
    return True


def exact_beliefs(card, factors):
    """The exact variable marginals, factor marginals and log Z, by enumeration."""
    var_b = [[0.0] * c for c in card]
    fac_b = [{x: 0.0 for x in table} for _, table in factors]
    z = 0.0
    for x in itertools.product(*[range(c) for c in card]):
        w = 1.0
        for scope, table in factors:
            w *= table[tuple(x[j] for j in scope)]
        z += w
        for i, xi in enumerate(x):
            var_b[i][xi] += w
        for a, (scope, _) in enumerate(factors):
            fac_b[a][tuple(x[j] for j in scope)] += w
    var_b = [[v / z for v in b] for b in var_b]
    fac_b = [{k: v / z for k, v in b.items()} for b in fac_b]
    return var_b, fac_b, math.log(z)


def gibbs_free_energy(card, factors, q):
    """The exact variational free energy G(q) = sum_x q log q - sum_x q log prod f
    of a full joint q (a dict over all assignments). Its minimum is -log Z at q = p."""
    g = 0.0
    for x, prob in q.items():
        if prob > 0:
            w = 1.0
            for scope, table in factors:
                w *= table[tuple(x[j] for j in scope)]
            g += prob * (math.log(prob) - math.log(w))
    return g


def ising_factors(n, fields, couplings):
    """Factors of an Ising model on spins in {-1, +1} (state 0 is -1, state 1 is +1)."""
    spin = (-1, 1)
    factors = []
    for i, h in enumerate(fields):
        factors.append(((i,), {(a,): math.exp(h * spin[a]) for a in range(2)}))
    for i, j, w in couplings:
        factors.append(((i, j), {(a, b): math.exp(w * spin[a] * spin[b]) for a in range(2) for b in range(2)}))
    return [2] * n, factors


def symmetric_ising_beliefs(n, factors, m, c):
    """Beliefs with b_i(s) = (1 + m s)/2 for every spin and b_ij(s, t) = (1 + m s + m t + c s t)/4
    for every pair factor. They are in the local polytope when every b_ij >= 0."""
    spin = (-1, 1)
    var_b = [[(1 - m) / 2, (1 + m) / 2] for _ in range(n)]
    fac_b = []
    for scope, _ in factors:
        if len(scope) == 1:
            fac_b.append({(a,): (1 + m * spin[a]) / 2 for a in range(2)})
        else:
            fac_b.append({(a, b): (1 + m * spin[a] + m * spin[b] + c * spin[a] * spin[b]) / 4
                          for a in range(2) for b in range(2)})
    return var_b, fac_b
