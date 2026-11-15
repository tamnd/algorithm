# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reciprocal-rank-fusion/. The authors are listed in prov/552S8S.jsonl.

from fractions import Fraction
from typing import Any, Hashable, Mapping, Sequence

Ranking = Sequence[Hashable]


def to_ranking(scores: Mapping[Hashable, float]) -> list[Any]:
    """Turn a run of scores into a ranking: score descending, then id ascending."""
    return sorted(scores, key=lambda d: (-scores[d], d))


def rrf_scores(rankings: Sequence[Ranking], k: int = 60, exact: bool = False) -> dict[Any, Any]:
    """Return the RRF score of each document: the sum over the rankings that hold it of 1/(k + rank).

    Ranks start at 1. A ranking that does not hold a document adds 0 for it. With
    exact=True the scores are Fractions.
    """
    one = Fraction(1) if exact else 1.0
    score: dict[Any, Any] = {}  # @line L1
    for r in rankings:  # @line L2
        for i, d in enumerate(r, start=1):  # @line L3
            score[d] = score.get(d, 0 * one) + one / (k + i)  # @line L4
    return score


def rrf(rankings: Sequence[Ranking], k: int = 60, depth: int | None = None) -> list[Any]:
    """Fuse the rankings, each cut to its first depth documents when depth is given."""
    cut = [list(r)[:depth] if depth is not None else list(r) for r in rankings]
    score = rrf_scores(cut, k, exact=True)
    return sorted(score, key=lambda d: (-score[d], d))  # @line L5
