# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/feature-selection/. The authors are listed in prov/MFR8P0.jsonl.

"""Feature selection for least squares and for discrete data.

best_subset        exhaustive search over all subsets of size k (the exact problem)
forward_stepwise   greedy wrapper: add the feature that lowers the residual most
backward_stepwise  greedy wrapper: remove the feature whose loss raises the residual least
mrmr               filter: maximum relevance, minimum redundancy (Peng, Long and Ding 2005)

The residual sum of squares is computed exactly with fractions, by Gram-Schmidt
on the selected columns, so ties and zero residuals are exact.
"""

from fractions import Fraction
from itertools import combinations
import math

Matrix = list[list[float]]


def _columns(x: Matrix) -> list[list[Fraction]]:
    """Columns of the n x d matrix x, as exact fractions."""
    return [[Fraction(row[j]) for row in x] for j in range(len(x[0]))]


def _dot(a: list[Fraction], b: list[Fraction]) -> Fraction:
    return sum((p * q for p, q in zip(a, b)), Fraction(0))


def rss(x: Matrix, y: list[float], subset) -> Fraction:
    """min over beta of ||y - X_S beta||^2, exactly. The empty subset gives ||y||^2."""
    cols = _columns(x)
    basis: list[list[Fraction]] = []
    for j in subset:
        v = cols[j][:]
        for b in basis:
            c = _dot(v, b) / _dot(b, b)
            v = [p - c * q for p, q in zip(v, b)]
        if any(v):  # skip a column that is a combination of earlier ones
            basis.append(v)
    r = [Fraction(t) for t in y]
    for b in basis:
        c = _dot(r, b) / _dot(b, b)
        r = [p - c * q for p, q in zip(r, b)]
    return _dot(r, r)


def best_subset(x: Matrix, y: list[float], k: int) -> tuple[tuple[int, ...], Fraction]:
    """The subset of exactly k features with the smallest RSS, by trying all C(d, k) subsets."""
    d = len(x[0])
    if not 0 <= k <= d:
        raise ValueError("k must be between 0 and the number of features")
    best = None
    for s in combinations(range(d), k):
        e = rss(x, y, s)
        if best is None or e < best[1]:
            best = (s, e)
    return best


def forward_stepwise(x: Matrix, y: list[float], k: int) -> list[tuple[int, Fraction]]:
    """Add k features one at a time; each step adds the feature that gives the smallest RSS.

    Returns the path [(feature, RSS after adding it), ...]. Ties go to the lower index.
    """
    d = len(x[0])
    if not 0 <= k <= d:
        raise ValueError("k must be between 0 and the number of features")
    chosen: list[int] = []
    path = []
    for _ in range(k):
        best = None
        for j in range(d):
            if j in chosen:
                continue
            e = rss(x, y, chosen + [j])
            if best is None or e < best[1]:
                best = (j, e)
        chosen.append(best[0])
        path.append(best)
    return path


def backward_stepwise(x: Matrix, y: list[float], k: int) -> list[int]:
    """Start from all features and remove one at a time until k remain.

    Each step removes the feature whose removal gives the smallest RSS.
    """
    d = len(x[0])
    if not 0 <= k <= d:
        raise ValueError("k must be between 0 and the number of features")
    kept = list(range(d))
    while len(kept) > k:
        best = None
        for j in kept:
            e = rss(x, y, [i for i in kept if i != j])
            if best is None or e < best[1]:
                best = (j, e)
        kept.remove(best[0])
    return kept


def entropy(values: list) -> float:
    """Empirical Shannon entropy in bits."""
    n = len(values)
    counts: dict = {}
    for v in values:
        counts[v] = counts.get(v, 0) + 1
    return -sum(c / n * math.log2(c / n) for c in counts.values())


def mutual_information(a: list, b: list) -> float:
    """Empirical I(A; B) = H(A) + H(B) - H(A, B) in bits."""
    return entropy(a) + entropy(b) - entropy(list(zip(a, b)))


def mrmr(features: list[list], y: list, k: int) -> list[int]:
    """mRMR with the difference criterion (MID) of Peng, Long and Ding.

    features[j] is the column of discrete feature j. The first pick has the largest
    I(f; y). Each later pick maximizes I(f; y) - mean over chosen s of I(f; s).
    """
    d = len(features)
    if not 0 <= k <= d:
        raise ValueError("k must be between 0 and the number of features")
    relevance = [mutual_information(f, y) for f in features]
    chosen: list[int] = []
    redundancy = [0.0] * d  # running sum of I(f_j; f_s) over chosen s
    for _ in range(k):
        best, best_score = -1, -math.inf
        for j in range(d):
            if j in chosen:
                continue
            score = relevance[j] - (redundancy[j] / len(chosen) if chosen else 0.0)
            if score > best_score + 1e-12:
                best, best_score = j, score
        chosen.append(best)
        for j in range(d):
            if j not in chosen:
                redundancy[j] += mutual_information(features[j], features[best])
    return chosen
