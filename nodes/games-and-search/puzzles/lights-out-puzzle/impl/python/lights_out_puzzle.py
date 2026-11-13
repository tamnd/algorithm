# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lights-out-puzzle/. The authors are listed in prov/XKXX36.jsonl.
"""Lights Out on an r x c grid: Gaussian elimination over GF(2), light chasing, brute force.

Cell (i, j) has index i * c + j. A board or a set of presses is an integer
bit mask over the cells. Pressing a cell toggles it and its orthogonal
neighbours. A board is solved when every light is off.
"""

from typing import List, Optional, Sequence, Tuple


def press_masks(r: int, c: int) -> List[int]:
    """Mask of the cells that pressing each cell toggles (the rows of A + I)."""
    masks = []
    for i in range(r):
        for j in range(c):
            m = 1 << (i * c + j)
            if i > 0:
                m |= 1 << ((i - 1) * c + j)
            if i < r - 1:
                m |= 1 << ((i + 1) * c + j)
            if j > 0:
                m |= 1 << (i * c + j - 1)
            if j < c - 1:
                m |= 1 << (i * c + j + 1)
            masks.append(m)
    return masks


def graph_masks(adj: Sequence[Sequence[int]]) -> List[int]:
    """The same masks for Lights Out on any graph, given adjacency lists."""
    return [(1 << v) | sum(1 << u for u in set(adj[v])) for v in range(len(adj))]


def effect(masks: Sequence[int], presses: int) -> int:
    """The board toggled by a set of presses."""
    out = 0
    k = 0
    while presses:
        if presses & 1:
            out ^= masks[k]
        presses >>= 1
        k += 1
    return out


def eliminate(masks: Sequence[int], board: int) -> Tuple[Optional[int], int, List[int]]:
    """Solve (A + I) x = b over GF(2) by Gauss-Jordan elimination.

    The matrix is symmetric, so row v of the system is masks[v]: cell v is
    toggled by the presses in masks[v]. Returns (one solution or None, rank,
    a basis of the null space).
    """
    n = len(masks)
    rows = [masks[v] | (((board >> v) & 1) << n) for v in range(n)]
    pivots: List[int] = []
    rank = 0
    for col in range(n):
        bit = 1 << col
        p = next((k for k in range(rank, n) if rows[k] & bit), None)
        if p is None:
            continue
        rows[rank], rows[p] = rows[p], rows[rank]
        for k in range(n):
            if k != rank and rows[k] & bit:
                rows[k] ^= rows[rank]
        pivots.append(col)
        rank += 1
    full = (1 << n) - 1
    if any(rows[k] >> n for k in range(rank, n)):
        solution = None
    else:
        solution = 0
        for k, col in enumerate(pivots):
            if rows[k] >> n:
                solution |= 1 << col
    free = [col for col in range(n) if col not in set(pivots)]
    basis = []
    for f in free:
        x = 1 << f
        for k, col in enumerate(pivots):
            if rows[k] & full & (1 << f):
                x |= 1 << col
        basis.append(x)
    return solution, rank, basis


def solve(r: int, c: int, board: int) -> Optional[int]:
    """One set of presses that turns every light off, or None."""
    return eliminate(press_masks(r, c), board)[0]


def rank(r: int, c: int) -> int:
    return eliminate(press_masks(r, c), 0)[1]


def fewest_presses(r: int, c: int, board: int) -> Optional[int]:
    """A solution with the fewest presses, by trying every null-space combination."""
    x, _, basis = eliminate(press_masks(r, c), board)
    if x is None:
        return None
    best = x
    for s in range(1, 1 << len(basis)):
        y = x
        for k, b in enumerate(basis):
            if s >> k & 1:
                y ^= b
        if bin(y).count("1") < bin(best).count("1"):
            best = y
    return best


def brute_force(r: int, c: int, board: int) -> List[int]:
    """All 2^(rc) press sets that solve the board, by trying each one."""
    masks = press_masks(r, c)
    return [x for x in range(1 << (r * c)) if effect(masks, x) == board]


def light_chasing(r: int, c: int, board: int) -> Optional[int]:
    """Solve by chasing the lights down with the first row of presses as unknowns.

    Each light is tracked as an affine function of the c first-row presses:
    bits 0 .. c - 1 give the variables, bit c the constant. Pressing the cell
    below every lit cell clears rows 0 .. r - 2; the last row then gives c
    equations in c unknowns. Time O(r c^2) word operations for the chase
    plus O(c^3) for the small system.
    """
    const = 1 << c
    light = [[const if (board >> (i * c + j)) & 1 else 0 for j in range(c)] for i in range(r)]
    press = [[0] * c for _ in range(r)]

    def do(i: int, j: int, f: int) -> None:
        press[i][j] ^= f
        for di, dj in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
            a, b = i + di, j + dj
            if 0 <= a < r and 0 <= b < c:
                light[a][b] ^= f

    for j in range(c):
        do(0, j, 1 << j)
    for i in range(1, r):
        for j in range(c):
            do(i, j, light[i - 1][j])
    # The last row must be dark: solve light[r - 1][j] = 0 for all j.
    eqs = list(light[r - 1])
    x_val = 0
    pivots = []
    k = 0
    for col in range(c):
        p = next((t for t in range(k, c) if eqs[t] >> col & 1), None)
        if p is None:
            continue
        eqs[k], eqs[p] = eqs[p], eqs[k]
        for t in range(c):
            if t != k and eqs[t] >> col & 1:
                eqs[t] ^= eqs[k]
        pivots.append(col)
        k += 1
    if any(eqs[t] for t in range(k, c)):
        return None
    for t, col in enumerate(pivots):
        if eqs[t] & const:
            x_val |= 1 << col
    out = 0
    for i in range(r):
        for j in range(c):
            f = press[i][j]
            v = (bin(f & x_val & (const - 1)).count("1") + (1 if f & const else 0)) & 1
            if v:
                out |= 1 << (i * c + j)
    return out
