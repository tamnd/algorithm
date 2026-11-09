# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/redelmeier-algorithm/. The authors are listed in prov/R79V1G.jsonl.

from collections.abc import Iterator

Cell = tuple[int, int]


def _allowed(cell: Cell) -> bool:
    # The cells after the origin in the order (row, column): a later row, or
    # the same row and a column at least 0.
    x, y = cell
    return y > 0 or (y == 0 and x >= 0)


def _neighbors(cell: Cell) -> tuple[Cell, Cell, Cell, Cell]:
    x, y = cell
    return ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))


def _search(n: int, counts: list[int], want: int) -> Iterator[tuple[Cell, ...]]:
    """Run Redelmeier's search for sizes up to n.

    counts[k] receives the number of fixed polyominoes with k cells. When
    want > 0, the polyominoes with want cells are yielded as sorted tuples.
    """
    occupied: list[Cell] = []
    reached: set[Cell] = {(0, 0)}

    def extend(untried: list[Cell]) -> Iterator[tuple[Cell, ...]]:
        untried = list(untried)  # this call owns its copy
        while untried:  # @line L3
            c = untried.pop()  # @line L4
            occupied.append(c)  # @line L5
            size = len(occupied)
            counts[size] += 1
            if size == want:
                yield tuple(sorted(occupied))
            if size < n:  # @line L6
                new = [d for d in _neighbors(c) if _allowed(d) and d not in reached]  # @line L7
                reached.update(new)  # @line L8
                yield from extend(untried + new)  # @line L9
                reached.difference_update(new)  # @line L10
            occupied.pop()  # @line L11

    yield from extend([(0, 0)])  # @line L2


def redelmeier_counts(n: int) -> list[int]:
    """Return [a(1), ..., a(n)], where a(k) is the number of fixed polyominoes with k cells."""
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return []
    counts = [0] * (n + 1)  # @line L1
    for _ in _search(n, counts, 0):
        pass
    return counts[1:]


def fixed_polyominoes(k: int) -> Iterator[tuple[Cell, ...]]:
    """Yield each fixed polyomino with k cells once, as a sorted tuple of (x, y) cells.

    Each polyomino is placed so that its first cell in the order (y, x) is (0, 0).
    """
    if k < 1:
        raise ValueError("k must be positive")
    counts = [0] * (k + 1)
    yield from _search(k, counts, k)
