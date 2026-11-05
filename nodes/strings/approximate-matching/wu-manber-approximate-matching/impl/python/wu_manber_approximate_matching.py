# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wu-manber-approximate-matching/. The authors are listed in prov/QT4WGM.jsonl.

"""The Wu-Manber bit-parallel algorithm for approximate string matching.

Edit model: unit-cost insertion, deletion and substitution (Levenshtein),
no transpositions. Indices are 0-based. The result is the sorted list of end
positions j in 0..len(text) such that some substring text[h:j] has edit
distance at most k to the pattern.

Bit i - 1 of the vector R[e] (for 1 <= i <= m) is set after column j when the
pattern prefix of length i matches a substring that ends at j with at most e
errors. This is the shift-and form, with 1 for an active state.
"""


def wu_manber(pattern: str, text: str, k: int) -> list[int]:
    """Return the end positions of the approximate matches of pattern in text.

    Precondition: k >= 0. Cost: O((k + 1) n) operations on m-bit vectors,
    O(sigma + k) vectors of extra space.
    """
    return [j for j, _ in wu_manber_states(pattern, text, k) if j >= 0]


def wu_manber_states(pattern: str, text: str, k: int) -> list[tuple[int, list[int]]]:
    """Return, for each column j = 0..n, the pair (j or -1, [R[0], ..., R[k]]),
    where j marks a reported end and -1 a column without a match."""
    if k < 0:
        raise ValueError("k must be at least 0")
    m = len(pattern)
    full = (1 << m) - 1
    high = 1 << (m - 1) if m > 0 else 0
    masks: dict[str, int] = {}  # @line L1
    for i, ch in enumerate(pattern):
        masks[ch] = masks.get(ch, 0) | (1 << i)
    r = [(1 << min(e, m)) - 1 for e in range(k + 1)]  # @line L2
    hit = m == 0 or (r[k] & high) != 0  # @line L3
    out = [(0 if hit else -1, r[:])]
    for j in range(1, len(text) + 1):  # @line L4
        b = masks.get(text[j - 1], 0)
        old = r[0]
        r[0] = ((old << 1) | 1) & b  # @line L5
        for e in range(1, k + 1):  # @line L6
            prev_old = old
            old = r[e]
            r[e] = ((((old << 1) | 1) & b)  # @line L7
                    | (prev_old << 1) | 1 | prev_old | (r[e - 1] << 1)) & full
        hit = m == 0 or (r[k] & high) != 0  # @line L8
        out.append((j if hit else -1, r[:]))
    return out
