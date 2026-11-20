# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-median-voter-rule/. The authors are listed in prov/N9KT39.jsonl.
"""Moulin's generalized median voter rules on a line of m candidates.

The candidates are the points 0, ..., m - 1 of the axis, in this order. Each voter reports a
peak. The rule adds a fixed list of phantom peaks and returns the median of all the values.
With n voters, Moulin's rules use n + 1 phantoms (2n + 1 values in all); the rules that are
also Pareto efficient use n - 1 phantoms (2n - 1 values). Any odd total is accepted.
"""

from typing import Sequence


def generalized_median(peaks: Sequence[int], phantoms: Sequence[int], m: int) -> int:
    """Return the median of the peaks and the phantoms, all in 0, ..., m - 1.

    The number of values len(peaks) + len(phantoms) must be odd. Counting sort: O(n + m).
    """
    total = len(peaks) + len(phantoms)
    if total % 2 == 0:
        raise ValueError("the number of peaks and phantoms together must be odd")
    cnt = [0] * m  # @line L1
    for p in peaks:  # @line L2
        cnt[p] += 1
    for a in phantoms:  # @line L3
        cnt[a] += 1
    need = (total + 1) // 2  # @line L4
    seen = 0
    for x in range(m):  # @line L5
        seen += cnt[x]
        if seen >= need:
            return x  # @line L6
    raise AssertionError("unreachable")


def median_rule(phantoms: Sequence[int]):
    """Return the voting rule rule(profile, m) that applies the phantoms to the voters' tops.

    The profile is a sequence of rankings, best first, so the peak of voter i is profile[i][0].
    """

    def rule(profile, m):
        return generalized_median([r[0] for r in profile], phantoms, m)

    return rule


def plain_median_phantoms(n: int, m: int) -> list:
    """Phantoms that make the rule the median of the peaks for odd n, the lower median for even n.

    Half of the n + 1 phantoms (rounded up) sit at 0 and the rest at m - 1.
    """
    low = (n + 2) // 2
    return [0] * low + [m - 1] * (n + 1 - low)
