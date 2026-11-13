# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kociemba-algorithm/. The authors are listed in prov/42Y3XQ.jsonl.
"""Kociemba's two-phase algorithm for the Rubik's cube.

The cube is stored at the cubie level. Corners URF, UFL, ULB, UBR, DFR, DLF,
DBL, DRB are 0..7 and edges UR, UF, UL, UB, DR, DF, DL, DB, FR, FL, BL, BR
are 0..11. A cube is (cp, co, ep, eo): cp[i] is the corner in position i and
co[i] its twist, and the same for edges. Moves are named U, U2, U' and so on,
in the half-turn metric.

Phase 1 takes the cube into G1 = <U, D, R2, L2, F2, B2>, the cubes with no
corner twist, no edge flip and the four middle-slice edges in the middle
slice. Phase 2 solves the cube inside G1 with those six generators. Both
phases are IDA* searches over small coordinates with pruning tables built by
breadth-first search.
"""

from collections import deque
from itertools import combinations
from math import factorial
from typing import Callable, Dict, Iterator, List, Optional, Sequence, Tuple

Cube = Tuple[Tuple[int, ...], Tuple[int, ...], Tuple[int, ...], Tuple[int, ...]]

SOLVED: Cube = (tuple(range(8)), (0,) * 8, tuple(range(12)), (0,) * 12)

_BASIC = {
    "U": ((3, 0, 1, 2, 4, 5, 6, 7), (0,) * 8,
          (3, 0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11), (0,) * 12),
    "R": ((4, 1, 2, 0, 7, 5, 6, 3), (2, 0, 0, 1, 1, 0, 0, 2),
          (8, 1, 2, 3, 11, 5, 6, 7, 4, 9, 10, 0), (0,) * 12),
    "F": ((1, 5, 2, 3, 0, 4, 6, 7), (1, 2, 0, 0, 2, 1, 0, 0),
          (0, 9, 2, 3, 4, 8, 6, 7, 1, 5, 10, 11), (0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0)),
    "D": ((0, 1, 2, 3, 5, 6, 7, 4), (0,) * 8,
          (0, 1, 2, 3, 5, 6, 7, 4, 8, 9, 10, 11), (0,) * 12),
    "L": ((0, 2, 6, 3, 4, 1, 5, 7), (0, 1, 2, 0, 0, 2, 1, 0),
          (0, 1, 10, 3, 4, 5, 9, 7, 8, 2, 6, 11), (0,) * 12),
    "B": ((0, 1, 3, 7, 4, 5, 2, 6), (0, 0, 1, 2, 0, 0, 2, 1),
          (0, 1, 2, 11, 4, 5, 6, 10, 8, 9, 3, 7), (0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1)),
}
FACES = "URFDLB"
OPPOSITE = {"U": "D", "D": "U", "R": "L", "L": "R", "F": "B", "B": "F"}


def multiply(a: Cube, b: Cube) -> Cube:
    """The cube a followed by the move or cube b."""
    acp, aco, aep, aeo = a
    bcp, bco, bep, beo = b
    return (tuple(acp[bcp[i]] for i in range(8)),
            tuple((aco[bcp[i]] + bco[i]) % 3 for i in range(8)),
            tuple(aep[bep[i]] for i in range(12)),
            tuple((aeo[bep[i]] + beo[i]) % 2 for i in range(12)))


MOVES: Dict[str, Cube] = {}
for _f in FACES:
    _c = _BASIC[_f]
    MOVES[_f] = _c
    MOVES[_f + "2"] = multiply(_c, _c)
    MOVES[_f + "'"] = multiply(MOVES[_f + "2"], _c)
ALL_MOVES = [f + s for f in FACES for s in ("", "2", "'")]
PHASE2_MOVES = ["U", "U2", "U'", "D", "D2", "D'", "R2", "L2", "F2", "B2"]


def apply(cube: Cube, seq: Sequence[str]) -> Cube:
    for m in seq:
        cube = multiply(cube, MOVES[m])
    return cube


def parse(text: str) -> List[str]:
    return text.split()


