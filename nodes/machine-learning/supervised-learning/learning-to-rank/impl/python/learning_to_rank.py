# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/learning-to-rank/. The authors are listed in prov/B37NWE.jsonl.

"""NDCG, linear RankNet, LambdaRank and the ListNet top-one loss.

A query is a list of (feature vector, graded relevance) pairs. The scorer is
linear, s = w . x, and a ranking sorts the items by decreasing score, with
ties broken by the smaller index.

DCG uses the exponential gain 2^rel - 1 and the discount 1 / log2(1 + i) for
the item at rank i = 1, 2, ..., as in Burges et al. 2005. gain="linear" uses
rel as the gain instead.
"""

import math
from typing import Sequence

Query = Sequence[tuple[Sequence[float], int]]


def gain(rel: int, kind: str = "exp") -> float:
    return float(2 ** rel - 1) if kind == "exp" else float(rel)


def dcg(rels_in_rank_order: Sequence[int], k: int | None = None, kind: str = "exp") -> float:
    top = rels_in_rank_order if k is None else rels_in_rank_order[:k]
    return sum(gain(r, kind) / math.log2(i + 2) for i, r in enumerate(top))


def ndcg(rels_in_rank_order: Sequence[int], k: int | None = None, kind: str = "exp") -> float:
    """NDCG@k. A query with no relevant item has ideal DCG 0; we return 0 for it."""
    ideal = dcg(sorted(rels_in_rank_order, reverse=True), k, kind)
    return dcg(rels_in_rank_order, k, kind) / ideal if ideal > 0 else 0.0


def scores(w: Sequence[float], query: Query) -> list[float]:
    return [sum(a * b for a, b in zip(w, x)) for x, _ in query]


def ranking(s: Sequence[float]) -> list[int]:
    return sorted(range(len(s)), key=lambda i: (-s[i], i))


def query_ndcg(w: Sequence[float], query: Query, k: int | None = None) -> float:
    s = scores(w, query)
    return ndcg([query[i][1] for i in ranking(s)], k)


def pairs(query: Query) -> list[tuple[int, int]]:
    """All (i, j) with rel_i > rel_j: item i should be ranked above item j."""
    return [(i, j) for i in range(len(query)) for j in range(len(query)) if query[i][1] > query[j][1]]


def ranknet_loss(w: Sequence[float], queries: Sequence[Query], sigma: float = 1.0) -> float:
    """Sum over pairs of log(1 + exp(-sigma (s_i - s_j))), the cross entropy with target 1."""
    total = 0.0
    for q in queries:
        s = scores(w, q)
        for i, j in pairs(q):
            z = -sigma * (s[i] - s[j])
            total += z + math.log1p(math.exp(-z)) if z > 0 else math.log1p(math.exp(z))
    return total


def _swap_delta_ndcg(rels: Sequence[int], pos: dict, i: int, j: int, ideal: float) -> float:
    """|NDCG change| when items i and j swap their rank positions."""
    if ideal == 0:
        return 0.0
    gi, gj = gain(rels[i]), gain(rels[j])
    di, dj = 1 / math.log2(pos[i] + 2), 1 / math.log2(pos[j] + 2)
    return abs((gi - gj) * (di - dj)) / ideal


def lambdas(w: Sequence[float], query: Query, sigma: float = 1.0, lambdarank: bool = False) -> list[float]:
    """lambda_i for each item, so that the gradient of the query is sum_i lambda_i x_i.

    For a pair (i, j) with rel_i > rel_j, lambda_ij = -sigma / (1 + exp(sigma (s_i - s_j)))
    is dC/ds_i; it adds lambda_ij to lambda_i and subtracts it from lambda_j. LambdaRank
    multiplies lambda_ij by the |NDCG change| of swapping i and j in the current ranking.
    """
    s = scores(w, query)
    lam = [0.0] * len(query)
    rels = [r for _, r in query]
    pos = {item: p for p, item in enumerate(ranking(s))}
    ideal = dcg(sorted(rels, reverse=True))
    for i, j in pairs(query):
        u = sigma * (s[i] - s[j])
        lij = -sigma / (1 + math.exp(u)) if u > -700 else -sigma
        if lambdarank:
            lij *= _swap_delta_ndcg(rels, pos, i, j, ideal)
        lam[i] += lij
        lam[j] -= lij
    return lam


def gradient(w: Sequence[float], queries: Sequence[Query], sigma: float = 1.0, lambdarank: bool = False) -> list[float]:
    g = [0.0] * len(w)
    for q in queries:
        for lam_i, (x, _) in zip(lambdas(w, q, sigma, lambdarank), q):
            for t in range(len(w)):
                g[t] += lam_i * x[t]
    return g


def smoothness_bound(queries: Sequence[Query], sigma: float = 1.0) -> float:
    """L with Hessian <= L I: the second derivative of log(1 + e^-z) is at most 1/4."""
    return sigma * sigma / 4 * sum(
        sum((a - b) ** 2 for a, b in zip(q[i][0], q[j][0])) for q in queries for i, j in pairs(q)
    )


def train(queries: Sequence[Query], dim: int, steps: int, sigma: float = 1.0, lambdarank: bool = False,
          step_size: float | None = None) -> tuple[list[float], list[float]]:
    """Full-batch gradient descent from w = 0. Return w and the RankNet loss after each step.

    With step_size = 1/L (the default) and RankNet gradients, the loss never increases,
    because the loss is convex and L-smooth.
    """
    eta = step_size if step_size is not None else 1 / max(smoothness_bound(queries, sigma), 1e-12)
    w = [0.0] * dim
    history = [ranknet_loss(w, queries, sigma)]
    for _ in range(steps):
        g = gradient(w, queries, sigma, lambdarank)
        w = [a - eta * b for a, b in zip(w, g)]
        history.append(ranknet_loss(w, queries, sigma))
    return w, history


def listnet_loss(w: Sequence[float], query: Query) -> float:
    """Top-one ListNet: cross entropy between softmax(rel) and softmax(s)."""
    s = scores(w, query)
    rels = [float(r) for _, r in query]
    ms, mr = max(s), max(rels)
    zs = math.log(sum(math.exp(v - ms) for v in s)) + ms
    zr = sum(math.exp(v - mr) for v in rels)
    return -sum(math.exp(r - mr) / zr * (si - zs) for r, si in zip(rels, s))


def listnet_gradient(w: Sequence[float], query: Query) -> list[float]:
    s = scores(w, query)
    rels = [float(r) for _, r in query]
    ms, mr = max(s), max(rels)
    zs = sum(math.exp(v - ms) for v in s)
    zr = sum(math.exp(v - mr) for v in rels)
    coef = [math.exp(si - ms) / zs - math.exp(r - mr) / zr for si, r in zip(s, rels)]
    return [sum(c * x[t] for c, (x, _) in zip(coef, query)) for t in range(len(w))]
