# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/retrograde-analysis/. The authors are listed in prov/CADFGP.jsonl.

"""Retrograde analysis with exact distances to mate, layer by layer.

retrograde(game) works on any game object with these methods:

    positions()   all positions of the set S to be solved
    moves(p)      the positions after each legal move of p; a move that leaves S
                  (for example a capture into a smaller endgame) is given as None
    unmoves(q)    the positions p in S that have a move to q (the predecessors)
    lost(p)       True if p is a terminal loss for the side to move (a mate)

A move to None leads to a draw here, as in king and rook against king, where
the only way out of the set is the capture of the rook. It returns, for each
position, the value for the side to move (+1 win, -1 loss, 0 draw) and the
distance to mate in plies (None for a draw). The winner mates as fast as it
can, and the loser delays the mate as long as it can.

The toy game is king and rook against king on a 4 by 4 board (KRK4). It is a
chess-like toy, not chess: there are no pawns, no castling and no move counter.
"""

from typing import Dict, Iterable, List, Optional, Tuple

Pos = Tuple[int, int, int, int]  # (white king, white rook, black king, side to move: 0 white, 1 black)


def retrograde(game) -> Tuple[Dict, Dict]:
    """Label every position of game with its value and distance to mate.

    Precondition: unmoves is the inverse of moves on S. Cost: O(V + E) time
    for V positions and E moves, plus the cost of the move generators, and
    O(V) space for the labels and the counters.
    """
    val: Dict = {}
    dist: Dict = {}
    count: Dict = {}
    layer: List = []
    for p in game.positions():  # @line L1
        if game.lost(p):
            val[p], dist[p] = -1, 0
            layer.append(p)
    n = 0  # @line L2
    while layer:  # @line L3
        nxt: List = []
        for q in layer:  # @line L4
            for p in game.unmoves(q):
                if p in val:
                    continue
                if val[q] == -1:  # @line L5
                    val[p], dist[p] = 1, n + 1
                    nxt.append(p)
                else:  # q is won for its side to move
                    if p not in count:
                        count[p] = len(game.moves(p))
                    count[p] -= 1  # @line L6
                    if count[p] == 0:
                        val[p], dist[p] = -1, n + 1
                        nxt.append(p)
        layer, n = nxt, n + 1  # @line L7
    for p in game.positions():  # @line L8
        if p not in val:
            val[p], dist[p] = 0, None
    return val, dist


def forward_solve(game) -> Tuple[Dict, Dict]:
    """Reference: the sets W_n (win within n plies) and L_n (loss within n
    plies) computed forward from the moves, for n = 0, 1, 2, ... until they
    stop growing. A position in no set is a draw: neither side can force a
    mate, so the play can go on for ever or end in a draw."""
    ps = list(game.positions())
    kids = {p: game.moves(p) for p in ps}
    win: Dict = {}
    loss: Dict = {p: 0 for p in ps if game.lost(p)}
    n = 0
    while True:
        n += 1
        new_w = [p for p in ps if p not in win and any(c is not None and c in loss for c in kids[p])]
        new_l = [p for p in ps if p not in loss and kids[p] and all(c is not None and c in win for c in kids[p])]
        if not new_w and not new_l:
            break
        for p in new_w:
            win[p] = n
        for p in new_l:
            loss[p] = n
    val = {p: (1 if p in win else -1 if p in loss else 0) for p in ps}
    dist = {p: win.get(p, loss.get(p)) for p in ps}
    return val, dist


class GraphGame:
    """A game given as a directed graph. A vertex with no move is a loss for
    the side to move, unless it is in draws."""

    def __init__(self, succ: Dict[int, List[int]], draws: Iterable[int] = ()) -> None:
        self.succ = succ
        self.draws = set(draws)
        self.pred: Dict[int, List[int]] = {v: [] for v in succ}
        for p, qs in succ.items():
            for q in qs:
                self.pred[q].append(p)

    def positions(self):
        return list(self.succ)

    def moves(self, p):
        return self.succ[p]

    def unmoves(self, q):
        return self.pred[q]

    def lost(self, p):
        return not self.succ[p] and p not in self.draws


