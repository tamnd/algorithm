# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/alphafold/. The authors are listed in prov/VWHHRT.jsonl.

"""The confidence measure of AlphaFold: lDDT-C-alpha and pLDDT.

This file does not reproduce the AlphaFold network. It implements the score
that the network is trained to predict for each residue, the lDDT of
Mariani et al. (2013) on C-alpha atoms, and the way AlphaFold turns the
50 logits of its confidence head into the reported pLDDT (Jumper et al. 2021).

Coordinates are sequences of (x, y, z) tuples in angstroms, one per residue.
"""

import math
from typing import List, Optional, Sequence, Tuple

Point = Sequence[float]
THRESHOLDS = (0.5, 1.0, 2.0, 4.0)


def _dist(a: Point, b: Point) -> float:
    return math.sqrt(sum((u - v) ** 2 for u, v in zip(a, b)))


def lddt(model: Sequence[Point], ref: Sequence[Point], cutoff: float = 15.0,
         thresholds: Sequence[float] = THRESHOLDS) -> Tuple[float, List[Optional[float]]]:
    """Global and per-residue lDDT of model against ref, both in [0, 1].

    A pair (i, j), i != j, is scored if its distance in the reference is below
    cutoff. It is preserved at threshold t if its distance in the model differs
    from the reference distance by less than t. A residue with no scored pair
    gets None. The global score pools all scored pairs; it is 0 if there are none.
    """
    n = len(ref)
    if len(model) != n:
        raise ValueError("model and reference must have the same residues")
    per: List[Optional[float]] = []
    kept_total = 0.0
    pairs_total = 0
    for i in range(n):  # @line L1
        near = [j for j in range(n) if j != i and _dist(ref[i], ref[j]) < cutoff]  # @line L2
        dev = [abs(_dist(model[i], model[j]) - _dist(ref[i], ref[j])) for j in near]  # @line L3
        if not near:
            per.append(None)
            continue
        kept = sum(sum(1 for d in dev if d < t) for t in thresholds) / len(thresholds)
        per.append(kept / len(near))  # @line L4
        kept_total += kept
        pairs_total += len(near)
    score = kept_total / pairs_total if pairs_total else 0.0  # @line L5
    return score, per  # @line L6


def softmax(z: Sequence[float]) -> List[float]:
    top = max(z)
    w = [math.exp(v - top) for v in z]
    s = sum(w)
    return [v / s for v in w]


def bin_centers(n_bins: int = 50) -> List[float]:
    """Centers of n_bins equal bins on [0, 1]: (k + 1/2) / n_bins."""
    return [(k + 0.5) / n_bins for k in range(n_bins)]


def plddt(logits: Sequence[Sequence[float]]) -> List[float]:
    """pLDDT in [0, 100] for each residue from the logits of the confidence head."""
    out = []
    for z in logits:
        p = softmax(z)  # @line L7
        out.append(100.0 * sum(pk * c for pk, c in zip(p, bin_centers(len(z)))))  # @line L8
    return out  # @line L9


def target_bin(value: float, n_bins: int = 50) -> int:
    """The training target of the confidence head: the bin of a true lDDT value in [0, 1]."""
    return min(n_bins - 1, max(0, int(value * n_bins)))


def confidence_loss(logits: Sequence[Sequence[float]], true_lddt: Sequence[Optional[float]]) -> float:
    """Mean cross-entropy between the head and the binned true per-residue lDDT."""
    total, count = 0.0, 0
    for z, v in zip(logits, true_lddt):
        if v is None:
            continue
        p = softmax(z)
        total -= math.log(p[target_bin(v, len(z))])
        count += 1
    return total / count if count else 0.0
