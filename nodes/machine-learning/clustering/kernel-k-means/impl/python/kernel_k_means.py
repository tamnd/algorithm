# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kernel-k-means/. The authors are listed in prov/8RTBTG.jsonl.

"""Weighted kernel k-means: Lloyd's algorithm in a feature space given by a kernel matrix.

The squared distance from phi(x_i) to the weighted mean m_c of cluster c is
    K[i][i] - 2 sum_{j in c} w_j K[i][j] / W_c + sum_{j,l in c} w_j w_l K[j][l] / W_c^2,
with W_c = sum_{j in c} w_j. Only the kernel matrix is used. With all weights 1 this is
plain kernel k-means. The objective falls at each step when K is positive semidefinite.
"""

from typing import Optional, Sequence


def kernel_matrix(points: Sequence, kernel) -> list[list]:
    return [[kernel(x, y) for y in points] for x in points]


def objective(K, labels, k, w=None):
    """sum_i w_i |phi(x_i) - m_{a_i}|^2 for the weighted means of the clusters."""
    n = len(K)
    w = w or [1] * n
    total = sum(w[i] * K[i][i] for i in range(n))
    for c in range(k):
        mem = [i for i in range(n) if labels[i] == c]
        if mem:
            wc = sum(w[i] for i in mem)
            total -= sum(w[i] * w[j] * K[i][j] for i in mem for j in mem) / wc
    return total


def kernel_k_means(
    K: Sequence[Sequence],
    labels: Sequence[int],
    k: int,
    w: Optional[Sequence] = None,
    max_iter: int = 1000,
):
    """Run weighted kernel k-means from the initial labels (values in 0..k-1).

    Returns (labels, history), where history[t] is the objective after the t-th
    reassignment. A point keeps its cluster when that cluster is among the nearest.
    An empty cluster stays empty.
    """
    n = len(K)
    w = list(w) if w is not None else [1] * n
    a = list(labels)
    history = []
    for _ in range(max_iter):  # @line L1
        members = [[i for i in range(n) if a[i] == c] for c in range(k)]
        weight = [sum(w[i] for i in m) for m in members]
        self_term = [  # @line L2
            sum(w[j] * w[l] * K[j][l] for j in m for l in m) / (weight[c] * weight[c]) if m else None
            for c, m in enumerate(members)
        ]
        b = []
        for i in range(n):  # @line L3
            best_c, best_d = None, None
            for c in range(k):
                if not members[c]:
                    continue
                cross = sum(w[j] * K[i][j] for j in members[c]) / weight[c]
                d = K[i][i] - 2 * cross + self_term[c]  # @line L4
                # the current cluster of point i is never empty; it wins all ties
                if best_d is None or d < best_d or (d == best_d and c == a[i]):  # @line L5
                    best_c, best_d = c, d
            b.append(best_c)
        if b == a:  # @line L6
            break
        a = b  # @line L7
        history.append(objective(K, a, k, w))
    return a, history
