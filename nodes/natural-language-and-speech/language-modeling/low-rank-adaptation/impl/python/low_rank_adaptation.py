# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/low-rank-adaptation/. The authors are listed in prov/W05XMM.jsonl.

"""Low-rank adaptation (LoRA) of one frozen weight matrix.

Shapes, with named sizes:
    W0 is d x k (frozen, the pretrained weight; it maps k inputs to d outputs),
    B  is d x r (trained, zero at the start),
    A  is r x k (trained, random at the start),
    x  is a vector of k numbers (one token), g is a vector of d numbers.

The adapted layer computes h = W0 x + s B (A x) with the scale s = alpha / r.
The update s B A has rank at most r. merge() folds it into W0, so the merged
layer costs the same as the original one, and unmerge() takes it out again.

backward() returns the gradients of a loss with respect to A, B and x, given
g = dloss/dh. W0 gets no gradient: it is frozen.

Cost per token: Theta(d k + r (d + k)) for forward() and backward(), and
Theta(d k) for the merged layer. The trained parameters are r (d + k) numbers.

The code takes W0 and the data as given. It does not train a large network
and does not load pretrained weights.
"""

import math
import random
from typing import List, Sequence, Tuple

Matrix = List[List[float]]
Vector = List[float]


def matvec(M: Sequence[Sequence[float]], x: Sequence[float]) -> Vector:
    """Return M x."""
    return [math.fsum(row[j] * x[j] for j in range(len(x))) for row in M]


def matvec_t(M: Sequence[Sequence[float]], y: Sequence[float]) -> Vector:
    """Return M^T y."""
    cols = len(M[0])
    return [math.fsum(M[i][j] * y[i] for i in range(len(M))) for j in range(cols)]


def matmul(P: Sequence[Sequence[float]], Q: Sequence[Sequence[float]]) -> Matrix:
    """Return the product P Q."""
    inner, cols = len(Q), len(Q[0])
    return [[math.fsum(P[i][t] * Q[t][j] for t in range(inner)) for j in range(cols)] for i in range(len(P))]


def outer(u: Sequence[float], v: Sequence[float], s: float = 1.0) -> Matrix:
    """Return s u v^T."""
    return [[s * a * b for b in v] for a in u]


def _check_shapes(W0, A, B):
    d, k = len(W0), len(W0[0])
    r = len(A)
    if r < 1 or len(A[0]) != k or len(B) != d or any(len(row) != r for row in B):
        raise ValueError("need W0: d x k, A: r x k, B: d x r with r >= 1")
    return d, k, r


def init(d: int, k: int, r: int, rng: random.Random, sigma: float = 0.02) -> Tuple[Matrix, Matrix]:
    """Return (A, B): A has Gaussian entries of standard deviation sigma, B is zero."""
    if r < 1 or d < 1 or k < 1:
        raise ValueError("d, k and r must be at least 1")
    A = [[rng.gauss(0.0, sigma) for _ in range(k)] for _ in range(r)]  # @line L1
    B = [[0.0] * r for _ in range(d)]  # @line L2
    return A, B


def forward(W0: Matrix, A: Matrix, B: Matrix, alpha: float, x: Sequence[float]) -> Vector:
    """Return h = W0 x + (alpha / r) B (A x), without forming B A."""
    d, k, r = _check_shapes(W0, A, B)
    s = alpha / r
    u = matvec(A, x)  # @line L3
    bu = matvec(B, u)
    base = matvec(W0, x)
    return [base[i] + s * bu[i] for i in range(d)]  # @line L4


