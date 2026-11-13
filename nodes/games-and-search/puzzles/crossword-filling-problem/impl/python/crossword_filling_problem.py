# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/crossword-filling-problem/. The authors are listed in prov/WQC6R5.jsonl.
"""Crossword filling by slot backtracking with the fewest-candidates rule.

A grid is a list of equal-length strings. '#' is a block, '.' an empty white
cell, and a letter a white cell given in advance. A slot is a maximal run of
two or more white cells in a row (across) or a column (down). A filling
writes a word of the dictionary into every slot so that crossing slots agree
on their shared cell. With distinct=True no word is used twice.
"""

from itertools import product


def slots(grid):
    """All slots, each a list of (row, col) cells, across slots first."""
    h, w = len(grid), len(grid[0])
    out = []
    for r in range(h):
        c = 0
        while c < w:
            if grid[r][c] == "#":
                c += 1
                continue
            start = c
            while c < w and grid[r][c] != "#":
                c += 1
            if c - start >= 2:
                out.append([(r, k) for k in range(start, c)])
    for c in range(w):
        r = 0
        while r < h:
            if grid[r][c] == "#":
                r += 1
                continue
            start = r
            while r < h and grid[r][c] != "#":
                r += 1
            if r - start >= 2:
                out.append([(k, c) for k in range(start, r)])
    return out


def _fits(word, cells, letters):
    return len(word) == len(cells) and all(
        letters.get(cell, ".") in (".", ch) for cell, ch in zip(cells, word))


def _render(grid, letters):
    return ["".join(letters.get((r, c), grid[r][c]) if grid[r][c] != "#" else "#"
                    for c in range(len(grid[0]))) for r in range(len(grid))]


def solve(grid, words, distinct=True, limit=None):
    """All fillings of the grid, as lists of strings, up to limit of them."""
    words = sorted(set(words))
    all_slots = slots(grid)
    letters = {(r, c): ch for r, row in enumerate(grid) for c, ch in enumerate(row)
               if ch not in "#."}
    filled = [None] * len(all_slots)
    used = set()
    found = []

    def search():
        if limit is not None and len(found) >= limit:
            return
        open_ = [i for i in range(len(all_slots)) if filled[i] is None]
        if not open_:  # @line L1
            found.append(_render(grid, letters))
            return
        fits = {i: [x for x in words if _fits(x, all_slots[i], letters)
                    and not (distinct and x in used)] for i in open_}  # @line L2
        if any(not fits[i] for i in open_):  # @line L3
            return
        s = min(open_, key=lambda i: len(fits[i]))  # @line L4
        for x in fits[s]:  # @line L5
            new = [cell for cell in all_slots[s] if cell not in letters]
            for cell, ch in zip(all_slots[s], x):  # @line L6
                letters[cell] = ch
            filled[s] = x
            used.add(x)
            search()  # @line L7
            used.discard(x)  # @line L8
            filled[s] = None
            for cell in new:
                del letters[cell]

    search()
    return found


def is_filling(grid, words, result, distinct=True):
    """Check a filled grid against the rules. A white cell in no slot may stay empty."""
    if len(result) != len(grid) or any(len(a) != len(b) for a, b in zip(result, grid)):
        return False
    covered = {cell for cells in slots(grid) for cell in cells}
    for r, (row, out) in enumerate(zip(grid, result)):
        for c, (a, b) in enumerate(zip(row, out)):
            if a == "#":
                if b != "#":
                    return False
            elif b == "#" or (b == "." and (r, c) in covered) or (a != "." and a != b):
                return False
    vocab = set(words)
    seen = []
    for cells in slots(grid):
        word = "".join(result[r][c] for r, c in cells)
        if word not in vocab:
            return False
        seen.append(word)
    return not distinct or len(seen) == len(set(seen))


def brute_force(grid, words, distinct=True):
    """All fillings, by trying every choice of a word for every slot."""
    words = sorted(set(words))
    all_slots = slots(grid)
    given = {(r, c): ch for r, row in enumerate(grid) for c, ch in enumerate(row)
             if ch not in "#."}
    choices = [[x for x in words if len(x) == len(cells)] for cells in all_slots]
    found = set()
    for pick in product(*choices):
        if distinct and len(set(pick)) != len(pick):
            continue
        letters = dict(given)
        good = True
        for cells, x in zip(all_slots, pick):
            for cell, ch in zip(cells, x):
                if letters.setdefault(cell, ch) != ch:
                    good = False
                    break
            if not good:
                break
        if good:
            found.add(tuple(_render(grid, letters)))
    return sorted(list(t) for t in found)
