# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/histogram-diff/. The authors are listed in prov/BNZ7EN.jsonl.
"""Histogram diff, after the rules of the HistogramDiff class of JGit.

The old file is a and the new file is b. The common start and end of the two
files are matched first, once. In each remaining range the method counts how
often each line occurs in the old side, scans the new side, and grows each
match of a line to the longest run of equal lines around it. It keeps the run
whose rarest line has the lowest count, and among those the longest one, and it
runs again before and after that run. Lines that occur more than max_chain times
in the old side are not used; if the range then has common lines but no usable
run, the fallback matches it. JGit uses Myers' method there. This file uses the
dynamic program of the shared helper, or nothing when fallback is None.
"""

from collections.abc import Hashable, Sequence

from txdiff import Op, lcs_matching, matching_to_script

Region = tuple[int, int, int, int]  # (as, ae, bs, be): a[as:ae] == b[bs:be]


def best_region(a: Sequence[Hashable], b: Sequence[Hashable], alo: int, ahi: int, blo: int, bhi: int,
                max_chain: int = 64) -> Region | None:
    """Return the run chosen in a[alo:ahi] and b[blo:bhi], an empty run if no line is common, or None.

    None means that common lines exist, but each of them occurs more than max_chain times in a[alo:ahi].
    """
    where: dict[Hashable, list[int]] = {}  # @line L4
    for i in range(alo, ahi):
        where.setdefault(a[i], []).append(i)
    best: Region = (alo, alo, blo, blo)
    cnt = max_chain + 1  # @line L5
    has_common = False
    j = blo
    while j < bhi:  # @line L6
        j_next = j + 1
        places = where.get(b[j])
        if places is not None:
            has_common = True
            if len(places) <= cnt:  # @line L7
                k = 0
                while k < len(places):
                    as_, bs, ae, be = places[k], j, places[k] + 1, j + 1  # @line L8
                    rc = len(places)
                    while as_ > alo and bs > blo and a[as_ - 1] == b[bs - 1]:
                        as_, bs = as_ - 1, bs - 1
                        rc = min(rc, len(where[a[as_]]))
                    while ae < ahi and be < bhi and a[ae] == b[be]:
                        rc = min(rc, len(where[a[ae]]))
                        ae, be = ae + 1, be + 1
                    j_next = max(j_next, be)  # @line L9
                    if best[1] - best[0] < ae - as_ or rc < cnt:  # @line L10
                        best, cnt = (as_, ae, bs, be), rc
                    while k < len(places) and places[k] <= ae:  # copies up to the end of the run are skipped, as in JGit
                        k += 1
        j = j_next
    if has_common and cnt > max_chain:  # @line L11
        return None
    return best


def histogram_matching(a: Sequence[Hashable], b: Sequence[Hashable], max_chain: int = 64,
                       fallback: str | None = "lcs") -> list[tuple[int, int]]:
    """Return the matching (i, j) of histogram diff, increasing in both coordinates."""
    if fallback not in (None, "lcs"):
        raise ValueError("fallback must be None or 'lcs'")
    n, m = len(a), len(b)
    head = 0
    while head < n and head < m and a[head] == b[head]:  # @line L1
        head += 1
    tail = 0
    while tail < n - head and tail < m - head and a[n - 1 - tail] == b[m - 1 - tail]:
        tail += 1
    pairs = [(t, t) for t in range(head)]

    def match(alo: int, ahi: int, blo: int, bhi: int) -> None:
        if alo == ahi or blo == bhi:  # @line L3
            return
        region = best_region(a, b, alo, ahi, blo, bhi, max_chain)
        if region is None:  # @line L12
            if fallback == "lcs":
                pairs.extend((alo + i, blo + j) for i, j in lcs_matching(a[alo:ahi], b[blo:bhi]))
            return
        as_, ae, bs, be = region
        if as_ == ae:  # @line L13
            return
        match(alo, as_, blo, bs)  # @line L14
        pairs.extend((as_ + t, bs + t) for t in range(ae - as_))
        match(ae, ahi, be, bhi)

    match(head, n - tail, head, m - tail)  # @line L2
    pairs.extend((n - tail + t, m - tail + t) for t in range(tail))
    return pairs


def histogram_diff(a: Sequence[Hashable], b: Sequence[Hashable], max_chain: int = 64,
                   fallback: str | None = "lcs") -> list[Op]:
    """Return the edit script from a to b that keeps the histogram matching."""
    return matching_to_script(a, b, histogram_matching(a, b, max_chain, fallback))  # @line L15
