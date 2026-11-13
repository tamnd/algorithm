# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minesweeper-consistency/. The authors are listed in prov/G792KA.jsonl.
"""Minesweeper consistency and inference by frontier backtracking.

A board is a list of rows. A cell is an int 0..8 (revealed, the number of
mines among its up to 8 neighbors) or None (unrevealed). Mines can only be
in unrevealed cells. An optional total gives the number of mines on the
whole board.

The unrevealed cells next to a number form the frontier. The frontier is
split into components that share no number; each component is solved by
backtracking, and the components are joined by a knapsack over their mine
counts, with a binomial factor for the unrevealed cells off the frontier.
"""

from fractions import Fraction
from math import comb


def _neighbors(h, w, r, c):
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if (dr or dc) and 0 <= r + dr < h and 0 <= c + dc < w:
                yield r + dr, c + dc


def constraints(board):
    """(unknown cells, mine count) for each number; None if a number is already broken."""
    h, w = len(board), len(board[0])
    out = []
    for r in range(h):
        for c in range(w):
            k = board[r][c]
            if k is None:
                continue
            cells = [nb for nb in _neighbors(h, w, r, c) if board[nb[0]][nb[1]] is None]
            if not 0 <= k <= len(cells):
                return None
            if cells:
                out.append((cells, k))
    return out


def _components(cons):
    """Group the constraints by shared cells, with a small union-find."""
    parent = {}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for cells, _ in cons:
        for cell in cells:
            parent.setdefault(cell, cell)
        for cell in cells[1:]:
            a, b = find(cells[0]), find(cell)
            if a != b:
                parent[a] = b
    groups = {}
    for cells, k in cons:
        groups.setdefault(find(cells[0]), []).append((cells, k))
    return list(groups.values())


def _solve_component(cons):
    """Backtracking over the cells of one component.

    Returns (cells, count, mine_count): count[m] is the number of placements
    with m mines, mine_count[m][i] the number of those with a mine on cells[i].
    """
    cells = []
    for cs, _ in cons:
        for cell in cs:
            if cell not in cells:
                cells.append(cell)
    index = {cell: i for i, cell in enumerate(cells)}
    cons_ix = [([index[cell] for cell in cs], k) for cs, k in cons]
    watch = [[] for _ in cells]
    for j, (ids, _) in enumerate(cons_ix):
        for i in ids:
            watch[i].append(j)
    n = len(cells)
    value = [-1] * n
    count = {}
    mine_count = {}

    def ok(i):
        for j in watch[i]:
            ids, k = cons_ix[j]
            mines = sum(1 for t in ids if value[t] == 1)
            open_ = sum(1 for t in ids if value[t] == -1)
            if mines > k or mines + open_ < k:  # @line L5
                return False
        return True

    def search(i, mines):
        if i == n:
            count[mines] = count.get(mines, 0) + 1  # @line L6
            row = mine_count.setdefault(mines, [0] * n)
            for t in range(n):
                row[t] += value[t]
            return
        for v in (0, 1):  # @line L4
            value[i] = v
            if ok(i):
                search(i + 1, mines + v)
            value[i] = -1

    search(0, 0)  # @line L3
    return cells, count, mine_count


def analyze(board, total=None):
    """Exact mine probabilities of the unrevealed cells, or None if inconsistent.

    Without a total, every placement that fits the numbers counts once.
    With a total, only placements with exactly that many mines count.
    """
    h, w = len(board), len(board[0])
    cons = constraints(board)  # @line L1
    if cons is None:
        return None
    comps = [_solve_component(group) for group in _components(cons)]  # @line L2
    if any(not count for _, count, _ in comps):
        return None
    frontier = {cell for cells, _, _ in comps for cell in cells}
    interior = [(r, c) for r in range(h) for c in range(w)
                if board[r][c] is None and (r, c) not in frontier]
    q = len(interior)
    # ways[s] = number of frontier placements with s mines in all, by a knapsack.
    ways = {0: 1}
    for _, count, _ in comps:  # @line L7
        new = {}
        for s, a in ways.items():
            for m, b in count.items():
                new[s + m] = new.get(s + m, 0) + a * b
        ways = new

    def weight(s):
        if total is None:
            return 2 ** q
        return comb(q, total - s) if 0 <= total - s <= q else 0

    norm = sum(a * weight(s) for s, a in ways.items())
    if norm == 0:
        return None  # @line L8
    prob = {}
    for idx, (cells, count, mine_count) in enumerate(comps):
        # Placements of all other components, by their mine total.
        rest = {0: 1}
        for jdx, (_, other, _) in enumerate(comps):
            if jdx == idx:
                continue
            new = {}
            for s, a in rest.items():
                for m, b in other.items():
                    new[s + m] = new.get(s + m, 0) + a * b
            rest = new
        for t, cell in enumerate(cells):
            num = 0
            for m, row in mine_count.items():
                for s, a in rest.items():
                    num += row[t] * a * weight(m + s)
            prob[cell] = Fraction(num, norm)
    if q:
        if total is None:
            p_in = Fraction(1, 2)
        else:
            num = sum(a * comb(q - 1, total - s - 1) for s, a in ways.items() if 1 <= total - s <= q)
            p_in = Fraction(num, norm)
        for cell in interior:
            prob[cell] = p_in
    return prob


def consistent(board, total=None):
    return analyze(board, total) is not None


def safe_cells(board, total=None):
    """Unrevealed cells that hold no mine in any consistent placement."""
    prob = analyze(board, total)
    if prob is None:
        return None
    return sorted(cell for cell, p in prob.items() if p == 0)


def mine_cells(board, total=None):
    """Unrevealed cells that hold a mine in every consistent placement."""
    prob = analyze(board, total)
    if prob is None:
        return None
    return sorted(cell for cell, p in prob.items() if p == 1)


def brute_force(board, total=None):
    """Mine probabilities by listing all placements of mines in the unrevealed cells."""
    h, w = len(board), len(board[0])
    unknown = [(r, c) for r in range(h) for c in range(w) if board[r][c] is None]
    hits = [0] * len(unknown)
    good = 0
    for mask in range(1 << len(unknown)):
        mines = {unknown[i] for i in range(len(unknown)) if mask >> i & 1}
        if total is not None and len(mines) != total:
            continue
        fits = all(board[r][c] is None or board[r][c] == sum(nb in mines for nb in _neighbors(h, w, r, c))
                   for r in range(h) for c in range(w))
        if fits:
            good += 1
            for i in range(len(unknown)):
                hits[i] += mask >> i & 1
    if good == 0:
        return None
    return {cell: Fraction(hits[i], good) for i, cell in enumerate(unknown)}
