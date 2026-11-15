# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lambdamart/. The authors are listed in prov/HY1P4E.jsonl.

"""LambdaMART: boosted regression trees fitted to LambdaRank lambdas.

The model is F(x) = sum over trees of eta * tree(x). In each round, for
every document i of every query, with the current scores s = F(x):

    rho_ij = 1 / (1 + exp(sigma (s_i - s_j)))        for y_i > y_j
    g_i    = sum_j sigma |dZ_ij| rho_ij - sum_j sigma |dZ_ji| rho_ji
    h_i    = sum over the pairs of i of sigma^2 |dZ| rho (1 - rho)

g_i is minus the derivative, and h_i the second derivative, of the cost
C = sum |dZ_ij| log(1 + exp(-sigma (s_i - s_j))) in s_i, with the weights
|dZ_ij| = |delta NDCG_ij| held fixed at the current ranking. A tree of
depth 1 or 2 is fitted to the targets g_i by least squares, and each leaf
R gets the Newton value sum of g_i / sum of h_i over the documents in R
(Burges 2010, Section 7). NDCG uses the gain 2^g - 1, the discount
1 / log2(rank + 1), and ties by index ascending.
"""

import math


def sigmoid(z):
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    e = math.exp(z)
    return e / (1.0 + e)


def softplus(z):
    if z > 0:
        return z + math.log1p(math.exp(-z))
    return math.log1p(math.exp(z))


def ranking(s):
    return sorted(range(len(s)), key=lambda i: (-s[i], i))


def ideal_dcg(y, k):
    return sum((2 ** g - 1) / math.log2(r + 2) for r, g in enumerate(sorted(y, reverse=True)[:k]))


def ndcg(s, y, k=None):
    k = len(y) if k is None else k
    ideal = ideal_dcg(y, k)
    if ideal == 0:
        return None
    return sum((2 ** y[d] - 1) / math.log2(r + 2) for r, d in enumerate(ranking(s)[:k])) / ideal


def delta_ndcg(s, y, k=None):
    """|delta NDCG_ij| for the pairs with y_i > y_j, at the current ranking."""
    n = len(y)
    k = n if k is None else k
    ideal = ideal_dcg(y, k)
    rank = [0] * n
    for r, d in enumerate(ranking(s)):
        rank[d] = r + 1
    disc = [1.0 / math.log2(rank[i] + 1) if rank[i] <= k else 0.0 for i in range(n)]
    out = {}
    for i in range(n):
        for j in range(n):
            if y[i] > y[j]:
                out[(i, j)] = 0.0 if ideal == 0 else abs((2 ** y[i] - 2 ** y[j]) * (disc[j] - disc[i])) / ideal
    return out


def frozen_cost(s, y, weights, sigma=1.0):
    return sum(v * softplus(-sigma * (s[i] - s[j])) for (i, j), v in weights.items())


def targets_and_weights(s, y, sigma=1.0, k=None):
    """The targets g_i (minus the lambdas) and the Newton weights h_i of one query."""
    n = len(s)
    g = [0.0] * n
    h = [0.0] * n
    for (i, j), dz in delta_ndcg(s, y, k).items():
        rho = sigmoid(-sigma * (s[i] - s[j]))                            # @line L3
        g[i] += sigma * dz * rho                                         # @line L4
        g[j] -= sigma * dz * rho
        hw = sigma * sigma * dz * rho * (1.0 - rho)
        h[i] += hw
        h[j] += hw
    return g, h


class Tree:
    """A regression tree. A node is ('leaf', value) or ('split', f, t, left, right)."""

    def __init__(self, root):
        self.root = root

    def leaf_of(self, x):
        node, path = self.root, ""
        while node[0] == "split":
            if x[node[1]] <= node[2]:
                node, path = node[3], path + "L"
            else:
                node, path = node[4], path + "R"
        return path

    def predict(self, x):
        node = self.root
        while node[0] == "split":
            node = node[3] if x[node[1]] <= node[2] else node[4]
        return node[1]


def sse(vals):
    if not vals:
        return 0.0
    m = sum(vals) / len(vals)
    return sum((v - m) ** 2 for v in vals)


def best_split(xs, g, idx):
    """The (feature, threshold) of least squared error on the targets, or None.

    Thresholds are midpoints between consecutive distinct values. Ties of
    the error keep the first (smallest feature, then smallest threshold).
    """
    best = None
    for f in range(len(xs[0])):
        vals = sorted(set(xs[i][f] for i in idx))
        for a, b in zip(vals, vals[1:]):
            t = (a + b) / 2.0
            left = [g[i] for i in idx if xs[i][f] <= t]
            right = [g[i] for i in idx if xs[i][f] > t]
            err = sse(left) + sse(right)
            if best is None or err < best[0] - 1e-15:
                best = (err, f, t)
    return None if best is None else (best[1], best[2])


def leaf_value(idx, g, h):
    """The Newton step sum g / sum h; 0 if the leaf holds no pair."""
    hs = sum(h[i] for i in idx)
    return sum(g[i] for i in idx) / hs if hs > 0 else 0.0                # @line L6


def build(xs, g, h, idx, depth):
    split = best_split(xs, g, idx) if depth > 0 and len(idx) > 1 else None
    if split is None:
        return ("leaf", leaf_value(idx, g, h))
    f, t = split
    left = [i for i in idx if xs[i][f] <= t]
    right = [i for i in idx if xs[i][f] > t]
    return ("split", f, t, build(xs, g, h, left, depth - 1), build(xs, g, h, right, depth - 1))


def flatten(queries):
    xs, owner = [], []
    for q, (qx, _) in enumerate(queries):
        for x in qx:
            xs.append(x)
            owner.append(q)
    return xs, owner


def round_targets(queries, scores, sigma=1.0, k=None):
    """Targets and weights for all documents, in the order of flatten()."""
    g, h = [], []
    for (qx, y), s in zip(queries, scores):
        gq, hq = targets_and_weights(s, y, sigma, k)
        g += gq
        h += hq
    return g, h


def fit(queries, rounds=20, depth=2, eta=0.1, sigma=1.0, k=None):
    """Train LambdaMART from F = 0. Returns the trees and the mean NDCG@k per round."""
    xs, _ = flatten(queries)
    scores = [[0.0] * len(qx) for qx, _ in queries]                      # @line L1
    trees = []
    history = [mean_ndcg(queries, scores, k)]
    for _ in range(rounds):                                              # @line L2
        g, h = round_targets(queries, scores, sigma, k)
        tree = Tree(build(xs, g, h, list(range(len(xs))), depth))        # @line L5
        trees.append(tree)
        scores = [[s + eta * tree.predict(x) for s, x in zip(sq, qx)] for sq, (qx, _) in zip(scores, queries)]  # @line L7
        history.append(mean_ndcg(queries, scores, k))
    return trees, history                                                # @line L8


def predict(trees, x, eta=0.1):
    return sum(eta * t.predict(x) for t in trees)


def mean_ndcg(queries, scores, k=None):
    vals = [ndcg(s, y, k) for s, (_, y) in zip(scores, queries)]
    vals = [v for v in vals if v is not None]
    return sum(vals) / len(vals) if vals else None