def inverse(seq: Sequence[str]) -> List[str]:
    flip = {"": "'", "'": "", "2": "2"}
    return [m[0] + flip[m[1:]] for m in reversed(seq)]


# Coordinates ----------------------------------------------------------------

_SLICE_INDEX = {frozenset(c): k for k, c in enumerate(combinations(range(12), 4))}


def twist(c: Cube) -> int:
    v = 0
    for x in c[1][:7]:
        v = 3 * v + x
    return v


def flip(c: Cube) -> int:
    v = 0
    for x in c[3][:11]:
        v = 2 * v + x
    return v


def slice_coord(c: Cube) -> int:
    """Which 4 of the 12 edge positions hold the middle-slice edges FR, FL, BL, BR."""
    return _SLICE_INDEX[frozenset(i for i, e in enumerate(c[2]) if e >= 8)]


def rank(perm: Sequence[int]) -> int:
    """Lehmer rank of a permutation of distinct values."""
    n = len(perm)
    r = 0
    for i in range(n):
        smaller = sum(1 for j in range(i + 1, n) if perm[j] < perm[i])
        r += smaller * factorial(n - 1 - i)
    return r


def corner_perm(c: Cube) -> int:
    return rank(c[0])


def ud_edge_perm(c: Cube) -> int:
    return rank(c[2][:8])


def slice_perm(c: Cube) -> int:
    return rank(c[2][8:])


def in_g1(c: Cube) -> bool:
    return twist(c) == 0 and flip(c) == 0 and all(e >= 8 for e in c[2][8:])


# Tables ---------------------------------------------------------------------

def move_table(coord: Callable[[Cube], int], moves: Sequence[str]) -> Dict[int, List[int]]:
    """table[v][k] = coordinate after move k from any cube with coordinate v.

    The coordinates used here are well defined on cosets, so one representative
    cube per value is enough; the values are found by breadth-first search.
    """
    rep = {coord(SOLVED): SOLVED}
    queue = deque([SOLVED])
    table: Dict[int, List[int]] = {}
    while queue:
        cube = queue.popleft()
        v = coord(cube)
        row = []
        for m in moves:
            nxt = multiply(cube, MOVES[m])
            w = coord(nxt)
            row.append(w)
            if w not in rep:
                rep[w] = nxt
                queue.append(nxt)
        table[v] = row
    return table


def pruning_table(a: Dict[int, List[int]], b: Dict[int, List[int]],
                  a0: int, b0: int) -> Tuple[bytearray, int]:
    """Exact distance to (a0, b0) in the product of two coordinates.

    Entry a * size_b + b of the returned array is the distance, or 255 if
    the pair is not reachable. Returns (array, size_b).
    """
    na = max(a) + 1
    nb = max(b) + 1
    dist = bytearray([255]) * (na * nb)
    nmoves = len(a[a0])
    arow = [a.get(x, [0] * nmoves) for x in range(na)]
    brow = [b.get(y, [0] * nmoves) for y in range(nb)]
    dist[a0 * nb + b0] = 0
    frontier = [(a0, b0)]
    d = 0
    while frontier:
        d += 1
        nxt = []
        for x, y in frontier:
            ra, rb = arow[x], brow[y]
            for k in range(nmoves):
                u, v = ra[k], rb[k]
                i = u * nb + v
                if dist[i] == 255:
                    dist[i] = d
                    nxt.append((u, v))
        frontier = nxt
    return dist, nb


class Tables:
    """Move and pruning tables for both phases (built once, a few seconds)."""

    def __init__(self) -> None:
        self.tw = move_table(twist, ALL_MOVES)
        self.fl = move_table(flip, ALL_MOVES)
        self.sl = move_table(slice_coord, ALL_MOVES)
        self.sl0 = slice_coord(SOLVED)
        self.p_sl_tw, self.n_tw = pruning_table(self.sl, self.tw, self.sl0, 0)
        self.p_sl_fl, self.n_fl = pruning_table(self.sl, self.fl, self.sl0, 0)
        self.cp = move_table(corner_perm, PHASE2_MOVES)
        self.ep = move_table(ud_edge_perm, PHASE2_MOVES)
        self.sp = move_table(slice_perm, PHASE2_MOVES)
        self.p_cp_sp, self.n_sp = pruning_table(self.cp, self.sp, 0, 0)
        self.p_ep_sp, _ = pruning_table(self.ep, self.sp, 0, 0)

    def h1(self, tw: int, fl: int, sl: int) -> int:
        return max(self.p_sl_tw[sl * self.n_tw + tw], self.p_sl_fl[sl * self.n_fl + fl])

    def h2(self, cp: int, ep: int, sp: int) -> int:
        return max(self.p_cp_sp[cp * self.n_sp + sp], self.p_ep_sp[ep * self.n_sp + sp])


