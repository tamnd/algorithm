# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gods-number/. The authors are listed in prov/YQFNF0.jsonl.
"""Two checks around God's number.

1. The counting lower bound: there are fewer canonical move sequences of
   length at most k than cube positions, for every k below the bound.
2. God's number of the 2 x 2 x 2 cube, by breadth-first search over all
   3,674,160 positions, in the half-turn and the quarter-turn metric.

The values 20 and 26 for the 3 x 3 x 3 cube come from a computation far too
large to repeat here; see the references on the page.
"""

from math import factorial
from typing import Dict, List, Sequence, Tuple

CUBE_POSITIONS = factorial(8) * 3 ** 7 * factorial(12) * 2 ** 11 // 2
POCKET_POSITIONS = factorial(7) * 3 ** 6

FACES = "URFDLB"
AXIS = {"U": 0, "D": 0, "R": 1, "L": 1, "F": 2, "B": 2}


def canonical_counts_htm(k: int) -> List[int]:
    """Number of move sequences of each length 0..k in the half-turn metric
    with no two turns of the same face in a row and, for two opposite faces
    in a row, only one of the two orders. Every position at distance d is
    reached by at least one such sequence of length d."""
    # state: the last face, or None at the start
    counts = [1]
    ways: Dict[object, int] = {None: 1}
    for _ in range(k):
        nxt: Dict[object, int] = {}
        for last, w in ways.items():
            for f in FACES:
                if last is not None:
                    if f == last:
                        continue
                    if AXIS[f] == AXIS[last] and FACES.index(f) < FACES.index(last):
                        continue
                nxt[f] = nxt.get(f, 0) + 3 * w
        ways = nxt
        counts.append(sum(ways.values()))
    return counts


def canonical_counts_qtm(k: int) -> List[int]:
    """The same in the quarter-turn metric: a turn may follow a turn of the
    same face in the same direction once (two quarter turns make a half
    turn), never in the opposite direction, and opposite faces are ordered.
    The state is the last face, its direction and how many times in a row."""
    counts = [1]
    ways: Dict[object, int] = {None: 1}
    for _ in range(k):
        nxt: Dict[object, int] = {}
        for state, w in ways.items():
            for f in FACES:
                for d in (1, -1):
                    if state is None:
                        key = (f, d, 1)
                    else:
                        lf, ld, run = state
                        if f == lf:
                            if d != ld or run == 2:
                                continue
                            key = (f, d, 2)
                        else:
                            if AXIS[f] == AXIS[lf] and FACES.index(f) < FACES.index(lf):
                                continue
                            key = (f, d, 1)
                    nxt[key] = nxt.get(key, 0) + w
        ways = nxt
        counts.append(sum(ways.values()))
    return counts


def counting_lower_bound(counts: Sequence[int], positions: int) -> int:
    """The least k such that the sequences of length at most k could cover
    all positions; every k below it leaves some position unreached."""
    total = 0
    for k, c in enumerate(counts):
        total += c
        if total >= positions:
            return k
    raise ValueError("not enough lengths")


def parity_lower_bound_qtm(counts: Sequence[int], positions: int) -> int:
    """In the quarter-turn metric every move is an odd permutation of the
    corners, so the half of the positions with odd corner permutation lie at
    odd distances only, and the other half at even distances only. The
    bound is the least odd k such that odd lengths up to k cover half."""
    total = 0
    for k, c in enumerate(counts):
        if k % 2 == 1:
            total += c
            if total >= positions // 2:
                return k
    raise ValueError("not enough lengths")


# The 3 x 3 x 3 cube, for short distances ------------------------------------
# Corners URF, UFL, ULB, UBR, DFR, DLF, DBL, DRB = 0..7 and edges UR, UF, UL,
# UB, DR, DF, DL, DB, FR, FL, BL, BR = 0..11.

_EDGE_MOVES = {
    "U": ((3, 0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11), (0,) * 12),
    "R": ((8, 1, 2, 3, 11, 5, 6, 7, 4, 9, 10, 0), (0,) * 12),
    "F": ((0, 9, 2, 3, 4, 8, 6, 7, 1, 5, 10, 11), (0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0)),
    "D": ((0, 1, 2, 3, 5, 6, 7, 4, 8, 9, 10, 11), (0,) * 12),
    "L": ((0, 1, 10, 3, 4, 5, 9, 7, 8, 2, 6, 11), (0,) * 12),
    "B": ((0, 1, 2, 11, 4, 5, 6, 10, 8, 9, 3, 7), (0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1)),
}
_OTHER_CORNER_MOVES = {
    "D": ((0, 1, 2, 3, 5, 6, 7, 4), (0,) * 8),
    "L": ((0, 2, 6, 3, 4, 1, 5, 7), (0, 1, 2, 0, 0, 2, 1, 0)),
    "B": ((0, 1, 3, 7, 4, 5, 2, 6), (0, 0, 1, 2, 0, 0, 2, 1)),
}


