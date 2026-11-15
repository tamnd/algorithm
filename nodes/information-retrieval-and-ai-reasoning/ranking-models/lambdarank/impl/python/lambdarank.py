# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lambdarank/. The authors are listed in prov/6YEMD5.jsonl.

"""LambdaRank lambdas for a linear scoring function s = w . x.

For a pair (i, j) of one query with y[i] > y[j], RankNet has the gradient

    dC_ij/ds_i = -sigma / (1 + exp(sigma (s_i - s_j))).

LambdaRank multiplies it by |delta NDCG_ij|, the change of NDCG@k when the
documents i and j swap their positions in the current ranking, and sums
the results per document:

    lambda_i = sum over j with y_i > y_j of lambda_ij
             - sum over j with y_j > y_i of lambda_ji.

The lambdas are defined directly. They are not the gradient of NDCG, which
is flat almost everywhere. The update is w <- w - eta sum_i lambda_i x_i.
NDCG uses the gain 2^g - 1 and the discount 1 / log2(rank + 1), and the
ranking sorts by score descending, then by index ascending.
"""

import math


def dot(a, b):
    return sum(p * q for p, q in zip(a, b))


def sigmoid(z):
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    e = math.exp(z)
    return e / (1.0 + e)


def softplus(z):
    if z > 0:
        return z + math.log1p(math.exp(-z))
    return math.log1p(math.exp(z))


def scores(w, xs):
    return [dot(w, x) for x in xs]


def ranking(s):
    """Indices by score descending, then index ascending."""
    return sorted(range(len(s)), key=lambda i: (-s[i], i))


def gain(g):
    return 2 ** g - 1


def discount(r):
    """The discount of rank r (r starts at 1)."""
    return 1.0 / math.log2(r + 1)


def ideal_dcg(y, k):
    return sum(gain(g) * discount(r + 1) for r, g in enumerate(sorted(y, reverse=True)[:k]))


def ndcg_of_order(order, y, k=None):
    """NDCG@k of a given order of the documents; None if no positive label."""
    k = len(y) if k is None else k
    ideal = ideal_dcg(y, k)
    if ideal == 0:
        return None
    return sum(gain(y[d]) * discount(r + 1) for r, d in enumerate(order[:k])) / ideal


def ndcg(s, y, k=None):
    return ndcg_of_order(ranking(s), y, k)


def delta_ndcg(s, y, k=None):
    """|delta NDCG_ij| for every pair, by the closed form.

    With r_i the rank of i in the current ranking, the swap changes DCG@k
    by (gain(y_i) - gain(y_j)) (D(r_j) - D(r_i)), where D(r) is the
    discount of rank r if r <= k and 0 otherwise.
    """
    n = len(y)
    k = n if k is None else k
    ideal = ideal_dcg(y, k)
    rank = [0] * n
    for r, d in enumerate(ranking(s)):                                   # @line L3
        rank[d] = r + 1
    disc = [discount(rank[i]) if rank[i] <= k else 0.0 for i in range(n)]
    out = {}
    for i in range(n):
        for j in range(n):
            if y[i] > y[j]:
                out[(i, j)] = 0.0 if ideal == 0 else abs((gain(y[i]) - gain(y[j])) * (disc[j] - disc[i])) / ideal
    return out


def ranknet_pair_gradient(s, i, j, sigma=1.0):
    """dC_ij/ds_i of the RankNet cost log(1 + exp(-sigma (s_i - s_j)))."""
    return -sigma * sigmoid(-sigma * (s[i] - s[j]))


def pair_lambdas(s, y, sigma=1.0, k=None):
    """lambda_ij for every pair with y_i > y_j."""
    dz = delta_ndcg(s, y, k)
    return {(i, j): ranknet_pair_gradient(s, i, j, sigma) * v for (i, j), v in dz.items()}   # @line L4


def lambdas(s, y, sigma=1.0, k=None):
    """The per-document lambdas (Burges 2010, Section 4.1)."""
    lam = [0.0] * len(s)
    for (i, j), v in pair_lambdas(s, y, sigma, k).items():
        lam[i] += v                                                      # @line L5
        lam[j] -= v
    return lam


def frozen_cost(s, y, weights, sigma=1.0):
    """sum of |delta Z_ij| log(1 + exp(-sigma (s_i - s_j))) with fixed weights.

    For scores near s with the same ranking, the gradient of this function
    in s is the lambda vector (Burges 2010, Section 4.3).
    """
    return sum(v * softplus(-sigma * (s[i] - s[j])) for (i, j), v in weights.items())


def direction(w, queries, sigma=1.0, k=None):
    """sum over queries and documents of lambda_i x_i."""
    g = [0.0] * len(w)
    for xs, y in queries:
        lam = lambdas(scores(w, xs), y, sigma, k)
        for li, x in zip(lam, xs):
            for c in range(len(w)):
                g[c] += li * x[c]
    return g


def train(queries, d, eta=0.1, sigma=1.0, k=None, steps=100):
    """Full-batch steps w <- w - eta * direction, from w = 0.

    Returns w and the mean NDCG@k after each step. Nothing guarantees that
    the mean NDCG grows; it is measured.
    """
    w = [0.0] * d                                                        # @line L1
    history = [mean_ndcg(w, queries, k)]
    for _ in range(steps):                                               # @line L2
        g = direction(w, queries, sigma, k)
        w = [a - eta * b for a, b in zip(w, g)]                          # @line L6
        history.append(mean_ndcg(w, queries, k))
    return w, history                                                    # @line L7


def mean_ndcg(w, queries, k=None):
    vals = [ndcg(scores(w, xs), y, k) for xs, y in queries]
    vals = [v for v in vals if v is not None]
    return sum(vals) / len(vals) if vals else None
