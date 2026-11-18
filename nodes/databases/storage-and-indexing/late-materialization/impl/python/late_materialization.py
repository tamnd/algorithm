# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/late-materialization/. The authors are listed in prov/DADXAP.jsonl.

"""Early and late materialization of a select-project query on a column store.

A table is a dict from column name to a list of values, all of the same length
N; record i is the i-th value of every column. A query is a conjunction of
predicates (column, op, constant) and a list of output columns. A comparison
with None (NULL) is not true, as in SQL.

early() stitches each record from all the columns the query uses and then
filters it. late() works on position lists: it filters one column at a time,
reading each column only at the positions that are still alive, and fetches the
output columns only for the positions that pass. bitmap() is the parallel form
of late materialization: every predicate scans its whole column into a bitmap,
and the bitmaps are combined with AND.

Every function counts the column values it reads in self.reads.
"""

import operator
from typing import Dict, List, Sequence, Tuple

OPS = {"=": operator.eq, "<>": operator.ne, "<": operator.lt,
       "<=": operator.le, ">": operator.gt, ">=": operator.ge}
Pred = Tuple[str, str, object]


def holds(op: str, x: object, v: object) -> bool:
    return x is not None and v is not None and OPS[op](x, v)


class ColumnTable:
    def __init__(self, columns: Dict[str, List[object]]) -> None:
        lengths = {len(v) for v in columns.values()}
        if len(lengths) > 1:
            raise ValueError("all columns must have the same length")
        self.columns = {c: list(v) for c, v in columns.items()}
        self.N = lengths.pop() if lengths else 0
        self.reads = 0

    def value(self, c: str, i: int) -> object:
        self.reads += 1
        return self.columns[c][i]

    # ------------------------------------------------------------ late

    def late(self, preds: Sequence[Pred], out: Sequence[str]) -> List[Tuple[object, ...]]:
        for c, op, _ in preds:
            if c not in self.columns or op not in OPS:
                raise ValueError(f"bad predicate on {c}")
        P = list(range(self.N))                               # @line L1
        for c, op, v in preds:                                # @line L2
            P = [i for i in P if holds(op, self.value(c, i), v)]  # @line L3
        cols = [[self.value(c, i) for i in P] for c in out]   # @line L4 L5
        return list(zip(*cols)) if out else [()] * len(P)     # @line L6

    def positions(self, preds: Sequence[Pred]) -> List[int]:
        """The sorted positions of the records that satisfy every predicate."""
        P = list(range(self.N))
        for c, op, v in preds:
            P = [i for i in P if holds(op, self.columns[c][i], v)]
        return P

    # ------------------------------------------------------------ bitmap

    def bitmap(self, preds: Sequence[Pred], out: Sequence[str]) -> List[Tuple[object, ...]]:
        bits = (1 << self.N) - 1
        for c, op, v in preds:
            b = 0
            for i in range(self.N):
                if holds(op, self.value(c, i), v):
                    b |= 1 << i
            bits &= b
        P = [i for i in range(self.N) if bits >> i & 1]
        cols = [[self.value(c, i) for i in P] for c in out]
        return list(zip(*cols)) if out else [()] * len(P)

    # ------------------------------------------------------------ early

    def early(self, preds: Sequence[Pred], out: Sequence[str]) -> List[Tuple[object, ...]]:
        used = list(dict.fromkeys([c for c, _, _ in preds] + list(out)))
        result = []
        for i in range(self.N):                               # @line L7
            t = {c: self.value(c, i) for c in used}           # @line L8
            if all(holds(op, t[c], v) for c, op, v in preds):  # @line L9
                result.append(tuple(t[c] for c in out))       # @line L9
        return result


def order_by_selectivity(table: ColumnTable, preds: Sequence[Pred]) -> List[Pred]:
    """The predicates, the most selective first (by an exact count, for the tests)."""
    def passing(p: Pred) -> int:
        c, op, v = p
        return sum(1 for x in table.columns[c] if holds(op, x, v))
    return sorted(preds, key=passing)
