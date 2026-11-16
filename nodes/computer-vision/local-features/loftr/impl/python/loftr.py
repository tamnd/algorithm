# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/loftr/. The authors are listed in prov/JB95QG.jsonl.

"""The matching steps of LoFTR (Sun, Shen, Wang, Bao and Zhou 2021).

The networks are not part of this file: the convolutional backbone and the
transformer layers. Their outputs are given:

- FA and FB, the coarse features of the two images after the transformer,
  as flat lists of vectors in row-major order over grids of width WcA and WcB.
  The coarse grid has stride 8, and coarse cell i of a grid of width Wc is at
  pixel (8 (i % Wc), 8 (i // Wc)). This placement is a convention of this file.
- GA and GB, the fine feature maps at stride 2, as grids of rows of vectors.
  Coarse cell (x, y) is at fine position (4 x, 4 y).

Coarse matching: S = <FA_i, FB_j> / tau, P = (row softmax of S) times
(column softmax of S), elementwise, and the coarse matches are the mutual
best pairs of P with P at least theta.

Fine refinement: for a coarse match (i, j), take the fine vector of A at the
position of i and a w x w window of B around the position of j. A softmax
of the scaled dot products over the window gives weights, and the expected
offset moves the position of j. Window positions outside the map are left out.
"""

import math
from typing import List, Sequence, Tuple

Vec = Sequence[float]
COARSE = 8
FINE = 2


def dot(a: Vec, b: Vec) -> float:
    return sum(x * y for x, y in zip(a, b))


def softmax(z: Sequence[float]) -> List[float]:
    m = max(z)
    e = [math.exp(x - m) for x in z]
    s = sum(e)
    return [x / s for x in e]


def dual_softmax(FA: Sequence[Vec], FB: Sequence[Vec], tau: float) -> List[List[float]]:
    """Return P with P_ij = softmax_j(S_i.)_j * softmax_i(S_.j)_i and S = <FA_i, FB_j> / tau."""
    S = [[dot(a, b) / tau for b in FB] for a in FA]  # @line L1
    R = [softmax(row) for row in S]  # @line L2
    cols = [softmax([S[i][j] for i in range(len(FA))]) for j in range(len(FB))]
    return [[R[i][j] * cols[j][i] for j in range(len(FB))] for i in range(len(FA))]  # @line L3


def coarse_matches(P: Sequence[Sequence[float]], theta: float) -> List[Tuple[int, int, float]]:
    """Mutual best pairs of P with P_ij >= theta. Ties go to the smaller index."""
    m, n = len(P), len(P[0])
    row_best = [max(range(n), key=lambda j: (P[i][j], -j)) for i in range(m)]  # @line L4
    col_best = [max(range(m), key=lambda i: (P[i][j], -i)) for j in range(n)]
    return [(i, j, P[i][j]) for i, j in enumerate(row_best)
            if col_best[j] == i and P[i][j] >= theta]


def refine(center: Vec, G: Sequence[Sequence[Vec]], fx: int, fy: int, w: int,
           scale: float) -> Tuple[float, float]:
    """Expected position, in fine pixels, of center inside the w x w window of G at (fx, fy)."""
    h, wd = len(G), len(G[0])
    half = w // 2
    pos, score = [], []
    for dy in range(-half, half + 1):  # @line L6
        for dx in range(-half, half + 1):
            x, y = fx + dx, fy + dy
            if 0 <= x < wd and 0 <= y < h:
                pos.append((x, y))
                score.append(dot(center, G[y][x]) * scale)
    q = softmax(score)  # @line L7
    return (sum(p * x for p, (x, _) in zip(q, pos)),  # @line L8
            sum(p * y for p, (_, y) in zip(q, pos)))


def loftr_match(FA: Sequence[Vec], FB: Sequence[Vec], wca: int, wcb: int,
                GA: Sequence[Sequence[Vec]], GB: Sequence[Sequence[Vec]],
                tau: float = 0.1, theta: float = 0.2, w: int = 5,
                scale: float = 1.0) -> List[Tuple[Tuple[float, float], Tuple[float, float], float]]:
    """Return matches as (pixel in A, refined pixel in B, coarse confidence)."""
    P = dual_softmax(FA, FB, tau)
    out = []
    for i, j, p in coarse_matches(P, theta):  # @line L5
        ax, ay = i % wca, i // wca
        bx, by = j % wcb, j // wcb
        center = GA[4 * ay][4 * ax]
        x, y = refine(center, GB, 4 * bx, 4 * by, w, scale)
        out.append(((COARSE * ax, COARSE * ay), (FINE * x, FINE * y), p))
    return out
