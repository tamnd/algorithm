# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bitap-algorithm/. The authors are listed in prov/F82Z8Y.jsonl.

"""Bitap (shift-add) search for a pattern with at most k mismatches.

Edit model: Hamming distance (substitutions only, no insertions, deletions
or transpositions). Indices are 0-based. The result is the sorted list of
start positions i in 0..len(text)-len(pattern) such that the window
text[i:i+m] differs from the pattern in at most k positions. An empty
pattern matches at every i in 0..len(text).

Python integers have no fixed width, so the state vector is one integer of
m * B bits, where B = ceil(log2(k + 1)) + 1.
"""


def field_width(k: int) -> int:
    """Return B, the least width with 2**(B-1) >= k + 1."""
    return (k).bit_length() + 1


def bitap_mismatches(pattern: str, text: str, k: int) -> list[int]:
    """Return the start positions of the windows with at most k mismatches.

    Precondition: k >= 0. Cost: O(len(text) + len(pattern) * sigma) word
    operations on vectors of len(pattern) * B bits, where sigma is the number
    of distinct characters of the pattern.
    """
    if k < 0:
        raise ValueError("k must be at least 0")
    m, n = len(pattern), len(text)
    if m == 0:
        return list(range(n + 1))
    b = field_width(k)  # @line L1
    full = (1 << (m * b)) - 1
    high = 0
    for i in range(m):
        high |= 1 << (i * b + b - 1)
    ones = 0
    for i in range(m):
        ones |= 1 << (i * b)
    table: dict[str, int] = {}  # @line L2
    for i, c in enumerate(pattern):
        table.setdefault(c, ones)
    for c in table:
        for i in range(m):
            if pattern[i] == c:
                table[c] &= ~(1 << (i * b))
    shift_last = (m - 1) * b
    field_mask = (1 << b) - 1
    state = 0  # @line L3
    over = 0
    starts: list[int] = []
    for j in range(n):  # @line L4
        state = ((state << b) + table.get(text[j], ones)) & full  # @line L5
        over = ((over << b) | (state & high)) & full  # @line L6
        state &= ~high  # @line L7
        if j >= m - 1 and ((state | over) >> shift_last) & field_mask <= k:  # @line L8
            starts.append(j - m + 1)
    return starts


def mismatch_fields(pattern: str, text: str, k: int) -> list[list[int | None]]:
    """Return, after each text character, the decoded field of each prefix.

    Entry [j][i] is the mismatch count of pattern[0..i] against text[j-i..j],
    or None when the overflow bit says the count is at least 2**(B-1). Only
    fields with i <= j are meaningful; the others are None. For examples.
    """
    m = len(pattern)
    b = field_width(k)
    full = (1 << (m * b)) - 1
    high = sum(1 << (i * b + b - 1) for i in range(m))
    ones = sum(1 << (i * b) for i in range(m))
    state = over = 0
    rows: list[list[int | None]] = []
    for j, t in enumerate(text):
        vec = ones
        for i in range(m):
            if pattern[i] == t:
                vec &= ~(1 << (i * b))
        state = ((state << b) + vec) & full
        over = ((over << b) | (state & high)) & full
        state &= ~high
        row: list[int | None] = []
        for i in range(m):
            if i > j or (over >> (i * b)) & ((1 << b) - 1):
                row.append(None)
            else:
                row.append((state >> (i * b)) & ((1 << b) - 1))
        rows.append(row)
    return rows
