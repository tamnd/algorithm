# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dense-passage-retrieval/. The authors are listed in prov/GDMYGR.jsonl.

"""The in-batch negative loss of DPR and exact inner-product retrieval.

The encoders are outside this file. The inputs are the vectors that they
would produce: q_1..q_B for the questions of a batch, and c_1..c_m for the
passages of the batch, where c_i (i < B) is the positive passage of
question i and the other rows are negatives (for example one BM25 hard
negative per question). With S = Q C^T,

    L = (1 / B) sum_i -log( exp(S_ii) / sum_k exp(S_ik) ).

With p_ik the softmax of row i of S,

    dL/dq_i = (1 / B) sum_k (p_ik - [k = i]) c_k,
    dL/dc_k = (1 / B) sum_i (p_ik - [k = i]) q_i.

Retrieval returns the k passages of largest q . c, with ties broken by the
smaller passage id.
"""

import math


def dot(a, b):
    return sum(p * q for p, q in zip(a, b))


def similarity(qs, cs):
    return [[dot(q, c) for c in cs] for q in qs]                       # @line L1


def softmax(v):
    m = max(v)
    e = [math.exp(x - m) for x in v]
    z = sum(e)
    return [x / z for x in e]


def log_softmax(v):
    m = max(v)
    lz = m + math.log(sum(math.exp(x - m) for x in v))
    return [x - lz for x in v]


def in_batch_loss(qs, cs):
    """The mean negative log-likelihood of the positive passage c_i for question i."""
    s = similarity(qs, cs)
    rows = [log_softmax(row) for row in s]                             # @line L2
    return -sum(row[i] for i, row in enumerate(rows)) / len(qs)        # @line L3


def in_batch_gradients(qs, cs):
    """(dL/dq, dL/dc) as lists of vectors."""
    b = len(qs)
    s = similarity(qs, cs)
    gq = [[0.0] * len(qs[0]) for _ in qs]
    gc = [[0.0] * len(cs[0]) for _ in cs]
    for i, row in enumerate(s):
        p = softmax(row)
        for k, pk in enumerate(p):
            coef = (pk - (1.0 if k == i else 0.0)) / b                  # @line L4
            for c in range(len(qs[0])):
                gq[i][c] += coef * cs[k][c]                             # @line L5
                gc[k][c] += coef * qs[i][c]
    return gq, gc                                                      # @line L6


def top_k(q, passages, k):
    """The ids of the k passages with the largest inner product, ties by id."""
    order = sorted(range(len(passages)), key=lambda p: (-dot(q, passages[p]), p))
    return order[:k]                                                   # @line L7
