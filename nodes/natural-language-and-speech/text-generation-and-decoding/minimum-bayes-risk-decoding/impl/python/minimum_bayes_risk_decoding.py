# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimum-bayes-risk-decoding/. The authors are listed in prov/FTCX13.jsonl.

"""Minimum Bayes risk decoding.

The decoder picks, from a set of candidate outputs, the one with the least
expected loss under the model. The expectation runs over a list of evidence
outputs with weights: the exact distribution of a small model, or N samples
of the model with weight 1 / N each. The code takes the candidates, the
samples and their log probabilities as given; it does not run a network.
"""

import math
from typing import Callable, Hashable, List, Optional, Sequence, Tuple, TypeVar

from nlslog import log_normalize

Y = TypeVar("Y", bound=Hashable)
Loss = Callable[[Y, Y], float]


def mbr_decode(
    candidates: Sequence[Y], evidence: Sequence[Tuple[Y, float]], loss: Loss
) -> Tuple[Y, float]:
    """Return (the candidate of least risk, its risk).

    The risk of h is the sum over (y, w) in evidence of w * loss(h, y). On
    ties the first candidate wins. The weights need not sum to 1; the choice
    does not change when every weight is scaled by the same positive number.
    """
    if not candidates:
        raise ValueError("no candidates")
    best: Optional[Y] = None
    best_risk = math.inf  # @line L1
    for h in candidates:  # @line L2
        risk = sum(w * loss(h, y) for y, w in evidence)  # @line L3
        if risk < best_risk:  # @line L4
            best, best_risk = h, risk
    return best, best_risk  # @line L5


def mbr_from_log_probs(
    candidates: Sequence[Y], evidence: Sequence[Tuple[Y, float]], loss: Loss
) -> Tuple[Y, float]:
    """MBR with evidence given as (y, log p(y)); the weights are normalized in log space."""
    ws = [math.exp(v) for v in log_normalize([lp for _, lp in evidence])]
    return mbr_decode(candidates, [(y, w) for (y, _), w in zip(evidence, ws)], loss)


def mbr_from_samples(samples: Sequence[Y], loss: Loss) -> Tuple[Y, float]:
    """Sample-based MBR: the distinct samples are the candidates, all samples the evidence.

    The cost is N * (the number of distinct samples) loss calls for N samples,
    so at most N^2.
    """
    if not samples:
        raise ValueError("no samples")
    seen = {}
    for y in samples:
        seen.setdefault(y, None)
    w = 1.0 / len(samples)
    return mbr_decode(list(seen), [(y, w) for y in samples], loss)


def word_edit_distance(a: Sequence[str], b: Sequence[str]) -> int:
    """Return the Levenshtein distance between two token sequences (unit costs)."""
    prev = list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        cur = [i] + [0] * len(b)
        for j in range(1, len(b) + 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] != b[j - 1]))
        prev = cur
    return prev[-1]


def zero_one_loss(a, b) -> int:
    """Return 0 if a equals b, else 1."""
    return 0 if a == b else 1


def expected_losses(candidates: Sequence[Y], evidence: Sequence[Tuple[Y, float]], loss: Loss) -> List[float]:
    """Return the risk of each candidate, in order."""
    return [sum(w * loss(h, y) for y, w in evidence) for h in candidates]
