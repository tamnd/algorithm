# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/what-if-index-analysis/. The authors are listed in prov/STWF16.jsonl.

"""What-if index analysis (Chaudhuri and Narasayya, SIGMOD 1998), on a toy
optimizer.

The optimizer never looks at index data. It costs a plan from metadata (the
number of entries, leaf pages and the height of the index) and from the
statistics of the column (an equi-depth histogram). So an index can be made
"hypothetical": the catalog gets its metadata and statistics, built from a
sample, and no index is built. A what-if call adds such indexes to the
catalog for one optimization and then removes them.
"""

import math
import random
from bisect import bisect_left, bisect_right
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

ROWS_PER_PAGE = 50
ENTRIES_PER_LEAF = 200
FANOUT = 200


class Histogram:
    """An equi-depth histogram: the bucket bounds of sorted values."""

    def __init__(self, values: Sequence[int], buckets: int, total: int):
        v = sorted(values)
        self.total = total
        self.bounds = [v[min(len(v) - 1, (i * len(v)) // buckets)] for i in range(buckets)] + [v[-1]]
        self.buckets = buckets

    def selectivity(self, lo: int, hi: int) -> float:
        """The estimated fraction of rows with lo <= value <= hi."""
        f = 0.0
        for i in range(self.buckets):
            a, b = self.bounds[i], self.bounds[i + 1]
            width = b - a + 1
            ov = min(b, hi) - max(a, lo) + 1
            if ov > 0:
                f += ov / width / self.buckets
        return min(1.0, f)


@dataclass
class IndexMeta:
    column: str
    entries: int
    leaf_pages: int
    height: int
    hypothetical: bool


def btree_shape(n: int) -> Tuple[int, int]:
    """The leaf pages and the height of a bulk-loaded B+ tree with n entries."""
    leaves = max(1, math.ceil(n / ENTRIES_PER_LEAF))
    height, level = 1, leaves
    while level > 1:
        level = math.ceil(level / FANOUT)
        height += 1
    return leaves, height


class BuiltIndex:
    """A real index: the sorted (value, row id) pairs, in pages."""

    def __init__(self, table: "Table", column: str):
        self.column = column
        self.entries = sorted((r[column], i) for i, r in enumerate(table.rows))
        self.leaves = [self.entries[i:i + ENTRIES_PER_LEAF]
                       for i in range(0, len(self.entries), ENTRIES_PER_LEAF)] or [[]]
        # build the upper levels to get the real height
        level, height = len(self.leaves), 1
        while level > 1:
            level = math.ceil(level / FANOUT)
            height += 1
        self.height = height
        table.rows_read += len(table.rows)

    def meta(self) -> IndexMeta:
        return IndexMeta(self.column, len(self.entries), len(self.leaves), self.height, False)


class Table:
    def __init__(self, rows: List[Dict[str, int]]):
        self.rows = rows
        self.rows_read = 0

    def sample(self, column: str, fraction: float, seed: int) -> List[int]:
        if fraction >= 1.0:
            self.rows_read += len(self.rows)
            return [r[column] for r in self.rows]
        rng = random.Random(seed)
        k = max(1, int(fraction * len(self.rows)))
        idx = rng.sample(range(len(self.rows)), k)
        self.rows_read += k
        return [self.rows[i][column] for i in idx]


class Optimizer:
    def __init__(self, table: Table, buckets: int = 20):
        self.table = table
        self.buckets = buckets
        self.catalog: Dict[str, IndexMeta] = {}
        self.stats: Dict[str, Histogram] = {}
        self.built: Dict[str, BuiltIndex] = {}

    # ----- real indexes -----

    def create_index(self, column: str) -> None:
        ix = BuiltIndex(self.table, column)
        self.built[column] = ix
        self.catalog[column] = ix.meta()
        self.stats[column] = Histogram([e[0] for e in ix.entries], self.buckets, len(ix.entries))

    # ----- costing (metadata and statistics only) -----

    def cost(self, column: str, lo: int, hi: int) -> Tuple[float, str]:
        """The cheapest plan for lo <= column <= hi, and its cost in pages."""
        n = len(self.table.rows)
        best, plan = math.ceil(n / ROWS_PER_PAGE), "scan"
        meta = self.catalog.get(column)
        if meta is not None:
            if column not in self.stats:
                raise KeyError("no statistics for " + column)
            rows = self.stats[column].selectivity(lo, hi) * n
            c = (meta.height - 1) + max(1.0, rows / ENTRIES_PER_LEAF) + rows   # one page per row fetched
            if c < best:
                best, plan = c, "index"
        return best, plan

    # ----- the what-if call -----

    def what_if(self, query: Tuple[str, int, int], hypothetical: Sequence[str],
                fraction: float = 0.05, seed: int = 0) -> Tuple[float, str]:
        column, lo, hi = query
        saved_cat, saved_stats = dict(self.catalog), dict(self.stats)
        try:
            for col in hypothetical:
                if col in self.catalog:
                    continue
                leaves, height = btree_shape(len(self.table.rows))              # @line L1
                self.catalog[col] = IndexMeta(col, len(self.table.rows), leaves, height, True)   # @line L1
                values = self.table.sample(col, fraction, seed)                  # @line L2
                self.stats[col] = Histogram(values, self.buckets, len(self.table.rows))   # @line L2
            return self.cost(column, lo, hi)                                     # @line L3
        finally:
            self.catalog, self.stats = saved_cat, saved_stats                    # @line L4

    # ----- running a plan -----

    def run(self, column: str, lo: int, hi: int) -> Tuple[List[int], int]:
        """Run the chosen plan with the built indexes. Returns row ids and pages read."""
        _, plan = self.cost(column, lo, hi)
        if plan == "index":
            ix = self.built[column]
            i = bisect_left(ix.entries, (lo, -1))
            j = bisect_right(ix.entries, (hi, math.inf))
            leaves = max(1, math.ceil((j - i) / ENTRIES_PER_LEAF))
            return sorted(rid for _, rid in ix.entries[i:j]), (ix.height - 1) + leaves + (j - i)
        out = [i for i, r in enumerate(self.table.rows) if lo <= r[column] <= hi]
        return out, math.ceil(len(self.table.rows) / ROWS_PER_PAGE)


def full_scan(table: Table, column: str, lo: int, hi: int) -> List[int]:
    return [i for i, r in enumerate(table.rows) if lo <= r[column] <= hi]
