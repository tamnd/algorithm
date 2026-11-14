# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/karnaugh-map/. The authors are listed in prov/KAW0FH.jsonl.

"""Karnaugh maps for two to four variables.

The variables are x1..xn, and x1 is the high bit of a minterm. For
n = 2 the rows are x1 and the columns x2; for n = 3 the rows are x1 and
the columns x2 x3; for n = 4 the rows are x1 x2 and the columns x3 x4.
Each axis is in Gray code order, so cells next to each other (with
wrap-around) differ in one variable. A cube is a string over '0', '1'
and '-'.
"""

from typing import Iterable

GRAY = {1: ["0", "1"], 2: ["00", "01", "11", "10"]}


def split(n: int) -> tuple[int, int]:
    """The number of row variables and of column variables."""
    if n not in (2, 3, 4):
        raise ValueError("this map handles 2 to 4 variables")
    return (1, 1) if n == 2 else (1, 2) if n == 3 else (2, 2)


def cell(n: int, r: int, c: int) -> int:
    """The minterm in row r and column c."""
    a, b = split(n)
    return int(GRAY[a][r] + GRAY[b][c], 2)


def grid(n: int, on: Iterable[int], dc: Iterable[int] = ()) -> list[str]:
    """The map as text rows of '1', '0' and 'x' (don't care)."""
    on, dc = set(on), set(dc)
    a, b = split(n)
    out = []
    for r in range(2 ** a):
        row = ""
        for c in range(2 ** b):
            m = cell(n, r, c)
            row += "1" if m in on else "x" if m in dc else "0"
        out.append(row)
    return out


def intervals(size: int) -> list[list[int]]:
    """The cyclic runs of length 1, 2, 4, ... on an axis of the given size."""
    out = []
    length = 1
    while length < size:
        out += [[(s + t) % size for t in range(length)] for s in range(size)]
        length *= 2
    out.append(list(range(size)))
    return out


def rectangles(n: int) -> list[frozenset[int]]:
    """Every rectangle of the map with sides 1, 2 or 4 cells, with wrap-around, as a set of minterms."""
    a, b = split(n)
    return [frozenset(cell(n, r, c) for r in rs for c in cs) for rs in intervals(2 ** a) for cs in intervals(2 ** b)]


def cube_of(n: int, cells: frozenset[int]) -> str:
    """The cube of a rectangle: a variable is fixed where every cell agrees."""
    out = ""
    for i in range(n):
        bits = {(m >> (n - 1 - i)) & 1 for m in cells}
        out += str(bits.pop()) if len(bits) == 1 else "-"
    return out


def groups(n: int, on: Iterable[int], dc: Iterable[int] = ()) -> list[frozenset[int]]:
    """The largest groups: rectangles inside on | dc, in no larger such rectangle, with a 1 cell."""
    on, dc = set(on), set(dc)
    ok = [g for g in set(rectangles(n)) if g <= on | dc]  # @line L2: legal groups
    big = [g for g in ok if not any(g < h for h in ok)]  # @line L3: keep the maximal ones
    return sorted((g for g in big if g & on), key=lambda g: (-len(g), sorted(g)))


def read_cover(n: int, on: Iterable[int], dc: Iterable[int] = ()) -> list[str]:
    """The cover a person reads from the map: essential groups first, then the largest useful group."""
    on, dc = set(on), set(dc)
    big = groups(n, on, dc)  # @line L1
    chosen: list[frozenset[int]] = []
    for m in sorted(on):  # @line L4: a 1 cell in exactly one largest group
        holders = [g for g in big if m in g]
        if len(holders) == 1 and holders[0] not in chosen:
            chosen.append(holders[0])  # @line L5
    left = on - set().union(*chosen) if chosen else set(on)
    while left:  # @line L6
        g = max(big, key=lambda g: (len(g & left), len(g), [-x for x in sorted(g)]))  # @line L7
        chosen.append(g)
        left -= g  # @line L8
    return sorted(cube_of(n, g) for g in chosen)
