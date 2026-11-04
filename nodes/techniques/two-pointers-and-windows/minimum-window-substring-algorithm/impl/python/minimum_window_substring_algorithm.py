# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimum-window-substring-algorithm/. The authors are listed in prov/380AMB.jsonl.

from collections import Counter


def min_window(s: str, t: str) -> str:
    """Return the leftmost shortest substring of s that contains every character of t
    with at least its multiplicity in t, or "" if there is none (or if t is empty).

    Cost: O(len(s) + len(t)) expected time, O(len(t)) extra space.
    """
    if not t:
        return ""
    need = Counter(t)  # @line L1
    missing = len(t)
    left = 0
    best_len, best_start = len(s) + 1, 0
    for r, c in enumerate(s):  # @line L2
        if need[c] > 0:  # @line L3
            missing -= 1
        need[c] -= 1  # @line L4
        while missing == 0:  # @line L5
            if r - left + 1 < best_len:  # @line L6
                best_len, best_start = r - left + 1, left
            need[s[left]] += 1  # @line L7
            if need[s[left]] > 0:  # @line L8
                missing += 1
            left += 1  # @line L9
    if best_len > len(s):  # @line L10
        return ""
    return s[best_start : best_start + best_len]
