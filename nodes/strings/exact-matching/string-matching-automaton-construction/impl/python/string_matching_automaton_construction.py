# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/string-matching-automaton-construction/. The authors are listed in prov/HCTKVB.jsonl.

from collections.abc import Sequence


def compute_transition_function(pattern: Sequence[int], sigma: int) -> list[list[int]]:
    """delta[q][c] for states 0..m and characters 0..sigma-1 of an integer alphabet.

    delta[q][c] is the length of the longest prefix of pattern that is a suffix
    of pattern[:q] + [c].
    """
    m = len(pattern)  # @line L1
    delta = [[0] * sigma for _ in range(m + 1)]
    if m > 0:  # @line L2
        delta[0][pattern[0]] = 1
    x = 0  # @line L3
    for q in range(1, m + 1):  # @line L4
        row, lag = delta[q], delta[x]
        for c in range(sigma):  # @line L5
            row[c] = lag[c]  # @line L6
        if q < m:  # @line L7
            row[pattern[q]] = q + 1  # @line L8
            x = delta[x][pattern[q]]  # @line L9
    return delta  # @line L10


def compute_transition_function_naive(pattern: Sequence[int], sigma: int) -> list[list[int]]:
    """The direct method: try every k from min(m, q + 1) down; O(m^3 sigma) time."""
    m = len(pattern)
    p = list(pattern)
    delta = [[0] * sigma for _ in range(m + 1)]
    for q in range(m + 1):
        for c in range(sigma):
            w = p[:q] + [c]
            k = min(m, q + 1)
            while k > 0 and p[:k] != w[len(w) - k :]:
                k -= 1
            delta[q][c] = k
    return delta


def automaton_search(text: Sequence[int], pattern: Sequence[int], sigma: int) -> list[int]:
    """All shifts of pattern in text, both over the alphabet 0..sigma-1."""
    n, m = len(text), len(pattern)
    if m == 0:
        return list(range(n + 1))
    delta = compute_transition_function(pattern, sigma)
    q, out = 0, []
    for i, c in enumerate(text):
        q = delta[q][c]
        if q == m:
            out.append(i - m + 1)
    return out
