# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/semi-global-matching/. The authors are listed in prov/NJ87X5.jsonl.
"""Semi-global matching (Hirschmuller) on a given cost volume.

The cost volume is C[v][u][d], the matching cost of left pixel (u, v) at
disparity d in [0, D). For a direction r = (du, dv), the path cost is

    L_r(p, d) = C(p, d) + min(L_r(p - r, d),
                              L_r(p - r, d - 1) + P1,
                              L_r(p - r, d + 1) + P1,
                              min_k L_r(p - r, k) + P2)
                        - min_k L_r(p - r, k),

with L_r(p, d) = C(p, d) when p - r is outside the image. The costs of all
directions are added, S(p, d) = sum_r L_r(p, d), and each pixel takes the
least d with the least S(p, d) (winner-takes-all).
"""

from __future__ import annotations

from typing import List, Sequence, Tuple

DIRECTIONS_2 = [(1, 0), (-1, 0)]
DIRECTIONS_4 = DIRECTIONS_2 + [(0, 1), (0, -1)]
DIRECTIONS_8 = DIRECTIONS_4 + [(1, 1), (-1, -1), (1, -1), (-1, 1)]
DIRECTIONS_16 = DIRECTIONS_8 + [(2, 1), (-2, -1), (2, -1), (-2, 1),
                                (1, 2), (-1, -2), (1, -2), (-1, 2)]

Volume = Sequence[Sequence[Sequence[float]]]


def path_cost(C: Volume, P1: float, P2: float,
              r: Tuple[int, int]) -> List[List[List[float]]]:
    """L_r for all pixels and disparities, for one direction r."""
    H, W, D = len(C), len(C[0]), len(C[0][0])
    du, dv = r
    # p - r must come before p: rows in the order of dv, columns of du.
    rows = range(H) if dv >= 0 else range(H - 1, -1, -1)
    cols = range(W) if du >= 0 else range(W - 1, -1, -1)
    L = [[None] * W for _ in range(H)]
    for v in rows:  # @line L3
        for u in cols:  # @line L3
            pu, pv = u - du, v - dv
            c = C[v][u]
            if not (0 <= pu < W and 0 <= pv < H):  # @line L4
                L[v][u] = list(c)  # @line L4
                continue
            prev = L[pv][pu]
            m = min(prev)  # @line L5
            jump = m + P2
            out = [0.0] * D
            for d in range(D):  # @line L6
                best = prev[d]
                if d > 0 and prev[d - 1] + P1 < best:
                    best = prev[d - 1] + P1
                if d + 1 < D and prev[d + 1] + P1 < best:
                    best = prev[d + 1] + P1
                if jump < best:
                    best = jump
                out[d] = c[d] + best - m  # @line L6
            L[v][u] = out
    return L


def aggregate(C: Volume, P1: float, P2: float,
              directions: Sequence[Tuple[int, int]] = DIRECTIONS_8
              ) -> List[List[List[float]]]:
    """S(p, d), the sum of L_r(p, d) over the directions."""
    H, W, D = len(C), len(C[0]), len(C[0][0])
    S = [[[0.0] * D for _ in range(W)] for _ in range(H)]  # @line L1
    for r in directions:  # @line L2
        L = path_cost(C, P1, P2, r)
        for v in range(H):
            for u in range(W):
                Sp, Lp = S[v][u], L[v][u]
                for d in range(D):
                    Sp[d] += Lp[d]  # @line L7
    return S


def winner_takes_all(S: Volume) -> List[List[int]]:
    """For each pixel, the least d with the least cost."""
    return [[min(range(len(s)), key=s.__getitem__) for s in row]  # @line L8
            for row in S]


def sgm(C: Volume, P1: float, P2: float,
        directions: Sequence[Tuple[int, int]] = DIRECTIONS_8) -> List[List[int]]:
    """The disparity map of semi-global matching."""
    return winner_takes_all(aggregate(C, P1, P2, directions))  # @line L9


def absolute_difference_volume(left, right, D: int) -> List[List[List[int]]]:
    """C[v][u][d] = |left(u, v) - right(u - d, v)|, where a right column
    left of the image takes the value of column 0."""
    return [[[abs(lrow[u] - rrow[u - d if u >= d else 0]) for d in range(D)]
             for u in range(len(lrow))]
            for lrow, rrow in zip(left, right)]
