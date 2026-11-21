# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/l-diversity/. The authors are listed in prov/HGM0PD.jsonl.

from collections import Counter
from collections.abc import Hashable, Sequence
from fractions import Fraction

Row = Sequence[Hashable]


def blocks(table: Sequence[Row], qi: Sequence[int]) -> dict[tuple[Hashable, ...], list[Row]]:
    """Group the rows of the table by their values on the quasi-identifier columns qi.

    Cost: O(n) expected time for n rows and a fixed number of columns.
    """
    out: dict[tuple[Hashable, ...], list[Row]] = {}
    for row in table:
        out.setdefault(tuple(row[j] for j in qi), []).append(row)
    return out


def block_is_diverse(
    counts: Sequence[int], l: int, variant: str = "distinct", c: Fraction | int = 1
) -> bool:
    """Test one block, given the counts of its distinct sensitive values.

    Precondition: every count is positive, l >= 1, c > 0, and variant is
    "distinct", "entropy" or "recursive". The entropy test is exact: it
    compares N^N with l^N * prod(r^r), where N is the size of the block.
    Cost: O(m log m) for m values, plus the big integer products.
    """
    r = sorted(counts, reverse=True)  # @line L3
    m = len(r)
    size = sum(r)
    if variant == "distinct":
        return m >= l  # @line L4
    if variant == "entropy":
        rhs = l**size
        for x in r:
            rhs *= x**x
        return size**size >= rhs  # @line L5
    if variant == "recursive":
        return Fraction(r[0]) < Fraction(c) * sum(r[l - 1 :]) if m > 0 else False  # @line L6
    raise ValueError("unknown variant " + repr(variant))


def is_l_diverse(
    table: Sequence[Row],
    qi: Sequence[int],
    s: int,
    l: int,
    variant: str = "distinct",
    c: Fraction | int = 1,
) -> bool:
    """Return True if every block of the table is l-diverse in the given sense.

    table is a list of rows, qi the column indices of the quasi-identifier and
    s the column index of the sensitive attribute. An empty table is l-diverse.
    Precondition: l >= 1 and c > 0. Cost: O(n log n) for n rows in the word-RAM
    model, plus the integer products of the entropy test.
    """
    groups = blocks(table, qi)  # @line L1
    for rows in groups.values():  # @line L2
        counts = list(Counter(row[s] for row in rows).values())
        if not block_is_diverse(counts, l, variant, c):
            return False
    return True  # @line L7
