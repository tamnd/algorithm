# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/alibi-attention-bias/. The authors are listed in prov/FKDFWV.jsonl.

"""Attention with linear biases (ALiBi) of Press, Smith and Lewis.

One causal attention head with slope m > 0. Query i at position p_i sees the
keys at positions j <= p_i, and its score for key j is

    s_ij = q_i . k_j / sqrt(d_k) - m (p_i - j).

The bias is not scaled by 1/sqrt(d_k). The scores go through a softmax and
weight the values as usual. No position vector is added anywhere.

With n queries and M keys (M >= n), query i (from 0) sits at position
i + (M - n), so the last query is the newest token. M > n is the case of
generation with a key-value cache.

alibi_slopes(h) gives the fixed slopes of h heads: for h a power of 2, the
geometric sequence that starts at 2^(-8/h) with ratio 2^(-8/h). For other h,
the slopes of the largest power of 2 below h, followed by every other slope
of the next power of 2, as in the code of the authors.

Precondition: Q is n x d_k, K is M x d_k, V is M x d_v, 1 <= n <= M, m >= 0.
Cost: Theta(n M (d_k + d_v)) operations, Theta(M) extra memory per query row.
The code takes the queries, keys and values as given. It does not train a network.
"""

import math
from typing import List, Sequence

Matrix = List[List[float]]


def _slopes_power_of_2(h: int) -> List[float]:
    start = 2.0 ** (-8.0 / h)
    return [start ** (r + 1) for r in range(h)]


def alibi_slopes(h: int) -> List[float]:
    """The fixed slopes of h heads, from the largest to the smallest for h a power of 2."""
    if h < 1:
        raise ValueError("h must be at least 1")
    if h & (h - 1) == 0:
        return _slopes_power_of_2(h)
    p = 1 << (h.bit_length() - 1)
    return _slopes_power_of_2(p) + alibi_slopes(2 * p)[0::2][: h - p]


def alibi_bias(n: int, M: int, slope: float) -> Matrix:
    """The n x M bias matrix: -slope (p_i - j) where key j is visible, -inf where it is masked."""
    shift = M - n
    return [[-slope * (i + shift - j) if j <= i + shift else float("-inf") for j in range(M)] for i in range(n)]


def alibi_attention(
    Q: Sequence[Sequence[float]],
    K: Sequence[Sequence[float]],
    V: Sequence[Sequence[float]],
    slope: float,
) -> Matrix:
    """One causal head with the linear bias of the given slope. Returns an n x d_v matrix."""
    n, M = len(Q), len(K)
    if n < 1 or M < n or len(V) != M:
        raise ValueError("need 1 <= n <= M queries and M keys and values")
    dk = len(K[0])
    if any(len(q) != dk for q in Q) or any(len(k) != dk for k in K):
        raise ValueError("queries and keys must have the same size")
    if not slope >= 0:
        raise ValueError("the slope must be non-negative")
    shift = M - n
    scale = 1.0 / math.sqrt(dk)
    out: Matrix = []
    for i in range(n):  # @line L1
        p_i = i + shift
        s = []
        for j in range(p_i + 1):  # @line L2
            s.append(math.fsum(a * b for a, b in zip(Q[i], K[j])) * scale - slope * (p_i - j))  # @line L3
        mu = max(s)
        w = [math.exp(x - mu) for x in s]
        z = math.fsum(w)
        p = [x / z for x in w]  # @line L4
        out.append([math.fsum(p[j] * V[j][c] for j in range(p_i + 1)) for c in range(len(V[0]))])  # @line L5
    return out  # @line L6
