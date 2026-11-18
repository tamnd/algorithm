# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/heckel-diff/. The authors are listed in prov/T7BYC1.jsonl.
"""Heckel's six-pass difference method (CACM 21(4), 1978).

The old file is a, the new file is b. Heckel calls them O and N. The arrays OA
and NA hold, for each line, either a symbol table entry or the number of the
line that it is linked to in the other file. Index 0 and the index after the
last line are the begin and end lines that the paper adds to both files.
Lines are numbered from 1 inside heckel_links, as in the paper, and the
results use 0-based indices.
"""

from bisect import bisect_left
from collections.abc import Hashable, Sequence

from txdiff import Op, matching_to_script


class _Entry:
    """A symbol table entry: the counts OC and NC and the old line number OLNO."""

    __slots__ = ("oc", "nc", "olno")

    def __init__(self) -> None:
        self.oc = 0
        self.nc = 0
        self.olno = 0


def _same_entry(x: object, y: object) -> bool:
    return isinstance(x, _Entry) and x is y


def heckel_links(a: Sequence[Hashable], b: Sequence[Hashable]) -> list[tuple[int, int]]:
    """Return the linked pairs (i, j) with a[i] == b[j], 0-based, sorted by j. The pairs may cross."""
    m, n = len(a), len(b)
    table: dict[Hashable, _Entry] = {}  # @line L1
    na: list[object] = [None] * (n + 2)
    oa: list[object] = [None] * (m + 2)
    for i in range(1, n + 1):  # @line L2
        entry = table.setdefault(b[i - 1], _Entry())
        entry.nc += 1
        na[i] = entry
    for j in range(1, m + 1):  # @line L3
        entry = table.setdefault(a[j - 1], _Entry())
        entry.oc += 1
        entry.olno = j
        oa[j] = entry
    na[0], oa[0], na[n + 1], oa[m + 1] = 0, 0, m + 1, n + 1  # @line L4
    for i in range(1, n + 1):  # @line L5
        entry = na[i]
        if isinstance(entry, _Entry) and entry.nc == 1 and entry.oc == 1:
            j = entry.olno
            na[i], oa[j] = j, i
    for i in range(0, n + 1):  # @line L6
        j = na[i]
        if isinstance(j, int) and _same_entry(na[i + 1], oa[j + 1]):
            na[i + 1], oa[j + 1] = j + 1, i + 1
    for i in range(n + 1, 0, -1):  # @line L7
        j = na[i]
        if isinstance(j, int) and j >= 1 and _same_entry(na[i - 1], oa[j - 1]):
            na[i - 1], oa[j - 1] = j - 1, i - 1
    links: list[tuple[int, int]] = []
    for i in range(1, n + 1):  # @line L8
        j = na[i]
        if isinstance(j, int):
            links.append((j - 1, i - 1))
    return links


def increasing_pairs(links: Sequence[tuple[int, int]]) -> list[tuple[int, int]]:
    """Return a longest subset of the links that is increasing in both coordinates.

    The links are sorted by their second coordinate, and their first coordinates are
    distinct, so this is a longest increasing subsequence of the first coordinates,
    found with patience piles in O(r log r) time.
    """
    tops: list[int] = []  # the first coordinate on top of each pile
    top_index: list[int] = []  # the index in links of that top
    back: list[int] = [-1] * len(links)
    for t, (i, _) in enumerate(links):
        p = bisect_left(tops, i)
        back[t] = top_index[p - 1] if p > 0 else -1
        if p == len(tops):
            tops.append(i)
            top_index.append(t)
        else:
            tops[p] = i
            top_index[p] = t
    out: list[tuple[int, int]] = []
    t = top_index[-1] if top_index else -1
    while t >= 0:
        out.append(links[t])
        t = back[t]
    out.reverse()
    return out


def moved_blocks(links: Sequence[tuple[int, int]],
                 kept: Sequence[tuple[int, int]]) -> list[tuple[int, int, int]]:
    """Group the links that are not kept into blocks (i, j, length) of consecutive lines."""
    keep = set(kept)
    blocks: list[tuple[int, int, int]] = []
    for i, j in links:
        if (i, j) in keep:
            continue
        if blocks:
            bi, bj, length = blocks[-1]
            if bi + length == i and bj + length == j:
                blocks[-1] = (bi, bj, length + 1)
                continue
        blocks.append((i, j, 1))
    return blocks


def heckel_diff(a: Sequence[Hashable], b: Sequence[Hashable]) -> tuple[list[Op], list[tuple[int, int, int]]]:
    """Return an edit script from a to b and the moved blocks (i, j, length) that it shows as delete and insert."""
    links = heckel_links(a, b)
    kept = increasing_pairs(links)  # @line L9
    return matching_to_script(a, b, kept), moved_blocks(links, kept)  # @line L10
