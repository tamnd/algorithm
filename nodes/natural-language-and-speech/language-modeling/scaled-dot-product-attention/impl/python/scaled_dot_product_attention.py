# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scaled-dot-product-attention/. The authors are listed in prov/YMRYDZ.jsonl.

"""Scaled dot-product attention, softmax(Q K^T / sqrt(d_k)) V, one query row at a time.

Shapes, with named sizes:
    Q is n x d_k (one row per query),
    K is m x d_k (one row per key),
    V is m x d_v (one row per value, the value of key j is row j).

A mask says which keys each query may see. mask[i][j] is True when query i
may see key j. With causal=True, query i sees key j when j <= i + (m - n),
so the last n keys belong to the n queries (m = n is the usual case; m > n
is the case of a key-value cache). A masked score is -inf and gets weight 0.

Precondition: n >= 1, m >= 1, d_k >= 1, d_v >= 1, all rows of a matrix have
the same length, and every query sees at least one key.

Cost: Theta(n m (d_k + d_v)) arithmetic operations and Theta(m) extra memory
for one row of scores at a time, plus the n x d_v output. The full n x m
weight matrix is stored only by attention_weights.

The code takes Q, K and V as given. It does not train a network.
"""

import math
from typing import List, Optional, Sequence, Tuple

Matrix = List[List[float]]
NEG_INF = float("-inf")


def _shape(name: str, a: Sequence[Sequence[float]]) -> Tuple[int, int]:
    if len(a) == 0 or len(a[0]) == 0:
        raise ValueError(f"{name} must have at least one row and one column")
    cols = len(a[0])
    for row in a:
        if len(row) != cols:
            raise ValueError(f"the rows of {name} must have the same length")
    return len(a), cols


def _check(
    Q: Sequence[Sequence[float]],
    K: Sequence[Sequence[float]],
    V: Sequence[Sequence[float]],
    mask: Optional[Sequence[Sequence[bool]]],
    causal: bool,
) -> Tuple[int, int, int, int]:
    n, dq = _shape("Q", Q)
    m, dk = _shape("K", K)
    mv, dv = _shape("V", V)
    if dq != dk:
        raise ValueError("Q and K must have the same number of columns")
    if mv != m:
        raise ValueError("K and V must have the same number of rows")
    if mask is not None:
        if len(mask) != n or any(len(r) != m for r in mask):
            raise ValueError("the mask must be n x m")
    if causal and m < n:
        raise ValueError("a causal mask needs at least as many keys as queries")
    return n, m, dk, dv


def _run(
    Q: Sequence[Sequence[float]],
    K: Sequence[Sequence[float]],
    V: Sequence[Sequence[float]],
    mask: Optional[Sequence[Sequence[bool]]],
    causal: bool,
    keep_weights: bool,
) -> Tuple[Matrix, Matrix]:
    n, m, dk, dv = _check(Q, K, V, mask, causal)
    scale = 1.0 / math.sqrt(dk)
    shift = m - n
    out: Matrix = []
    weights: Matrix = []
    for i in range(n):  # @line L1
        s = []
        for j in range(m):  # @line L2
            x = math.fsum(Q[i][t] * K[j][t] for t in range(dk)) * scale  # @line L3
            if (mask is not None and not mask[i][j]) or (causal and j > i + shift):
                x = NEG_INF  # @line L4
            s.append(x)
        mu = max(s)  # @line L5
        if mu == NEG_INF:
            raise ValueError(f"query {i} sees no key")
        p = [math.exp(x - mu) for x in s]  # @line L6
        z = math.fsum(p)  # @line L6
        p = [e / z for e in p]  # @line L7
        out.append([math.fsum(p[j] * V[j][c] for j in range(m)) for c in range(dv)])  # @line L8
        if keep_weights:
            weights.append(p)
    return out, weights  # @line L9


def attention(
    Q: Sequence[Sequence[float]],
    K: Sequence[Sequence[float]],
    V: Sequence[Sequence[float]],
    mask: Optional[Sequence[Sequence[bool]]] = None,
    causal: bool = False,
) -> Matrix:
    """Return the n x d_v matrix softmax(Q K^T / sqrt(d_k)) V, with masked scores set to -inf."""
    return _run(Q, K, V, mask, causal, False)[0]


def attention_weights(
    Q: Sequence[Sequence[float]],
    K: Sequence[Sequence[float]],
    V: Sequence[Sequence[float]],
    mask: Optional[Sequence[Sequence[bool]]] = None,
    causal: bool = False,
) -> Tuple[Matrix, Matrix]:
    """Return (O, P): the output and the n x m weight matrix P. Each row of P sums to 1."""
    return _run(Q, K, V, mask, causal, True)
