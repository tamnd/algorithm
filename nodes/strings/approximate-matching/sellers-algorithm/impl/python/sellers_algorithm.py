# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sellers-algorithm/. The authors are listed in prov/TZXPTF.jsonl.

"""Sellers' dynamic program for approximate string matching.

Edit model: unit-cost insertion, deletion and substitution (Levenshtein),
no transpositions. Indices are 0-based. The result is the sorted list of end
positions j in 0..len(text) such that some substring text[i:j] has edit
distance at most k to the pattern.
"""


def sellers(pattern: str, text: str, k: int) -> list[int]:
    """Return the end positions of the approximate matches of pattern in text.

    Precondition: k >= 0. Cost: Theta(len(pattern) * len(text)) time and
    O(len(pattern)) extra space.
    """
    if k < 0:
        raise ValueError("k must be at least 0")
    m = len(pattern)
    col = list(range(m + 1))  # @line L1
    ends = [0] if col[m] <= k else []  # @line L2
    for j in range(1, len(text) + 1):  # @line L3
        t = text[j - 1]
        prev = col[0]  # @line L4
        col[0] = 0
        for i in range(1, m + 1):  # @line L5
            c = 0 if pattern[i - 1] == t else 1  # @line L6
            new = min(col[i] + 1, col[i - 1] + 1, prev + c)  # @line L7
            prev, col[i] = col[i], new  # @line L8
        if col[m] <= k:  # @line L9
            ends.append(j)
    return ends


def last_row(pattern: str, text: str) -> list[int]:
    """Return C[m][j] for j = 0..len(text): the least edit distance between the
    pattern and a substring of text that ends at j. Cost: Theta(mn)."""
    m = len(pattern)
    col = list(range(m + 1))
    row = [col[m]]
    for t in text:
        prev, col[0] = col[0], 0
        for i in range(1, m + 1):
            new = min(col[i] + 1, col[i - 1] + 1, prev + (pattern[i - 1] != t))
            prev, col[i] = col[i], new
        row.append(col[m])
    return row
