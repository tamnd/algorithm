# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/loopy-belief-propagation/. The authors are listed in prov/BP1TB7.jsonl.

"""Loopy belief propagation (sum-product) on a factor graph, with damping.

A model is a list card of variable cardinalities and a list of factors. Each
factor is a pair (scope, table): scope is a tuple of distinct variables and
table maps each assignment tuple of the scope to a positive number. The
distribution is p(x) = prod_a f_a(x_a) / Z.

The schedule is synchronous (flooding): in one iteration every variable to
factor message is computed from the old factor to variable messages, and then
every factor to variable message is computed from the new variable to factor
messages. Damping mixes each new factor to variable message with the old one:
    mu <- (1 - damping) * mu_new + damping * mu_old.
"""

import itertools
import math


def _normalize(v):
    s = sum(v)
    return [x / s for x in v]


def _edges(card, factors):
    var_factors = [[] for _ in card]
    for a, (scope, _) in enumerate(factors):
        for i in scope:
            var_factors[i].append(a)
    return var_factors


def var_to_factor(card, var_factors, f2v, i, a):
    """nu_{i->a}(x_i): the product of the messages from the other factors of i."""
    out = [1.0] * card[i]
    for b in var_factors[i]:
        if b != a:
            m = f2v[(b, i)]
            out = [o * x for o, x in zip(out, m)]
    return _normalize(out)


def factor_to_var(card, factors, v2f, a, i):
    """mu_{a->i}(x_i): sum over the other variables of f_a times their messages."""
    scope, table = factors[a]
    pos = scope.index(i)
    out = [0.0] * card[i]
    for assignment in itertools.product(*[range(card[j]) for j in scope]):
        w = table[assignment]
        for k, j in enumerate(scope):
            if k != pos:
                w *= v2f[(j, a)][assignment[k]]
        out[assignment[pos]] += w
    return _normalize(out)


def loopy_bp(card, factors, damping=0.0, tol=1e-10, max_iter=1000, record=False, rng=None):
    """Run loopy BP. Return a dict with the variable beliefs, the factor beliefs,
    the number of iterations, whether it converged, the final messages and,
    with record=True, the belief of variable 0 after each iteration."""
    if not 0.0 <= damping < 1.0:
        raise ValueError("damping must be in [0, 1)")
    var_factors = _edges(card, factors)
    f2v = {(a, i): [1.0 / card[i]] * card[i] for a, (scope, _) in enumerate(factors) for i in scope}  # @line L1
    if rng is not None:  # a random positive start, for tests of uniqueness
        f2v = {key: _normalize([rng.uniform(0.05, 1.0) for _ in v]) for key, v in f2v.items()}
    v2f = {}
    history = []
    converged = False
    it = 0
    for it in range(1, max_iter + 1):  # @line L2
        v2f = {(i, a): var_to_factor(card, var_factors, f2v, i, a) for (a, i) in f2v}  # @line L3
        new = {(a, i): factor_to_var(card, factors, v2f, a, i) for (a, i) in f2v}  # @line L4
        delta = max(abs(x - y) for key in f2v for x, y in zip(new[key], f2v[key]))  # @line L5
        f2v = {key: _normalize([(1 - damping) * x + damping * y for x, y in zip(new[key], f2v[key])])
               for key in f2v}  # @line L6
        if record:
            history.append(variable_beliefs(card, var_factors, f2v)[0])
        if delta < tol:  # @line L7
            converged = True
            break
    v2f = {(i, a): var_to_factor(card, var_factors, f2v, i, a) for (a, i) in f2v}
    return {  # @line L8
        "beliefs": variable_beliefs(card, var_factors, f2v),
        "factor_beliefs": factor_beliefs(card, factors, v2f),
        "iterations": it,
        "converged": converged,
        "f2v": f2v,
        "v2f": v2f,
        "history": history,
    }


def variable_beliefs(card, var_factors, f2v):
    out = []
    for i in range(len(card)):
        b = [1.0] * card[i]
        for a in var_factors[i]:
            b = [x * y for x, y in zip(b, f2v[(a, i)])]
        out.append(_normalize(b))
    return out


def factor_beliefs(card, factors, v2f):
    out = []
    for a, (scope, table) in enumerate(factors):
        b = {}
        for assignment, w in table.items():
            for k, j in enumerate(scope):
                w *= v2f[(j, a)][assignment[k]]
            b[assignment] = w
        s = sum(b.values())
        out.append({k: v / s for k, v in b.items()})
    return out


def exact_marginals(card, factors):
    """Exact single-variable marginals and log Z by enumeration."""
    marg = [[0.0] * c for c in card]
    z = 0.0
    for x in itertools.product(*[range(c) for c in card]):
        w = 1.0
        for scope, table in factors:
            w *= table[tuple(x[j] for j in scope)]
        z += w
        for i, xi in enumerate(x):
            marg[i][xi] += w
    return [[v / z for v in m] for m in marg], math.log(z)


def mooij_kappen_radius(n, couplings, iters=2000):
    """Spectral radius of the Mooij-Kappen matrix of a binary pairwise model.

    The rows and columns are the directed edges i->j, and the entry for
    (i->j, k->i) with k != j is tanh|J_ki|. If the radius is below 1, BP
    converges to a unique fixed point from any start (Mooij and Kappen 2007).
    The matrix is nonnegative, so the power method from the all-ones vector
    gives the radius (it is an estimate only if the matrix is reducible)."""
    nb = [[] for _ in range(n)]
    w = {}
    for i, j, c in couplings:
        nb[i].append(j)
        nb[j].append(i)
        w[(i, j)] = w[(j, i)] = math.tanh(abs(c))
    directed = [(i, j) for i in range(n) for j in nb[i]]
    if not directed:
        return 0.0
    v = {e: 1.0 for e in directed}
    logs = [0.0]
    for _ in range(iters):
        nv = {(i, j): sum(w[(k, i)] * v[(k, i)] for k in nb[i] if k != j) for (i, j) in directed}
        norm = max(nv.values())
        if norm == 0.0:
            return 0.0
        logs.append(logs[-1] + math.log(norm))
        v = {e: x / norm for e, x in nv.items()}
    half = iters // 2
    # ||A^k 1|| grows like rho^k; the ratio over the second half removes the start-up.
    return math.exp((logs[iters] - logs[half]) / (iters - half))


def ising_factors(n, fields, couplings):
    """Factors of an Ising model on spins in {-1, +1} (state 0 is -1, state 1 is +1):
    unary exp(h_i s_i) and pairwise exp(J s_i s_j)."""
    spin = (-1, 1)
    factors = []
    for i, h in enumerate(fields):
        factors.append(((i,), {(a,): math.exp(h * spin[a]) for a in range(2)}))
    for i, j, w in couplings:
        factors.append(((i, j), {(a, b): math.exp(w * spin[a] * spin[b]) for a in range(2) for b in range(2)}))
    return [2] * n, factors
