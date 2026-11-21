# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/truncated-svd/. The authors are listed in prov/7EBBWK.jsonl.
"""Truncated singular value decomposition (TSVD) for a real linear system A x = y.

The regularized solution is x_k = sum_{i=1}^{k} (<u_i, y> / sigma_i) v_i, with
the singular triples of A in descending order of sigma_i.
"""

import math

from imgla import svd


def tsvd(a, y, k):
    """The TSVD solution x_k of A x = y. Computes one SVD of A."""
    u, s, v = svd(a)  # @line L1
    return tsvd_from_svd(u, s, v, y, k)


def tsvd_from_svd(u, s, v, y, k):
    """x_k from a thin SVD (U, S, V) of A, S descending. Costs O(k (m + n))."""
    if not 0 <= k <= len(s):
        raise ValueError("k must be between 0 and min(m, n)")
    if k > 0 and not s[k - 1] > 0.0:
        raise ValueError("k is larger than the rank")
    m, n = len(u), len(v)
    x = [0.0] * n  # @line L2
    for i in range(k):  # @line L3
        c = sum(u[r][i] * y[r] for r in range(m)) / s[i]  # @line L4
        for j in range(n):  # @line L5
            x[j] += c * v[j][i]
    return x  # @line L6


def tsvd_path(u, s, y):
    """Residual norms and solution norms of x_k for k = 0, 1, ..., r.

    With beta_i = <u_i, y>: ||A x_k - y||^2 = ||y_perp||^2 + sum_{i>k} beta_i^2,
    where y_perp is the part of y outside the range of A, and
    ||x_k||^2 = sum_{i<=k} (beta_i / sigma_i)^2. r is the number of positive
    singular values. Costs O(m r) for the coefficients, then O(1) per k.
    """
    m = len(u)
    r = sum(1 for si in s if si > 0.0)
    beta = [sum(u[q][i] * y[q] for q in range(m)) for i in range(r)]  # @line L7
    perp = [y[q] - sum(beta[i] * u[q][i] for i in range(r)) for q in range(m)]
    tail = [0.0] * (r + 1)
    tail[r] = sum(v * v for v in perp)
    for i in range(r - 1, -1, -1):  # @line L8
        tail[i] = tail[i + 1] + beta[i] * beta[i]  # @line L9
    sol2 = 0.0
    norms = [0.0]
    for i in range(r):
        sol2 += (beta[i] / s[i]) ** 2
        norms.append(math.sqrt(sol2))
    return [math.sqrt(t) for t in tail], norms


def discrepancy_index(residuals, delta, tau=1.1):
    """The smallest k with ||A x_k - y|| <= tau delta, or None if no k qualifies."""
    for k, rk in enumerate(residuals):  # @line L10
        if rk <= tau * delta:
            return k
    return None


def filter_factors(k, p):
    """The TSVD filter factors f_i = 1 for i <= k and 0 for k < i <= p."""
    return [1.0 if i < k else 0.0 for i in range(p)]
