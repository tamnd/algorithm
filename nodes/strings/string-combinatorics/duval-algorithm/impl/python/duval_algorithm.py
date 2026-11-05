# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/duval-algorithm/. The authors are listed in prov/2134ZX.jsonl.

from typing import List, Sequence, TypeVar

T = TypeVar("T")


def duval(s: Sequence[T]) -> List[int]:
    """Return the start indices of the Lyndon factorization of s.

    Precondition: the items of s are totally ordered by < and ==.
    Indices are 0-based; factor r is s[F[r]:F[r + 1]], with F[k] = len(s).
    Cost: O(n) time, at most 2n - 1 three-way comparisons, O(1) extra
    space besides the output.
    """
    n = len(s)
    # @line L1
    i = 0
    starts: List[int] = []
    # @line L2
    while i < n:
        # @line L3
        j, k = i + 1, i
        # @line L4
        while j < n and s[k] <= s[j]:
            # @line L5
            if s[k] < s[j]:
                k = i
            else:
                k += 1
            # @line L6
            j += 1
        # @line L7
        while i <= k:
            # @line L8
            starts.append(i)
            # @line L9
            i += j - k
    # @line L10
    return starts


def lyndon_factors(s: Sequence[T]) -> List[Sequence[T]]:
    """Return the factors of the Lyndon factorization of s as slices."""
    b = duval(s) + [len(s)]
    return [s[b[r] : b[r + 1]] for r in range(len(b) - 1)]
