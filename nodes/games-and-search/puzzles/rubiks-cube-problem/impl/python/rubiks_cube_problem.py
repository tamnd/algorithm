# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rubiks-cube-problem/. The authors are listed in prov/CVDGSV.jsonl.
"""The Rubik's cube at the cubie level: moves, invariants, the number of
states, and shortest solutions of short scrambles by meeting in the middle.

Corners URF, UFL, ULB, UBR, DFR, DLF, DBL, DRB are 0..7 and edges UR, UF,
UL, UB, DR, DF, DL, DB, FR, FL, BL, BR are 0..11. A cube is (cp, co, ep, eo):
cp[i] is the corner in position i and co[i] its twist (0, 1 or 2), and the
same for edges with flips 0 or 1.
"""

from math import factorial
from typing import Dict, List, Sequence, Tuple

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
    MOVES[_f] = _BASIC[_f]
    MOVES[_f + "2"] = multiply(_BASIC[_f], _BASIC[_f])
    MOVES[_f + "'"] = multiply(MOVES[_f + "2"], _BASIC[_f])
HTM = [f + s for f in FACES for s in ("", "2", "'")]   # half-turn metric: 18 moves
QTM = [f + s for f in FACES for s in ("", "'")]        # quarter-turn metric: 12 moves


def apply(cube: Cube, seq: Sequence[str]) -> Cube:
    for m in seq:
        cube = multiply(cube, MOVES[m])
    return cube


def order(seq: Sequence[str]) -> int:
    """How many times seq must be repeated to return to the solved cube."""
    step = apply(SOLVED, seq)
    cube = step
    k = 1
    while cube != SOLVED:
        cube = multiply(cube, step)
        k += 1
    return k


def parity(perm: Sequence[int]) -> int:
    seen = [False] * len(perm)
    p = 0
    for i in range(len(perm)):
        if not seen[i]:
            j = i
            length = 0
            while not seen[j]:
                seen[j] = True
                j = perm[j]
                length += 1
            p ^= (length - 1) & 1
    return p


def invariants(cube: Cube) -> Tuple[int, int, int]:
    """(total twist mod 3, total flip mod 2, corner parity xor edge parity).

    A face turn moves four corners and four edges in 4-cycles, which are odd
    permutations of each, and changes twists and flips by amounts that sum to
    0, so all three values stay 0 on every reachable cube.
    """
    cp, co, ep, eo = cube
    return sum(co) % 3, sum(eo) % 2, parity(cp) ^ parity(ep)


def state_count() -> int:
    """8! 3^7 12! 2^11 / 2: the assemblies with all three invariants zero."""
    return factorial(8) * 3 ** 7 * factorial(12) * 2 ** 11 // 2


def assemblies() -> int:
    """All ways to put the cubies into the frame, reachable or not."""
    return factorial(8) * 3 ** 8 * factorial(12) * 2 ** 12


def ball(start: Cube, radius: int, moves: Sequence[str]) -> Dict[Cube, int]:
    """Distance from start of every cube within radius, by breadth-first search."""
    dist = {start: 0}
    frontier = [start]
    for d in range(1, radius + 1):
        nxt = []
        for c in frontier:
            for m in moves:
                n = multiply(c, MOVES[m])
                if n not in dist:
                    dist[n] = d
                    nxt.append(n)
        frontier = nxt
    return dist


def layer_counts(radius: int, moves: Sequence[str]) -> List[int]:
    dist = ball(SOLVED, radius, moves)
    counts = [0] * (radius + 1)
    for d in dist.values():
        counts[d] += 1
    return counts


def distance_meet_in_middle(cube: Cube, solved_ball: Dict[Cube, int], radius: int,
                            moves: Sequence[str]) -> int:
    """Exact distance of cube to the solved cube if it is at most 2 * radius,
    else -1. solved_ball is ball(SOLVED, radius, moves).

    Every move set used here is closed under inverses, so a cube x is at
    distance j from SOLVED exactly when SOLVED is at distance j from x, and a
    path of length i + j through a middle cube x exists exactly when x is i
    moves from cube and j moves from SOLVED.
    """
    best = -1
    for x, i in ball(cube, radius, moves).items():
        j = solved_ball.get(x)
        if j is not None and (best < 0 or i + j < best):
            best = i + j
    return best


def superflip() -> Cube:
    """Every edge flipped in place, everything else solved."""
    return (tuple(range(8)), (0,) * 8, tuple(range(12)), (1,) * 12)
