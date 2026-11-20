# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/approval-voting/. The authors are listed in prov/2YTCNT.jsonl.

from typing import AbstractSet, Sequence

Ballot = AbstractSet[int]


def approval_scores(ballots: Sequence[Ballot], m: int) -> list[int]:
    """Return s with s[a] the number of ballots that approve candidate a.

    The candidates are 0, ..., m - 1 and each ballot is a set of candidates. The time is
    O(n + m + L), with L the total size of the n ballots.
    """
    s = [0] * m  # @line L1
    for S in ballots:  # @line L2
        for a in S:  # @line L3
            s[a] += 1  # @line L4
    return s


def approval_winners(ballots: Sequence[Ballot], m: int) -> frozenset[int]:
    """Return the set of candidates with the most approvals (the approval correspondence)."""
    s = approval_scores(ballots, m)
    best = max(s)  # @line L5
    return frozenset(a for a in range(m) if s[a] == best)  # @line L6


def approval(ballots: Sequence[Ballot], m: int) -> int:
    """Return the approval winner; a tie goes to the candidate with the smallest index.

    Precondition: m >= 1. Empty ballots are allowed. Time O(n + m + L), extra space O(m).
    """
    return min(approval_winners(ballots, m))  # @line L7


def sincere_ballot(ranking: Sequence[int], k: int) -> frozenset[int]:
    """Return the ballot that approves the k best candidates of the ranking."""
    return frozenset(ranking[:k])
