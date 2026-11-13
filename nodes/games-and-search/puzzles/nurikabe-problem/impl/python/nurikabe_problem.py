# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nurikabe-problem/. The authors are listed in prov/69KGGJ.jsonl.
"""Nurikabe solver: backtracking over cells with constraint propagation.

A board is a list of rows; a cell holds a positive clue or 0 (no clue).
A shading is a list of rows with 1 (black, sea), 0 (white, island) or -1
(unknown). Clue cells are always white.

Rules: each white component holds exactly one clue and has as many cells
as the clue; the black cells form one connected set; no 2 by 2 block is all
black.
"""


def _neighbors(h, w, r, c):
    if r > 0:
        yield r - 1, c
    if r + 1 < h:
        yield r + 1, c
    if c > 0:
        yield r, c - 1
    if c + 1 < w:
        yield r, c + 1


def _components(h, w, cells):
    """Connected components (4-neighbor) of a set of cells."""
    seen = set()
    out = []
    for start in cells:
        if start in seen:
            continue
        seen.add(start)
        comp = [start]
        stack = [start]
        while stack:
            r, c = stack.pop()
            for nb in _neighbors(h, w, r, c):
                if nb in cells and nb not in seen:
                    seen.add(nb)
                    comp.append(nb)
                    stack.append(nb)
        out.append(comp)
    return out


def _black_pool(h, w, shade):
    for r in range(h - 1):
        for c in range(w - 1):
            if shade[r][c] == 1 and shade[r + 1][c] == 1 and shade[r][c + 1] == 1 and shade[r + 1][c + 1] == 1:
                return True
    return False


def is_solution(board, shade):
    """Check a complete shading against the three rules."""
    h, w = len(board), len(board[0])
    if any(v == -1 for row in shade for v in row):
        return False
    if any(board[r][c] and shade[r][c] for r in range(h) for c in range(w)):
        return False
    if _black_pool(h, w, shade):
        return False
    white = {(r, c) for r in range(h) for c in range(w) if shade[r][c] == 0}
    for comp in _components(h, w, white):
        clues = [board[r][c] for r, c in comp if board[r][c]]
        if len(clues) != 1 or clues[0] != len(comp):
            return False
    black = {(r, c) for r in range(h) for c in range(w) if shade[r][c] == 1}
    return len(_components(h, w, black)) <= 1


def _check_and_propagate(board, shade):
    """Apply forced moves in place. Return False if the partial shading is dead."""
    h, w = len(board), len(board[0])
    total = sum(v for row in board for v in row)
    changed = True
    while changed:
        changed = False
        if _black_pool(h, w, shade):
            return False
        white = {(r, c) for r in range(h) for c in range(w) if shade[r][c] == 0}
        unknown = {(r, c) for r in range(h) for c in range(w) if shade[r][c] == -1}
        if len(white) > total or len(white) + len(unknown) < total:
            return False
        owner = {}
        for idx, comp in enumerate(_components(h, w, white)):
            clues = [board[r][c] for r, c in comp if board[r][c]]
            if len(clues) > 1:
                return False
            frontier = {nb for r, c in comp for nb in _neighbors(h, w, r, c) if nb in unknown}
            if clues:
                need = clues[0]
                if len(comp) > need:
                    return False
                if len(comp) < need and not frontier:
                    return False
                if len(comp) == need and frontier:
                    # A finished island is walled in by sea.
                    for r, c in frontier:
                        shade[r][c] = 1
                    changed = True
                    break
                for cell in comp:
                    owner[cell] = idx
            elif not frontier:
                return False
        if changed:
            continue
        # An unknown cell next to two different clued islands must be sea.
        for r, c in unknown:
            ids = {owner[nb] for nb in _neighbors(h, w, r, c) if nb in owner}
            if len(ids) > 1:
                shade[r][c] = 1
                changed = True
        if changed:
            continue
        # All sea cells must be joinable through sea or unknown cells.
        black = {(r, c) for r in range(h) for c in range(w) if shade[r][c] == 1}
        if black:
            reach = None
            for comp in _components(h, w, black | unknown):
                if black & set(comp):
                    if reach is not None:
                        return False
                    reach = comp
    return True


def solve(board, limit=None):
    """All solutions, found by propagation and a branch on one unknown cell."""
    h, w = len(board), len(board[0])
    out = []
    start = [[0 if board[r][c] else -1 for c in range(w)] for r in range(h)]
    stack = [start]  # @line L1
    while stack:  # @line L2
        shade = stack.pop()  # @line L3
        alive = _check_and_propagate(board, shade)  # @line L4
        if not alive:
            continue  # @line L5
        unknown = [(r, c) for r in range(h) for c in range(w) if shade[r][c] == -1]
        if not unknown:
            if is_solution(board, shade):  # @line L6
                out.append(shade)
                if limit is not None and len(out) >= limit:
                    break
            continue
        r, c = unknown[0]  # @line L7
        for v in (1, 0):
            child = [list(row) for row in shade]
            child[r][c] = v
            stack.append(child)  # @line L8
    return out


def brute_force(board):
    """All solutions, found by trying every shading of the cells without a clue."""
    h, w = len(board), len(board[0])
    free = [(r, c) for r in range(h) for c in range(w) if not board[r][c]]
    out = []
    for mask in range(1 << len(free)):
        shade = [[0] * w for _ in range(h)]
        for i, (r, c) in enumerate(free):
            if mask >> i & 1:
                shade[r][c] = 1
        if is_solution(board, shade):
            out.append(shade)
    return out
