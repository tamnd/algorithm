# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/listnet/. The authors are listed in prov/TRPVZ8.jsonl.

"""ListNet with the top-one probability and a linear scoring function.

For one query with scores s and labels y, the top-one probabilities with
phi = exp are the softmax values

    P_s(j) = exp(s_j) / sum_k exp(s_k),   P_y(j) = exp(y_j) / sum_k exp(y_k).

The loss of the query is the cross-entropy L = -sum_j P_y(j) log P_s(j),
and its gradient in s is P_s - P_y. With s_j = w . x_j the gradient in w
is sum_j (P_s(j) - P_y(j)) x_j. Training is full-batch gradient descent
with the step 1 / M, where M = sum over queries of max_j ||x_j||^2 bounds
the curvature, so the loss never increases (see proofs/correctness.md).
NDCG uses the gain 2^g - 1 and the discount 1 / log2(rank + 1).
"""

import math


def dot(a, b):
    return sum(p * q for p, q in zip(a, b))


def softmax(v):
    m = max(v)
    e = [math.exp(x - m) for x in v]
    z = sum(e)
    return [x / z for x in e]


def log_softmax(v):
    m = max(v)
    lz = m + math.log(sum(math.exp(x - m) for x in v))
    return [x - lz for x in v]


def scores(w, xs):
    return [dot(w, x) for x in xs]


def query_loss(s, y):
    py = softmax([float(g) for g in y])
    return -sum(p * l for p, l in zip(py, log_softmax(s)))


def query_score_gradient(s, y):
    """dL/ds = P_s - P_y."""
    return [a - b for a, b in zip(softmax(s), softmax([float(g) for g in y]))]   # @line L4


def loss(w, queries):
    return sum(query_loss(scores(w, xs), y) for xs, y in queries)


def gradient(w, queries):
    g = [0.0] * len(w)
    for xs, y in queries:
        for d, x in zip(query_score_gradient(scores(w, xs), y), xs):     # @line L3
            for c in range(len(w)):
                g[c] += d * x[c]                                         # @line L5
    return g


def curvature_bound(queries):
    """M = sum over queries of max_j ||x_j||^2; the Hessian of the loss is at most M I."""
    return sum(max(dot(x, x) for x in xs) for xs, _ in queries)


def train(queries, d, steps=100):
    """Gradient descent from w = 0 with the step 1 / M. Returns w and the loss history."""
    w = [0.0] * d                                                        # @line L1
    eta = 1.0 / curvature_bound(queries)
    history = [loss(w, queries)]
    for _ in range(steps):                                               # @line L2
        g = gradient(w, queries)
        w = [a - eta * b for a, b in zip(w, g)]                          # @line L6
        history.append(loss(w, queries))
    return w, history                                                    # @line L7


def plackett_luce(s, perm):
    """Probability of the full permutation perm under the Plackett-Luce model with phi = exp."""
    p = 1.0
    rest = list(perm)
    for j in perm:
        p *= math.exp(s[j]) / sum(math.exp(s[k]) for k in rest)
        rest.remove(j)
    return p


def ranking(s):
    return sorted(range(len(s)), key=lambda i: (-s[i], i))


def ndcg(s, y, k=None):
    k = len(y) if k is None else k
    ideal = sum((2 ** g - 1) / math.log2(r + 2) for r, g in enumerate(sorted(y, reverse=True)[:k]))
    if ideal == 0:
        return None
    return sum((2 ** y[d] - 1) / math.log2(r + 2) for r, d in enumerate(ranking(s)[:k])) / ideal


def mean_ndcg(w, queries, k=None):
    vals = [ndcg(scores(w, xs), y, k) for xs, y in queries]
    vals = [v for v in vals if v is not None]
    return sum(vals) / len(vals) if vals else None
