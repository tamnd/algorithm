# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/trustworthiness-and-continuity/. The authors are listed in prov/B3SH8J.jsonl.
"""Trustworthiness and continuity of an embedding (Venna and Kaski 2001, 2006).

For k < n/2, with r(i, j) the rank of j among the other points by input distance from i
(1 for the nearest), r'(i, j) the same rank in the embedding, N_k(i) and N'_k(i) the k
nearest neighbors of i in the input and in the embedding:

    T(k) = 1 - 2 / (n k (2n - 3k - 1)) * sum_i sum_{j in N'_k(i) minus N_k(i)} (r(i, j) - k)
    C(k) = 1 - 2 / (n k (2n - 3k - 1)) * sum_i sum_{j in N_k(i) minus N'_k(i)} (r'(i, j) - k)

Ties in distance are broken by the index of the point, so the ranks are a permutation.
"""

import math


def rank_matrix(points):
    """rank[i][j] = the rank of j by distance from i among the other points; rank[i][i] = 0."""
    n = len(points)
    ranks = []
    for i in range(n):
        order = sorted((j for j in range(n) if j != i), key=lambda j: (math.dist(points[i], points[j]), j))
        row = [0] * n
        for r, j in enumerate(order, 1):
            row[j] = r
        ranks.append(row)
    return ranks


def normalizer(n, k):
    """The factor 2 / (n k (2n - 3k - 1)); it needs 1 <= k < n / 2."""
    if not 1 <= k or not 2 * k < n:
        raise ValueError("need 1 <= k < n/2")
    return 2.0 / (n * k * (2 * n - 3 * k - 1))


def _penalty(rank_from, rank_to, k):
    """Sum over i of (rank_from[i][j] - k) for j in the k-neighborhood of rank_to but not of rank_from."""
    total = 0
    for i in range(len(rank_from)):
        for j, r in enumerate(rank_to[i]):
            if 1 <= r <= k and rank_from[i][j] > k:
                total += rank_from[i][j] - k
    return total


def trustworthiness(x, y, k):
    """T(k) for input points x and embedded points y (lists of equal length)."""
    rx, ry = rank_matrix(x), rank_matrix(y)
    return 1.0 - normalizer(len(x), k) * _penalty(rx, ry, k)


def continuity(x, y, k):
    """C(k): the trustworthiness with the roles of the two spaces exchanged."""
    rx, ry = rank_matrix(x), rank_matrix(y)
    return 1.0 - normalizer(len(x), k) * _penalty(ry, rx, k)


def trustworthiness_and_continuity(x, y, k):
    rx, ry = rank_matrix(x), rank_matrix(y)
    c = normalizer(len(x), k)
    return 1.0 - c * _penalty(rx, ry, k), 1.0 - c * _penalty(ry, rx, k)
