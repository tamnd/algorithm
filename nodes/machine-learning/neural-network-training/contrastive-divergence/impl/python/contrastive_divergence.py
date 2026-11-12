# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/contrastive-divergence/. The authors are listed in prov/ZQSFAJ.jsonl.

"""Contrastive divergence (CD-k) and persistent CD for a binary restricted Boltzmann machine.

The RBM has m visible units v in {0,1}^m and n hidden units h in {0,1}^n with
energy E(v, h) = -a.v - b.h - v^T W h and p(v, h) = exp(-E) / Z. Parameters
are (W, a, b) with W an m x n list of lists.

For small m the module also computes, by enumeration of all 2^m visible
states, the exact log likelihood, its exact gradient, the visible Gibbs
transition matrix T and the exact expected CD-k update, so that the sampled
algorithm can be checked against exact values.
"""

import itertools
import math
from typing import List, Sequence, Tuple

Vector = List[float]
Matrix = List[List[float]]
Params = Tuple[Matrix, Vector, Vector]


def sigmoid(x: float) -> float:
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    e = math.exp(x)
    return e / (1.0 + e)


def softplus(x: float) -> float:
    return max(x, 0.0) + math.log1p(math.exp(-abs(x)))


def hidden_probs(params: Params, v: Sequence[int]) -> Vector:
    """p(h_j = 1 | v) = sigmoid(b_j + sum_i v_i W_ij)."""
    w, _, b = params
    return [sigmoid(b[j] + sum(v[i] * w[i][j] for i in range(len(v)))) for j in range(len(b))]


def visible_probs(params: Params, h: Sequence[int]) -> Vector:
    """p(v_i = 1 | h) = sigmoid(a_i + sum_j W_ij h_j)."""
    w, a, _ = params
    return [sigmoid(a[i] + sum(w[i][j] * h[j] for j in range(len(h)))) for i in range(len(a))]


def bernoulli(ps: Sequence[float], rng) -> List[int]:
    return [1 if rng.random() < p else 0 for p in ps]


def stats(v: Sequence[int], q: Sequence[float]) -> Tuple[Matrix, Vector, Vector]:
    """The sufficient statistics (v q^T, v, q) of one visible vector and its hidden probabilities."""
    return [[vi * qj for qj in q] for vi in v], [float(x) for x in v], list(q)


def _add(acc, s, c=1.0):
    gw, ga, gb = acc
    sw, sa, sb = s
    for i in range(len(gw)):
        for j in range(len(gw[i])):
            gw[i][j] += c * sw[i][j]
        ga[i] += c * sa[i]
    for j in range(len(gb)):
        gb[j] += c * sb[j]


def _zeros(m: int, n: int):
    return [[0.0] * n for _ in range(m)], [0.0] * m, [0.0] * n


def _scale(g, c):
    gw, ga, gb = g
    return [[x * c for x in row] for row in gw], [x * c for x in ga], [x * c for x in gb]


def gibbs_chain(params: Params, v0: Sequence[int], k: int, rng) -> Tuple[List[int], Vector]:
    """Run k full Gibbs steps v -> h -> v from v0. Returns v_k and p(h | v_k)."""
    v = list(v0)
    for _ in range(k):
        h = bernoulli(hidden_probs(params, v), rng)
        v = bernoulli(visible_probs(params, h), rng)
    return v, hidden_probs(params, v)


def cd_gradient(params: Params, batch: Sequence[Sequence[int]], k: int, rng):
    """The CD-k estimate of the log likelihood gradient, averaged over the batch.

    Positive phase: v0 p(h | v0)^T. Negative phase: v_k p(h | v_k)^T, with v_k
    from k Gibbs steps started at the data vector v0.
    """
    m, n = len(params[1]), len(params[2])
    g = _zeros(m, n)  # @line L1
    for v0 in batch:  # @line L2
        p0 = hidden_probs(params, v0)  # @line L3
        v, h = list(v0), bernoulli(p0, rng)  # @line L4
        q = p0
        for t in range(1, k + 1):  # @line L5
            v = bernoulli(visible_probs(params, h), rng)  # @line L6
            q = hidden_probs(params, v)  # @line L7
            if t < k:  # @line L8
                h = bernoulli(q, rng)
        _add(g, stats(v0, p0))  # @line L9 (with L10: the statistics of W, a and b together)
        _add(g, stats(v, q), -1.0)  # @line L10
    return _scale(g, 1.0 / len(batch))


def cd_update(params: Params, batch: Sequence[Sequence[int]], k: int, eta: float, rng) -> Params:
    """One CD-k update of (W, a, b) with learning rate eta on a minibatch."""
    return step(params, cd_gradient(params, batch, k, rng), eta)  # @line L11


