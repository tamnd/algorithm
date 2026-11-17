# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tandem-repeat-finding/. The authors are listed in prov/3VVNE0.jsonl.
"""Tandem repeat finding in the style of Benson's Tandem Repeats Finder (TRF).

A small version of the method. It keeps the two main parts of TRF:
- detection: k-tuple matches found with history lists, counted per distance d
  in a sliding window, and a sum of heads test that makes the pair (position,
  d) a candidate;
- confirmation: wraparound dynamic programming (WDP) of the candidate pattern
  against the sequence around it, a majority consensus, a second WDP with the
  consensus, and a report if at least two copies align with a score of at
  least min_score.

It leaves out these parts of TRF (the page says so too): the indel test that
also updates the distances d - 1, ..., d - delta and d + 1, ..., d + delta, the
random walk, apparent size and waiting time tests, the tuple size that depends
on the pattern size, banded WDP for large patterns, a consensus whose length
can differ from d, and the rules that let TRF report up to three periods for
one region. Here a candidate (position, d) is skipped when the position is in a
reported repeat with a period of at most d, or within one period after it, so
each region gets one report, usually with the smallest period.

Positions are 0-based and intervals half-open. Scores use TRF's convention:
match is a positive number and mismatch and indel are positive penalties that
are subtracted. The default weights (2, 7, 7) are those of the TRF paper.
"""

from collections import deque
from typing import Dict, List, NamedTuple, Optional, Sequence, Tuple

Number = float


class Repeat(NamedTuple):
    """A reported tandem repeat: s[start:end] is about copies copies of pattern."""

    start: int
    end: int
    period: int
    pattern: str
    score: int
    copies: float


def heads_distribution(w: int, k: int, p):
    """The law of the number of heads that lie in runs of at least k heads.

    The w positions are independent, each a head with probability p (a float or
    a Fraction). Returns a list q with q[c] = P(count = c) for c = 0..w. The
    state is the length of the current run, capped at k.
    """
    zero = p - p
    one = zero + 1
    # dist[r][c]: run length r (0..k, k means at least k) and count c
    dist = [[zero] * (w + 1) for _ in range(k + 1)]
    dist[0][0] = one
    for _ in range(w):
        new = [[zero] * (w + 1) for _ in range(k + 1)]
        for r in range(k + 1):
            row = dist[r]
            for c in range(w + 1):
                pr = row[c]
                if pr == zero:
                    continue
                new[0][c] += pr * (one - p)
                if r + 1 < k:
                    new[r + 1][c] += pr * p
                elif r + 1 == k:
                    new[k][c + k] += pr * p  # the run reaches k: its k heads count
                else:
                    new[k][c + 1] += pr * p
        dist = new
    return [sum(dist[r][c] for r in range(k + 1)) for c in range(w + 1)]


_THRESHOLDS: Dict[Tuple[int, int, float, float], int] = {}


def sum_of_heads_threshold(w: int, k: int, p_match: float, alpha: float = 0.05) -> int:
    """The largest c with P(count < c) <= alpha, for the count of heads_distribution.

    A true repeat whose copies match with probability p_match per position passes
    the test count >= c with probability at least 1 - alpha in each window.
    """
    key = (w, k, p_match, alpha)
    if key not in _THRESHOLDS:
        q = heads_distribution(w, k, p_match)
        c, below = 0, 0.0
        while c < w and below + q[c] <= alpha:
            below += q[c]
            c += 1
        _THRESHOLDS[key] = c
    return _THRESHOLDS[key]


