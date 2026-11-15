# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ranknet/. The authors are listed in prov/DHZW3Q.jsonl.

"""RankNet with a linear scoring function s = w . x.

A query is a pair (X, y): X is a list of feature vectors and y the list of
integer labels. For each pair (i, j) of one query with y[i] > y[j] the model
probability that i ranks above j is

    P_ij = 1 / (1 + exp(-sigma (s_i - s_j)))

and the cost of the pair is the cross-entropy with the target 1,

    C_ij = log(1 + exp(-sigma (s_i - s_j))).

The general cost with a target probability pbar is pair_cost below. The
gradient factorizes (Burges 2010, Section 2.1): dC/dw = sum_i lambda_i x_i,
with lambda_i = dC/ds_i, so one pass over the documents replaces one pass
over the pairs. NDCG is computed here only for the tests and the examples;
it uses the gain 2^g - 1 and the discount 1 / log2(rank + 1).
"""

import math


def dot(a, b):
    return sum(p * q for p, q in zip(a, b))


def softplus(z):
    """log(1 + e^z), without overflow."""
    if z > 0:
        return z + math.log1p(math.exp(-z))
    return math.log1p(math.exp(z))


def sigmoid(z):
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    e = math.exp(z)
    return e / (1.0 + e)


def scores(w, xs):
    return [dot(w, x) for x in xs]


def preferred_pairs(y):
    """All (i, j) with y[i] > y[j]."""
    n = len(y)
    return [(i, j) for i in range(n) for j in range(n) if y[i] > y[j]]


def pair_cost(o, pbar, sigma=1.0):
    """Cross-entropy -pbar log P - (1 - pbar) log(1 - P), with P = sigmoid(sigma o)."""
    # -log P = softplus(-sigma o) and -log(1 - P) = softplus(sigma o).
    return pbar * softplus(-sigma * o) + (1.0 - pbar) * softplus(sigma * o)


def query_cost(s, y, sigma=1.0):
    """Sum of C_ij over the preferred pairs of one query, given the scores s."""
    return sum(softplus(-sigma * (s[i] - s[j])) for i, j in preferred_pairs(y))


def cost(w, queries, sigma=1.0):
    return sum(query_cost(scores(w, xs), y, sigma) for xs, y in queries)


def lambdas(s, y, sigma=1.0):
    """lambda_i = dC/ds_i for one query (Burges 2010, Section 2.1)."""
    lam = [0.0] * len(s)
    for i, j in preferred_pairs(y):
        lij = -sigma * sigmoid(-sigma * (s[i] - s[j]))  # dC_ij/ds_i    # @line L4
        lam[i] += lij                                                    # @line L5
        lam[j] -= lij
    return lam


def gradient(w, queries, sigma=1.0):
    """dC/dw by the factorization sum over documents of lambda_i x_i."""
    g = [0.0] * len(w)
    for xs, y in queries:
        lam = lambdas(scores(w, xs), y, sigma)                           # @line L3
        for li, x in zip(lam, xs):
            for k in range(len(w)):
                g[k] += li * x[k]                                        # @line L6
    return g


def gradient_by_pairs(w, queries, sigma=1.0):
    """dC/dw summed pair by pair, without the factorization."""
    g = [0.0] * len(w)
    for xs, y in queries:
        s = scores(w, xs)
        for i, j in preferred_pairs(y):
            c = -sigma * sigmoid(-sigma * (s[i] - s[j]))
            for k in range(len(w)):
                g[k] += c * (xs[i][k] - xs[j][k])
    return g


def lipschitz(queries, sigma=1.0):
    """L = sigma^2 / 4 times the sum of |x_i - x_j|^2 over the preferred pairs.

    The Hessian of C_ij in w is sigma^2 p (1 - p) z z^T with z = x_i - x_j,
    and p (1 - p) <= 1/4, so L bounds the curvature of the whole cost.
    """
    total = 0.0
    for xs, y in queries:
        for i, j in preferred_pairs(y):
            total += sum((a - b) ** 2 for a, b in zip(xs[i], xs[j]))
    return sigma * sigma * total / 4.0


def train(queries, d, sigma=1.0, steps=100):
    """Full-batch gradient descent from w = 0 with the step 1/L.

    Returns w and the list of costs, one per iterate. With this step the
    cost never increases (descent lemma for an L-smooth function).
    """
    w = [0.0] * d                                                        # @line L1
    big_l = lipschitz(queries, sigma)
    history = [cost(w, queries, sigma)]
    if big_l == 0.0:
        return w, history
    eta = 1.0 / big_l
    for _ in range(steps):                                               # @line L2
        g = gradient(w, queries, sigma)
        w = [wk - eta * gk for wk, gk in zip(w, g)]                      # @line L7
        history.append(cost(w, queries, sigma))
    return w, history                                                    # @line L8


def ranking(s):
    """Indices by score descending, then index ascending."""
    return sorted(range(len(s)), key=lambda i: (-s[i], i))


def dcg(labels):
    return sum((2 ** g - 1) / math.log2(r + 2) for r, g in enumerate(labels))


def ndcg(s, y, k=None):
    """NDCG@k with gain 2^g - 1; None when the query has no positive label."""
    k = len(y) if k is None else k
    ideal = dcg(sorted(y, reverse=True)[:k])
    if ideal == 0:
        return None
    return dcg([y[i] for i in ranking(s)[:k]]) / ideal
