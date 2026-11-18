# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/autoadmin-index-selection/. The authors are listed in prov/Q7Z4FQ.jsonl.

"""The index selection tool of Chaudhuri and Narasayya (VLDB 1997).

The tool has three parts:

1. Candidate selection: each query alone is a workload of one, and the
   indexes of its best configuration become candidates.
2. Configuration enumeration, Greedy(m, k): the best configuration of m
   indexes by exhaustive search, then one index at a time while the cost
   falls, up to k indexes.
3. Multi-column indexes, built up by width: the indexes of width j are the
   chosen indexes of width j - 1 with one more column (the MC-LEAD rule).

Costs come from a what-if function, which stands in for the query optimizer
with hypothetical indexes. The optimizer model on this page uses at most one
index per query, so the atomic configurations of a query are the single
indexes, and the cost of a query in any configuration is the minimum over
them. Each distinct (query, atomic configuration) pair costs one what-if call.
"""

from dataclasses import dataclass, field
from itertools import combinations
from typing import Dict, FrozenSet, Iterable, List, Optional, Sequence, Set, Tuple

ROWS_PER_PAGE = 20

Index = Tuple[str, Tuple[str, ...]]          # (table, columns in key order)


@dataclass(frozen=True)
class Table:
    name: str
    rows: int
    distinct: Tuple[Tuple[str, int], ...]   # (column, number of distinct values)

    def ndv(self, col: str) -> int:
        return dict(self.distinct)[col]


@dataclass(frozen=True)
class Select:
    weight: float
    table: str
    eq: Tuple[str, ...] = ()                 # columns with an equality predicate
    rng: Optional[str] = None                # column with a range predicate
    rng_sel: float = 1.0
    out: Tuple[str, ...] = ()                # other columns the query reads

    def indexable(self) -> Set[str]:
        return set(self.eq) | ({self.rng} if self.rng else set())

    def needed(self) -> Set[str]:
        return self.indexable() | set(self.out)


@dataclass(frozen=True)
class Update:
    weight: float
    table: str
    cols: Tuple[str, ...]                    # the columns it changes


class WhatIf:
    """A toy optimizer that costs a query under hypothetical indexes."""

    def __init__(self, tables: Iterable[Table], maint: float = 4.0):
        self.tables: Dict[str, Table] = {t.name: t for t in tables}
        self.maint = maint
        self.calls = 0
        self.cache: Dict[Tuple[object, FrozenSet[Index]], float] = {}

    def index_cost(self, q: Select, ix: Index) -> Optional[float]:
        """The cost of the plan for q that uses ix, or None if ix is of no use."""
        t = self.tables[q.table]
        table, cols = ix
        if table != q.table:
            return None
        sel, used, pos = 1.0, 0, 0
        while pos < len(cols) and cols[pos] in q.eq:
            sel /= t.ndv(cols[pos])
            used, pos = used + 1, pos + 1
        if pos < len(cols) and cols[pos] == q.rng:
            sel *= q.rng_sel
            used += 1
        if used == 0:
            return None
        rows = sel * t.rows
        covering = q.needed() <= set(cols)
        return 3.0 + rows * (1.0 / ROWS_PER_PAGE if covering else 1.0)

    def optimize(self, q, config: FrozenSet[Index]) -> float:
        """The optimizer's cost for q with exactly the indexes in config."""
        t = self.tables[q.table]
        if isinstance(q, Update):
            touched = [ix for ix in config if ix[0] == q.table and set(ix[1]) & set(q.cols)]
            return 1.0 + self.maint * len(touched)
        best = t.rows / ROWS_PER_PAGE                    # a full scan
        for ix in config:
            c = self.index_cost(q, ix)
            if c is not None and c < best:
                best = c
        return best

    def call(self, q, config: FrozenSet[Index]) -> float:
        """A what-if call, with a cache, as the tool makes it."""
        key = (q, config)
        if key not in self.cache:
            self.calls += 1
            self.cache[key] = self.optimize(q, config)
        return self.cache[key]