def wraparound_table(text: str, pattern: str, match: int = 2, mismatch: int = 7,
                     indel: int = 7) -> List[List[int]]:
    """The WDP table of a local alignment of text with any number of copies of pattern.

    V[x][j] for x = 0..len(text) and j = 0..d is the best score of an alignment
    that ends with text[x - 1] and pattern[j - 1]; column 0 is a copy of column d,
    the end of one copy and the start of the next. Scores are at least 0.
    """
    d = len(pattern)
    if d == 0:
        raise ValueError("the pattern must not be empty")
    V = [[0] * (d + 1) for _ in range(len(text) + 1)]  # @line W1
    for x in range(1, len(text) + 1):  # @line W2
        a, up, row = text[x - 1], V[x - 1], V[x]
        for j in range(1, d + 1):  # @line W3
            diag = up[j - 1] + (match if a == pattern[j - 1] else -mismatch)
            row[j] = max(0, diag, up[j] - indel, row[j - 1] - indel)
        row[0] = row[d]  # @line W4
        for j in range(1, d + 1):  # @line W5
            v = row[j - 1] - indel
            if v <= row[j]:
                break
            row[j] = v
        row[0] = row[d]
    return V


def wraparound_align(text: str, pattern: str, match: int = 2, mismatch: int = 7,
                     indel: int = 7):
    """The best local WDP alignment of text against copies of pattern.

    Returns (score, a, b, cols) where text[a:b] is the aligned part and cols is
    the list of alignment columns from left to right: (x, j) for text[x] against
    pattern[j], (x, None) for text[x] against a gap and (None, j) for pattern[j]
    against a gap. The traceback prefers the diagonal, then a gap in the pattern,
    then a gap in the text, and stops at a cell of score 0. Among best cells the
    first in row order wins. An alignment of score 0 is empty: (0, 0, 0, []).
    """
    d = len(pattern)
    V = wraparound_table(text, pattern, match, mismatch, indel)
    best, bx, bj = 0, 0, 0
    for x in range(1, len(text) + 1):  # @line W6
        row = V[x]
        for j in range(1, d + 1):
            if row[j] > best:
                best, bx, bj = row[j], x, j
    if best == 0:
        return 0, 0, 0, []
    cols: List[Tuple[Optional[int], Optional[int]]] = []
    x, j = bx, bj
    while V[x][j] > 0:  # @line W7
        v = V[x][j]
        pj = j - 1 if j > 1 else d  # the column before j; column 0 is column d
        sub = match if text[x - 1] == pattern[j - 1] else -mismatch
        if V[x - 1][pj] + sub == v:
            cols.append((x - 1, j - 1))
            x, j = x - 1, pj
            continue
        if V[x - 1][j] - indel == v:
            cols.append((x - 1, None))
            x -= 1
            continue
        cols.append((None, j - 1))
        j = pj
    cols.reverse()
    a = x
    return best, a, bx, cols


def consensus(text: str, d: int, cols, old: str) -> str:
    """Majority base for each pattern position over the aligned text bases.

    Positions with no aligned base keep the old base. Ties go to the old base if
    it is among the most common bases, then to the first in the order ACGT.
    """
    counts = [dict() for _ in range(d)]
    for x, j in cols:
        if x is not None and j is not None:
            c = text[x]
            counts[j][c] = counts[j].get(c, 0) + 1
    out = []
    for j in range(d):
        if not counts[j]:
            out.append(old[j])
            continue
        top = max(counts[j].values())
        winners = [c for c in counts[j] if counts[j][c] == top]
        out.append(old[j] if old[j] in winners else min(winners, key="ACGTN".find))
    return "".join(out)


def pattern_length_used(cols) -> int:
    """The number of pattern positions that the alignment uses (matched or deleted)."""
    return sum(1 for _, j in cols if j is not None)


def _covered(reports: Sequence[Repeat], pos: int, d: int) -> bool:
    """True if pos is in a reported repeat with period at most d, or one period after it."""
    return any(r.start <= pos < r.end + r.period and r.period <= d for r in reports)


