# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/simcse/. The authors are listed in prov/355PND.jsonl.
"""The SimCSE contrastive loss and its gradient.

The code takes the encoder outputs as given: H holds the N sentence vectors
of a batch under one dropout mask, Hp the same N sentences under a second
dropout mask (unsupervised SimCSE) or their entailment partners (supervised
SimCSE), and Hn, when given, one hard negative per sentence (the
contradiction hypotheses of supervised SimCSE). It implements the loss of
Gao, Yao and Chen 2021 (their equations 1 and 5) and its exact gradient with
respect to every vector. It does not train an encoder.

The loss is in nats. Matrices are lists of rows.
"""

import math
from typing import List, Optional, Sequence, Tuple

from nlslog import log_sum

Vector = List[float]
Matrix = List[List[float]]


def dot(a: Sequence[float], b: Sequence[float]) -> float:
    return math.fsum(x * y for x, y in zip(a, b))


def norm(a: Sequence[float]) -> float:
    return math.sqrt(dot(a, a))


def cosine(a: Sequence[float], b: Sequence[float]) -> float:
    """The cosine a.b / (|a| |b|). Raise ValueError for a zero vector."""
    na, nb = norm(a), norm(b)
    if na == 0 or nb == 0:
        raise ValueError("the cosine of a zero vector is not defined")
    return dot(a, b) / (na * nb)


def cosine_grad(a: Sequence[float], b: Sequence[float]) -> Tuple[Vector, Vector]:
    """The gradients of cos(a, b) with respect to a and to b.

    d cos / d a = b / (|a| |b|) - cos(a, b) a / |a|^2, and the same with a
    and b swapped.
    """
    na, nb = norm(a), norm(b)
    c = dot(a, b) / (na * nb)
    ga = [y / (na * nb) - c * x / (na * na) for x, y in zip(a, b)]
    gb = [x / (na * nb) - c * y / (nb * nb) for x, y in zip(a, b)]
    return ga, gb


def similarity_matrix(H: Matrix, P: Matrix) -> Matrix:
    """The N x M matrix of cosines cos(H[i], P[j])."""
    return [[cosine(h, p) for p in P] for h in H]


def _check(H: Matrix, Hp: Matrix, Hn: Optional[Matrix], tau: float) -> None:
    if not H:
        raise ValueError("the batch is empty")
    if len(Hp) != len(H) or (Hn is not None and len(Hn) != len(H)):
        raise ValueError("H, Hp and Hn must have one row per sentence")
    if not tau > 0:
        raise ValueError("the temperature must be positive")


def simcse_loss_and_grad(
    H: Matrix, Hp: Matrix, tau: float = 0.05, Hn: Optional[Matrix] = None
) -> Tuple[float, Matrix, Matrix, Optional[Matrix]]:
    """Return (loss, dL/dH, dL/dHp, dL/dHn) for one batch.

    loss = (1/N) sum_i [ log_sum_j (z_ij, z'_ij) - z_ii ] with
    z_ij = cos(h_i, hp_j) / tau and z'_ij = cos(h_i, hn_j) / tau. The other
    rows of the batch are the negatives of row i (in-batch negatives).
    Cost: O(N^2 d) time and O(N^2 + N d) space.
    """
    _check(H, Hp, Hn, tau)
    n = len(H)  # @line L1
    z = [[0.0] * n for _ in range(n)]
    zn = [[0.0] * n for _ in range(n)] if Hn is not None else None
    log_z = [0.0] * n
    losses = [0.0] * n
    for i in range(n):  # @line L2
        for j in range(n):  # @line L3
            z[i][j] = cosine(H[i], Hp[j]) / tau
        row = list(z[i])
        if zn is not None:  # @line L4
            for j in range(n):
                zn[i][j] = cosine(H[i], Hn[j]) / tau
            row += zn[i]
        log_z[i] = log_sum(row)  # @line L5
        losses[i] = log_z[i] - z[i][i]
    loss = math.fsum(losses) / n  # @line L6
    d = len(H[0])
    gH = [[0.0] * d for _ in range(n)]
    gP = [[0.0] * d for _ in range(n)]
    gN = [[0.0] * d for _ in range(n)] if Hn is not None else None
    for i in range(n):
        for j in range(n):
            p_ij = math.exp(z[i][j] - log_z[i])  # @line L7
            g = (p_ij - (1.0 if i == j else 0.0)) / (n * tau)  # @line L8
            ga, gb = cosine_grad(H[i], Hp[j])
            for k in range(d):
                gH[i][k] += g * ga[k]  # @line L9
                gP[j][k] += g * gb[k]  # @line L10
            if zn is not None:
                g2 = math.exp(zn[i][j] - log_z[i]) / (n * tau)
                ga, gb = cosine_grad(H[i], Hn[j])
                for k in range(d):
                    gH[i][k] += g2 * ga[k]
                    gN[j][k] += g2 * gb[k]
    return loss, gH, gP, gN  # @line L11


def simcse_loss(H: Matrix, Hp: Matrix, tau: float = 0.05, Hn: Optional[Matrix] = None) -> float:
    """The SimCSE loss alone, in nats."""
    return simcse_loss_and_grad(H, Hp, tau, Hn)[0]


def simcse_loss_direct(H: Matrix, Hp: Matrix, tau: float = 0.05, Hn: Optional[Matrix] = None) -> float:
    """The same loss by the formula of the paper, with plain exp and no log-sum-exp.

    It overflows for a small tau (exp of more than about 709). Use it only to
    check simcse_loss.
    """
    _check(H, Hp, Hn, tau)
    n = len(H)
    total = 0.0
    for i in range(n):
        den = sum(math.exp(cosine(H[i], Hp[j]) / tau) for j in range(n))
        if Hn is not None:
            den += sum(math.exp(cosine(H[i], Hn[j]) / tau) for j in range(n))
        total += -math.log(math.exp(cosine(H[i], Hp[i]) / tau) / den)
    return total / n


def alignment(H: Matrix, Hp: Matrix) -> float:
    """The alignment of Wang and Isola 2020: the mean of |f(x) - f(x+)|^2 over the pairs.

    The vectors are normalized to unit length first, as in the paper.
    """
    total = 0.0
    for h, p in zip(H, Hp):
        nh, np_ = norm(h), norm(p)
        total += math.fsum((x / nh - y / np_) ** 2 for x, y in zip(h, p))
    return total / len(H)


def uniformity(H: Matrix, t: float = 2.0) -> float:
    """The uniformity of Wang and Isola 2020: log of the mean of exp(-t |f(x) - f(y)|^2) over distinct pairs.

    The vectors are normalized to unit length first. Lower is more uniform.
    """
    units = [[x / norm(h) for x in h] for h in H]
    terms = []
    for i in range(len(units)):
        for j in range(i + 1, len(units)):
            sq = math.fsum((a - b) ** 2 for a, b in zip(units[i], units[j]))
            terms.append(-t * sq)
    if not terms:
        raise ValueError("uniformity needs at least two vectors")
    return log_sum(terms) - math.log(len(terms))
