# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multi-head-attention/. The authors are listed in prov/YXWRTE.jsonl.

"""Multi-head attention: h scaled dot-product attentions on learned projections, concatenated.

Shapes, with named sizes:
    X_q  is n x d (the query side, one row per token),
    X_kv is m x d (the key and value side; X_kv = X_q for self-attention),
    W_Q and W_K are d x (h d_k), W_V is d x (h d_v), W_O is (h d_v) x d.
Head r uses the columns r d_k to (r + 1) d_k - 1 of W_Q and W_K, the columns
r d_v to (r + 1) d_v - 1 of W_V, and the same rows of W_O.

With causal=True, query i sees key j when j <= i + (m - n).

Precondition: h >= 1, the column counts of W_Q, W_K and W_V are multiples of
h, all shapes agree, and every query sees at least one key.

Cost: Theta(n d h d_k + m d h (d_k + d_v) + h n m (d_k + d_v) + n h d_v d)
operations. With m = n and h d_k = h d_v = d this is Theta(n d^2 + n^2 d).
Extra memory Theta(n h d_v + m h (d_k + d_v)) for the projections and the
heads, plus Theta(m) for one row of scores at a time.

The code takes the inputs and the weights as given. It does not train a network.
"""

import math
from typing import List, Sequence

Matrix = List[List[float]]
NEG_INF = float("-inf")


def matmul(A: Sequence[Sequence[float]], B: Sequence[Sequence[float]]) -> Matrix:
    """The product of an a x b and a b x c matrix."""
    if len(A[0]) != len(B):
        raise ValueError("inner sizes do not match")
    cols = len(B[0])
    return [[math.fsum(row[t] * B[t][c] for t in range(len(B))) for c in range(cols)] for row in A]


def columns(A: Sequence[Sequence[float]], lo: int, hi: int) -> Matrix:
    """The columns lo to hi - 1 of A."""
    return [list(row[lo:hi]) for row in A]


def attention(Q: Matrix, K: Matrix, V: Matrix, causal: bool = False) -> Matrix:
    """softmax(Q K^T / sqrt(d_k)) V for one head, with a stable softmax."""
    n, m, dk = len(Q), len(K), len(K[0])
    shift = m - n
    out = []
    for i in range(n):
        s = [
            math.fsum(Q[i][t] * K[j][t] for t in range(dk)) / math.sqrt(dk) if not (causal and j > i + shift) else NEG_INF
            for j in range(m)
        ]
        mu = max(s)
        if mu == NEG_INF:
            raise ValueError(f"query {i} sees no key")
        p = [math.exp(x - mu) for x in s]
        z = math.fsum(p)
        out.append([math.fsum(p[j] * V[j][c] for j in range(m)) / z for c in range(len(V[0]))])
    return out


def multi_head_attention(
    X_q: Sequence[Sequence[float]],
    X_kv: Sequence[Sequence[float]],
    W_Q: Sequence[Sequence[float]],
    W_K: Sequence[Sequence[float]],
    W_V: Sequence[Sequence[float]],
    W_O: Sequence[Sequence[float]],
    h: int,
    causal: bool = False,
) -> Matrix:
    """Return Concat(head_1, ..., head_h) W_O, an n x d matrix."""
    if h < 1:
        raise ValueError("h must be at least 1")
    d = len(X_q[0])
    if len(X_kv[0]) != d or len(W_Q) != d or len(W_K) != d or len(W_V) != d:
        raise ValueError("the input size d does not match the weights")
    if len(W_Q[0]) != len(W_K[0]) or len(W_Q[0]) % h or len(W_V[0]) % h:
        raise ValueError("the projection sizes must agree and be multiples of h")
    if len(W_O) != len(W_V[0]):
        raise ValueError("W_O must have h d_v rows")
    if causal and len(X_kv) < len(X_q):
        raise ValueError("a causal mask needs at least as many keys as queries")
    dk, dv = len(W_Q[0]) // h, len(W_V[0]) // h
    heads: List[Matrix] = []
    for r in range(h):  # @line L1
        Q_r = matmul(X_q, columns(W_Q, r * dk, (r + 1) * dk))  # @line L2
        K_r = matmul(X_kv, columns(W_K, r * dk, (r + 1) * dk))  # @line L3
        V_r = matmul(X_kv, columns(W_V, r * dv, (r + 1) * dv))  # @line L4
        heads.append(attention(Q_r, K_r, V_r, causal))  # @line L5
    H = [[x for head in heads for x in head[i]] for i in range(len(X_q))]  # @line L6
    return matmul(H, W_O)  # @line L7


def parameter_count(d: int, h: int, d_k: int, d_v: int, bias: bool = False) -> int:
    """The number of weights: 2 d h d_k + 2 d h d_v, plus the biases if asked. 4 d^2 when h d_k = h d_v = d."""
    count = 2 * d * h * d_k + 2 * h * d_v * d
    if bias:
        count += 2 * h * d_k + h * d_v + d
    return count