def cube_layers(radius: int, metric: str) -> List[int]:
    """Number of 3 x 3 x 3 positions at each distance 0..radius, by
    breadth-first search. Only small radii are feasible."""
    def mul(a, b):
        return (tuple(a[0][b[0][i]] for i in range(8)),
                tuple((a[1][b[0][i]] + b[1][i]) % 3 for i in range(8)),
                tuple(a[2][b[2][i]] for i in range(12)),
                tuple((a[3][b[2][i]] + b[3][i]) % 2 for i in range(12)))

    corners = dict(_CORNER_MOVES)
    corners.update(_OTHER_CORNER_MOVES)
    moves = []
    for f in FACES:
        m = corners[f] + _EDGE_MOVES[f]
        m2 = mul(m, m)
        m3 = mul(m2, m)
        moves += [m, m2, m3] if metric == "htm" else [m, m3]
    start = (tuple(range(8)), (0,) * 8, tuple(range(12)), (0,) * 12)
    seen = {start}
    frontier = [start]
    counts = [1]
    for _ in range(radius):
        nxt = []
        for c in frontier:
            for m in moves:
                n = mul(c, m)
                if n not in seen:
                    seen.add(n)
                    nxt.append(n)
        frontier = nxt
        counts.append(len(nxt))
    return counts


# The 2 x 2 x 2 cube --------------------------------------------------------
# Corners URF, UFL, ULB, UBR, DFR, DLF, DBL, DRB = 0..7. Turning U, R and F
# only keeps corner DBL fixed, so every position has one representative.

_CORNER_MOVES = {
    "U": ((3, 0, 1, 2, 4, 5, 6, 7), (0, 0, 0, 0, 0, 0, 0, 0)),
    "R": ((4, 1, 2, 0, 7, 5, 6, 3), (2, 0, 0, 1, 1, 0, 0, 2)),
    "F": ((1, 5, 2, 3, 0, 4, 6, 7), (1, 2, 0, 0, 2, 1, 0, 0)),
}
Corners = Tuple[Tuple[int, ...], Tuple[int, ...]]


def corner_multiply(a: Corners, b: Corners) -> Corners:
    return (tuple(a[0][b[0][i]] for i in range(8)),
            tuple((a[1][b[0][i]] + b[1][i]) % 3 for i in range(8)))


def pocket_moves(metric: str) -> List[Corners]:
    out = []
    for f in "URF":
        m = _CORNER_MOVES[f]
        m2 = corner_multiply(m, m)
        m3 = corner_multiply(m2, m)
        out += [m, m2, m3] if metric == "htm" else [m, m3]
    return out


def pocket_distances(metric: str) -> List[int]:
    """Number of 2 x 2 x 2 positions at each distance from the solved one.

    A position is (permutation, orientation); both parts have their own move
    tables, built from one representative each, and the search runs over
    the 5040 x 729 index pairs in a byte array.
    """
    moves = pocket_moves(metric)
    solved: Corners = (tuple(range(8)), (0,) * 8)

    def table(key, start):
        index = {key(start): 0}
        reps = [start]
        rows = []
        i = 0
        while i < len(reps):
            row = []
            for m in moves:
                n = corner_multiply(reps[i], m)
                k = key(n)
                if k not in index:
                    index[k] = len(reps)
                    reps.append(n)
                row.append(index[k])
            rows.append(row)
            i += 1
        return rows

    perm = table(lambda c: c[0], solved)
    ori = table(lambda c: c[1], solved)
    np_, no = len(perm), len(ori)
    dist = bytearray([255]) * (np_ * no)
    dist[0] = 0
    frontier = [0]
    counts = [1]
    d = 0
    nm = len(moves)
    while frontier:
        d += 1
        nxt = []
        for s in frontier:
            p, o = divmod(s, no)
            pr, orow = perm[p], ori[o]
            for k in range(nm):
                t = pr[k] * no + orow[k]
                if dist[t] == 255:
                    dist[t] = d
                    nxt.append(t)
        frontier = nxt
        if nxt:
            counts.append(len(nxt))
    return counts
