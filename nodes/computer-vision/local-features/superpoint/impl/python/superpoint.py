# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/superpoint/. The authors are listed in prov/P2KH05.jsonl.

"""The decoding step of SuperPoint (DeTone, Malisiewicz and Rabinovich 2018).

The network is not part of this file. Its two outputs are given:

- X, the detector output: Hc rows of Wc cells, each a list of 65 logits.
  Channels 0..63 are the 64 pixels of the 8 x 8 cell in row-major order,
  channel c at row c // 8 and column c % 8 of the cell; channel 64 is the
  "no interest point" bin (the dustbin).
- F, the coarse descriptor map: Hc rows of Wc vectors of the same length.

The image has H = 8 Hc rows and W = 8 Wc columns. A pixel is (u, v), with u
the column and v the row; heat[v][u] is its score.

The decoder takes a softmax over the 65 channels of each cell, drops the
dustbin and places the 64 values in the cell (the "depth to space" step).
Then it keeps the pixels with score at least tau that are not too close to the
border, and runs greedy non-maximum suppression: in order of decreasing score,
a pixel is kept if no kept pixel is within Chebyshev distance r.

The descriptor of a kept pixel is sampled from F by bilinear interpolation
and divided by its Euclidean norm. The paper uses bicubic interpolation; this
code uses bilinear interpolation, with the center of coarse cell (cx, cy) at
pixel (8 cx + 3.5, 8 cy + 3.5). The alignment is a convention.
"""

import math
from typing import List, Sequence, Tuple

CELL = 8


def softmax(z: Sequence[float]) -> List[float]:
    m = max(z)
    e = [math.exp(x - m) for x in z]
    s = sum(e)
    return [x / s for x in e]


def decode_heatmap(X: Sequence[Sequence[Sequence[float]]]) -> List[List[float]]:
    """Turn Hc x Wc cells of 65 logits into an H x W heat map."""
    hc, wc = len(X), len(X[0])
    heat = [[0.0] * (CELL * wc) for _ in range(CELL * hc)]
    for cy in range(hc):  # @line L1
        for cx in range(wc):
            logits = X[cy][cx]
            if len(logits) != CELL * CELL + 1:
                raise ValueError("each cell needs 65 logits")
            p = softmax(logits)  # @line L2
            for c in range(CELL * CELL):  # @line L3
                heat[CELL * cy + c // CELL][CELL * cx + c % CELL] = p[c]
    return heat


def nms(heat: Sequence[Sequence[float]], tau: float, r: int, border: int) -> List[Tuple[int, int, float]]:
    """Greedy grid NMS. Return the kept (u, v, score), by decreasing score."""
    h, w = len(heat), len(heat[0])
    cand = [(heat[v][u], u, v)  # @line L4
            for v in range(border, h - border) for u in range(border, w - border)
            if heat[v][u] >= tau]
    cand.sort(key=lambda t: (-t[0], t[2], t[1]))  # @line L5
    free = [[True] * w for _ in range(h)]  # @line L6
    kept = []
    for s, u, v in cand:  # @line L7
        if free[v][u]:  # @line L8
            kept.append((u, v, s))
            for y in range(max(0, v - r), min(h, v + r + 1)):
                row = free[y]
                for x in range(max(0, u - r), min(w, u + r + 1)):
                    row[x] = False
    return kept


def sample_descriptor(F: Sequence[Sequence[Sequence[float]]], u: float, v: float,
                      normalize: bool = True) -> List[float]:
    """Bilinear sample of the coarse map F at pixel (u, v), then L2 normalization."""
    hc, wc = len(F), len(F[0])
    fx = min(max((u - 3.5) / CELL, 0.0), wc - 1.0)  # @line L10
    fy = min(max((v - 3.5) / CELL, 0.0), hc - 1.0)
    x0, y0 = int(math.floor(fx)), int(math.floor(fy))
    x1, y1 = min(x0 + 1, wc - 1), min(y0 + 1, hc - 1)
    ax, ay = fx - x0, fy - y0
    f = [(1 - ax) * (1 - ay) * a + ax * (1 - ay) * b + (1 - ax) * ay * c + ax * ay * d
         for a, b, c, d in zip(F[y0][x0], F[y0][x1], F[y1][x0], F[y1][x1])]
    if not normalize:
        return f
    n = math.sqrt(sum(t * t for t in f))  # @line L11
    return [t / n for t in f] if n > 0 else f


def superpoint_decode(X, F, tau: float = 0.015, r: int = 4, border: int = 4):
    """Return (keypoints, descriptors): keypoints as (u, v, score), descriptors of unit norm."""
    heat = decode_heatmap(X)
    kept = nms(heat, tau, r, border)
    desc = [sample_descriptor(F, u, v) for u, v, _ in kept]  # @line L9
    return kept, desc