N = 4  # the board is N by N; a square is r * N + c


def _rc(s: int) -> Tuple[int, int]:
    return divmod(s, N)


def _adjacent(a: int, b: int) -> bool:
    (r1, c1), (r2, c2) = _rc(a), _rc(b)
    return max(abs(r1 - r2), abs(c1 - c2)) == 1


def _king_steps(s: int) -> List[int]:
    r, c = _rc(s)
    out = []
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if (dr or dc) and 0 <= r + dr < N and 0 <= c + dc < N:
                out.append((r + dr) * N + c + dc)
    return out


def _rook_rays(s: int, blockers: Iterable[int]) -> List[int]:
    """The squares a rook on s reaches, stopping before any blocker."""
    block = set(blockers)
    r, c = _rc(s)
    out = []
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        rr, cc = r + dr, c + dc
        while 0 <= rr < N and 0 <= cc < N and rr * N + cc not in block:
            out.append(rr * N + cc)
            rr, cc = rr + dr, cc + dc
    return out


def _rook_hits(s: int, blockers: Iterable[int]) -> List[int]:
    """The first blocker on each ray of a rook on s."""
    block = set(blockers)
    r, c = _rc(s)
    out = []
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        rr, cc = r + dr, c + dc
        while 0 <= rr < N and 0 <= cc < N:
            if rr * N + cc in block:
                out.append(rr * N + cc)
                break
            rr, cc = rr + dr, cc + dc
    return out


class KRK4:
    """King and rook against king on a 4 by 4 board, a chess-like toy.

    White has a king and a rook, Black has a king. Black loses when it is
    checkmated. Stalemate and the capture of the rook are draws; the capture
    leaves S and is given as the move None.
    """

    def legal(self, p: Pos) -> bool:
        wk, wr, bk, stm = p
        if len({wk, wr, bk}) < 3 or _adjacent(wk, bk):
            return False
        # The side that is not to move may not be in check.
        return not (stm == 0 and self.in_check(p))

    def in_check(self, p: Pos) -> bool:
        """True if the black king is attacked by the rook."""
        wk, wr, bk, _ = p
        return bk in _rook_hits(wr, [wk, bk])

    def positions(self) -> List[Pos]:
        out = []
        for wk in range(N * N):
            for wr in range(N * N):
                for bk in range(N * N):
                    for stm in (0, 1):
                        if self.legal((wk, wr, bk, stm)):
                            out.append((wk, wr, bk, stm))
        return out

    def moves(self, p: Pos) -> List[Optional[Pos]]:
        wk, wr, bk, stm = p
        out: List[Optional[Pos]] = []
        if stm == 0:
            for s in _king_steps(wk):
                if s != wr and s != bk and not _adjacent(s, bk):
                    out.append((s, wr, bk, 1))
            for s in _rook_rays(wr, [wk, bk]):
                out.append((wk, s, bk, 1))
        else:
            for s in _king_steps(bk):
                if s == wk or _adjacent(s, wk):
                    continue
                if s == wr:
                    out.append(None)  # the rook is taken: a draw
                    continue
                if s in _rook_hits(wr, [wk, s]):
                    continue  # the new square is attacked by the rook
                out.append((wk, wr, s, 0))
        return out

    def unmoves(self, q: Pos) -> List[Pos]:
        """The positions in S with a move to q. They are found from q alone,
        by moving a piece of the side that just moved backwards."""
        wk, wr, bk, stm = q
        out: List[Pos] = []
        if stm == 1:  # White just moved: undo a king step or a rook slide.
            for s in _king_steps(wk):
                p = (s, wr, bk, 0)
                if s != wr and s != bk and self.legal(p):
                    out.append(p)
            for s in _rook_rays(wr, [wk, bk]):
                p = (wk, s, bk, 0)
                if self.legal(p):
                    out.append(p)
        else:  # Black just moved: undo a king step. There is no uncapture.
            for s in _king_steps(bk):
                p = (wk, wr, s, 1)
                if s != wk and s != wr and self.legal(p):
                    out.append(p)
        return out

    def lost(self, p: Pos) -> bool:
        return p[3] == 1 and self.in_check(p) and not self.moves(p)
