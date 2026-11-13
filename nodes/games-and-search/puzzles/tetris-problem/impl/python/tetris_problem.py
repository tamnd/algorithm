# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tetris-problem/. The authors are listed in prov/QESA6R.jsonl.
"""Offline Tetris on small wells, with pieces dropped straight down.

A board is a tuple of h row masks, bottom row first; bit c is column c. A
placement picks a rotation and a column, and the piece falls straight down
from above the well until it rests. Full rows are then cleared. The game is
lost when a piece rests with a cell at row h or above.

This model has no slides or turns during the fall, so it allows fewer
placements than the model of Demaine, Hohenberger and Liben-Nowell.
"""

BASE = {
    'I': [(0, 0), (0, 1), (0, 2), (0, 3)],
    'O': [(0, 0), (0, 1), (1, 0), (1, 1)],
    'T': [(0, 0), (0, 1), (0, 2), (1, 1)],
    'S': [(0, 0), (0, 1), (1, 1), (1, 2)],
    'Z': [(0, 1), (0, 2), (1, 0), (1, 1)],
    'L': [(0, 0), (0, 1), (0, 2), (1, 2)],
    'J': [(0, 0), (0, 1), (0, 2), (1, 0)],
}


def _normal(cells):
    r0 = min(r for r, _ in cells)
    c0 = min(c for _, c in cells)
    return tuple(sorted((r - r0, c - c0) for r, c in cells))


def rotations(name):
    """The distinct rotations of a tetromino, as sorted (row, column) offsets."""
    out = []
    cells = BASE[name]
    for _ in range(4):
        shape = _normal(cells)
        if shape not in out:
            out.append(shape)
        cells = [(c, -r) for r, c in cells]
    return out


def drop(board, shape, col, width):
    """Drop `shape` with its left edge at `col`; return (board, lost) or None if it does not fit."""
    h = len(board)
    if any(c + col >= width for _, c in shape):
        return None
    rows = list(board) + [0] * 4

    def hits(y):
        return y < 0 or any(rows[y + r] >> (c + col) & 1 for r, c in shape)

    y = h
    while not hits(y - 1):
        y -= 1
    for r, c in shape:
        rows[y + r] |= 1 << (c + col)
    lost = any(rows[i] for i in range(h, h + 4))
    full = (1 << width) - 1
    kept = [x for x in rows[:h] if x != full]
    return tuple(kept + [0] * (h - len(kept))), lost


def placements(board, name, width):
    """All boards reachable by one placement of `name` that do not lose."""
    out = set()
    for shape in rotations(name):
        for col in range(width):
            res = drop(board, shape, col, width)
            if res is not None and not res[1]:
                out.add(res[0])
    return out


def survive_count(sequence, width, height):
    """Largest number of leading pieces of `sequence` that can be placed without losing.

    Dynamic programming over the set of boards reachable after each piece.
    """
    layer = {tuple([0] * height)}
    for i, name in enumerate(sequence):
        nxt = set()
        for board in layer:
            nxt |= placements(board, name, width)
        if not nxt:
            return i
        layer = nxt
    return len(sequence)


def survive_count_brute(sequence, width, height):
    """Independent check: depth-first search over every placement, with no merging of boards."""

    def best(board, i):
        if i == len(sequence):
            return 0
        top = 0
        for shape in rotations(sequence[i]):
            for col in range(width):
                res = drop(board, shape, col, width)
                if res is not None and not res[1]:
                    top = max(top, 1 + best(res[0], i + 1))
                    if top == len(sequence) - i:
                        return top
        return top

    return best(tuple([0] * height), 0)


def survives_forever(pattern, width, height):
    """Can the periodic sequence pattern, pattern, ... be played forever?

    The sets of boards reachable after each full period form a deterministic
    sequence over a finite space, so it either becomes empty (the game is lost)
    or repeats a set seen before (every prefix can be played, so by König's
    lemma the whole infinite sequence can).
    """
    layer = frozenset({tuple([0] * height)})
    seen = set()
    while layer and layer not in seen:
        seen.add(layer)
        for name in pattern:
            nxt = set()
            for board in layer:
                nxt |= placements(board, name, width)
            layer = nxt
        layer = frozenset(layer)
    return bool(layer)
