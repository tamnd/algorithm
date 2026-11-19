# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/length-normalization/. The authors are listed in prov/AP6ENR.jsonl.

"""Length normalization of the scores of finished hypotheses.

The length |Y| of a hypothesis counts every predicted token, "</s>"
included. Toolkits differ on this point; the code follows one rule
everywhere. A model is a function from a prefix (a tuple of strings) to a
dict of log probabilities, in natural log. The code takes these log
probabilities as given; it does not run a network.
"""

import math
from typing import Callable, Dict, List, Optional, Sequence, Tuple

from nlslog import NEG_INF

EOS = "</s>"

Model = Callable[[Tuple[str, ...]], Dict[str, float]]
Penalty = Callable[[int], float]


def power_penalty(alpha: float) -> Penalty:
    """lp(Y) = |Y|^alpha. alpha = 0 is the raw score, alpha = 1 the mean log probability."""
    return lambda length: float(length) ** alpha


def gnmt_penalty(alpha: float) -> Penalty:
    """lp(Y) = ((5 + |Y|) / 6)^alpha of Wu et al. 2016. lp = 1 for |Y| = 1."""
    return lambda length: ((5.0 + length) / 6.0) ** alpha


def gnmt_coverage(attention: Sequence[Sequence[float]], beta: float) -> float:
    """cp = beta * sum over source words i of log(min(sum over target words j of p_ij, 1)).

    attention[j][i] is the attention weight of target position j on source
    word i. A source word with no attention gives NEG_INF.
    """
    if not attention:
        return 0.0
    total = 0.0
    for i in range(len(attention[0])):
        mass = math.fsum(row[i] for row in attention)
        if mass <= 0:
            return NEG_INF
        total += math.log(min(mass, 1.0))
    return beta * total


def normalized(log_p: float, length: int, lp: Penalty) -> float:
    """Return log p / lp(|Y|)."""
    return log_p / lp(length)


def word_reward(log_p: float, length: int, reward: float) -> float:
    """Return log p + reward * |Y|, the additive fix of Murray and Chiang 2018 and others."""
    return log_p + reward * length


def rerank(hyps: Sequence[Tuple[Sequence[str], float]], lp: Penalty) -> Optional[Tuple[List[str], float]]:
    """Return the finished hypothesis with the best normalized score, and that score.

    hyps holds (tokens, log p). On ties the first one wins.
    """
    best: Optional[Tuple[List[str], float]] = None  # @line L1
    for y, log_p in hyps:  # @line L2
        s = normalized(log_p, len(y), lp)  # @line L3
        if best is None or s > best[1]:  # @line L4
            best = (list(y), s)
    return best  # @line L5


def beam_search_normalized(model: Model, max_len: int, width: int, lp: Penalty) -> Optional[Tuple[List[str], float]]:
    """Beam search that ranks open hypotheses by log p and finished ones by log p / lp.

    It stops when no open hypothesis can beat the best finished one. Since
    log p <= 0 can only go down and lp does not go down with the length, an
    open hypothesis of score s can reach at most s / lp(max_len) when lp is
    non-decreasing and positive. The function needs that property of lp.
    """
    beam: List[Tuple[Tuple[str, ...], float]] = [((), 0.0)]
    best: Optional[Tuple[List[str], float]] = None
    for _ in range(max_len):
        cand = []
        for y, s in beam:
            for w, lpw in model(y).items():
                if lpw > NEG_INF:
                    cand.append((y + (w,), s + lpw))
        beam = []
        for y, s in sorted(cand, key=lambda t: -t[1]):
            if y[-1] == EOS:
                score = normalized(s, len(y), lp)
                if best is None or score > best[1]:
                    best = (list(y), score)
            elif len(beam) < width:
                beam.append((y, s))
        if not beam:
            break
        if best is not None and all(s / lp(max_len) <= best[1] for _, s in beam):
            break
    return best