def pcd_gradient(params: Params, batch: Sequence[Sequence[int]], chains: List[List[int]], k: int, rng):
    """Persistent CD (Tieleman 2008): the negative phase continues the chains of the previous update.

    `chains` is updated in place.
    """
    m, n = len(params[1]), len(params[2])
    g = _zeros(m, n)
    for v0 in batch:
        _add(g, stats(v0, hidden_probs(params, v0)), 1.0 / len(batch))
    for c in range(len(chains)):
        vk, qk = gibbs_chain(params, chains[c], k, rng)
        chains[c] = vk
        _add(g, stats(vk, qk), -1.0 / len(chains))
    return g


def step(params: Params, grad, eta: float) -> Params:
    """Gradient ascent: params + eta * grad."""
    (w, a, b), (gw, ga, gb) = params, grad
    return ([[x + eta * y for x, y in zip(rw, rg)] for rw, rg in zip(w, gw)],
            [x + eta * y for x, y in zip(a, ga)], [x + eta * y for x, y in zip(b, gb)])


# Exact quantities by enumeration (small m only).

def all_states(m: int) -> List[Tuple[int, ...]]:
    return list(itertools.product((0, 1), repeat=m))


def free_energy(params: Params, v: Sequence[int]) -> float:
    """F(v) = -a.v - sum_j softplus(b_j + sum_i v_i W_ij), so that p(v) = exp(-F(v)) / Z."""
    w, a, b = params
    return -sum(ai * vi for ai, vi in zip(a, v)) - sum(
        softplus(b[j] + sum(v[i] * w[i][j] for i in range(len(v)))) for j in range(len(b)))


def visible_marginal(params: Params) -> Tuple[List[Tuple[int, ...]], Vector]:
    """All visible states and their probabilities p(v)."""
    states = all_states(len(params[1]))
    neg = [-free_energy(params, v) for v in states]
    top = max(neg)
    e = [math.exp(x - top) for x in neg]
    s = sum(e)
    return states, [x / s for x in e]


def log_likelihood(params: Params, data: Sequence[Sequence[int]]) -> float:
    """The mean of log p(v) over the data."""
    states = all_states(len(params[1]))
    neg = [-free_energy(params, v) for v in states]
    top = max(neg)
    log_z = top + math.log(sum(math.exp(x - top) for x in neg))
    return sum(-free_energy(params, v) - log_z for v in data) / len(data)


def model_stats(params: Params, dist: Sequence[float]):
    """sum over v of dist(v) times (v q(v)^T, v, q(v))."""
    m, n = len(params[1]), len(params[2])
    g = _zeros(m, n)
    for v, pv in zip(all_states(m), dist):
        if pv:
            _add(g, stats(v, hidden_probs(params, v)), pv)
    return g


def exact_gradient(params: Params, data: Sequence[Sequence[int]]):
    """The gradient of the mean log likelihood: data statistics minus model statistics."""
    m, n = len(params[1]), len(params[2])
    g = _zeros(m, n)
    for v in data:
        _add(g, stats(v, hidden_probs(params, v)), 1.0 / len(data))
    _, p = visible_marginal(params)
    _add(g, model_stats(params, p), -1.0)
    return g


def transition_matrix(params: Params) -> Matrix:
    """T[v][v'] = sum_h p(h | v) p(v' | h): one Gibbs step on the visible units."""
    m, n = len(params[1]), len(params[2])
    vs, hs = all_states(m), all_states(n)
    hcond = []
    for h in hs:
        pv = visible_probs(params, h)
        hcond.append([math.prod(p if x else 1 - p for p, x in zip(pv, v2)) for v2 in vs])
    t = []
    for v in vs:
        ph = hidden_probs(params, v)
        wts = [math.prod(p if x else 1 - p for p, x in zip(ph, h)) for h in hs]
        t.append([sum(wts[r] * hcond[r][c] for r in range(len(hs))) for c in range(len(vs))])
    return t


def expected_cd(params: Params, data: Sequence[Sequence[int]], k: int):
    """The exact expectation of cd_gradient: the negative phase uses the law T^k(v0, .) of v_k."""
    m, n = len(params[1]), len(params[2])
    vs = all_states(m)
    index = {v: i for i, v in enumerate(vs)}
    t = transition_matrix(params)
    start = [0.0] * len(vs)
    for v in data:
        start[index[tuple(v)]] += 1.0 / len(data)
    dist = start
    for _ in range(k):
        dist = [sum(dist[r] * t[r][c] for r in range(len(vs))) for c in range(len(vs))]
    g = _zeros(m, n)
    _add(g, model_stats(params, start))
    _add(g, model_stats(params, dist), -1.0)
    return g


def flatten(g) -> Vector:
    gw, ga, gb = g
    return [x for row in gw for x in row] + list(ga) + list(gb)


def unflatten(x: Sequence[float], m: int, n: int) -> Params:
    w = [list(x[i * n:(i + 1) * n]) for i in range(m)]
    return w, list(x[m * n:m * n + m]), list(x[m * n + m:])
