# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/myers-diff/. The authors are listed in prov/245ETE.jsonl.

from collections.abc import Sequence
from typing import TypeVar

T = TypeVar("T")


def furthest_points(a: Sequence[T], b: Sequence[T]) -> list[dict[int, int]]:
    """Return the rows V_0, ..., V_D; V_d[k] is the largest x reached on diagonal k = x - y at cost d."""
    m, n = len(a), len(b)
    v = {1: 0}  # @line L1
    rows: list[dict[int, int]] = []
    for d in range(m + n + 1):  # @line L2
        row: dict[int, int] = {}
        for k in range(-d, d + 1, 2):  # @line L3
            if k == -d or (k != d and v[k - 1] < v[k + 1]):  # @line L4
                x = v[k + 1]
            else:
                x = v[k - 1] + 1  # @line L5
            y = x - k  # @line L6
            while x < m and y < n and a[x] == b[y]:  # @line L7
                x, y = x + 1, y + 1
            v[k] = x  # @line L8
            row[k] = x
        rows.append(row)
        if any(x >= m and x - k >= n for k, x in row.items()):  # @line L9
            return rows
    raise AssertionError("unreachable: d = m + n always reaches (m, n)")


def edit_distance_indel(a: Sequence[T], b: Sequence[T]) -> int:
    """Return D, the least number of insertions and deletions that turn a into b."""
    return len(furthest_points(a, b)) - 1


def diff(a: Sequence[T], b: Sequence[T]) -> list[tuple[str, T]]:
    """Return a shortest edit script as a list of ('=', item), ('-', item) and ('+', item)."""
    m, n = len(a), len(b)
    rows = furthest_points(a, b)
    ops: list[tuple[str, T]] = []
    x, y = m, n  # @line L10
    for d in range(len(rows) - 1, 0, -1):  # @line L11
        prev = rows[d - 1]
        k = x - y
        if k == -d or (k != d and prev[k - 1] < prev[k + 1]):  # @line L12
            pk = k + 1
        else:
            pk = k - 1
        px = prev[pk]
        py = px - pk
        sx, sy = (px, py + 1) if pk == k + 1 else (px + 1, py)  # @line L13
        while x > sx:  # @line L14
            x, y = x - 1, y - 1
            ops.append(("=", a[x]))
        if pk == k + 1:  # @line L15
            ops.append(("+", b[py]))
        else:
            ops.append(("-", a[px]))
        x, y = px, py
    while x > 0:  # @line L16
        x, y = x - 1, y - 1
        ops.append(("=", a[x]))
    ops.reverse()
    return ops
