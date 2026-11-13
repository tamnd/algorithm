# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/polyomino-tiling-problem/. The authors are listed in prov/6M5XGW.jsonl.
"""Polyomino tiling as exact cover, solved by Algorithm X.

A polyomino is a set of (row, col) cells. A region is a set of cells. A
tiling covers every cell of the region exactly once by placed copies of the
pieces, each copy turned or flipped in any way (or only turned, if
reflect=False). With once=True every piece is used exactly once, as in
pentomino puzzles; otherwise each piece may be used any number of times.
"""

def normalize(cells):
    r0 = min(r for r, _ in cells)
    c0 = min(c for _, c in cells)
    return frozenset((r - r0, c - c0) for r, c in cells)


def orientations(piece, reflect=True):
    """The distinct images of a piece under the 4 rotations, and reflections if allowed."""
    out = set()
    cells = list(piece)
    for flip in ((False, True) if reflect else (False,)):
        cur = [(r, -c) for r, c in cells] if flip else cells
        for _ in range(4):
            cur = [(c, -r) for r, c in cur]
            out.add(normalize(cur))
    return sorted(out, key=sorted)


def placements(region, pieces, reflect=True):
    """(piece index, frozenset of cells) for every way to put a piece inside the region."""
    region = frozenset(region)
    out = []
    for k, piece in enumerate(pieces):
        seen = set()
        for shape in orientations(piece, reflect):
            for r, c in region:
                ar, ac = min(shape)
                cells = frozenset((r + dr - ar, c + dc - ac) for dr, dc in shape)
                if cells <= region and cells not in seen:
                    seen.add(cells)
                    out.append((k, cells))
    return out


def rectangle(h, w):
    return {(r, c) for r in range(h) for c in range(w)}


def tilings(region, pieces, once=False, reflect=True, limit=None):
    """All tilings, each a sorted list of (piece index, sorted cells), by Algorithm X."""
    rows = placements(region, pieces, reflect)
    # Columns: every cell, and with once=True every piece.
    items = [("cell", cell) for cell in region]  # @line L1
    if once:
        items += [("piece", k) for k in range(len(pieces))]
    cols = {item: set() for item in items}
    row_items = []
    for i, (k, cells) in enumerate(rows):
        its = [("cell", cell) for cell in cells] + ([("piece", k)] if once else [])
        row_items.append(its)
        for it in its:
            cols[it].add(i)
    found = []
    chosen = []

    def select(i):
        removed = []
        for it in row_items[i]:
            for j in cols[it]:
                for other in row_items[j]:
                    if other != it:
                        cols[other].discard(j)
            removed.append((it, cols.pop(it)))
        return removed

    def deselect(i, removed):
        for it, rows_of in reversed(removed):
            cols[it] = rows_of
            for j in rows_of:
                for other in row_items[j]:
                    if other != it:
                        cols[other].add(j)

    def search():
        if limit is not None and len(found) >= limit:
            return
        if not cols:  # @line L2
            found.append(sorted((rows[i][0], sorted(rows[i][1])) for i in chosen))
            return
        c = min(cols, key=lambda it: len(cols[it]))  # @line L3
        if not cols[c]:  # @line L4
            return
        for i in sorted(cols[c]):  # @line L5
            chosen.append(i)
            removed = select(i)  # @line L6
            search()  # @line L7
            deselect(i, removed)  # @line L8
            chosen.pop()

    search()
    return sorted(found)


def count_tilings(region, pieces, once=False, reflect=True):
    return len(tilings(region, pieces, once, reflect))


def brute_force(region, pieces, once=False, reflect=True):
    """All tilings, by listing every set of pairwise disjoint placements and
    keeping those that cover the region (and use each piece once, if asked)."""
    region = frozenset(region)
    rows = placements(region, pieces, reflect)
    found = []
    pick = []

    def walk(i, covered):
        if i == len(rows):
            if covered == region and (not once or sorted(rows[j][0] for j in pick) == list(range(len(pieces)))):
                found.append(sorted((rows[j][0], sorted(rows[j][1])) for j in pick))
            return
        walk(i + 1, covered)
        if not covered & rows[i][1]:
            pick.append(i)
            walk(i + 1, covered | rows[i][1])
            pick.pop()

    walk(0, frozenset())
    return sorted(found)


PENTOMINOES = {
    "F": {(0, 1), (0, 2), (1, 0), (1, 1), (2, 1)},
    "I": {(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)},
    "L": {(0, 0), (1, 0), (2, 0), (3, 0), (3, 1)},
    "N": {(0, 1), (1, 1), (2, 0), (2, 1), (3, 0)},
    "P": {(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)},
    "T": {(0, 0), (0, 1), (0, 2), (1, 1), (2, 1)},
    "U": {(0, 0), (0, 2), (1, 0), (1, 1), (1, 2)},
    "V": {(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)},
    "W": {(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)},
    "X": {(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)},
    "Y": {(0, 1), (1, 0), (1, 1), (2, 1), (3, 1)},
    "Z": {(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)},
}
