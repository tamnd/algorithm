# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/partial-index/. The authors are listed in prov/5RMQCY.jsonl.

"""A partial index (Stonebraker 1989): an ordered index over only the rows
that satisfy a predicate P, and a planner that uses it only when the query
predicate implies P.

Rows are dicts of integer columns. A predicate is a conjunction of atoms
(column, op, constant) with op in =, <, <=, >, >=. On integer columns each
conjunction is a box: one closed interval per column. Q implies P exactly
when the box of Q lies in the box of P (or the box of Q is empty).
"""

import math
from bisect import bisect_left, bisect_right, insort
from typing import Dict, List, Optional, Sequence, Tuple

Atom = Tuple[str, str, int]
Row = Dict[str, int]
NEG, POS = -math.inf, math.inf


def box(pred: Sequence[Atom]) -> Dict[str, Tuple[float, float]]:
    """The closed interval of each column that the conjunction allows."""
    out: Dict[str, Tuple[float, float]] = {}
    for col, op, c in pred:
        lo, hi = out.get(col, (NEG, POS))
        if op == "=":
            lo, hi = max(lo, c), min(hi, c)
        elif op == "<":
            hi = min(hi, c - 1)
        elif op == "<=":
            hi = min(hi, c)
        elif op == ">":
            lo = max(lo, c + 1)
        elif op == ">=":
            lo = max(lo, c)
        else:
            raise ValueError(op)
        out[col] = (lo, hi)
    return out


def holds(pred: Sequence[Atom], row: Row) -> bool:
    return all(lo <= row[col] <= hi for col, (lo, hi) in box(pred).items())


def implies(q: Sequence[Atom], p: Sequence[Atom]) -> bool:
    """Does every row that satisfies q also satisfy p? Exact for integer boxes."""
    bq, bp = box(q), box(p)
    if any(lo > hi for lo, hi in bq.values()):
        return True                                      # q is never true
    for col, (plo, phi) in bp.items():                   # @line L7
        qlo, qhi = bq.get(col, (NEG, POS))
        if qlo < plo or qhi > phi:                       # @line L7
            return False
    return True                                          # @line L8


class Table:
    def __init__(self, rows: Sequence[Row]):
        self.rows: Dict[int, Row] = {i: dict(r) for i, r in enumerate(rows)}
        self.next_id = len(self.rows)
        self.indexes: List["PartialIndex"] = []
        self.stats = {"scanned": 0, "index_entries": 0, "index_writes": 0}

    def insert(self, row: Row) -> int:
        rid = self.next_id
        self.next_id += 1
        self.rows[rid] = dict(row)
        for ix in self.indexes:
            ix.change(rid, None, self.rows[rid])
        return rid

    def update(self, rid: int, **values) -> None:
        old = dict(self.rows[rid])
        self.rows[rid].update(values)
        for ix in self.indexes:
            ix.change(rid, old, self.rows[rid])

    def delete(self, rid: int) -> None:
        old = self.rows.pop(rid)
        for ix in self.indexes:
            ix.change(rid, old, None)


class PartialIndex:
    """An ordered index on one key column over the rows that satisfy pred."""

    def __init__(self, table: Table, key: str, pred: Sequence[Atom]):
        self.table, self.key, self.pred = table, key, list(pred)
        self.entries: List[Tuple[int, int]] = sorted(               # @line L1
            (r[key], rid) for rid, r in table.rows.items() if holds(self.pred, r))
        table.indexes.append(self)

    def change(self, rid: int, old: Optional[Row], new: Optional[Row]) -> None:
        if old is not None and holds(self.pred, old):               # @line L2
            i = bisect_left(self.entries, (old[self.key], rid))
            del self.entries[i]                                     # @line L2
            self.table.stats["index_writes"] += 1
        if new is not None and holds(self.pred, new):               # @line L3
            insort(self.entries, (new[self.key], rid))              # @line L3
            self.table.stats["index_writes"] += 1


def query(table: Table, key: str, lo: int, hi: int, pred: Sequence[Atom],
          index: Optional[PartialIndex] = None) -> Tuple[List[int], str]:
    """The row ids with lo <= key <= hi and pred, in key order, and the plan used."""
    full = list(pred) + [(key, ">=", lo), (key, "<=", hi)]
    if index is not None and index.key == key and implies(full, index.pred):   # @line L4
        i = bisect_left(index.entries, (lo, -1))
        j = bisect_right(index.entries, (hi, math.inf))
        out = []
        for k, rid in index.entries[i:j]:                            # @line L5
            table.stats["index_entries"] += 1
            if holds(pred, table.rows[rid]):                         # @line L5
                out.append(rid)
        return out, "index"
    out = []
    for rid, r in table.rows.items():                                # @line L6
        table.stats["scanned"] += 1
        if holds(full, r):                                           # @line L6
            out.append(rid)
    out.sort(key=lambda rid: (table.rows[rid][key], rid))
    return out, "scan"
