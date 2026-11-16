# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cost-volume/. The authors are listed in prov/YWMV35.jsonl.
"""The cost volume of a rectified stereo pair.

An image is a list of rows; the value at pixel (u, v), column u and row v,
is img[v][u]. The left pixel (u, v) at disparity d is compared with the
right pixel (u - d, v). The volume has W * H * D entries in one flat list,
with the disparity as the fastest index: entry (u, v, d) is at
(v * W + u) * D + d. An entry whose right pixel is outside the image holds
INVALID (infinity), so that winner-takes-all never picks it.
"""

from __future__ import annotations

import math
from typing import Callable, List, Sequence

INVALID = math.inf


def absolute_difference(left, right, u: int, v: int, d: int) -> float:
    return abs(left[v][u] - right[v][u - d])


class CostVolume:
    """A W x H x D array of matching costs."""

    def __init__(self, W: int, H: int, D: int, fill: float = INVALID):
        if W < 1 or H < 1 or D < 1:
            raise ValueError("W, H and D must be positive")
        self.W, self.H, self.D = W, H, D
        self.data: List[float] = [fill] * (W * H * D)

    def index(self, u: int, v: int, d: int) -> int:
        if not (0 <= u < self.W and 0 <= v < self.H and 0 <= d < self.D):
            raise IndexError((u, v, d))
        return (v * self.W + u) * self.D + d  # @line L1

    def get(self, u: int, v: int, d: int) -> float:
        return self.data[self.index(u, v, d)]

    def set(self, u: int, v: int, d: int, c: float) -> None:
        self.data[self.index(u, v, d)] = c

    @classmethod
    def build(cls, left: Sequence[Sequence[float]], right: Sequence[Sequence[float]], D: int,
              cost: Callable = absolute_difference) -> "CostVolume":
        """BUILD: C(u, v, d) = cost(u, v, d) if u - d >= 0, else INVALID."""
        H, W = len(left), len(left[0])
        cv = cls(W, H, D)
        k = 0
        for v in range(H):  # @line L2
            for u in range(W):  # @line L2
                for d in range(D):  # @line L3
                    if u - d >= 0:  # @line L4
                        cv.data[k] = cost(left, right, u, v, d)  # @line L4
                    k += 1
        return cv

    def slice(self, d: int) -> List[List[float]]:
        """The H x W image of the costs at one disparity."""
        D, W = self.D, self.W
        return [[self.data[(v * W + u) * D + d] for u in range(W)] for v in range(self.H)]

    def set_slice(self, d: int, img: Sequence[Sequence[float]]) -> None:
        D, W = self.D, self.W
        for v in range(self.H):
            for u in range(W):
                self.data[(v * W + u) * D + d] = img[v][u]

    def wta(self) -> List[List[int]]:
        """WTA: for each pixel the least d with the least cost."""
        D, W, data = self.D, self.W, self.data
        out = []
        for v in range(self.H):  # @line L5
            row = []
            for u in range(W):  # @line L5
                base = (v * W + u) * D
                best, bd = data[base], 0  # @line L6
                for d in range(1, D):  # @line L7
                    if data[base + d] < best:  # @line L7
                        best, bd = data[base + d], d  # @line L7
                row.append(bd)  # @line L8
            out.append(row)
        return out

    def right_view(self) -> "CostVolume":
        """RIGHT-VIEW: the volume with the right image as reference,
        C_R(x, v, d) = C(x + d, v, d) if x + d < W, else INVALID."""
        out = CostVolume(self.W, self.H, self.D)
        for v in range(self.H):  # @line L9
            for x in range(self.W):  # @line L9
                for d in range(self.D):  # @line L10
                    if x + d < self.W:  # @line L11
                        out.data[out.index(x, v, d)] = self.get(x + d, v, d)  # @line L11
        return out

    def nbytes(self, bytes_per_entry: int) -> int:
        return self.W * self.H * self.D * bytes_per_entry
