# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/diverse-beam-search/. The authors are listed in prov/K6SZXR.jsonl.

"""Diverse beam search with the Hamming diversity penalty (Vijayakumar et al. 2018).

A model is a function that takes the prefix y_1 ... y_t (a tuple of strings)
and returns a dict from each token to log p(w | prefix), in natural log. The
end token is the string "</s>". The code takes these log probabilities as
given; it does not run or train a network.
"""

from collections import Counter
from typing import Callable, Dict, List, Tuple

from nlslog import NEG_INF

EOS = "</s>"

Model = Callable[[Tuple[str, ...]], Dict[str, float]]
Output = Tuple[List[str], float, int]


def diverse_beam_search(
    model: Model, max_len: int, groups: int, width: int, lam: float
) -> List[Output]:
    """Return the finished outputs of all groups as (tokens, log p, group).

    The beam has groups * width slots, split into groups of width slots. At
    each step, group g ranks its candidates by log p minus lam times the
    number of times the earlier groups chose the same last token at this
    step. A candidate that ends with "</s>" leaves the beam as a finished
    output. Outputs that are still open after max_len tokens are dropped.
    The result is sorted by log p, best first; on ties the lower group and
    the earlier finish come first.
    """
    if groups < 1 or width < 1 or max_len < 1:
        raise ValueError("groups, width and max_len must be at least 1")
    beams: List[List[Tuple[Tuple[str, ...], float]]] = [[((), 0.0)] for _ in range(groups)]  # @line L1
    finished: List[Output] = []
    for t in range(max_len):  # @line L2
        used: Counter = Counter()  # @line L3
        for g in range(groups):  # @line L4
            cand = []
            for y, s in beams[g]:  # @line L5
                for w, lp in model(y).items():
                    if lp == NEG_INF:
                        continue
                    cand.append((s + lp - hamming_penalty(w, used, lam), s + lp, y + (w,)))  # @line L6
            order = sorted(range(len(cand)), key=lambda i: (-cand[i][0], i))
            chosen = [cand[i] for i in order[:width]]  # @line L7
            beams[g] = []
            for _, s, y in chosen:
                used[y[-1]] += 1  # @line L8
                if y[-1] == EOS:  # @line L9
                    finished.append((list(y), s, g))
                else:
                    beams[g].append((y, s))
        if not any(beams):
            break
    order = sorted(range(len(finished)), key=lambda i: (-finished[i][1], finished[i][2], i))
    return [finished[i] for i in order]  # @line L10


def hamming_penalty(token: str, used: Counter, lam: float) -> float:
    """Return the Hamming diversity term lam * (the number of earlier uses of token)."""
    return lam * used[token]
