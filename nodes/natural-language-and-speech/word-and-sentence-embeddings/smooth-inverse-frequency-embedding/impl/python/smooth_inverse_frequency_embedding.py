# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/smooth-inverse-frequency-embedding/. The authors are listed in prov/V5GPPB.jsonl.
"""Smooth inverse frequency (SIF) sentence vectors of Arora, Liang and Ma 2017.

A sentence vector is the mean of the word vectors of the sentence, each
weighted by a / (a + p(w)), where p(w) is the unigram probability of the word.
Then the projection of every sentence vector on the first singular vector u of
the matrix of all sentence vectors is removed. As in the authors' code, the
matrix is not centered before u is computed. The word vectors and the word
probabilities are given; the code does not train them.
"""

import math
import random
from typing import Dict, Iterable, List, Sequence, Tuple

Vector = List[float]


def dot(a: Sequence[float], b: Sequence[float]) -> float:
    return math.fsum(x * y for x, y in zip(a, b))


def norm(a: Sequence[float]) -> float:
    return math.sqrt(dot(a, a))


def word_probabilities(corpus: Iterable[Iterable[str]]) -> Dict[str, float]:
    """The unigram probability count(w) / (number of tokens) of each word of a tokenized corpus."""
    counts: Dict[str, int] = {}
    for sentence in corpus:
        for w in sentence:
            counts[w] = counts.get(w, 0) + 1
    total = sum(counts.values())
    if total == 0:
        raise ValueError("the corpus is empty")
    return {w: c / total for w, c in counts.items()}


def sif_weight(p: float, a: float = 1e-3) -> float:
    """a / (a + p): close to 1 for a rare word and close to a / p for a frequent one."""
    if not a > 0 or p < 0:
        raise ValueError("a must be positive and p must not be negative")
    return a / (a + p)


def weighted_average(
    tokens: Sequence[str], vectors: Dict[str, Sequence[float]], p: Dict[str, float], a: float, dim: int
) -> Vector:
    """(1 / |s|) sum over the words of s of a / (a + p(w)) v_w.

    Words without a vector are skipped and do not count in |s|. A word with no
    probability gets p = 0, the weight of an unseen word. A sentence with no
    known word gives the zero vector.
    """
    used = [w for w in tokens if w in vectors]
    if not used:
        return [0.0] * dim
    out = [0.0] * dim
    for w in used:
        c = sif_weight(p.get(w, 0.0), a)
        out = [o + c * x for o, x in zip(out, vectors[w])]
    return [o / len(used) for o in out]


def first_singular_vector(X: Sequence[Sequence[float]], seed: int = 0, tol: float = 1e-14, max_iter: int = 20000) -> Tuple[Vector, float]:
    """The first right singular vector u of X and the largest singular value.

    Power iteration on X^T X, which is not centered. The sign is fixed so that
    the largest entry of u is positive. Convergence needs a gap between the
    two largest singular values.
    """
    d = len(X[0])
    G = [[math.fsum(row[i] * row[j] for row in X) for j in range(d)] for i in range(d)]
    rng = random.Random(seed)
    u = [rng.gauss(0.0, 1.0) for _ in range(d)]
    n0 = norm(u)
    u = [x / n0 for x in u]
    for _ in range(max_iter):
        y = [dot(row, u) for row in G]
        ny = norm(y)
        if ny == 0:
            raise ValueError("every sentence vector is zero")
        y = [x / ny for x in y]
        done = max(abs(a - b) for a, b in zip(u, y)) < tol
        u = y
        if done:
            break
    big = max(range(d), key=lambda i: abs(u[i]))
    if u[big] < 0:
        u = [-x for x in u]
    sigma = math.sqrt(max(0.0, dot(u, [dot(row, u) for row in G])))
    return u, sigma


def remove_projection(v: Sequence[float], u: Sequence[float]) -> Vector:
    """v - u u^T v for a unit vector u."""
    c = dot(u, v)
    return [x - c * y for x, y in zip(v, u)]


def sif_embeddings(
    sentences: Sequence[Sequence[str]],
    vectors: Dict[str, Sequence[float]],
    p: Dict[str, float],
    a: float = 1e-3,
    seed: int = 0,
) -> Tuple[List[Vector], Vector]:
    """Return (the SIF vectors of the sentences, the removed direction u)."""
    dim = len(next(iter(vectors.values())))
    V = []
    for s in sentences:  # @line L1
        V.append(weighted_average(s, vectors, p, a, dim))  # @line L2
    X = V  # @line L3
    u, _ = first_singular_vector(X, seed)  # @line L4
    out = []
    for v in V:  # @line L5
        out.append(remove_projection(v, u))  # @line L6
    return out, u  # @line L7
