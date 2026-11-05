# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shift-or/. The authors are listed in prov/D9WFTK.jsonl.

from collections.abc import Hashable, Sequence


def shift_or_masks(pattern: Sequence[Hashable]) -> tuple[dict, int]:
    """B[c] has bit j cleared exactly when pattern[j] == c; absent characters use all ones."""
    m = len(pattern)
    ones = (1 << m) - 1
    masks = {}  # @line L3
    for j, c in enumerate(pattern):  # @line L4
        masks[c] = masks.get(c, ones) & ~(1 << j)
    return masks, ones


def shift_or(text: Sequence[Hashable], pattern: Sequence[Hashable]) -> list[int]:
    """All shifts s with text[s:s+m] == pattern, in increasing order.

    Python integers have no fixed width, so one integer plays the role of the
    ceil(m / w) machine words of the analysis.
    """
    n, m = len(text), len(pattern)  # @line L1
    if m == 0:  # @line L2
        return list(range(n + 1))
    masks, ones = shift_or_masks(pattern)
    top = 1 << (m - 1)
    state = ones  # @line L5
    out = []
    for i in range(n):  # @line L6
        state = ((state << 1) | masks.get(text[i], ones)) & ones  # @line L7
        if not state & top:  # @line L8
            out.append(i - m + 1)
    return out