class Tool:
    def __init__(self, whatif: WhatIf, workload: Sequence, k: int, m: int = 2, width: int = 2):
        self.w = whatif
        self.workload = list(workload)
        self.k, self.m, self.width = k, m, width
        self.pairs: Set[Tuple[object, FrozenSet[Index]]] = set()   # (query, configuration) pairs costed

    # ----- costs from atomic configurations -----

    def query_cost(self, q, config: FrozenSet[Index]) -> float:
        if isinstance(q, Update):                       # maintenance adds up per index
            return 1.0 + sum(self.w.call(q, frozenset([ix])) - 1.0 for ix in config
                             if ix[0] == q.table)
        best = self.w.call(q, frozenset())              # @line L13
        for ix in config:
            if ix[0] == q.table and self.w.index_cost(q, ix) is not None:
                best = min(best, self.w.call(q, frozenset([ix])))   # @line L13
        return best

    def cost(self, workload: Sequence, config: Iterable[Index]) -> float:
        c = frozenset(config)
        self.pairs.update((q, c) for q in workload)
        return sum(q.weight * self.query_cost(q, c) for q in workload)

    # ----- Greedy(m, k) -----

    def enumerate(self, workload: Sequence, cands: Iterable[Index], k: int) -> FrozenSet[Index]:
        cands = sorted(set(cands))
        best, best_cost = frozenset(), self.cost(workload, ())
        for r in range(1, min(self.m, k) + 1):                       # @line L7
            for s in combinations(cands, r):
                c = self.cost(workload, s)
                if c < best_cost:
                    best, best_cost = frozenset(s), c
        while len(best) < k:                                         # @line L8
            step, step_cost = None, best_cost
            for ix in cands:                                         # @line L9
                if ix not in best:
                    c = self.cost(workload, best | {ix})
                    if c < step_cost:
                        step, step_cost = ix, c
            if step is None:                                         # @line L10
                break
            best, best_cost = best | {step}, step_cost               # @line L11
        return best                                                  # @line L12

    # ----- candidate selection and multi-column indexes -----

    def indexable_columns(self, table: str, lead: bool) -> Set[str]:
        out: Set[str] = set()
        for q in self.workload:
            if isinstance(q, Select) and q.table == table:
                out |= q.indexable() if lead else q.needed()
        return out

    def admissible(self, j: int, chosen: Iterable[Index]) -> Set[Index]:
        if j == 1:
            return {(t, (c,)) for t in self.w.tables for c in self.indexable_columns(t, True)}
        out = set()
        for t, cols in chosen:                                       # MC-LEAD
            if len(cols) == j - 1:
                for c in self.indexable_columns(t, False):
                    if c not in cols:
                        out.add((t, cols + (c,)))
        return out

    def relevant(self, q, indexes: Iterable[Index]) -> List[Index]:
        if not isinstance(q, Select):
            return []
        return [ix for ix in indexes if self.w.index_cost(q, ix) is not None]

    def run(self) -> FrozenSet[Index]:
        chosen: FrozenSet[Index] = frozenset()                       # @line L1
        pool: Set[Index] = set()
        self.trace = []
        for j in range(1, self.width + 1):                           # @line L2
            pool |= self.admissible(j, chosen)                       # @line L3
            cands: Set[Index] = set(chosen)
            for q in self.workload:                                  # @line L4
                cands |= self.enumerate([q], self.relevant(q, pool), self.k)   # @line L5
            chosen = self.enumerate(self.workload, cands, self.k)    # @line L6
            self.trace.append((j, sorted(cands), sorted(chosen)))
        return chosen


def all_indexes(tool: Tool) -> List[Index]:
    """Every index of width at most tool.width that some select query can use."""
    out = set()
    for t in tool.w.tables:
        lead = tool.indexable_columns(t, True)
        cols = sorted(tool.indexable_columns(t, False))
        for c in lead:
            out.add((t, (c,)))
        for wdt in range(2, tool.width + 1):
            for ix in list(out):
                if ix[0] == t and len(ix[1]) == wdt - 1:
                    for c in cols:
                        if c not in ix[1]:
                            out.add((t, ix[1] + (c,)))
    return sorted(out)


def brute_force(tool: Tool) -> Tuple[float, FrozenSet[Index]]:
    """The optimum over all configurations of at most k indexes."""
    idx = all_indexes(tool)
    best, best_cost = frozenset(), tool.cost(tool.workload, ())
    for r in range(1, tool.k + 1):
        for s in combinations(idx, r):
            c = tool.cost(tool.workload, s)
            if c < best_cost - 1e-9:
                best, best_cost = frozenset(s), c
    return best_cost, best
