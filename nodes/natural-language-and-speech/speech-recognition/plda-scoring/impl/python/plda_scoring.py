# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/plda-scoring/. The authors are listed in prov/MHT9KM.jsonl.

"""PLDA scoring in the two-covariance model.

An embedding (i-vector or x-vector) of dimension d is modeled as

    x = m + y + e,   y ~ N(0, B) (the speaker),   e ~ N(0, W) (the session),

with y shared by all embeddings of one speaker. B and W are symmetric positive
definite matrices given as lists of rows; the code does not train them. With
A = B + W (the total covariance), the log likelihood ratio of "same speaker"
against "different speakers" for two embeddings is the closed form

    LLR(x1, x2) = 1/2 u'Qu + 1/2 v'Qv + u'Pv + c,   u = x1 - m, v = x2 - m,
    Q = A^-1 - (A - B A^-1 B)^-1,   P = A^-1 B (A - B A^-1 B)^-1,
    c = 1/2 (log|A| - log|A - B A^-1 B|).

score_multi scores a test embedding against several enrollment embeddings
through the posterior of the speaker variable. prince_elder_to_two_cov turns
the parameters (F, G, Sigma) of Prince and Elder 2007 into B and W. Every log
is the natural log.
"""

import math
from typing import List, Sequence, Tuple

Vector = List[float]
Matrix = List[List[float]]


def mat_add(X: Sequence[Sequence[float]], Y: Sequence[Sequence[float]], s: float = 1.0) -> Matrix:
    """Return X + s Y."""
    return [[a + s * b for a, b in zip(rx, ry)] for rx, ry in zip(X, Y)]


def mat_mul(X: Sequence[Sequence[float]], Y: Sequence[Sequence[float]]) -> Matrix:
    """Return the product X Y."""
    cols = list(zip(*Y))
    return [[math.fsum(a * b for a, b in zip(row, col)) for col in cols] for row in X]


def mat_vec(X: Sequence[Sequence[float]], v: Sequence[float]) -> Vector:
    """Return X v."""
    return [math.fsum(a * b for a, b in zip(row, v)) for row in X]


def dot(u: Sequence[float], v: Sequence[float]) -> float:
    return math.fsum(a * b for a, b in zip(u, v))


def transpose(X: Sequence[Sequence[float]]) -> Matrix:
    return [list(c) for c in zip(*X)]


def symmetrize(X: Sequence[Sequence[float]]) -> Matrix:
    n = len(X)
    return [[0.5 * (X[i][j] + X[j][i]) for j in range(n)] for i in range(n)]


def cholesky(S: Sequence[Sequence[float]]) -> Matrix:
    """Return the lower triangular L with L L' = S. Raise ValueError if S is not positive definite."""
    n = len(S)
    L = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = S[i][j] - math.fsum(L[i][k] * L[j][k] for k in range(j))
            if i == j:
                if s <= 0.0:
                    raise ValueError("the matrix is not positive definite")
                L[i][i] = math.sqrt(s)
            else:
                L[i][j] = s / L[j][j]
    return L


def logdet(S: Sequence[Sequence[float]]) -> float:
    """Return log det S for a positive definite S."""
    L = cholesky(S)
    return 2.0 * math.fsum(math.log(L[i][i]) for i in range(len(S)))


def inverse(S: Sequence[Sequence[float]]) -> Matrix:
    """Return the inverse of a positive definite S, through its Cholesky factor."""
    n = len(S)
    L = cholesky(S)
    inv = []
    for col in range(n):
        e = [1.0 if i == col else 0.0 for i in range(n)]
        z = [0.0] * n
        for i in range(n):
            z[i] = (e[i] - math.fsum(L[i][k] * z[k] for k in range(i))) / L[i][i]
        x = [0.0] * n
        for i in range(n - 1, -1, -1):
            x[i] = (z[i] - math.fsum(L[k][i] * x[k] for k in range(i + 1, n))) / L[i][i]
        inv.append(x)
    return symmetrize(transpose(inv))


def log_gauss(x: Sequence[float], mean: Sequence[float], S: Sequence[Sequence[float]]) -> float:
    """Return log N(x; mean, S) for a full covariance S."""
    diff = [a - b for a, b in zip(x, mean)]
    Si = inverse(S)
    return -0.5 * (len(x) * math.log(2.0 * math.pi) + logdet(S) + dot(diff, mat_vec(Si, diff)))


def prepare(B: Sequence[Sequence[float]], W: Sequence[Sequence[float]]) -> Tuple[Matrix, Matrix, float]:
    """Return (Q, P, c) of the closed form for between covariance B and within covariance W."""
    A = mat_add(B, W)  # @line L1
    Ai = inverse(A)
    S = symmetrize(mat_add(A, mat_mul(mat_mul(B, Ai), B), -1.0))  # A - B A^-1 B, the Schur complement
    Si = inverse(S)  # @line L2
    Q = symmetrize(mat_add(Ai, Si, -1.0))
    P = symmetrize(mat_mul(mat_mul(Ai, B), Si))  # @line L3
    c = 0.5 * (logdet(A) - logdet(S))  # @line L4
    return Q, P, c


def score(x1: Sequence[float], x2: Sequence[float], m: Sequence[float], prepared: Tuple[Matrix, Matrix, float]) -> float:
    """Return the closed form LLR of same speaker against different speakers."""
    Q, P, c = prepared
    u = [a - b for a, b in zip(x1, m)]  # @line L5
    v = [a - b for a, b in zip(x2, m)]
    return 0.5 * dot(u, mat_vec(Q, u)) + 0.5 * dot(v, mat_vec(Q, v)) + dot(u, mat_vec(P, v)) + c  # @line L6


def score_multi(enroll: Sequence[Sequence[float]], test: Sequence[float], m: Sequence[float],
                B: Sequence[Sequence[float]], W: Sequence[Sequence[float]]) -> float:
    """Return log p(test | enroll, same speaker) - log p(test | other speaker).

    The posterior of the speaker variable given n enrollment embeddings is
    N(mu_n, C_n) with C_n = (B^-1 + n W^-1)^-1 and mu_n = C_n W^-1 sum (x_i - m).
    The test embedding then has the predictive density N(m + mu_n, W + C_n).
    """
    n = len(enroll)
    if n == 0:
        raise ValueError("no enrollment embeddings")
    d = len(m)
    Wi = inverse(W)
    Cn = inverse(mat_add(inverse(B), Wi, float(n)))  # @line L7
    tot = [math.fsum(x[i] - m[i] for x in enroll) for i in range(d)]
    mu = mat_vec(Cn, mat_vec(Wi, tot))  # @line L8
    same = log_gauss(test, [a + b for a, b in zip(m, mu)], mat_add(W, Cn))
    diff = log_gauss(test, m, mat_add(B, W))
    return same - diff  # @line L9


def prince_elder_to_two_cov(F: Sequence[Sequence[float]], G: Sequence[Sequence[float]],
                            Sigma: Sequence[float]) -> Tuple[Matrix, Matrix]:
    """Map x = m + F h + G w + eps, eps ~ N(0, diag(Sigma)), to B = F F' and W = G G' + diag(Sigma)."""
    B = mat_mul(F, transpose(F))
    W = mat_mul(G, transpose(G)) if G and G[0] else [[0.0] * len(F) for _ in F]
    for i, s in enumerate(Sigma):
        W[i][i] += s
    return B, W
