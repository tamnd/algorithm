# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lexrank/. The authors are listed in prov/EFQYD8.jsonl.

"""LexRank of Erkan and Radev (2004), with a threshold or with continuous weights.

Sentences are lists of str tokens; the module does no tokenization, no stop
word removal and no stemming. Words are compared after lower casing.

Similarity: the idf-modified cosine (equation 2 of the paper),

    sum_w tf(w, x) tf(w, y) idf(w)^2
    / ( sqrt(sum_w (tf(w, x) idf(w))^2) * sqrt(sum_w (tf(w, y) idf(w))^2) ).

The idf table is given by the caller (the paper computes it from a large
corpus); `idf_from_sentences` uses the sentences themselves as documents,
idf(w) = log(n / n_w). A word missing from the table gets idf 0. A sentence
whose weighted vector is zero has cosine 0 with every other sentence.

Graph: A[i][j] = 1 if the cosine is above the threshold, else 0 (LexRank), or
A[i][j] = the cosine (continuous LexRank). The diagonal is always 1, as the
cosine of a nonzero vector with itself, so no row is empty. B is A with each
row divided by its sum.

Ranking: the stationary distribution of the chain d/n J + (1 - d) B, where d
is the probability of a random jump (equation 8 of the paper writes d for this
jump probability, between 0.1 and 0.2). It is found by the power method from
the uniform vector, stopping when the 1-norm of the change is below eps.
"""

import math
from collections import Counter
from typing import Dict, List, Optional, Sequence, Tuple

Matrix = List[List[float]]


def idf_from_sentences(sentences: Sequence[Sequence[str]]) -> Dict[str, float]:
    """Return idf(w) = log(n / n_w), with each sentence as a document."""
    n = len(sentences)
    df: Counter = Counter()
    for s in sentences:
        df.update({w.lower() for w in s})
    return {w: math.log(n / c) for w, c in df.items()}


def idf_modified_cosine(x: Sequence[str], y: Sequence[str], idf: Dict[str, float]) -> float:
    """Return the idf-modified cosine of two sentences, 0 if a vector is zero."""
    tx = Counter(w.lower() for w in x)
    ty = Counter(w.lower() for w in y)
    num = sum(tx[w] * ty[w] * idf.get(w, 0.0) ** 2 for w in tx if w in ty)
    nx = math.sqrt(sum((c * idf.get(w, 0.0)) ** 2 for w, c in tx.items()))
    ny = math.sqrt(sum((c * idf.get(w, 0.0)) ** 2 for w, c in ty.items()))
    if nx == 0.0 or ny == 0.0:
        return 0.0
    return num / (nx * ny)


def lexrank_matrix(
    sentences: Sequence[Sequence[str]],
    threshold: float = 0.1,
    idf: Optional[Dict[str, float]] = None,
    continuous: bool = False,
) -> Matrix:
    """Return the row-stochastic matrix B of the sentence graph."""
    if idf is None:
        idf = idf_from_sentences(sentences)
    n = len(sentences)
    a = [[0.0] * n for _ in range(n)]
    for i in range(n):  # @line L1
        for j in range(n):
            if i == j:
                a[i][j] = 1.0
                continue
            c = idf_modified_cosine(sentences[i], sentences[j], idf)  # @line L2
            if continuous:
                a[i][j] = c
            else:
                a[i][j] = 1.0 if c > threshold else 0.0  # @line L3
    b = []
    for i in range(n):
        deg = sum(a[i])  # @line L4
        b.append([x / deg for x in a[i]])
    return b


def power_method(
    b: Matrix, d: float = 0.15, eps: float = 1e-8, max_iter: int = 10000
) -> Tuple[List[float], int]:
    """Return the stationary distribution of d/n J + (1 - d) B and the number of steps."""
    n = len(b)
    if n == 0:
        return [], 0
    p = [1.0 / n] * n  # @line L5
    it = 0
    while it < max_iter:  # @line L6
        it += 1
        q = [d / n + (1.0 - d) * sum(b[i][j] * p[i] for i in range(n))
             for j in range(n)]  # @line L7
        delta = sum(abs(x - y) for x, y in zip(q, p))  # @line L8
        p = q
        if delta < eps:  # @line L9
            break
    return p, it  # @line L10


def lexrank(
    sentences: Sequence[Sequence[str]],
    threshold: float = 0.1,
    d: float = 0.15,
    eps: float = 1e-8,
    idf: Optional[Dict[str, float]] = None,
    continuous: bool = False,
) -> List[float]:
    """Return the LexRank score of every sentence; the scores sum to 1."""
    b = lexrank_matrix(sentences, threshold, idf, continuous)
    return power_method(b, d, eps)[0]


def lexrank_summarize(
    sentences: Sequence[Sequence[str]],
    k: int,
    threshold: float = 0.1,
    d: float = 0.15,
    idf: Optional[Dict[str, float]] = None,
    continuous: bool = False,
) -> List[int]:
    """Return the indices of the k best sentences in document order (ties to the earlier one)."""
    p = lexrank(sentences, threshold, d, 1e-10, idf, continuous)
    order = sorted(range(len(sentences)), key=lambda i: (-p[i], i))
    return sorted(order[:k])
