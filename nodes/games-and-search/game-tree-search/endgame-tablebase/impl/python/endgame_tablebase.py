# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/endgame-tablebase/. The authors are listed in prov/Q9YYTV.jsonl.

"""An endgame tablebase for a chess-like toy: king and rook against king on
a 4 by 4 board (KRK4). It is a toy, not chess: no pawns, no castling, no move
counter. Black loses when checkmated; a stalemate or the capture of the rook
is a draw.

A position is (white king, white rook, black king, side to move), with the
squares numbered r * 4 + c. The table is a bytearray indexed by

    index = (king class * 16 + rook square) * 2 + side to move,

where the king class numbers the placements of the two kings up to the 8
symmetries of the square board. One byte per entry holds the value and the
distance to mate (DTM) in plies.
"""

from typing import Dict, List, Optional, Tuple

N = 4
Pos = Tuple[int, int, int, int]
UNUSED, DRAW = 0, 1


def _rc(s: int) -> Tuple[int, int]:
    return divmod(s, N)


def symmetries(n: int) -> List:
    """The 8 maps of the n by n board onto itself, as functions on squares."""
    maps = []
    for swap in (False, True):
        for fr in (False, True):
            for fc in (False, True):
                def f(s, swap=swap, fr=fr, fc=fc):
                    r, c = divmod(s, n)
                    if swap:
                        r, c = c, r
                    if fr:
                        r = n - 1 - r
                    if fc:
                        c = n - 1 - c
                    return r * n + c
                maps.append(f)
    return maps


