# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bertscore/. The authors are listed in prov/T124HA.jsonl.

"""BERTScore (Zhang, Kishore, Wu, Weinberger and Artzi, ICLR 2020).

The code takes the contextual token embeddings of the network as given: a
reference is a list of n vectors of width d, and a candidate is a list of m
vectors of width d. It does not run or train a network. It implements the
greedy matching by cosine similarity, the optional idf weights and the
baseline rescaling.
"""

import math
from typing import Dict, Hashable, List, Optional, Sequence, Tuple

Vec = Sequence[float]


def normalize(v: Vec) -> List[float]:
    """Return v divided by its Euclidean length. A zero vector stays zero."""
    n = math.sqrt(sum(a * a for a in v))
    if n == 0.0:
        return [0.0 for _ in v]
    return [a / n for a in v]


def similarity_matrix(ref: Sequence[Vec], cand: Sequence[Vec]) -> List[List[float]]:
    """S[i][j] = cosine of reference token i and candidate token j (n x m)."""
    x = [normalize(v) for v in ref]
    y = [normalize(v) for v in cand]
    return [[sum(a * b for a, b in zip(u, v)) for v in y] for u in x]


def idf_from_references(references: Sequence[Sequence[Hashable]]) -> Dict[Hashable, float]:
    """idf(w) = log((M + 1) / (df(w) + 1)) over M reference token lists.

    This is one way to apply the plus-one smoothing that the paper names; a
    token not seen in any reference gets log(M + 1) (see unknown_idf).
    """
    m = len(references)
    df: Dict[Hashable, int] = {}
    for toks in references:
        for w in set(toks):
            df[w] = df.get(w, 0) + 1
    return {w: math.log((m + 1) / (c + 1)) for w, c in df.items()}


def unknown_idf(num_references: int) -> float:
    """The idf of a token that occurs in no reference."""
    return math.log(num_references + 1)


def weighted_mean(values: Sequence[float], weights: Optional[Sequence[float]]) -> float:
    if not values:
        return 0.0
    if weights is None:
        return sum(values) / len(values)
    total = sum(weights)
    if total == 0.0:
        return 0.0
    return sum(w * v for w, v in zip(weights, values)) / total


def bertscore(
    ref: Sequence[Vec],
    cand: Sequence[Vec],
    ref_weights: Optional[Sequence[float]] = None,
    cand_weights: Optional[Sequence[float]] = None,
) -> Tuple[float, float, float]:
    """Return (P, R, F) for one candidate and one reference.

    ref_weights and cand_weights are the idf weights of the tokens, or None
    for equal weights.
    """
    n, m = len(ref), len(cand)
    if n == 0 or m == 0:
        return 0.0, 0.0, 0.0
    x = [normalize(v) for v in ref]  # @line L1
    y = [normalize(v) for v in cand]
    s = [[sum(a * b for a, b in zip(u, v)) for v in y] for u in x]  # @line L2
    best_for_ref = [max(s[i][j] for j in range(m)) for i in range(n)]  # @line L3
    best_for_cand = [max(s[i][j] for i in range(n)) for j in range(m)]  # @line L4
    r = weighted_mean(best_for_ref, ref_weights)  # @line L5
    p = weighted_mean(best_for_cand, cand_weights)  # @line L6
    f = 2 * p * r / (p + r) if p + r != 0.0 else 0.0  # @line L7
    return p, r, f  # @line L9


def rescale(score: float, baseline: float) -> float:
    """Baseline rescaling (score - b) / (1 - b), for a baseline b < 1."""
    return (score - baseline) / (1.0 - baseline)  # @line L8


def bertscore_rescaled(
    ref: Sequence[Vec],
    cand: Sequence[Vec],
    baselines: Tuple[float, float, float],
    ref_weights: Optional[Sequence[float]] = None,
    cand_weights: Optional[Sequence[float]] = None,
) -> Tuple[float, float, float]:
    """(P, R, F), each rescaled with its own baseline (b_P, b_R, b_F)."""
    p, r, f = bertscore(ref, cand, ref_weights, cand_weights)
    bp, br, bf = baselines
    return rescale(p, bp), rescale(r, br), rescale(f, bf)
