# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hough-transform/. The authors are listed in prov/ZV0TVQ.jsonl.

"""The Hough transform for straight lines, in the normal form of Duda and Hart.

The input is a list of edge pixels (x, y) of a W by H image, with x to the
right and y downward and integer pixel centers. A line is the set of points
with x cos(theta) + y sin(theta) = rho. The angle bins are theta_k = k pi / T
for k = 0 .. T - 1, and the distance bins have width 1 and centers
rho_j = j - D for j = 0 .. 2D, with D = ceil(sqrt((W - 1)^2 + (H - 1)^2)).
A point votes in bin j when rho_j - 1/2 <= rho < rho_j + 1/2.
"""

import math


def hough_lines(points: list[tuple[int, int]], width: int, height: int, angles: int) -> list[list[int]]:
    """Return the T by (2D + 1) accumulator of votes."""
    if angles < 1:
        raise ValueError("need at least one angle")
    d = math.ceil(math.hypot(max(width - 1, 0), max(height - 1, 0)))  # @line L1
    acc = [[0] * (2 * d + 1) for _ in range(angles)]  # @line L2
    cos_t = [math.cos(k * math.pi / angles) for k in range(angles)]
    sin_t = [math.sin(k * math.pi / angles) for k in range(angles)]
    for x, y in points:  # @line L3
        for k in range(angles):  # @line L4
            rho = x * cos_t[k] + y * sin_t[k]  # @line L5
            j = math.floor(rho)
            if rho - j >= 0.5:  # exact; floor(rho + 0.5) can round up a value just below a half
                j += 1
            acc[k][j + d] += 1  # @line L6
    return acc  # @line L7


def peaks(acc: list[list[int]], angles: int, threshold: int) -> list[tuple[int, float, int]]:
    """Return (votes, theta, rho) for each cell with at least threshold votes that is a maximum
    of its 3 by 3 neighborhood. On a tie the cell that comes first in scan order wins.
    The list is sorted by votes, most first."""
    if not acc:
        return []
    rows, cols = len(acc), len(acc[0])
    d = (cols - 1) // 2
    found = []
    for k in range(rows):  # @line L8
        for j in range(cols):
            v = acc[k][j]
            if v < threshold:  # @line L9
                continue
            best = True
            for dk in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    kk, jj = k + dk, j + dj
                    if (dk or dj) and 0 <= kk < rows and 0 <= jj < cols:
                        u = acc[kk][jj]
                        if u > v or (u == v and (dk, dj) < (0, 0)):  # @line L10
                            best = False
            if best:
                found.append((v, k * math.pi / angles, j - d))  # @line L11
    found.sort(key=lambda t: -t[0])
    return found
