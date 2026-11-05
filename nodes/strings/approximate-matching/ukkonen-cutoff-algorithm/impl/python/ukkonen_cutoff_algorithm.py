# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ukkonen-cutoff-algorithm/. The authors are listed in prov/V58QHM.jsonl.

"""Ukkonen's cut-off algorithm: Sellers' dynamic program restricted to the
active cells, the cells with a value at most k.

Edit model: unit-cost insertion, deletion and substitution (Levenshtein),
no transpositions. Indices are 0-based. The result is the sorted list of end
positions j in 0..len(text) such that some substring text[h:j] has edit
distance at most k to the pattern.
"""


def ukkonen_cutoff(pattern: str, text: str, k: int) -> list[int]:
    """Return the end positions of the approximate matches of pattern in text.

    Precondition: k >= 0. Cost: O(m n) time in the worst case, O(k n) expected
    time on random text, O(m) extra space.
    """
    return ukkonen_cutoff_trace(pattern, text, k)[0]


def ukkonen_cutoff_trace(pattern: str, text: str, k: int) -> tuple[list[int], list[int], int]:
    """Return (ends, lact, cells): the end positions, the last active row of
    each column j = 0..n, and the number of cells computed."""
    if k < 0:
        raise ValueError("k must be at least 0")
    m = len(pattern)
    col = list(range(m + 1))  # @line L1
    lact = min(k, m)  # @line L2
    ends = [0] if lact == m else []  # @line L3
    trace = [lact]
    cells = 0
    for j in range(1, len(text) + 1):  # @line L4
        t = text[j - 1]
        top = min(lact + 1, m)  # @line L5
        prev = col[0]  # @line L6
        for i in range(1, top + 1):  # @line L7
            c = 0 if pattern[i - 1] == t else 1
            new = min(col[i] + 1, col[i - 1] + 1, prev + c)  # @line L8
            prev, col[i] = col[i], new
        cells += top
        lact = top  # @line L9
        while col[lact] > k:
            lact -= 1
        if lact == m:  # @line L10
            ends.append(j)
        else:
            col[lact + 1] = k + 1  # @line L11
        trace.append(lact)
    return ends, trace, cells
