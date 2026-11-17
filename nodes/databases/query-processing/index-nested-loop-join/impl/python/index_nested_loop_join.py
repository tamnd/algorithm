# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/index-nested-loop-join/. The authors are listed in prov/N97W1G.jsonl.

"""Index nested-loop join over a small page-and-buffer simulator.

A relation is a list of pages, and a page is a list of tuples. A record id
(rid) is the pair (page number, slot). The index on the inner S holds data
entries (key, rid), as in alternative 2 of Ramakrishnan and Gehrke. Each page
of the index and each data page that the join touches costs one read. The
cost is M + (sum over the tuples r of R of the cost of one probe), without
the writes of the output (Ramakrishnan and Gehrke, Section 14.4.1).
"""

from bisect import bisect_left
from typing import Optional, Sequence

Row = tuple
Page = list[Row]
Rid = tuple[int, int]


class Disk:
    """Counts page reads and page writes."""

    def __init__(self) -> None:
        self.reads = 0
        self.writes = 0

    def read(self, page):
        self.reads += 1
        return page

    @property
    def ios(self) -> int:
        return self.reads + self.writes


def paginate(rows: Sequence[Row], per_page: int) -> list[Page]:
    """Pack rows into pages of per_page rows. The last page can be partial."""
    if per_page < 1:
        raise ValueError("per_page must be at least 1")
    return [list(rows[i:i + per_page]) for i in range(0, len(rows), per_page)]


def _entries(s_pages: Sequence[Page], col: int) -> list[tuple[object, Rid]]:
    return [(row[col], (p, i)) for p, page in enumerate(s_pages) for i, row in enumerate(page)]


class HashIndex:
    """Static hash index: each bucket is a chain of pages of data entries.

    A probe reads every page of the chain of bucket hash(key) mod buckets.
    The chain of a bucket with c entries has max(1, ceil(c / per_page)) pages.
    """

    def __init__(self, s_pages: Sequence[Page], col: int, buckets: int, per_page: int) -> None:
        if buckets < 1 or per_page < 1:
            raise ValueError("buckets and per_page must be at least 1")
        self.buckets = buckets
        chains: list[list[tuple[object, Rid]]] = [[] for _ in range(buckets)]
        for key, rid in _entries(s_pages, col):
            chains[hash(key) % buckets].append((key, rid))
        self.chains = [[c[i:i + per_page] for i in range(0, len(c), per_page)] or [[]] for c in chains]

    def probe(self, key, disk: Disk) -> list[Rid]:
        rids: list[Rid] = []
        for page in self.chains[hash(key) % self.buckets]:
            rids.extend(rid for k, rid in disk.read(page) if k == key)
        return rids


class _Leaf:
    __slots__ = ("entries", "next", "high")

    def __init__(self, entries) -> None:
        self.entries = entries
        self.next: Optional["_Leaf"] = None
        self.high = None  # smallest key of the next leaf (a fence key), or None


class _Inner:
    __slots__ = ("children", "maxkeys")

    def __init__(self, children, maxkeys) -> None:
        self.children = children
        self.maxkeys = maxkeys


def _max_key(node):
    while isinstance(node, _Inner):
        node = node.children[-1]
    return node.entries[-1][0]


class BPlusTreeIndex:
    """Bulk-loaded B+ tree on (key, rid) data entries.

    Each inner node keeps, for each child, the largest key below it, so the
    descent to the first child whose largest key is at least the search key
    reaches the leftmost leaf that can hold the key. Each leaf keeps the
    smallest key of the next leaf, so the scan reads exactly the leaves that
    hold the key. A probe costs h + max(1, leaves holding the key) reads,
    where h is the number of inner levels (h = 0 for a one-leaf tree).
    """

    def __init__(self, s_pages: Sequence[Page], col: int, leaf_size: int, fanout: int) -> None:
        if leaf_size < 1 or fanout < 2:
            raise ValueError("leaf_size >= 1 and fanout >= 2 are required")
        entries = sorted(_entries(s_pages, col))
        leaves = [_Leaf(entries[i:i + leaf_size]) for i in range(0, len(entries), leaf_size)]
        if not leaves:
            leaves = [_Leaf([])]
        for a, b in zip(leaves, leaves[1:]):
            a.next, a.high = b, b.entries[0][0]
        level: list = leaves
        self.height = 0
        while len(level) > 1:
            groups = [level[i:i + fanout] for i in range(0, len(level), fanout)]
            level = [_Inner(g, [_max_key(c) for c in g]) for g in groups]
            self.height += 1
        self.root = level[0]

    def probe(self, key, disk: Disk) -> list[Rid]:
        node = disk.read(self.root)
        while isinstance(node, _Inner):
            i = bisect_left(node.maxkeys, key)
            if i == len(node.maxkeys):
                return []
            node = disk.read(node.children[i])
        rids: list[Rid] = []
        leaf = node
        while True:
            rids.extend(rid for k, rid in leaf.entries if k == key)
            if leaf.high is None or leaf.high != key:
                return rids
            leaf = disk.read(leaf.next)


def index_nested_loop_join(r_pages: Sequence[Page], s_pages: Sequence[Page], r_col: int,
                           index, clustered: bool = False) -> tuple[list[Row], Disk]:
    """Join R (outer) with S (inner) on r[r_col] == key of the index on S.

    For each tuple r of R, probe the index with r[r_col], then fetch the
    matching tuples of S. Clustered: S is sorted on the key, the matches of a
    probe lie on consecutive pages, and each such page costs one read.
    Unclustered: each match costs one read. Total cost: M + sum of the probes.
    """
    disk = Disk()
    out: list[Row] = []  # @line L1
    for r_page in r_pages:  # @line L2
        page = disk.read(r_page)  # @line L3
        for r in page:  # @line L4
            last = None
            rids = index.probe(r[r_col], disk)  # @line L5
            for p, i in rids:  # @line L6
                if not clustered or p != last:  # @line L7
                    disk.read(s_pages[p])  # @line L8
                    last = p
                out.append(r + s_pages[p][i])  # @line L9
    return out, disk  # @line L10
