# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scanline-dynamic-programming-stereo/. The authors are listed in prov/ZQ13H8.jsonl.
"""Dynamic programming stereo on each scanline, with occlusions.

The pair is rectified, and the left pixel i of a row matches the right
pixel j = i - d of the same row, with the disparity d in [0, D). A matching
of one row is a set of pairs (i, j) with 0 <= i - j < D that is strictly
increasing in both i and j: no pixel is matched twice (uniqueness), and
the order of the pixels is the same in both images (ordering). Its cost is

    sum over the matched pairs of c(l[i], r[j])  +  kappa * (unmatched pixels),

where the unmatched pixels of both images count, so a row of width W with
M matches has 2 (W - M) unmatched pixels. The default c is the absolute
difference. A matching is a monotone path from (0, 0) to (W, W) in the
grid of prefixes, and the dynamic program over the band 0 <= i - j < D
finds the cheapest one in O(W D) time.
"""

from __future__ import annotations

from typing import Callable, List, Optional, Sequence, Tuple

INF = float("inf")
START, MATCH, LEFT_OCC, RIGHT_OCC = 0, 1, 2, 3


def absolute_difference(a: float, b: float) -> float:
    return abs(a - b)


def scanline_dp(lrow: Sequence[float], rrow: Sequence[float], D: int,
                kappa: float,
                cost: Callable[[float, float], float] = absolute_difference
                ) -> Tuple[float, List[Optional[int]], List[Tuple[int, int]]]:
    """Return (least cost, disparity of each left pixel or None if it is
    unmatched, the matched pairs (i, j) in increasing order).

    The state (i, j) is the cost of matching the prefixes l[:i] and r[:j];
    it is stored as C[i][k] with k = i - j in [0, D). The band needs
    D >= 2: with D = 1 a path in the band could not skip any pixel."""
    W = len(lrow)
    if len(rrow) != W or D < 2:
        raise ValueError("rows must have the same width and D >= 2")
    C = [[INF] * D for _ in range(W + 1)]
    move = [[START] * D for _ in range(W + 1)]
    C[0][0] = 0  # @line L1
    for i in range(W + 1):  # @line L2
        for k in range(min(D - 1, i), -1, -1):  # @line L3
            j = i - k
            if i == 0:
                continue
            best, how = INF, START
            if j >= 1:  # pair (i - 1, j - 1) has the same k  # @line L4
                c = C[i - 1][k] + cost(lrow[i - 1], rrow[j - 1])  # @line L4
                if c < best:
                    best, how = c, MATCH
            if k >= 1:  # left pixel i - 1 unmatched, from (i - 1, j)  # @line L5
                c = C[i - 1][k - 1] + kappa  # @line L5
                if c < best:
                    best, how = c, LEFT_OCC
            if j >= 1 and k + 1 <= D - 1:  # right pixel j - 1 unmatched  # @line L6
                c = C[i][k + 1] + kappa  # @line L6
                if c < best:
                    best, how = c, RIGHT_OCC
            C[i][k], move[i][k] = best, how  # @line L7
    disp: List[Optional[int]] = [None] * W
    pairs: List[Tuple[int, int]] = []
    i, k = W, 0
    while i > 0 or k > 0:  # walk back from (W, W)  # @line L8
        how = move[i][k]
        if how == MATCH:
            disp[i - 1] = k  # @line L8
            pairs.append((i - 1, i - 1 - k))
            i -= 1
        elif how == LEFT_OCC:
            i, k = i - 1, k - 1
        else:
            k += 1
    pairs.reverse()
    return C[W][0], disp, pairs  # @line L9


def matching_cost(lrow, rrow, pairs, kappa, cost=absolute_difference) -> float:
    """The cost of a given matching of one row."""
    W = len(lrow)
    return (sum(cost(lrow[i], rrow[j]) for (i, j) in pairs)
            + kappa * 2 * (W - len(pairs)))


def is_valid_matching(pairs, W: int, D: int) -> bool:
    """Pairs in range, in the band, and strictly increasing in i and j."""
    for t, (i, j) in enumerate(pairs):
        if not (0 <= j <= i < W and i - j < D):
            return False
        if t and not (pairs[t - 1][0] < i and pairs[t - 1][1] < j):
            return False
    return True


def dp_stereo(left: Sequence[Sequence[float]], right: Sequence[Sequence[float]],
              D: int, kappa: float,
              cost: Callable[[float, float], float] = absolute_difference
              ) -> List[List[Optional[int]]]:
    """Run the scanline program on every row; None marks unmatched pixels."""
    return [scanline_dp(lrow, rrow, D, kappa, cost)[1]
            for lrow, rrow in zip(left, right)]
