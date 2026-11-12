# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/residual-belief-propagation/. The authors are listed in prov/BP947G.jsonl.

"""Residual belief propagation (Elidan, McGraw and Koller 2006) on a pairwise
Markov random field, with synchronous loopy BP as a reference.

A model is (card, unary, pair): card[i] is the number of states of x_i,
unary[i][x_i] > 0, and pair maps an edge (i, j) with i < j to a table
pair[(i, j)][x_i][x_j] > 0. The distribution is
    p(x) = prod_i unary[i][x_i] * prod_(i,j) pair[(i, j)][x_i][x_j] / Z.

The message m[(i, j)] is a list over the states of x_j. The candidate message
F_ij(m)(x_j) is proportional to
    sum_{x_i} unary_i(x_i) psi_ij(x_i, x_j) prod_{k in N(i), k != j} m[(k, i)](x_i).
The residual of (i, j) is the max norm of F_ij(m) - m[(i, j)]. Residual BP keeps
the candidates and the residuals of all directed edges in a priority queue and
always commits the message with the largest residual.
"""

import heapq
import itertools
import math


def _normalize(v):
    s = sum(v)
    return [x / s for x in v]


def neighbors(card, pair):
    nb = [[] for _ in card]
    for i, j in pair:
        nb[i].append(j)
        nb[j].append(i)
    return nb


def psi(pair, i, j, xi, xj):
    return pair[(i, j)][xi][xj] if (i, j) in pair else pair[(j, i)][xj][xi]


def candidate(card, unary, pair, nb, m, i, j):
    """F_ij(m): the message that i would send to j now."""
    pre = list(unary[i])
    for k in nb[i]:
        if k != j:
            pre = [p * x for p, x in zip(pre, m[(k, i)])]
    return _normalize([sum(pre[xi] * psi(pair, i, j, xi, xj) for xi in range(card[i])) for xj in range(card[j])])


def residual(a, b):
    return max(abs(x - y) for x, y in zip(a, b))


def beliefs(card, unary, nb, m):
    out = []
    for i in range(len(card)):
        b = list(unary[i])
        for k in nb[i]:
            b = [p * x for p, x in zip(b, m[(k, i)])]
        out.append(_normalize(b))
    return out


def residual_bp(card, unary, pair, tol=1e-10, max_updates=10 ** 6):
    """Return (beliefs, messages, number of committed updates, converged)."""
    nb = neighbors(card, pair)
    directed = [(i, j) for i in range(len(card)) for j in nb[i]]
    m = {e: [1.0 / card[e[1]]] * card[e[1]] for e in directed}  # @line L1
    cand, res, version, heap = {}, {}, {e: 0 for e in directed}, []
    for e in directed:  # @line L2
        cand[e] = candidate(card, unary, pair, nb, m, *e)
        res[e] = residual(cand[e], m[e])
        heapq.heappush(heap, (-res[e], 0, e))
    updates = 0
    converged = False
    while heap and updates < max_updates:  # @line L3
        neg_r, ver, (i, j) = heapq.heappop(heap)  # @line L4
        if ver != version[(i, j)]:
            continue  # a stale entry: the residual of this edge has changed since
        if -neg_r <= tol:  # @line L5
            converged = True
            break
        m[(i, j)] = cand[(i, j)]  # @line L6
        res[(i, j)] = 0.0
        version[(i, j)] += 1
        heapq.heappush(heap, (0.0, version[(i, j)], (i, j)))
        updates += 1
        for k in nb[j]:  # @line L7
            if k != i:
                e = (j, k)
                cand[e] = candidate(card, unary, pair, nb, m, j, k)
                res[e] = residual(cand[e], m[e])
                version[e] += 1
                heapq.heappush(heap, (-res[e], version[e], e))
    if not heap:
        converged = True
    return beliefs(card, unary, nb, m), m, updates, converged  # @line L8


def synchronous_bp(card, unary, pair, tol=1e-10, max_iter=10 ** 5, damping=0.0):
    """Flooding loopy BP. Return (beliefs, messages, number of message updates, converged).
    One iteration recomputes every directed message from the old ones."""
    nb = neighbors(card, pair)
    directed = [(i, j) for i in range(len(card)) for j in nb[i]]
    m = {e: [1.0 / card[e[1]]] * card[e[1]] for e in directed}
    updates = 0
    for _ in range(max_iter):
        new = {e: candidate(card, unary, pair, nb, m, *e) for e in directed}
        delta = max((residual(new[e], m[e]) for e in directed), default=0.0)
        if delta <= tol:
            return beliefs(card, unary, nb, m), m, updates, True
        m = {e: _normalize([(1 - damping) * x + damping * y for x, y in zip(new[e], m[e])]) for e in directed}
        updates += len(directed)
    return beliefs(card, unary, nb, m), m, updates, False


def exact_marginals(card, unary, pair):
    marg = [[0.0] * c for c in card]
    z = 0.0
    for x in itertools.product(*[range(c) for c in card]):
        w = 1.0
        for i, xi in enumerate(x):
            w *= unary[i][xi]
        for (i, j), t in pair.items():
            w *= t[x[i]][x[j]]
        z += w
        for i, xi in enumerate(x):
            marg[i][xi] += w
    return [[v / z for v in mm] for mm in marg]


def ising(n, fields, couplings):
    """Spins in {-1, +1}, state 0 is -1: unary exp(h s), pair exp(J s t)."""
    s = (-1, 1)
    unary = [[math.exp(h * s[a]) for a in range(2)] for h in fields]
    pair = {}
    for i, j, w in couplings:
        a, b = (i, j) if i < j else (j, i)
        pair[(a, b)] = [[math.exp(w * s[x] * s[y]) for y in range(2)] for x in range(2)]
    return [2] * n, unary, pair