def mirror_only(n: int) -> List:
    """The identity and the left-right mirror, the symmetries left when pawns are on the board."""
    return [lambda s: s, lambda s: (s // n) * n + (n - 1 - s % n)]


def _adjacent(a: int, b: int, n: int = N) -> bool:
    (r1, c1), (r2, c2) = divmod(a, n), divmod(b, n)
    return max(abs(r1 - r2), abs(c1 - c2)) == 1


def king_pair_classes(n: int, group: List) -> List[Tuple[int, int]]:
    """The legal placements of two kings (distinct, not adjacent) on an n by n
    board, one representative per class under the group, the least one."""
    reps = set()
    for a in range(n * n):
        for b in range(n * n):
            if a != b and not _adjacent(a, b, n):
                reps.add(min((g(a), g(b)) for g in group))
    return sorted(reps)


SYM = symmetries(N)
CLASSES = king_pair_classes(N, SYM)
CLASS_OF = {kp: i for i, kp in enumerate(CLASSES)}
SIZE = len(CLASSES) * N * N * 2


def canonical(p: Pos) -> Pos:
    """The least image of p under the 8 symmetries, comparing the kings first."""
    wk, wr, bk, stm = p
    best = min(((g(wk), g(bk)), g(wr)) for g in SYM)
    (cwk, cbk), cwr = best
    return (cwk, cwr, cbk, stm)


def index(p: Pos) -> int:
    """The table index of p. Positions related by a symmetry get the same index. O(8)."""
    cwk, cwr, cbk, stm = canonical(p)  # @line L1
    return (CLASS_OF[(cwk, cbk)] * N * N + cwr) * 2 + stm  # @line L2


def encode(value: int, dist: Optional[int]) -> int:
    return DRAW if value == 0 else 2 + 2 * dist + (1 if value == 1 else 0)


def decode(b: int) -> Tuple[int, Optional[int]]:
    if b == DRAW:
        return 0, None
    return (1 if b % 2 else -1), (b - 2) // 2


def _king_steps(s: int) -> List[int]:
    r, c = _rc(s)
    return [(r + dr) * N + c + dc for dr in (-1, 0, 1) for dc in (-1, 0, 1)
            if (dr or dc) and 0 <= r + dr < N and 0 <= c + dc < N]


def _rook_scan(s: int, blockers) -> Tuple[List[int], List[int]]:
    """The empty squares a rook on s reaches, and the first blocker on each ray."""
    block = set(blockers)
    r, c = _rc(s)
    free, hits = [], []
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        rr, cc = r + dr, c + dc
        while 0 <= rr < N and 0 <= cc < N:
            t = rr * N + cc
            if t in block:
                hits.append(t)
                break
            free.append(t)
            rr, cc = rr + dr, cc + dc
    return free, hits


def in_check(p: Pos) -> bool:
    wk, wr, bk, _ = p
    return bk in _rook_scan(wr, [wk, bk])[1]


def legal(p: Pos) -> bool:
    wk, wr, bk, stm = p
    if len({wk, wr, bk}) < 3 or _adjacent(wk, bk):
        return False
    return not (stm == 0 and in_check(p))


def all_positions() -> List[Pos]:
    return [(a, b, c, s) for a in range(N * N) for b in range(N * N) for c in range(N * N)
            for s in (0, 1) if legal((a, b, c, s))]


def moves(p: Pos, frozen: bool = False) -> List[Optional[Pos]]:
    """The positions after each legal move; None for the capture of the rook.
    With frozen true, the white king may not move (a variant with draws by
    endless play)."""
    wk, wr, bk, stm = p
    out: List[Optional[Pos]] = []
    if stm == 0:
        if not frozen:
            out += [(s, wr, bk, 1) for s in _king_steps(wk) if s != wr and s != bk and not _adjacent(s, bk)]
        out += [(wk, s, bk, 1) for s in _rook_scan(wr, [wk, bk])[0]]
    else:
        for s in _king_steps(bk):
            if s == wk or _adjacent(s, wk):
                continue
            if s == wr:
                out.append(None)
            elif s not in _rook_scan(wr, [wk, s])[1]:
                out.append((wk, wr, s, 0))
    return out


def unmoves(q: Pos, frozen: bool = False) -> List[Pos]:
    """The legal positions with a move to q, found by moving a piece backwards."""
    wk, wr, bk, stm = q
    if stm == 1:
        out = [] if frozen else [(s, wr, bk, 0) for s in _king_steps(wk) if s != wr and s != bk]
        out += [(wk, s, bk, 0) for s in _rook_scan(wr, [wk, bk])[0]]
    else:
        out = [(wk, wr, s, 1) for s in _king_steps(bk) if s != wk and s != wr]
    return [p for p in out if legal(p)]


def mated(p: Pos) -> bool:
    return p[3] == 1 and in_check(p) and not moves(p)


def _orbit(p: Pos) -> List[Pos]:
    wk, wr, bk, stm = p
    return list({(g(wk), g(wr), g(bk), stm) for g in SYM})


def build(frozen: bool = False) -> bytearray:
    """Build the table by retrograde analysis on the symmetry classes.

    The counter of a class is the number of distinct classes of its
    children, and the predecessors of a class are found from every position
    of its orbit. Cost: O(v + e) table steps for v classes and e class moves,
    each with O(8) work for the symmetries.
    """
    reps = sorted({canonical(p) for p in all_positions()})
    kids = {p: {None if c is None else canonical(c) for c in moves(p, frozen)} for p in reps}
    val: Dict[Pos, int] = {}
    dist: Dict[Pos, int] = {}
    count = {p: len(kids[p]) for p in reps}
    layer = [p for p in reps if mated(p)]
    for p in layer:
        val[p], dist[p] = -1, 0
    n = 0
    while layer:  # @line L3
        nxt = []
        for q in layer:
            preds = {canonical(p) for x in _orbit(q) for p in unmoves(x, frozen)}
            for p in preds:
                if p in val:
                    continue
                if val[q] == -1:
                    val[p], dist[p] = 1, n + 1
                    nxt.append(p)
                else:
                    count[p] -= 1
                    if count[p] == 0:
                        val[p], dist[p] = -1, n + 1
                        nxt.append(p)
        layer, n = nxt, n + 1
    table = bytearray(SIZE)
    for p in reps:
        table[index(p)] = encode(val.get(p, 0), dist.get(p))  # @line L4
    return table


def probe(table: bytearray, p: Pos) -> Tuple[int, Optional[int]]:
    """The value (+1, 0, -1 for the side to move) and DTM of a legal position. O(8)."""
    b = table[index(p)]  # @line L5
    return decode(b)  # @line L6
