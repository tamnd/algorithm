# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/patience-diff/. The authors are listed in prov/3MB06K.jsonl.
"""Patience diff, after the four steps of Bram Cohen's description (2010).

The old file is a and the new file is b. A range of the problem is a pair of
half-open slices a[alo:ahi] and b[blo:bhi]. In each range the method matches
equal first lines, then equal last lines, then the lines that occur exactly once
in each side of the range, keeping a longest increasing subset of those, and it
runs again in each gap between two kept lines. If a range has no unique common
line, the fallback decides: None leaves the range unmatched, and "lcs" matches it
with the dynamic program of the shared helper, as Git falls back to Myers' method.
"""

from bisect import bisect_left
from collections.abc import Hashable, Sequence

from txdiff import Op, lcs_matching, matching_to_script


def longest_increasing(pairs: Sequence[tuple[int, int]]) -> list[tuple[int, int]]:
    """Return a longest subsequence of pairs whose second coordinates increase, by patience sorting.

    The pairs are sorted by their first coordinate, and the second coordinates are distinct.
    Each pair goes on the leftmost pile whose top is larger, and keeps a link to the top
    of the pile on its left; the links from the top of the last pile give the result.
    """
    tops: list[int] = []
    top_index: list[int] = []
    back = [-1] * len(pairs)
    for t, (_, j) in enumerate(pairs):
        p = bisect_left(tops, j)
        back[t] = top_index[p - 1] if p > 0 else -1
        if p == len(tops):
            tops.append(j)
            top_index.append(t)
        else:
            tops[p] = j
            top_index[p] = t
    out: list[tuple[int, int]] = []
    t = top_index[-1] if top_index else -1
    while t >= 0:
        out.append(pairs[t])
        t = back[t]
    out.reverse()
    return out


def unique_common(a: Sequence[Hashable], b: Sequence[Hashable],
                  alo: int, ahi: int, blo: int, bhi: int) -> list[tuple[int, int]]:
    """Return the pairs (i, j), sorted by i, of lines that occur once in a[alo:ahi] and once in b[blo:bhi]."""
    where: dict[Hashable, list[int]] = {}  # line -> [count in a, index in a, count in b, index in b]
    for i in range(alo, ahi):
        e = where.setdefault(a[i], [0, -1, 0, -1])
        e[0] += 1
        e[1] = i
    for j in range(blo, bhi):
        e = where.get(b[j])
        if e is not None:
            e[2] += 1
            e[3] = j
    return sorted((e[1], e[3]) for e in where.values() if e[0] == 1 and e[2] == 1)


def patience_matching(a: Sequence[Hashable], b: Sequence[Hashable],
                      fallback: str | None = None) -> list[tuple[int, int]]:
    """Return the matching (i, j) of patience diff, increasing in both coordinates."""
    if fallback not in (None, "lcs"):
        raise ValueError("fallback must be None or 'lcs'")
    pairs: list[tuple[int, int]] = []  # @line L1

    def match(alo: int, ahi: int, blo: int, bhi: int) -> None:
        while alo < ahi and blo < bhi and a[alo] == b[blo]:  # @line L2
            pairs.append((alo, blo))
            alo, blo = alo + 1, blo + 1
        tail: list[tuple[int, int]] = []
        while alo < ahi and blo < bhi and a[ahi - 1] == b[bhi - 1]:  # @line L3
            ahi, bhi = ahi - 1, bhi - 1
            tail.append((ahi, bhi))
        anchors = longest_increasing(unique_common(a, b, alo, ahi, blo, bhi))  # @line L4
        if not anchors:  # @line L5
            if fallback == "lcs" and alo < ahi and blo < bhi:
                pairs.extend((alo + i, blo + j) for i, j in lcs_matching(a[alo:ahi], b[blo:bhi]))
        else:
            for i, j in anchors:  # @line L6
                match(alo, i, blo, j)
                pairs.append((i, j))
                alo, blo = i + 1, j + 1
            match(alo, ahi, blo, bhi)
        pairs.extend(reversed(tail))  # @line L7

    match(0, len(a), 0, len(b))
    return pairs


def patience_diff(a: Sequence[Hashable], b: Sequence[Hashable], fallback: str | None = None) -> list[Op]:
    """Return the edit script from a to b that keeps the patience matching."""
    return matching_to_script(a, b, patience_matching(a, b, fallback))  # @line L8
