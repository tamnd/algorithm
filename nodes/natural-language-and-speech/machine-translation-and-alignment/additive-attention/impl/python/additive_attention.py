# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/additive-attention/. The authors are listed in prov/3X7CGK.jsonl.

"""Additive attention of Bahdanau, Cho and Bengio (2015), for one decoder step.

The score of the encoder state h_j for the decoder state s is

    e_j = v^T tanh(W s + U h_j),

the weights are alpha = softmax(e), and the context is c = sum_j alpha_j h_j.
The vectors and the parameters are given: s, h_j, W, U and v are the outputs
and the weights of a trained network, and this module does not train them.

Vectors are lists of floats and a matrix is a list of rows. With W of shape
(a, d_s), U of shape (a, d_h) and v of length a, the step costs
O(J a (d_s + d_h)) time, or O(J a + a d_s) when the keys U h_j are computed
once per source sentence and reused at every decoder step.

backward() returns the exact gradients of L = g . c for a given vector g,
so that the step can be tested against finite differences.
"""

import math
from typing import List, Optional, Sequence, Tuple

from nlslog import NEG_INF, softmax

Vector = List[float]
Matrix = List[List[float]]


def matvec(a: Sequence[Sequence[float]], x: Sequence[float]) -> Vector:
    """Return the product of the matrix a and the vector x."""
    return [math.fsum(r * y for r, y in zip(row, x)) for row in a]


def dot(x: Sequence[float], y: Sequence[float]) -> float:
    """Return the dot product of x and y."""
    return math.fsum(a * b for a, b in zip(x, y))


def keys(U: Sequence[Sequence[float]], H: Sequence[Sequence[float]]) -> List[Vector]:
    """Return the keys U h_j. They do not depend on the decoder step."""
    return [matvec(U, h) for h in H]  # @line L3


def additive_attention(s: Sequence[float], H: Sequence[Sequence[float]], W: Sequence[Sequence[float]],
                       U: Sequence[Sequence[float]], v: Sequence[float],
                       mask: Optional[Sequence[bool]] = None,
                       K: Optional[Sequence[Sequence[float]]] = None) -> Tuple[Vector, Vector, Vector]:
    """Return (context c, weights alpha, scores e) for the decoder state s.

    mask[j] = False marks a padding position, which gets the score -inf and
    the weight 0. K may hold the precomputed keys U h_j.
    """
    if not H:
        raise ValueError("attention needs at least one encoder state")
    q = matvec(W, s)  # @line L1
    if K is None:
        K = keys(U, H)
    e = []
    for j in range(len(H)):  # @line L2
        score = dot(v, [math.tanh(a + b) for a, b in zip(q, K[j])])  # @line L4
        if mask is not None and not mask[j]:  # @line L5
            score = NEG_INF
        e.append(score)
    alpha = softmax(e)  # @line L6
    c = [math.fsum(alpha[j] * H[j][t] for j in range(len(H))) for t in range(len(H[0]))]  # @line L7
    return c, alpha, e  # @line L8


def backward(g: Sequence[float], s: Sequence[float], H: Sequence[Sequence[float]],
             W: Sequence[Sequence[float]], U: Sequence[Sequence[float]], v: Sequence[float],
             mask: Optional[Sequence[bool]] = None):
    """Return the gradients (ds, dH, dW, dU, dv) of L = g . c."""
    q = matvec(W, s)
    K = keys(U, H)
    T = [[math.tanh(a + b) for a, b in zip(q, k)] for k in K]
    _, alpha, _ = additive_attention(s, H, W, U, v, mask, K)
    J, a_dim = len(H), len(v)
    gamma = [dot(g, h) for h in H]  # dL/d alpha_j
    mean = math.fsum(al * ga for al, ga in zip(alpha, gamma))
    de = [alpha[j] * (gamma[j] - mean) for j in range(J)]  # softmax backward; 0 where masked
    dH = [[alpha[j] * gt for gt in g] for j in range(J)]
    dv = [math.fsum(de[j] * T[j][t] for j in range(J)) for t in range(a_dim)]
    dz = [[de[j] * v[t] * (1 - T[j][t] ** 2) for t in range(a_dim)] for j in range(J)]
    dq = [math.fsum(dz[j][t] for j in range(J)) for t in range(a_dim)]
    dW = [[dq[t] * x for x in s] for t in range(a_dim)]
    ds = [math.fsum(W[t][i] * dq[t] for t in range(a_dim)) for i in range(len(s))]
    dU = [[math.fsum(dz[j][t] * H[j][i] for j in range(J)) for i in range(len(H[0]))] for t in range(a_dim)]
    for j in range(J):
        for i in range(len(H[0])):
            dH[j][i] += math.fsum(U[t][i] * dz[j][t] for t in range(a_dim))
    return ds, dH, dW, dU, dv
