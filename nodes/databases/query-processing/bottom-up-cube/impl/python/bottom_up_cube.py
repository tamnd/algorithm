# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bottom-up-cube/. The authors are listed in prov/78FNHM.jsonl.
"""Bottom-up cube computation (BUC) of an iceberg cube.

The input is a list of rows (tuples), the cube dimensions (column positions)
and a list of aggregates. The answer is every cell of the data cube whose
group holds at least minsup rows: for each subset S of the dimensions and each
value combination of S that occurs, a row with the values of S, the marker
ALL in the other dimensions, and the aggregates of the rows of that group.

BUC starts with the cell (ALL, ..., ALL) of the whole input. It sorts the
rows of a cell on one more dimension, splits them into blocks of equal value,
and recurses only into blocks of at least minsup rows. COUNT(*) of a block
can only shrink when more dimensions are fixed, so a small block has no
qualifying cell below it.

SQL semantics: a null value of a dimension is a value like any other and forms
its own group; count_star counts every row; the other aggregates skip nulls;
sum, avg, min and max of no non-null value give None.
"""

from collections.abc import Sequence
from fractions import Fraction
from numbers import Number


class _All:
    """The ALL marker of a dimension that is not grouped in a cell."""

    __slots__ = ()

    def __repr__(self) -> str:
        return "ALL"


ALL = _All()

AGG_FUNCS = ("count_star", "count", "sum", "avg", "min", "max")


def _vkey(v: object) -> tuple:
    """Sort order of one dimension value: None first, then numbers, then strings."""
    if v is None:
        return (0, 0)
    if isinstance(v, Number):
        return (1, v)
    if isinstance(v, str):
        return (2, v)
    return (3, repr(v))


def _agg(func: str, vals: list) -> object:
    """One SQL aggregate over the values of a group. count_star counts all."""
    if func == "count_star":
        return len(vals)
    nn = [v for v in vals if v is not None]
    if func == "count":
        return len(nn)
    if not nn:
        return None
    if func == "sum":
        return sum(nn)
    if func == "avg":
        total = sum(nn)
        if all(isinstance(v, (int, Fraction)) for v in nn):
            return Fraction(total, 1) / len(nn)
        return total / len(nn)
    if func == "min":
        return min(nn)
    return max(nn)


def buc(rows: Sequence[tuple], dims: Sequence[int], aggs: Sequence[tuple],
        minsup: int = 1, stats: dict | None = None) -> list:
    """Return the cells of the iceberg cube, in the depth-first order of BUC.

    rows are tuples; dims are the positions of the D cube dimensions; aggs is a
    list of (func, column), with column None for count_star. Each output row is
    a tuple of D dimension values (ALL where a dimension is not grouped)
    followed by the aggregates. A cell is output when its group has at least
    minsup >= 1 rows. If stats is a dict, it gets "calls" (the recursive calls,
    one per output cell), "sorted" (the rows sorted, summed over all sorts) and
    "pruned" (the blocks skipped because they are smaller than minsup).
    """
    if minsup < 1:
        raise ValueError("minsup must be at least 1")
    for f, _ in aggs:
        if f not in AGG_FUNCS:
            raise ValueError("unknown aggregate %r" % (f,))
    dims = list(dims)
    D = len(dims)
    X = list(rows)  # @line L1
    cell = [ALL] * D  # @line L1
    out: list = []
    counters = {"calls": 0, "sorted": 0, "pruned": 0}

    def emit(lo: int, hi: int) -> None:
        group = X[lo:hi]
        vals = [_agg(f, [None if c is None else r[c] for r in group]) for f, c in aggs]
        out.append(tuple(cell) + tuple(vals))

    def rec(lo: int, hi: int, d0: int) -> None:
        counters["calls"] += 1
        emit(lo, hi)  # @line L3
        for d in range(d0, D):  # @line L4
            col = dims[d]
            X[lo:hi] = sorted(X[lo:hi], key=lambda r: _vkey(r[col]))  # @line L5
            counters["sorted"] += hi - lo
            i = lo  # @line L6
            while i < hi:  # @line L7
                v = X[i][col]
                j = i + 1  # @line L8
                while j < hi and X[j][col] == v:  # @line L8
                    j += 1
                if j - i >= minsup:  # @line L9
                    cell[d] = v  # @line L10
                    rec(i, j, d + 1)  # @line L10
                    cell[d] = ALL  # @line L10
                else:
                    counters["pruned"] += 1
                i = j  # @line L11

    if len(X) >= minsup:  # @line L2
        rec(0, len(X), 0)  # @line L2
    if stats is not None:
        stats.update(counters)
    return out


def cube_size(cards: Sequence[int]) -> int:
    """The number of cells of the full cube when every value combination occurs: prod(C_i + 1)."""
    n = 1
    for c in cards:
        n *= c + 1
    return n
