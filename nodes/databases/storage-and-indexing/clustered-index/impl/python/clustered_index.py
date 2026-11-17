# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clustered-index/. The authors are listed in prov/KP39G2.jsonl.

"""A page simulator for range queries through a clustered or an unclustered index.

The table holds the keys 0..n-1, p tuples per data page. A layout maps each
key to its data page. The index is a B+ tree on the key with f entries per
leaf and fanout f above the leaves; its leaves are in key order whatever the
layout of the data. A range query reads the internal nodes on the path to the
first leaf, the leaves that hold the matching entries, and the data pages of
the matching tuples, with one buffer frame for data pages. It counts I/Os.
"""

import random
from fractions import Fraction
from math import comb
from typing import List, Tuple


def layout_clustered(n: int, p: int) -> List[int]:
    """Key k on page k // p: the data file is in key order."""
    return [k // p for k in range(n)]


def layout_striped(n: int, p: int) -> List[int]:
    """Key k on page k mod (n / p): consecutive keys are on different pages."""
    m = -(-n // p)
    return [k % m for k in range(n)]


def layout_random(n: int, p: int, seed: int) -> List[int]:
    """A heap file in random order: the pages hold a random permutation of the keys."""
    order = list(range(n))
    random.Random(seed).shuffle(order)
    page = [0] * n
    for slot, k in enumerate(order):
        page[k] = slot // p
    return page


class IndexedTable:
    def __init__(self, page_of: List[int], f: int) -> None:
        if f < 2:
            raise ValueError("f must be at least 2")
        self.page_of = page_of
        self.n = len(page_of)
        self.f = f
        self.pages = (max(page_of) + 1) if page_of else 0
        leaves = max(1, -(-self.n // f))
        h, width = 1, leaves
        while width > 1:
            width = -(-width // f)
            h += 1
        self.height = h            # levels of the index, leaves included

    def range_query(self, lo: int, hi: int, sort_rids: bool = False) -> Tuple[List[int], int, int]:
        """Keys in [lo, hi], index I/Os, data I/Os."""
        lo, hi = max(lo, 0), min(hi, self.n - 1)
        if lo > hi:
            return [], self.height, 0
        index_io = self.height - 1                                         # @line L1
        index_io += hi // self.f - lo // self.f + 1                        # @line L2
        keys = list(range(lo, hi + 1))                                     # @line L2
        if sort_rids:
            data_io = len({self.page_of[k] for k in keys})                 # @line L7
            return keys, index_io, data_io
        data_io, frame = 0, None
        for k in keys:                                                     # @line L3
            page = self.page_of[k]
            if page != frame:                                              # @line L4
                data_io += 1                                               # @line L5
                frame = page                                               # @line L5
        return keys, index_io, data_io                                     # @line L6

    def scan_cost(self) -> int:
        return self.pages


def yao_expected_pages(n: int, p: int, k: int) -> Fraction:
    """Expected number of distinct pages that hold k tuples chosen at random
    from n tuples stored p per page (n a multiple of p): Yao's formula."""
    m = n // p
    return m * (1 - Fraction(comb(n - p, k), comb(n, k)))