def _confirm(s: str, c: int, d: int, match: int, mismatch: int, indel: int):
    """WDP of the pattern s[c - d:c] around c, with the window grown as needed.

    The window grows until the alignment ends at least slack = d + 20 bases
    from each window edge (or at the end of s). Then the pattern is replaced by
    the majority consensus and aligned again, for at most max_rounds rounds or
    until the consensus does not change. Returns (score, start, end, cols,
    pattern) in coordinates of s, for the last pattern.
    """
    G = len(s)
    slack, step = d + 20, 3 * d + 30
    lo, hi = max(0, c - step), min(G, c + step)
    pattern = s[c - d:c]
    max_rounds = 3
    for round_ in range(max_rounds + 1):
        while True:
            score, a, b, cols = wraparound_align(s[lo:hi], pattern, match, mismatch, indel)
            grow_left = lo > 0 and a < slack
            grow_right = hi < G and b > hi - lo - slack
            if not (grow_left or grow_right):
                break
            if grow_left:
                lo = max(0, lo - step)
            if grow_right:
                hi = min(G, hi + step)
            step *= 2
        if round_ == max_rounds:
            break
        new = consensus(s[lo:hi], d, cols, pattern)
        if new == pattern:
            break
        pattern = new
    cols = [(None if x is None else x + lo, j) for x, j in cols]
    return score, a + lo, b + lo, cols, pattern


def find_tandem_repeats(s: str, k: int = 4, max_period: int = 50, p_match: float = 0.80,
                        min_window: int = 30, min_score: int = 50, match: int = 2,
                        mismatch: int = 7, indel: int = 7) -> List[Repeat]:
    """Find approximate tandem repeats with periods 1 to max_period in s.

    The window for distance d has length w(d) = max(d, min_window); min_window
    must be at least k. A pair (position, d) is a candidate when the number of
    heads (positions covered by k-tuple matches at distance d that lie fully in
    the window) reaches sum_of_heads_threshold(w(d), k, p_match). Distances are
    tried from the smallest. Reports are sorted by start, then by period.
    """
    if min_window < k:
        raise ValueError("min_window must be at least k")
    G = len(s)
    history: Dict[str, List[int]] = {}  # @line L1
    windows: Dict[int, deque] = {}
    covered_count: Dict[int, int] = {}
    next_test: Dict[int, int] = {}
    reports: List[Repeat] = []
    for i in range(G - k + 1):  # @line L2
        t, c = s[i:i + k], i + k  # @line L3
        h = history.setdefault(t, [])
        for idx in range(len(h) - 1, -1, -1):  # @line L4
            d = i - h[idx]
            if d > max_period:
                break
            w = max(d, min_window)
            win = windows.setdefault(d, deque())  # @line L5
            cov = covered_count.get(d, 0)
            gain = k if not win else min(k, i - win[-1][0])
            win.append([i, gain])
            cov += gain
            while win[0][0] < c - w:
                cov -= win.popleft()[1]
                cov += k - win[0][1]
                win[0][1] = k
            covered_count[d] = cov
            if cov < sum_of_heads_threshold(w, k, p_match):  # @line L6
                continue
            if next_test.get(d, 0) > i or _covered(reports, c - 1, d):
                continue
            next_test[d] = i + w
            score, a, b, cols, pattern = _confirm(s, c, d, match, mismatch, indel)  # @line L7
            used = pattern_length_used(cols)  # @line L8
            if used >= 2 * d and score >= min_score:  # @line L9
                reports.append(Repeat(a, b, d, pattern, score, round(used / d, 1)))  # @line L10
                next_test[d] = b
        h.append(i)  # @line L11
    reports = drop_multiples(reports)
    reports.sort(key=lambda r: (r.start, r.period))
    return reports  # @line L12


def drop_multiples(reports: Sequence[Repeat]) -> List[Repeat]:
    """Drop a report when a report with a smaller period that divides its period
    covers at least 90 percent of it with at least the same score."""
    keep = []
    for r in reports:
        length = r.end - r.start
        redundant = False
        for q in reports:
            if q.period < r.period and r.period % q.period == 0 and q.score >= r.score:
                overlap = min(q.end, r.end) - max(q.start, r.start)
                if 10 * overlap >= 9 * length:
                    redundant = True
                    break
        if not redundant:
            keep.append(r)
    return keep


def is_rotation(a: str, b: str) -> bool:
    """True if b is a cyclic rotation of a."""
    return len(a) == len(b) and b in a + a
