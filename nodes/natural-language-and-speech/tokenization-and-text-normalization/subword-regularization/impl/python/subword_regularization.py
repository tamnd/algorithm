# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/subword-regularization/. The authors are listed in prov/510HA2.jsonl.

"""Sampling of segmentations for subword regularization (Kudo 2018, Section 3.3).

A model is a dict from pieces to natural log probabilities. A segmentation s
of x has the log probability sum of log p(w) over its pieces. Both samplers
draw s with probability proportional to P(s)^a, where a > 0 is the smoothing
value:

    sample_lattice  over all segmentations, by forward filtering (LOG semiring)
                    and backward sampling
    sample_nbest    over the l best segmentations only

exact_distribution enumerates all segmentations, for tests and small examples.
Positions are fenceposts 0..n; the piece x[i:j] is the edge from i to j.
"""

import math
import random
from typing import Dict, List, Tuple

from nlslog import LOG, NEG_INF, log_sum

Model = Dict[str, float]
Seg = Tuple[str, ...]


def _max_len(model: Model) -> int:
    return max(len(w) for w in model)


def forward(x: str, model: Model, a: float) -> List[float]:
    """alpha[j] = log of the sum over segmentations s of x[:j] of P(s)^a."""
    n, m = len(x), _max_len(model)
    alpha = [LOG.zero] * (n + 1)
    alpha[0] = LOG.one
    for j in range(1, n + 1):
        alpha[j] = log_sum(LOG.times(alpha[i], a * model[x[i:j]])
                           for i in range(max(0, j - m), j) if x[i:j] in model)
    return alpha


def sample_lattice(x: str, model: Model, a: float, rng: random.Random) -> Seg:
    """Draw s with probability P(s)^a / Z, by forward filtering and backward sampling."""
    n, m = len(x), _max_len(model)
    alpha = forward(x, model, a)  # @line S1
    if alpha[n] == NEG_INF:  # @line S2
        raise ValueError("the word has no segmentation")
    pieces, j = [], n  # @line S3
    while j > 0:  # @line S4
        starts = [i for i in range(max(0, j - m), j) if x[i:j] in model]
        logw = [alpha[i] + a * model[x[i:j]] - alpha[j] for i in starts]  # @line S5
        r, acc, pick = rng.random(), 0.0, starts[-1]  # @line S6
        for i, lw in zip(starts, logw):
            acc += math.exp(lw)
            if r < acc:
                pick = i
                break
        pieces.append(x[pick:j])  # @line S7
        j = pick
    return tuple(pieces[::-1])  # @line S8


def nbest(x: str, model: Model, l: int) -> List[Tuple[float, Seg]]:
    """The l best segmentations with their log probabilities, best first (ties by the pieces)."""
    n, m = len(x), _max_len(model)
    best: List[List[Tuple[float, Seg]]] = [[] for _ in range(n + 1)]
    best[0] = [(0.0, ())]
    for j in range(1, n + 1):
        cands = [(score + model[x[i:j]], seg + (x[i:j],))
                 for i in range(max(0, j - m), j) if x[i:j] in model
                 for score, seg in best[i]]
        best[j] = sorted(cands, key=lambda t: (-t[0], t[1]))[:l]
    return best[n]


def sample_nbest(x: str, model: Model, a: float, l: int, rng: random.Random) -> Seg:
    """Draw one of the l best segmentations with probability proportional to P(s)^a."""
    top = nbest(x, model, l)  # @line N1
    if not top:
        raise ValueError("the word has no segmentation")
    z = log_sum(a * score for score, _ in top)  # @line N2
    r, acc = rng.random(), 0.0  # @line N3
    for score, seg in top:  # @line N4
        acc += math.exp(a * score - z)
        if r < acc:
            return seg
    return top[-1][1]


def segmentations(x: str, model: Model) -> List[Seg]:
    if not x:
        return [()]
    return [(x[:j],) + rest for j in range(1, len(x) + 1) if x[:j] in model
            for rest in segmentations(x[j:], model)]


def exact_distribution(x: str, model: Model, a: float, l: int = 0) -> Dict[Seg, float]:
    """P(s)^a / Z over all segmentations, or over the l best ones if l > 0."""
    segs = [(sum(model[w] for w in s), s) for s in segmentations(x, model)]
    if l > 0:
        segs = sorted(segs, key=lambda t: (-t[0], t[1]))[:l]
    z = log_sum(a * score for score, _ in segs)
    return {s: math.exp(a * score - z) for score, s in segs}
