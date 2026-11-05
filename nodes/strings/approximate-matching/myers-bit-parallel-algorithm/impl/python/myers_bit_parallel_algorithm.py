# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/myers-bit-parallel-algorithm/. The authors are listed in prov/MXPHKN.jsonl.

"""Myers' bit-parallel algorithm for approximate string matching, in the form
given by Hyyrö.

Edit model: unit-cost insertion, deletion and substitution (Levenshtein),
no transpositions. Indices are 0-based. The result is the sorted list of end
positions j in 0..len(text) such that some substring text[h:j] has edit
distance at most k to the pattern.

Bit i - 1 of pv (of mv) is set when C[i][j] - C[i-1][j] is +1 (is -1), where C
is the Sellers table of the current column j.
"""


def myers(pattern: str, text: str, k: int) -> list[int]:
    """Return the end positions of the approximate matches of pattern in text.

    Precondition: k >= 0. Cost: O(n) operations on m-bit vectors.
    """
    return [j for j, score, _, _ in myers_columns(pattern, text) if score <= k]


def myers_columns(pattern: str, text: str) -> list[tuple[int, int, int, int]]:
    """Return (j, C[m][j], pv, mv) for each column j = 0..n."""
    m = len(pattern)
    if m == 0:
        return [(j, 0, 0, 0) for j in range(len(text) + 1)]
    full = (1 << m) - 1
    high = 1 << (m - 1)
    peq: dict[str, int] = {}  # @line L1
    for i, ch in enumerate(pattern):
        peq[ch] = peq.get(ch, 0) | (1 << i)
    pv, mv, score = full, 0, m  # @line L2
    out = [(0, score, pv, mv)]  # @line L3
    for j in range(1, len(text) + 1):  # @line L4
        eq = peq.get(text[j - 1], 0)  # @line L5
        xv = eq | mv
        xh = ((((eq & pv) + pv) & full) ^ pv) | eq  # @line L6
        ph = mv | (~(xh | pv) & full)  # @line L7
        mh = pv & xh
        if ph & high:  # @line L8
            score += 1
        elif mh & high:
            score -= 1
        ph = (ph << 1) & full  # @line L9
        mh = (mh << 1) & full
        pv = mh | (~(xv | ph) & full)  # @line L10
        mv = ph & xv
        out.append((j, score, pv, mv))  # @line L11
    return out


def edit_distance(a: str, b: str) -> int:
    """Return the Levenshtein distance of a and b with the same vectors, where
    the first row of the table is C[0][j] = j instead of 0."""
    m = len(a)
    if m == 0:
        return len(b)
    full = (1 << m) - 1
    high = 1 << (m - 1)
    peq: dict[str, int] = {}
    for i, ch in enumerate(a):
        peq[ch] = peq.get(ch, 0) | (1 << i)
    pv, mv, score = full, 0, m
    for ch in b:
        eq = peq.get(ch, 0)
        xv = eq | mv
        xh = ((((eq & pv) + pv) & full) ^ pv) | eq
        ph = mv | (~(xh | pv) & full)
        mh = pv & xh
        if ph & high:
            score += 1
        elif mh & high:
            score -= 1
        ph = ((ph << 1) | 1) & full  # row 0 grows by 1 in each column
        mh = (mh << 1) & full
        pv = mh | (~(xv | ph) & full)
        mv = ph & xv
    return score
