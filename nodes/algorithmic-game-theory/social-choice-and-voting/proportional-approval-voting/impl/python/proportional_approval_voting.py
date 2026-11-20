# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/proportional-approval-voting/. The authors are listed in prov/95W632.jsonl.
"""Proportional approval voting (PAV), Thiele's rule with harmonic weights.

An approval profile is a sequence of n ballots, each a set of candidates among 0, ..., m - 1.
A voter with j approved members in the committee W contributes H(j) = 1 + 1/2 + ... + 1/j to
the PAV score of W. PAV elects a committee of size k with the largest score. Every score is
an exact Fraction.

Three algorithms:
- pav: exact search over all committees, ties to the lexicographically first;
- seq_pav: sequential PAV, a greedy rule that adds the candidate with the largest gain;
- ls_pav: local search with swaps of gain at least n / k^2 (Aziz et al. 2018), polynomial,
  and its output satisfies extended justified representation.
"""

from fractions import Fraction
from itertools import combinations
from typing import Optional, Sequence, Tuple


def harmonic(j: int) -> Fraction:
    """Return H(j) = 1 + 1/2 + ... + 1/j, with H(0) = 0."""
    return sum((Fraction(1, t) for t in range(1, j + 1)), Fraction(0))


def pav_score(profile, committee) -> Fraction:
    """Return the PAV score: the sum over voters of H(number of approved members)."""
    W = set(committee)
    return sum((harmonic(len(W & set(A))) for A in profile), Fraction(0))


def pav(profile, m: int, k: int) -> Tuple[int, ...]:
    """Return the lexicographically first committee of size k with the largest PAV score.

    Exact search over all C(m, k) committees: O(C(m, k) n k) time.
    """
    if not 0 <= k <= m:
        raise ValueError("need 0 <= k <= m")
    H = [harmonic(j) for j in range(k + 1)]
    ballots = [set(A) for A in profile]
    best, best_score = None, None
    for W in combinations(range(m), k):
        s = sum((H[sum(1 for c in W if c in A)] for A in ballots), Fraction(0))
        if best_score is None or s > best_score:
            best, best_score = W, s
    return best


def seq_pav(profile, m: int, k: int) -> Tuple[int, ...]:
    """Sequential PAV: k times, add the candidate with the largest gain in PAV score.

    A voter with j approved members so far gains 1 / (j + 1) if the new candidate is approved.
    Ties go to the smallest index. O(k m n) time.
    """
    if not 0 <= k <= m:
        raise ValueError("need 0 <= k <= m")
    ballots = [set(A) for A in profile]
    cnt = [0] * len(ballots)
    W = []
    for _ in range(k):
        pick, pick_gain = None, None
        for c in range(m):
            if c in W:
                continue
            g = sum((Fraction(1, x + 1) for A, x in zip(ballots, cnt) if c in A), Fraction(0))
            if pick_gain is None or g > pick_gain:
                pick, pick_gain = c, g
        W.append(pick)
        cnt = [x + (1 if pick in A else 0) for A, x in zip(ballots, cnt)]
    return tuple(sorted(W))


def swap_gain(ballots, cnt, out_c: int, in_c: int) -> Fraction:
    """Return PAV(W - out_c + in_c) - PAV(W), where cnt[i] = |A_i & W|, out_c in W, in_c not."""
    g = Fraction(0)
    for A, x in zip(ballots, cnt):
        a_in, a_out = in_c in A, out_c in A
        if a_in and not a_out:
            g += Fraction(1, x + 1)
        elif a_out and not a_in:
            g -= Fraction(1, x)
    return g


def ls_pav(profile, m: int, k: int, start: Optional[Sequence[int]] = None) -> Tuple[int, ...]:
    """Local search PAV: swap a member for a non-member while the PAV score rises by n / k^2.

    Starts from seq_pav unless a start committee is given. Each swap raises the score by at
    least n / k^2 and the score is at most n H(k), so there are at most k^2 H(k) swaps; each
    scan tries k (m - k) swaps in O(n) time each.
    """
    if not 0 <= k <= m:
        raise ValueError("need 0 <= k <= m")
    n = len(profile)
    ballots = [set(A) for A in profile]
    W = sorted(seq_pav(profile, m, k) if start is None else start)  # @line L1
    if n == 0 or k == 0 or k == m:
        return tuple(W)
    eps = Fraction(n, k * k)  # @line L2
    cnt = [len(A & set(W)) for A in ballots]  # @line L3
    while True:  # @line L4
        found = None
        for w in W:  # @line L5
            for c in range(m):
                if c in W:
                    continue
                if swap_gain(ballots, cnt, w, c) >= eps:  # @line L6
                    found = (w, c)
                    break
            if found:
                break
        if found is None:  # @line L7
            return tuple(W)
        w, c = found  # @line L8
        W.remove(w)
        W.append(c)
        W.sort()
        cnt = [x - (w in A) + (c in A) for A, x in zip(ballots, cnt)]  # @line L9
