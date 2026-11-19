# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/translation-edit-rate/. The authors are listed in prov/EWE8J4.jsonl.

"""Translation edit rate (TER) of Snover et al. (2006), with greedy shifts.

The input is pre-tokenized: a hypothesis is a list of tokens, and it has one or
more references, each a list of tokens. Every edit costs 1: the insertion, the
deletion or the substitution of one word, and the shift of a block of words.

Finding the fewest edits with shifts is NP-hard, so the shifts are chosen
greedily as in tercom: in each round, among the blocks of the hypothesis that
occur in the reference and contain an error on both sides, the shift that most
lowers the edit distance is applied, while some shift lowers it by at least 1.
The result is the cost of a valid sequence of edits, so it is an upper bound
on the fewest edits, and it is never above the plain edit distance.

This version tries every block and every destination, with no limit on the
block size or the distance moved (tercom limits both). Ties go to the larger
gain, then the longer block, then the earlier block, then the earlier
destination.
"""

from typing import List, Optional, Sequence, Tuple

Tokens = Sequence[str]


def edit_distance_errors(h: Tokens, r: Tokens) -> Tuple[int, List[bool], List[bool]]:
    """Return the word edit distance and, for one optimal alignment, the error flag of each word.

    A word of h or r has the flag False when the alignment matches it with an
    equal word. The traceback prefers a match, then a substitution, then a
    deletion of a word of h, then an insertion of a word of r.
    """
    n, m = len(h), len(r)
    d = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        d[i][0] = i
    for j in range(m + 1):
        d[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            d[i][j] = min(d[i - 1][j - 1] + (h[i - 1] != r[j - 1]), d[i - 1][j] + 1, d[i][j - 1] + 1)
    herr, rerr = [True] * n, [True] * m
    i, j = n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0 and h[i - 1] == r[j - 1] and d[i][j] == d[i - 1][j - 1]:
            herr[i - 1] = rerr[j - 1] = False
            i, j = i - 1, j - 1
        elif i > 0 and j > 0 and d[i][j] == d[i - 1][j - 1] + 1:
            i, j = i - 1, j - 1
        elif i > 0 and d[i][j] == d[i - 1][j] + 1:
            i -= 1
        else:
            j -= 1
    return d[n][m], herr, rerr


def shift(h: Tokens, i: int, k: int, p: int) -> List[str]:
    """Move the block h[i:i+k] so that it starts at index p of the result."""
    block = list(h[i:i + k])
    rest = list(h[:i]) + list(h[i + k:])
    return rest[:p] + block + rest[p:]


def best_shift(h: Tokens, r: Tokens, d: int, herr: List[bool],
               rerr: List[bool]) -> Optional[Tuple[int, int, int, int]]:
    """Return (gain, k, i, p) of the best shift with gain >= 1, or None."""
    n, m = len(h), len(r)
    best = None
    for i in range(n):
        for k in range(1, n - i + 1):
            if not any(herr[i:i + k]):  # @line L6
                continue
            block = list(h[i:i + k])
            if not any(block == list(r[j:j + k]) and any(rerr[j:j + k]) for j in range(m - k + 1)):
                continue
            for p in range(n - k + 1):
                if p == i:
                    continue
                d2, _, _ = edit_distance_errors(shift(h, i, k, p), r)  # @line L7
                key = (d - d2, k, -i, -p)
                if best is None or key > best:  # @line L8
                    best = key
    if best is None or best[0] < 1:  # @line L9
        return None
    return best[0], best[1], -best[2], -best[3]


def ter_edits(h: Tokens, r: Tokens) -> Tuple[int, int, List[str]]:
    """Return (edits, shifts, shifted hypothesis) against one reference."""
    cur = list(h)
    s = 0  # @line L3
    d, herr, rerr = edit_distance_errors(cur, r)  # @line L4
    while True:  # @line L5
        found = best_shift(cur, r, d, herr, rerr)
        if found is None:
            break
        _, k, i, p = found
        cur = shift(cur, i, k, p)  # @line L10
        s += 1
        d, herr, rerr = edit_distance_errors(cur, r)  # @line L11
    return s + d, s, cur


def ter_stats(h: Tokens, refs: Sequence[Tokens]) -> Tuple[int, float]:
    """Return (the fewest greedy edits over the references, the mean reference length)."""
    if not refs:
        raise ValueError("each hypothesis needs at least one reference")
    best = None  # @line L1
    for r in refs:  # @line L2
        e, _, _ = ter_edits(h, r)
        best = e if best is None else min(best, e)  # @line L12
    mean_len = sum(len(r) for r in refs) / len(refs)  # @line L13
    return best, mean_len


def ratio(edits: float, length: float) -> float:
    """Return edits / length, with 0/0 = 0 and e/0 = 1 for e > 0, as in sacreBLEU."""
    if length == 0:  # @line L14
        return 0.0 if edits == 0 else 1.0
    return edits / length  # @line L15


def sentence_ter(h: Tokens, refs: Sequence[Tokens]) -> float:
    """Return the TER of one hypothesis. Lower is better; it can exceed 1."""
    e, ell = ter_stats(h, refs)
    return ratio(e, ell)


def corpus_ter(hyps: Sequence[Tokens], refs: Sequence[Sequence[Tokens]]) -> float:
    """Return the corpus TER: the summed edits over the summed mean reference lengths."""
    if len(hyps) != len(refs):
        raise ValueError("one list of references per hypothesis")
    total_e, total_len = 0, 0.0
    for h, rs in zip(hyps, refs):
        e, ell = ter_stats(h, rs)
        total_e += e
        total_len += ell
    return ratio(total_e, total_len)
