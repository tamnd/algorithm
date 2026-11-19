# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/grouped-query-attention/. The authors are listed in prov/VQPZ6C.jsonl.

"""Grouped-query attention (GQA) of Ainslie et al.

h query heads share g key-value heads, with g dividing h. Query head r uses
key-value head s = floor(r / (h / g)), so each group of h / g consecutive
query heads reads the same keys and values. g = h is multi-head attention,
g = 1 is multi-query attention.

Shapes, with named sizes:
    X_q  is n x d, X_kv is M x d (X_kv = X_q for self-attention),
    W_Q is d x (h d_k), W_K is d x (g d_k), W_V is d x (g d_v),
    W_O is (h d_v) x d.

With causal=True, query i sees key j when j <= i + (M - n).

mean_pool_heads turns the key or value weights of an h-head model into those
of a g-group model by averaging the columns of the heads in each group, the
first step of uptraining.

Precondition: 1 <= g <= h, g divides h, all shapes agree, and every query
sees at least one key.
Cost: Theta(n d h d_k + M d g (d_k + d_v) + h n M (d_k + d_v) + n h d_v d)
operations. The key-value cache holds 2 M g d_k numbers per layer when
d_v = d_k, a factor g / h of the multi-head cache.
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
    n, M, dk = len(Q), len(K), len(K[0])
    shift = M - n
    out = []
    for i in range(n):
        s = [
            math.fsum(Q[i][t] * K[j][t] for t in range(dk)) / math.sqrt(dk) if not (causal and j > i + shift) else NEG_INF
            for j in range(M)
        ]
        mu = max(s)
        if mu == NEG_INF:
            raise ValueError(f"query {i} sees no key")
        p = [math.exp(x - mu) for x in s]
        z = math.fsum(p)
        out.append([math.fsum(p[j] * V[j][c] for j in range(M)) / z for c in range(len(V[0]))])
    return out


def group_of(r: int, h: int, g: int) -> int:
    """The key-value head used by query head r."""
    return r // (h // g)


def grouped_query_attention(
    X_q: Sequence[Sequence[float]],
    X_kv: Sequence[Sequence[float]],
    W_Q: Sequence[Sequence[float]],
    W_K: Sequence[Sequence[float]],
    W_V: Sequence[Sequence[float]],
    W_O: Sequence[Sequence[float]],
    h: int,
    g: int,
    causal: bool = False,
) -> Matrix:
    """Return Concat(head_0, ..., head_(h-1)) W_O, an n x d matrix."""
    if not (1 <= g <= h) or h % g:
        raise ValueError("need 1 <= g <= h with g dividing h")
    d = len(X_q[0])
    if len(X_kv[0]) != d or len(W_Q) != d or len(W_K) != d or len(W_V) != d:
        raise ValueError("the input size d does not match the weights")
    if len(W_Q[0]) % h or len(W_K[0]) % g or len(W_V[0]) % g:
        raise ValueError("the projection sizes must be multiples of h and g")
    dk, dv = len(W_Q[0]) // h, len(W_V[0]) // g
    if len(W_K[0]) // g != dk:
        raise ValueError("queries and keys must have the same head size")
    if len(W_O) != h * dv:
        raise ValueError("W_O must have h d_v rows")
    if causal and len(X_kv) < len(X_q):
        raise ValueError("a causal mask needs at least as many keys as queries")
    Ks: List[Matrix] = []
    Vs: List[Matrix] = []
    for s in range(g):  # @line L1
        Ks.append(matmul(X_kv, columns(W_K, s * dk, (s + 1) * dk)))  # @line L2
        Vs.append(matmul(X_kv, columns(W_V, s * dv, (s + 1) * dv)))  # @line L2
    heads: List[Matrix] = []
    for r in range(h):  # @line L3
        s = group_of(r, h, g)  # @line L4
        Q_r = matmul(X_q, columns(W_Q, r * dk, (r + 1) * dk))  # @line L5
        heads.append(attention(Q_r, Ks[s], Vs[s], causal))  # @line L6
    H = [[x for head in heads for x in head[i]] for i in range(len(X_q))]
    return matmul(H, W_O)  # @line L7


def mean_pool_heads(W: Sequence[Sequence[float]], h: int, g: int) -> Matrix:
    """Average the column blocks of the h heads in each of the g groups: d x (h c) to d x (g c)."""
    if not (1 <= g <= h) or h % g or len(W[0]) % h:
        raise ValueError("need g dividing h and h dividing the column count")
    c = len(W[0]) // h
    k = h // g
    return [
        [math.fsum(row[(s * k + t) * c + u] for t in range(k)) / k for s in range(g) for u in range(c)]
        for row in W
    ]


def kv_cache_entries(layers: int, tokens: int, g: int, d_k: int, d_v: int) -> int:
    """The numbers stored in the key-value cache: one key and one value per group, token and layer."""
    return layers * tokens * g * (d_k + d_v)
