# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/booth-algorithm/. The authors are listed in prov/PTQRP5.jsonl.

from typing import Sequence, TypeVar

T = TypeVar("T")


def least_rotation(s: Sequence[T]) -> int:
    """Return the least k such that s[k:] + s[:k] is the least rotation of s.

    Precondition: the items of s are totally ordered by < and ==.
    Indices are 0-based; the empty sequence gives 0.
    Cost: O(n) time and O(n) extra space, at most 8n comparisons.
    """
    n = len(s)
    if n == 0:
        return 0
    # @line L1
    t = list(s) + list(s)
    f = [-1] * (2 * n)
    k = 0
    # @line L2
    for j in range(1, 2 * n):
        # @line L3
        c = t[j]
        i = f[j - k - 1]
        # @line L4
        while i != -1 and c != t[k + i + 1]:
            # @line L5
            if c < t[k + i + 1]:
                k = j - i - 1
            # @line L6
            i = f[i]
        # @line L7
        if i == -1 and c != t[k]:
            # @line L8
            if c < t[k]:
                k = j
            # @line L9
            f[j - k] = -1
        else:
            # @line L10
            f[j - k] = i + 1
    # @line L11
    return k