def backward(W0: Matrix, A: Matrix, B: Matrix, alpha: float, x: Sequence[float],
             g: Sequence[float]) -> Tuple[Matrix, Matrix, Vector]:
    """Return (grad_A, grad_B, grad_x) for one token, given g = dloss/dh."""
    d, k, r = _check_shapes(W0, A, B)
    s = alpha / r
    u = matvec(A, x)  # @line L5
    c = matvec_t(B, g)  # @line L5
    grad_B = outer(g, u, s)  # @line L6
    grad_A = outer(c, x, s)  # @line L7
    a_t_c = matvec_t(A, c)
    w_t_g = matvec_t(W0, g)
    grad_x = [w_t_g[j] + s * a_t_c[j] for j in range(k)]  # @line L8
    return grad_A, grad_B, grad_x


def delta(A: Matrix, B: Matrix, alpha: float) -> Matrix:
    """Return the full update (alpha / r) B A, a d x k matrix of rank at most r."""
    r = len(A)
    BA = matmul(B, A)
    return [[alpha / r * v for v in row] for row in BA]


def merge(W0: Matrix, A: Matrix, B: Matrix, alpha: float) -> Matrix:
    """Return W = W0 + (alpha / r) B A."""
    _check_shapes(W0, A, B)
    D = delta(A, B, alpha)
    return [[W0[i][j] + D[i][j] for j in range(len(W0[0]))] for i in range(len(W0))]  # @line L9


def unmerge(W: Matrix, A: Matrix, B: Matrix, alpha: float) -> Matrix:
    """Return W0 = W - (alpha / r) B A, the inverse of merge up to rounding."""
    _check_shapes(W, A, B)
    D = delta(A, B, alpha)
    return [[W[i][j] - D[i][j] for j in range(len(W[0]))] for i in range(len(W))]  # @line L10


def forward_batch(W0: Matrix, A: Matrix, B: Matrix, alpha: float, X: Sequence[Sequence[float]]) -> Matrix:
    """Apply forward() to each of the n token rows of X (an n x k matrix)."""
    return [forward(W0, A, B, alpha, x) for x in X]


def backward_batch(W0: Matrix, A: Matrix, B: Matrix, alpha: float, X: Sequence[Sequence[float]],
                   G: Sequence[Sequence[float]]) -> Tuple[Matrix, Matrix]:
    """Return (grad_A, grad_B) summed over the n tokens, given G = dloss/dH (n x d)."""
    d, k, r = _check_shapes(W0, A, B)
    gA = [[0.0] * k for _ in range(r)]
    gB = [[0.0] * r for _ in range(d)]
    for x, g in zip(X, G):
        a, b, _ = backward(W0, A, B, alpha, x, g)
        for i in range(r):
            for j in range(k):
                gA[i][j] += a[i][j]
        for i in range(d):
            for j in range(r):
                gB[i][j] += b[i][j]
    return gA, gB


def squared_loss(W0: Matrix, A: Matrix, B: Matrix, alpha: float, X, Y) -> Tuple[float, Matrix]:
    """Return (loss, G) for loss = (1 / (2 n)) sum_t |h_t - y_t|^2 and G = dloss/dH."""
    n = len(X)
    H = forward_batch(W0, A, B, alpha, X)
    G = [[(H[t][i] - Y[t][i]) / n for i in range(len(H[t]))] for t in range(n)]
    loss = math.fsum((H[t][i] - Y[t][i]) ** 2 for t in range(n) for i in range(len(H[t]))) / (2 * n)
    return loss, G


def sgd_step(W0: Matrix, A: Matrix, B: Matrix, alpha: float, X, Y, lr: float) -> float:
    """Do one gradient step on A and B for the squared loss, in place. Return the loss before the step."""
    loss, G = squared_loss(W0, A, B, alpha, X, Y)
    gA, gB = backward_batch(W0, A, B, alpha, X, G)
    for i in range(len(A)):
        for j in range(len(A[0])):
            A[i][j] -= lr * gA[i][j]
    for i in range(len(B)):
        for j in range(len(B[0])):
            B[i][j] -= lr * gB[i][j]
    return loss


def trainable_parameters(d: int, k: int, r: int) -> int:
    """Return r (d + k), the number of entries of A and B."""
    return r * (d + k)