_TABLES: Optional[Tables] = None


def tables() -> Tables:
    global _TABLES
    if _TABLES is None:
        _TABLES = Tables()
    return _TABLES


# Search ---------------------------------------------------------------------

def _allowed(prev: Optional[str], move: str) -> bool:
    """Skip a turn of the same face, and fix the order of opposite faces."""
    if prev is None:
        return True
    if move[0] == prev[0]:
        return False
    return not (OPPOSITE[move[0]] == prev[0] and FACES.index(move[0]) < FACES.index(prev[0]))


G1_MOVES = set(PHASE2_MOVES)


def phase1_sequences(t: Tables, cube: Cube, depth: int) -> Iterator[List[str]]:
    """Every canonical sequence of exactly depth moves that takes cube into G1
    and does not end with a G1 move (an IDA* iteration with bound depth)."""
    path: List[str] = []
    idx = {m: k for k, m in enumerate(ALL_MOVES)}

    def dfs(tw: int, fl: int, sl: int, left: int) -> Iterator[List[str]]:
        if left == 0:
            if tw == 0 and fl == 0 and sl == t.sl0 and (not path or path[-1] not in G1_MOVES):
                yield list(path)
            return
        if t.h1(tw, fl, sl) > left:
            return
        prev = path[-1] if path else None
        for m in ALL_MOVES:
            if not _allowed(prev, m):
                continue
            k = idx[m]
            path.append(m)
            yield from dfs(t.tw[tw][k], t.fl[fl][k], t.sl[sl][k], left - 1)
            path.pop()

    yield from dfs(twist(cube), flip(cube), slice_coord(cube), depth)


def phase2(t: Tables, cube: Cube, limit: int) -> Optional[List[str]]:
    """A shortest sequence of G1 moves of length at most limit that solves a
    cube in G1, by IDA* with the phase-2 pruning tables, or None."""
    start = (corner_perm(cube), ud_edge_perm(cube), slice_perm(cube))
    path: List[str] = []

    def dfs(cp: int, ep: int, sp: int, left: int) -> bool:
        if cp == 0 and ep == 0 and sp == 0:
            return True
        if left == 0 or t.h2(cp, ep, sp) > left:
            return False
        prev = path[-1] if path else None
        for k, m in enumerate(PHASE2_MOVES):
            if not _allowed(prev, m):
                continue
            path.append(m)
            if dfs(t.cp[cp][k], t.ep[ep][k], t.sp[sp][k], left - 1):
                return True
            path.pop()
        return False

    for bound in range(t.h2(*start), limit + 1):
        if dfs(start[0], start[1], start[2], bound):
            return path
    return None


def solve(cube: Cube, max_length: int = 30, first_only: bool = True) -> Optional[List[str]]:
    """Kociemba's two-phase algorithm.

    With first_only, return the first solution found (at most 12 + 18 = 30
    moves). Without it, keep lengthening phase 1 until it alone is as long
    as the best solution; the result is then a shortest solution.
    """
    t = tables()  # @line L1
    best: Optional[List[str]] = None  # @line L2
    for d1 in range(0, max_length + 1):  # @line L3
        if best is not None and d1 >= len(best):  # @line L4
            return best
        for p in phase1_sequences(t, cube, d1):  # @line L5
            c2 = apply(cube, p)  # @line L6
            limit = (len(best) - 1 if best is not None else max_length) - d1  # @line L7
            q = phase2(t, c2, limit) if limit >= 0 else None  # @line L8
            if q is not None:  # @line L9
                best = p + q
                if first_only:
                    return best
    return best  # @line L10
