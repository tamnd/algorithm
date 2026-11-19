# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hard-debiasing/. The authors are listed in prov/92204H.jsonl.
"""Hard debiasing of word vectors (Bolukbasi, Chang, Zou, Saligrama and Kalai 2016).

The word vectors are given as a dict from a word to a list of floats; the
code does not train them. The bias subspace B is spanned by the top k
eigenvectors of the within-set covariance of the defining sets (for gender,
pairs such as she and he). Neutralize removes the B component of each neutral
word and normalizes it. Equalize moves each word of an equality set to the
same point outside B, with opposite B components of the same length, so that
every neutral word is equally far from all words of the set.
"""

import math
import random
from typing import Dict, List, Sequence, Tuple

Vector = List[float]
Matrix = List[List[float]]


def dot(a: Sequence[float], b: Sequence[float]) -> float:
    return math.fsum(x * y for x, y in zip(a, b))


def norm(a: Sequence[float]) -> float:
    return math.sqrt(dot(a, a))


def normalize(a: Sequence[float]) -> Vector:
    n = norm(a)
    if n == 0:
        raise ValueError("cannot normalize a zero vector")
    return [x / n for x in a]


def mean(vectors: Sequence[Sequence[float]]) -> Vector:
    return [math.fsum(col) / len(vectors) for col in zip(*vectors)]


def within_set_covariance(defining_sets: Sequence[Sequence[Sequence[float]]]) -> Matrix:
    """C = sum over the sets D of sum over w in D of (w - mu_D)(w - mu_D)^T / |D|."""
    d = len(defining_sets[0][0])
    C = [[0.0] * d for _ in range(d)]
    for D in defining_sets:
        mu = mean(D)
        for w in D:
            r = [x - m for x, m in zip(w, mu)]
            for a in range(d):
                for b in range(d):
                    C[a][b] += r[a] * r[b] / len(D)
    return C


def top_eigenvectors(C: Matrix, k: int, seed: int = 0, tol: float = 1e-13, max_iter: int = 20000) -> Tuple[List[Vector], List[float]]:
    """The top k eigenvectors and eigenvalues of a symmetric positive semidefinite C.

    Power iteration with deflation. Each vector is made unique by giving its
    largest entry a positive sign. Convergence needs a gap between the
    eigenvalues, as for any power iteration.
    """
    d = len(C)
    rng = random.Random(seed)
    M = [row[:] for row in C]
    vecs: List[Vector] = []
    vals: List[float] = []
    for _ in range(k):
        x = normalize([rng.gauss(0.0, 1.0) for _ in range(d)])
        for _ in range(max_iter):
            y = [dot(row, x) for row in M]
            for v in vecs:
                c = dot(v, y)
                y = [a - c * b for a, b in zip(y, v)]
            if norm(y) == 0:
                break
            y = normalize(y)
            done = max(abs(a - b) for a, b in zip(x, y)) < tol
            x = y
            if done:
                break
        big = max(range(d), key=lambda i: abs(x[i]))
        if x[big] < 0:
            x = [-a for a in x]
        lam = dot(x, [dot(row, x) for row in M])
        vecs.append(x)
        vals.append(lam)
        M = [[M[a][b] - lam * x[a] * x[b] for b in range(d)] for a in range(d)]
    return vecs, vals


def bias_subspace(defining_sets: Sequence[Sequence[Sequence[float]]], k: int = 1, seed: int = 0) -> List[Vector]:
    """An orthonormal basis of the bias subspace B: the top k eigenvectors of C."""
    return top_eigenvectors(within_set_covariance(defining_sets), k, seed)[0]


def project(w: Sequence[float], B: Sequence[Sequence[float]]) -> Vector:
    """w_B, the projection of w on the span of the orthonormal rows of B."""
    out = [0.0] * len(w)
    for b in B:
        c = dot(w, b)
        out = [o + c * x for o, x in zip(out, b)]
    return out


def neutralize(w: Sequence[float], B: Sequence[Sequence[float]]) -> Vector:
    """(w - w_B) / |w - w_B|."""
    wb = project(w, B)
    return normalize([x - y for x, y in zip(w, wb)])


def equalize(E: Sequence[Sequence[float]], B: Sequence[Sequence[float]]) -> List[Vector]:
    """Move each word of the equality set E to nu + sqrt(1 - |nu|^2) (w_B - mu_B) / |w_B - mu_B|.

    mu is the mean of E and nu = mu - mu_B. The words of E should be unit vectors.
    """
    mu = mean(E)
    mu_b = project(mu, B)
    nu = [x - y for x, y in zip(mu, mu_b)]
    scale = math.sqrt(max(0.0, 1.0 - dot(nu, nu)))
    out = []
    for w in E:
        diff = [x - y for x, y in zip(project(w, B), mu_b)]
        if norm(diff) == 0:
            raise ValueError("a word of the equality set has the same bias component as the mean")
        out.append([n + scale * x for n, x in zip(nu, normalize(diff))])
    return out


def hard_debias(
    vectors: Dict[str, Sequence[float]],
    defining_sets: Sequence[Sequence[str]],
    neutral_words: Sequence[str],
    equality_sets: Sequence[Sequence[str]],
    k: int = 1,
    seed: int = 0,
) -> Tuple[Dict[str, Vector], List[Vector]]:
    """Return (the debiased vectors, the basis of B). The input dict is not changed."""
    W = {w: normalize(v) for w, v in vectors.items()}  # @line L1
    D = [[W[w] for w in S] for S in defining_sets]  # @line L2
    C = within_set_covariance(D)  # @line L3
    B = top_eigenvectors(C, k, seed)[0]  # @line L4
    for w in neutral_words:
        W[w] = neutralize(W[w], B)  # @line L5
    for S in equality_sets:
        E = [W[w] for w in S]  # @line L6
        for w, v in zip(S, equalize(E, B)):
            W[w] = v  # @line L7
    return W, B  # @line L8


def direct_bias(words: Sequence[Sequence[float]], g: Sequence[float], c: float = 1.0) -> float:
    """DirectBias_c = the mean over the words of |cos(w, g)|^c."""
    ng = norm(g)
    return math.fsum(abs(dot(w, g) / (norm(w) * ng)) ** c for w in words) / len(words)
